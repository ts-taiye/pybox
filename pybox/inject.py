from typing import Any, Optional, Type

from pybox.service import Container, IService
from pybox.utils import T


__all__ = (
    'Inject',
    'InstanceIsRequiredException',
    'SetOperationIsNotPermittedException',
)


class SetOperationIsNotPermittedException(Exception):
    pass


class InstanceIsRequiredException(Exception):
    pass


class InjectLazy:
    _dependency: Type[IService]
    _attribute_name: Optional[str]

    def __init__(self, dependency: Type[IService]):
        self._dependency = dependency
        self._attribute_name = None

    def __set__(self, instance: IService, value: Any):
        raise SetOperationIsNotPermittedException()

    def __set_name__(self, owner: Type[IService], name: str):
        self._attribute_name = f'__di_{name}__'

    def __get__(self, instance: Optional[IService], owner: Type[IService]) -> IService:
        if instance is None:
            raise InstanceIsRequiredException()
        if self._attribute_name not in instance.__dict__:
            instance.__dict__[self._attribute_name] = Container().get(self._dependency)
        return instance.__dict__[self._attribute_name]


def Inject(dependency: Type[T]) -> T:
    return Container().get(dependency)
