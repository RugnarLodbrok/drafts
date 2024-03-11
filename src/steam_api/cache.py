import abc
from collections import defaultdict
from pathlib import Path
from typing import Callable, TypeVar, Any

import yaml
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
C = Callable[[Any, str | int], T | None]


class _CachedFuncBase:
    def __init__(self, path: Path, data: dict, model: BaseModel):
        path.mkdir(exist_ok=True)
        self.path = path
        self.data = data
        self.model = model

    @abc.abstractmethod
    def __call__(self, func: C) -> C:
        ...

    def key_file(self, key: str) -> Path:
        return self.path / f'{key}.yml'

    def _ensure_loaded(self, key: str) -> None:
        if key not in self.data:
            self._load(key)

    def _load(self, key: str) -> None:
        self.data[key] = yaml.load(self.key_file(key).read_text(), yaml.SafeLoader)

    def _check(self, key):
        if key in self.data:
            return True

        return self.key_file(key).exists()

    @abc.abstractmethod
    def _set(self, key: str, value: Any):
        ...


class _CachedFunc(_CachedFuncBase):
    def __call__(self, func: C) -> C:
        def wrapper(slf, key: str) -> T | None:
            if self._check(key):
                self._ensure_loaded(key)
                result = self.data[key]
                return result and self.model.parse_obj(result)
            else:
                result = func(slf, key)
                self._set(key, result)
                return result

        wrapper.cache = self
        return wrapper

    def _set(self, key: str, value: BaseModel | None):
        cached_vaule = value.dict(by_alias=True) if value is not None else value
        self.data[key] = cached_vaule
        self.key_file(key).write_text(yaml.dump(cached_vaule, allow_unicode=True))


class _CachedGenerator(_CachedFuncBase):
    def __call__(self, func: C) -> C:
        def wrapper(slf, key: str) -> T | None:
            if self._check(key):
                self._ensure_loaded(key)
                for item in self.data[key]:
                    yield self.model.parse_obj(item)
            else:
                result = []
                try:
                    for item in func(slf, key):
                        result.append(item)
                        yield item
                finally:
                    self._set(key, result)
                return result

        wrapper.cache = self
        return wrapper

    def _set(self, key: str, value: list[BaseModel]):
        cached_vaule = [item.dict(by_alias=True) for item in value]
        self.data[key] = cached_vaule
        self.key_file(key).write_text(yaml.dump(cached_vaule, allow_unicode=True))


class Cache:
    def __init__(self, path: Path):
        path.mkdir(exist_ok=True)
        self.path = path
        self.data = defaultdict(dict)

    def cache(self, key: str, model: BaseModel):
        path = self.path / key
        data = self.data[key]

        return _CachedFunc(path, data, model)

    def cache_generator(self, key: str, model: BaseModel):
        path = self.path / key
        data = self.data[key]

        return _CachedGenerator(path, data, model)


cache = Cache(Path(__file__).parent / 'cache')
