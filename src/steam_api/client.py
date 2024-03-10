import requests

from src.steam_api.cache import cache
from src.steam_api.config import config
from src.steam_api.schemas import OwnedGamesResponse, AppInfoOuter, App


class AppNotFound(Exception):
    pass


class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key

    @cache.cache('get_app_info', App)
    def get_app_info(self, app_id: int) -> App | None:
        r = requests.get(f'https://store.steampowered.com/api/appdetails?appids={app_id}')
        r.raise_for_status()
        raw = r.json()
        assert set(raw) == {str(app_id)}
        outer = AppInfoOuter.parse_obj(raw[str(app_id)])
        return outer.data

    def get_player_owned_games(self, steam_id: int) -> OwnedGamesResponse:
        r = requests.get(
            url=f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
                f'?key={self.api_key}'
                f'&steamid={steam_id}'
                f'&format=json'
        )
        r.raise_for_status()
        return OwnedGamesResponse.parse_obj(r.json()['response'])


client = Client(config.STEAM_API_KEY)
