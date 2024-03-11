from time import sleep
from typing import Type


def retry(exc_type: Type[Exception], n: int = 3, backoff_time: int = 0):
    def decorator(f):
        def wrapper(*args, **kwargs):
            ex = exc_type
            for _ in range(n):
                try:
                    return f(*args, **kwargs)
                except exc_type as e:
                    ex = e
                    print(f'retry {exc_type}... {backoff_time} sec')
                    sleep(backoff_time)
            else:
                raise ex

        return wrapper

    return decorator
