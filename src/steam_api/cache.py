import inspect
from functools import cached_property
from inspect import isgeneratorfunction as is_generator
from pathlib import Path
from typing import Callable, TypeVar, ParamSpec, Iterator

from py_tools.seq import identity
from pydantic import BaseModel

from src.steam_api.common import AnyDict, AnyJson
from src.steam_api.serializer import SerializerYaml, SerializerBase

T = TypeVar('T', bound=BaseModel)
P = ParamSpec('P')
F = Callable[P, T | None]


class CacheFiles:
    def __init__(self, path: Path, serializer: SerializerBase = SerializerYaml()):
        self._path = path
        self._no_args_mode: bool | None = None
        self._serializer = serializer

    @property
    def no_args_mode(self) -> bool:
        return self._no_args_mode

    @cached_property
    def ext(self):
        return self._serializer.EXT

    @no_args_mode.setter
    def no_args_mode(self, value: bool) -> None:
        if value is False:
            self._path.mkdir(exist_ok=True, parents=True)
        self._no_args_mode = value

    def _key_file(self, key: str) -> Path:
        if self._no_args_mode is False:
            return self._path / f'{key}.{self.ext}'
        elif self._no_args_mode is True:
            return Path(f'{self._path}.{self.ext}')
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
    def __init__(self, cache_backend: CacheFiles, model: BaseModel | None):
        self.cache_backend = cache_backend
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
        self.cache_backend.no_args_mode = self.get_arg_count(func) == 0
        if self.model:
            _dump = self._model_dump  # todo: move to external middleware
            _load = self._model_load
        else:
            _dump = identity
            _load = identity
        if not is_generator(func):
            def hit(key: str) -> T | None:
                result = self.cache_backend[key]
                return _load(result)

            def miss(key: str, result: T | None) -> T | None:
                self.cache_backend[key] = _dump(result)
                return result

        else:
            def hit(key: str) -> Iterator[T]:
                for item in self.cache_backend.iter(key):
                    yield _load(item)

            def miss(key: str, result: Iterator[T]) -> Iterator[T]:
                with self.cache_backend.iter_write(key) as feed:
                    for item in result:
                        feed(_dump(item))
                        yield item

        def wrapper(slf, *args) -> T | None:
            key = '_'.join(str(arg) for arg in args)
            if key in self.cache_backend:
                return hit(key)
            return miss(key, func(slf, *args))

        wrapper.cache = self
        return wrapper


class Cache:
    def __init__(self, path: Path):
        self.path = path

    def __call__(
            self,
            key: str, model: BaseModel | None = None,
            serializer: SerializerBase = SerializerYaml(),
    ) -> CacheDecorator:
        cache_backend = CacheFiles(path=self.path / key, serializer=serializer)
        return CacheDecorator(cache_backend, model)


cache = Cache(Path(__file__).parent / 'cache')
