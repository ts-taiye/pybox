from typing import Type, TypeVar, Optional

__all__ = (
    'Singleton',
    'T'
)


T = TypeVar('T')


class Singleton:

    _class_object: Type[T]
    _instance = Optional[T]

    def __init__(self, class_object: Type[T]) -> None:
        self._class_object = class_object
        self._instance = None

    def __call__(self, *args, **kwargs) -> T:
        if self._instance is None:
            self._instance = self._class_object(*args, **kwargs)
        return self._instance
