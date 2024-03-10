from src.steam_api.client import client
from src.steam_api.config import config

if __name__ == '__main__':
    games = client.get_player_owned_games(config.STEAM_MY_ID).games
    games = sorted(games, key=lambda game: -game.playtime_forever)
    for game in games:
        app_info = client.get_app_info(game.app_id)
        print(app_info and app_info.name, game.playtime_forever)
