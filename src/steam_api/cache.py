import abc
import inspect
from contextlib import contextmanager
from inspect import isgeneratorfunction as is_generator
from pathlib import Path
from typing import Callable, TypeVar, ParamSpec, Iterator, Iterable, Type

import yaml
from py_tools.seq import identity
from pydantic import BaseModel

from src.steam_api.common import AnyDict

T = TypeVar('T', bound=BaseModel)
P = ParamSpec('P')
F = Callable[P, T | None]
_AnyJsonItem = AnyDict | bool | None
AnyJson = list[_AnyJsonItem] | _AnyJsonItem


class SerializerBase:
    @abc.abstractmethod
    def dump(self, path: Path, data: AnyJson) -> None:
        ...

    @abc.abstractmethod
    def load(self, path: Path) -> AnyJson:
        ...

    def iter(self, path) -> Iterator[AnyJson]:
        raise NotImplementedError

    def iter_write(self, path) -> Iterator[Callable[[AnyDict], None]]:
        raise NotImplementedError


class SerializerYaml(SerializerBase):
    def dump(self, path: Path, data: AnyJson) -> None:
        with open(path, 'wt') as f:
            yaml.dump(data, stream=f, allow_unicode=True)

    def load(self, path: Path) -> AnyJson:
        with open(path, 'rt') as f:
            return yaml.load(f, yaml.SafeLoader)

    def iter(self, path) -> Iterator[AnyJson]:
        for chunk in self._yaml_chunks(path):
            yield yaml.load(chunk, yaml.SafeLoader)[0]

    @contextmanager
    def iter_write(self, path: Path) -> Iterator[Callable[[AnyDict], None]]:
        with open(path, 'wt') as f:
            def feed(item: AnyDict):
                f.write(yaml.dump([item], allow_unicode=True))

            yield feed

    def _yaml_chunks(self, path: Path) -> Iterator[str]:
        chunk = ''
        with open(path, 'rt') as f:
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


class CacheFiles:
    def __init__(self, path: Path, serializer: SerializerBase = SerializerYaml()):
        self._path = path
        self._no_args_mode: bool | None = None
        self._serializer = serializer

    @property
    def no_args_mode(self) -> bool:
        return self._no_args_mode

    @no_args_mode.setter
    def no_args_mode(self, value: bool) -> None:
        if value is False:
            self._path.mkdir(exist_ok=True)
        self._no_args_mode = value

    def _key_file(self, key: str) -> Path:
        if self._no_args_mode is False:
            return self._path / f'{key}.yml'
        elif self._no_args_mode is True:
            return Path(f'{self._path}.yml')
        raise RuntimeError('mode is not set')

    def __contains__(self, key: str) -> bool:
        return self._key_file(key).exists()

    def __getitem__(self, key: str) -> AnyJson:
        return self._serializer.load(self._key_file(key))

    def __setitem__(self, key: str, value: AnyJson) -> None:
        self._serializer.dump(self._key_file(key), value)

    def iter(self, key: str) -> Iterator[AnyJson]:
        return self._serializer.iter(self._key_file(key))

    def iter_write(self, key: str) -> Iterator[Callable[[AnyDict], None]]:
        return self._serializer.iter_write(self._key_file(key))


class CacheDecorator:
    def __init__(self, path: Path, model: BaseModel | None):
        self.cache = CacheFiles(path)
        self.model = model

    @staticmethod
    def _model_dump(data: BaseModel) -> AnyJson:
        return data and data.dict(by_alias=True)

    def _model_load(self, data: AnyJson) -> BaseModel | None:
        return data and self.model.parse_obj(data)

    def get_arg_count(self, func: F) -> int:
        spec = inspect.getfullargspec(func)
        args = spec.args
        if args[0] == 'self':
            args = args[1:]
        return len(args)

    def __call__(self, func: F) -> F:
        self.cache.no_args_mode = self.get_arg_count(func) == 0
        if self.model:
            _dump = self._model_dump
            _load = self._model_load
        else:
            _dump = identity
            _load = identity
        if not is_generator(func):
            def hit(key: str) -> T | None:
                result = self.cache[key]
                return _load(result)

            def miss(key: str, result: T | None) -> T | None:
                self.cache[key] = _dump(result)
                return result

        else:
            def hit(key: str) -> Iterator[T]:
                for item in self.cache.iter(key):
                    yield _load(item)

            def miss(key: str, result: Iterator[T]) -> Iterator[T]:
                with self.cache.iter_write(key) as feed:
                    for item in result:
                        feed(_dump(item))
                        yield item

        def wrapper(slf, *args) -> T | None:
            key = '_'.join(str(arg) for arg in args)
            if key in self.cache:
                return hit(key)
            return miss(key, func(slf, *args))

        wrapper.cache = self
        return wrapper


class Cache:
    def __init__(self, path: Path):
        self.path = path

    def __call__(self, key: str, model: BaseModel | None = None) -> CacheDecorator:
        self.path.mkdir(exist_ok=True)
        return CacheDecorator(self.path / key, model)


cache = Cache(Path(__file__).parent / 'cache')
