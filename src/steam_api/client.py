from typing import Iterator

import requests
from requests import ConnectTimeout

from src.steam_api.cache import cache
from src.steam_api.config import config
from src.steam_api.schemas import OwnedGamesResponse, AppInfoOuter, App, Review, ReviewsResponse, ReviewsSummary
from src.steam_api.utils import retry

CONN_TIMEOUT = 5
READ_TIMEOUT = 10
BACKOFF_TIMEOUT = 3


class AppNotFound(Exception):
    pass


class ReviewCollision(Exception):
    pass


class Client:
    STORE_API = 'https://store.steampowered.com'
    STEAM_API = 'https://api.steampowered.com'

    def __init__(self, api_key: str):
        self.api_key = api_key

    @cache('get_app_info', App)
    def get_app_info(self, app_id: int) -> App | None:
        r = requests.get(f'{self.STORE_API}/api/appdetails?appids={app_id}')
        r.raise_for_status()
        raw = r.json()
        assert set(raw) == {str(app_id)}
        outer = AppInfoOuter.parse_obj(raw[str(app_id)])
        return outer.data

    @cache('player_owned_games', OwnedGamesResponse)
    def get_player_owned_games(self, steam_id: int) -> OwnedGamesResponse:
        r = requests.get(
            url=f'{self.STEAM_API}/IPlayerService/GetOwnedGames/v0001/'
                f'?key={self.api_key}'
                f'&steamid={steam_id}'
                f'&format=json'
        )
        r.raise_for_status()
        return OwnedGamesResponse.parse_obj(r.json()['response'])

    def get_total_reviews(self, app_id: int) -> int:
        return self.get_review_summary(app_id).total_reviews

    @cache(key='review_summary', model=ReviewsSummary)
    def get_review_summary(self, app_id: int) -> ReviewsSummary:
        return self._get_reviews(app_id).query_summary

    @cache(key='reviews', model=Review)
    def get_reviews(self, app_id: int) -> Iterator[Review]:
        ids = set()
        cursor = '*'
        while True:
            batch = self._get_reviews(app_id, cursor=cursor)
            if not batch.reviews:
                break
            for review in batch.reviews:
                if review.id in ids:
                    raise ReviewCollision((review.id, ids))
                ids.add(review.id)
                yield review
            cursor = batch.cursor

    @retry(ConnectTimeout, n=30, backoff_time=BACKOFF_TIMEOUT)
    def _get_reviews(self, app_id: int, cursor: str = '*') -> ReviewsResponse:
        r = requests.get(
            f'{self.STORE_API}/appreviews/{app_id}',
            params={
                'json': 1,
                'language': 'all',
                'filter': 'recent',  # this means ordering, not filter. Cursor won't work with default 'all'
                'review_type': 'all',
                'appids': app_id,
                'cursor': cursor,
                'num_per_page': 100,
                'filter_offtopic_activity': 0,
            },
            timeout=(CONN_TIMEOUT, READ_TIMEOUT),
        )
        r.raise_for_status()
        result = ReviewsResponse.parse_obj(r.json())
        assert result.success
        return result


client = Client(config.STEAM_API_KEY)
