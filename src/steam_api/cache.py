from contextlib import contextmanager
from inspect import isgeneratorfunction as is_generator
from pathlib import Path
from typing import Callable, TypeVar, Any, ParamSpec, Iterator

import yaml
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
P = ParamSpec('P')
F = Callable[P, T | None]
AnyDict = dict[str, Any]
_AnyJsonItem = AnyDict | bool | None
AnyJson = list[_AnyJsonItem] | _AnyJsonItem


class CacheFiles:
    def __init__(self, path: Path):
        self._path = path

    def _key_file(self, key: str) -> Path:
        return self._path / f'{key}.yml'

    def __contains__(self, key: str) -> bool:
        return self._key_file(key).exists()

    def __getitem__(self, key: str) -> AnyJson:
        return yaml.load(self._key_file(key).read_text(), yaml.SafeLoader)

    def __setitem__(self, key: str, value: AnyJson):
        self._key_file(key).write_text(yaml.dump(value, allow_unicode=True))

    def _yaml_chunks(self, key: str) -> Iterator[str]:
        chunk = ''
        with open(self._key_file(key), 'rt') as f:
            for line in f:
                if not chunk:
                    assert line.startswith('- ')
                    chunk = line
                elif line.startswith('- '):
                    yield chunk
                    chunk = line
                else:
                    chunk += line
            if chunk:
                yield chunk

    def iter(self, key: str) -> Iterator[BaseModel]:
        for chunk in self._yaml_chunks(key):
            yield yaml.load(chunk, yaml.SafeLoader)[0]

    @contextmanager
    def iter_write(self, key: str) -> Iterator[Callable[[AnyDict], None]]:
        with open(self._key_file(key), 'wt') as f:
            def feed(item: AnyDict):
                f.write(yaml.dump([item], allow_unicode=True))

            yield feed


class CacheDecorator:
    def __init__(self, path: Path, model: BaseModel):
        path.mkdir(exist_ok=True)
        self.cache = CacheFiles(path)
        self.model = model

    @staticmethod
    def _model_dump(data: BaseModel) -> AnyDict | None:
        return data and data.dict(by_alias=True)

    def _model_load(self, data: AnyDict | None) -> BaseModel | None:
        return data and self.model.parse_obj(data)

    def __call__(self, func: F) -> F:
        if not is_generator(func):
            def wrapper(slf, key: str) -> T | None:
                if key in self.cache:
                    result = self.cache[key]
                    return self._model_load(result)
                else:
                    result = func(slf, key)
                    self.cache[key] = self._model_dump(result)
                    return result
        else:
            def wrapper(slf, key: str) -> Iterator[T]:
                if key in self.cache:
                    for item in self.cache.iter(key):
                        yield self.model.parse_obj(item)
                else:
                    with self.cache.iter_write(key) as feed:
                        for item in func(slf, key):
                            feed(self._model_dump(item))
                            yield item

        wrapper.cache = self
        return wrapper


class Cache:
    def __init__(self, path: Path):
        self.path = path

    def __call__(self, key: str, model: BaseModel) -> CacheDecorator:
        self.path.mkdir(exist_ok=True)
        return CacheDecorator(self.path / key, model)


cache = Cache(Path(__file__).parent / 'cache')
