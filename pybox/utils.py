from typing import Type, TypeVar

__all__ = (
    'Singleton',
    'T'
)


T = TypeVar('T')


class Singleton:
    def __init__(self, class_object: Type[T]) -> None:
        self.class_object = class_object
        self.instance = None

    def __call__(self, *args, **kwargs) -> T:
        if self.instance is None:
            self.instance = self.class_object(*args, **kwargs)
        return self.instance
