from pathlib import Path

from src.steam_api.client import client, NotFound
from src.steam_api.config import config


def main():
    games = client.get_player_owned_games(config.STEAM_MY_ID).games
    games = sorted(games, key=lambda game: -game.playtime_forever)
    for game in games[::-1]:
        try:
            app_info = client.get_app_info(game.app_id)
        except NotFound as e:
            print('NOT FOUND:', str(e))
            continue
        total_reviews = client.get_total_reviews(game.app_id)
        if not app_info:
            cache = client.get_app_info.cache.cache
            if not cache[game.app_id]:
                f: Path = cache._key_file(game.app_id)
                if f.exists():
                    f.unlink()
            else:
                raise AssertionError(game.app_id)
            continue
        print(app_info.id, app_info.name or 'UNKNOWN', total_reviews)

        if game.app_id in client.get_reviews.cache.cache:
            continue
        for i, r in enumerate(client.get_reviews(game.app_id), start=1):
            if not (i % 10):
                print(f'\r{i}/{total_reviews}', end='')
        print('')


if __name__ == '__main__':
    main()
