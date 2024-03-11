from src.steam_api.client import client
from src.steam_api.config import config


def main():
    games = client.get_player_owned_games(config.STEAM_MY_ID).games
    games = sorted(games, key=lambda game: -game.playtime_forever)
    for game in games[::-1]:
        app_info = client.get_app_info(game.app_id)
        if app_info is None:
            continue
        total_reviews = client.get_total_reviews(game.app_id)
        print(app_info.id, app_info.name or 'UNKNOWN', total_reviews)

        if game.app_id in client.get_reviews.cache.cache:
            continue
        for i, r in enumerate(client.get_reviews(game.app_id)):
            if not (i % 10):
                print(f'\r{i}/{total_reviews}', end='')
        print('')


if __name__ == '__main__':
    main()
