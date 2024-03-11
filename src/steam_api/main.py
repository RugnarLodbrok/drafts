from src.steam_api.client import client
from src.steam_api.config import config


def main():
    games = client.get_player_owned_games(config.STEAM_MY_ID).games
    games = sorted(games, key=lambda game: -game.playtime_forever)
    for game in games[::-1]:
        app_info = client.get_app_info(game.app_id)
        print(app_info.name or 'UNKNOWN')
        total_reviews = client.get_total_reviews(game.app_id)
        for i, r in enumerate(client.get_reviews(game.app_id)):
            if not (i % 10):
                print(f'{i}/{total_reviews}', end='\r')


if __name__ == '__main__':
    main()
