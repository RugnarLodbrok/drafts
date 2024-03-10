from collections import defaultdict

import yaml
from pathlib import Path
from typing import Callable, TypeVar, Any

from py_tools.dicts import defaultdict2
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
C = Callable[[Any, str | int], T | None]


class _CachedFunc:
    def __init__(self, path: Path, data: dict, model: BaseModel):
        self.path = path
        self.data = data
        self.model = model

    def __call__(self, func: C) -> C:
        def wrapper(slf, key: str) -> T | None:
            if self._check(key):
                result = self.data[key]
            else:
                result = func(slf, key)
                self._set(key, result)
            return result and self.model.parse_obj(result)

        return wrapper

    def _set(self, key: str, value: BaseModel | None):
        cached_vaule = value.dict(by_alias=True) if value is not None else value
        self.data[key] = cached_vaule
        self.key_file(key).write_text(yaml.dump(cached_vaule))

    def _check(self, key):
        if key in self.data:
            return True

        if self.key_file(key).exists():
            self.data[key] = yaml.load(self.key_file(key).read_text(), yaml.SafeLoader)
            return True
        return False

    def key_file(self, key: str) -> Path:
        return self.path / f'{key}.yml'


class Cache:
    def __init__(self, path: Path):
        path.mkdir(exist_ok=True)
        self.path = path
        self.data = defaultdict(dict)

    def cache(self, key: str, model: BaseModel):
        path = self.path / key
        data = self.data[key]

        return _CachedFunc(path, data, model)


cache = Cache(Path(__file__).parent / 'cache')
