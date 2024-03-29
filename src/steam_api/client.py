from typing import Iterator, cast

import requests
from requests import ConnectTimeout

from src.steam_api.cache import cache, SerializerJson
from src.steam_api.common import AnyDict
from src.steam_api.config import config
from src.steam_api.schemas import OwnedGamesResponse, App, Review, ReviewsResponse, ReviewsSummary, \
    AppInfoResponse
from src.steam_api.utils import retry

CONN_TIMEOUT = 5
READ_TIMEOUT = 10
BACKOFF_TIMEOUT = 3


class AppNotFound(Exception):
    pass


class ReviewCollision(Exception):
    pass


class NotFound(Exception):
    pass


class Client:
    STORE_API = 'https://store.steampowered.com'
    STEAM_API = 'https://api.steampowered.com'

    def __init__(self, api_key: str):
        self.api_key = api_key

    @cache('get_app_info', App)
    def get_app_info(self, app_id: int) -> App:
        r = requests.get(f'{self.STORE_API}/api/appdetails?appids={app_id}')
        r.raise_for_status()
        raw = AppInfoResponse.parse_raw(r.text)
        assert set(raw.__root__) == {str(app_id)}
        outer = raw.__root__[str(app_id)]
        if not outer.success:
            raise NotFound(f'app {app_id} retrieve failed')
        if not outer.data:
            raise NotFound(f'app {app_id} empty data')
        return cast(App, outer.data)

    @cache('player_owned_games', OwnedGamesResponse)
    def get_player_owned_games(self, steam_id: int) -> OwnedGamesResponse:
        r = requests.get(
            url=f'{self.STEAM_API}/IPlayerService/GetOwnedGames/v0001/',
            params={
                'key': self.api_key,
                'steamid': steam_id,
                'format': 'json',
            },
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
        while cursor:
            batch = self._get_reviews(app_id, cursor=cursor)
            if not batch.reviews:
                break
            for review in batch.reviews:
                if review.id in ids:
                    raise ReviewCollision((review.id, ids))
                ids.add(review.id)
                yield review
            cursor = batch.cursor
        else:
            print('MISSING CURSOR')

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

    @cache(key='all_apps', serializer=SerializerJson())
    def get_all_apps(self) -> list[AnyDict]:
        # todo: cache
        r = requests.get(f'{self.STEAM_API}/ISteamApps/GetAppList/v2/')
        r.raise_for_status()
        return r.json()['applist']['apps']


client = Client(config.STEAM_API_KEY)
