from abc import ABC, abstractmethod
from typing import Any, Optional, Type

from pybox.service import Container
from pybox.utils import T


__all__ = (
    'Inject',
    'InjectFromString',
    'InstanceIsRequiredException',
    'SetOperationIsNotPermittedException',
)


class SetOperationIsNotPermittedException(Exception):
    pass


class InstanceIsRequiredException(Exception):
    pass


class BaseInject:
    _attribute_name: Optional[str]

    def __init__(self):
        self._attribute_name = None

    def __set__(self, instance: T, value: Any):
        raise SetOperationIsNotPermittedException()

    def __set_name__(self, owner: Type[T], name: str):
        self._attribute_name = f'__di_{name}__'

    @abstractmethod
    def _get_service(self) -> T:
        pass

    def __get__(self, instance: Optional[T], owner: Type[T]) -> T:
        if instance is None:
            raise InstanceIsRequiredException()
        if self._attribute_name not in instance.__dict__:
            instance.__dict__[self._attribute_name] = self._get_service()
        return instance.__dict__[self._attribute_name]


class Inject(BaseInject):
    _dependency: Type[T]

    def __init__(self, dependency: Type[T]):
        super().__init__()
        self._dependency = dependency

    def _get_service(self) -> T:
        return Container().get(self._dependency)


class InjectFromString(BaseInject):
    _dependency: str

    def __init__(self, dependency: str):
        super().__init__()
        self._dependency = dependency

    def _get_service(self) -> T:
        return Container().get_from_string(self._dependency)
