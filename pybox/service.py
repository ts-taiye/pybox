from abc import ABC, abstractmethod
from enum import Enum, unique
from importlib import import_module
from typing import Dict, Optional, Type

from pybox.utils import Singleton

__all__ = (
    'Container',
    'FactoryInstanceGetter',
    'InstanceGetter',
    'InvalidServiceModeException',
    'IService',
    'ServiceIsAlreadyRegisteredException',
    'ServiceIsNotFoundException',
    'ServiceMeta',
    'ServiceMode',
    'SingletonInstanceGetter',
)


@unique
class ServiceMode(Enum):
    SINGLETON = 'singleton'
    FACTORY = 'factory'


class IService:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Container().register(cls)

    @classmethod
    def service_mode(cls) -> ServiceMode:
        return ServiceMode.SINGLETON


class InvalidServiceModeException(Exception):
    pass


class InstanceGetter(ABC):
    _service: Type[IService]

    def __init__(self, service: Type[IService]):
        self._service = service

    @abstractmethod
    def get_instance(self) -> IService:
        pass


class SingletonInstanceGetter(InstanceGetter):
    _instance: Optional[IService]

    def __init__(self, service: Type[IService]):
        super().__init__(service)
        self._instance = None

    def get_instance(self) -> IService:
        if self._instance is None:
            self._instance = self._service()
        return self._instance


class FactoryInstanceGetter(InstanceGetter):
    def get_instance(self) -> IService:
        return self._service()


class ServiceMeta:
    _service: Type[IService]
    _instance_getter: Optional[InstanceGetter]

    def __init__(self, service: Type[IService]):
        self._service = service
        self._instance_getter = None

    def _get_instance_getter(self) -> InstanceGetter:
        if self._instance_getter is None:
            mode = self._service.service_mode()
            if ServiceMode.SINGLETON == mode:
                self._instance_getter = SingletonInstanceGetter(self._service)
            elif ServiceMode.FACTORY == mode:
                self._instance_getter = FactoryInstanceGetter(self._service)
            else:
                raise InvalidServiceModeException()
        return self._instance_getter

    def get_instance(self) -> IService:
        return self._get_instance_getter().get_instance()


class ServiceIsAlreadyRegisteredException(Exception):
    pass


class ServiceIsNotFoundException(Exception):
    pass


@Singleton
class Container:
    _storage: Dict[Type[IService], ServiceMeta]

    def __init__(self):
        self._storage = {}

    @staticmethod
    def _import(path):
        last_dot = path.rfind('.')
        module = import_module(path[:last_dot])
        return getattr(module, path[last_dot + 1:])

    def register(self, service: Type[IService]):
        if service in self._storage:
            raise ServiceIsAlreadyRegisteredException()

        self._storage[service] = ServiceMeta(service)

    def get_from_string(self, service: str) -> IService:
        return self.get(self._import(service))

    def get(self, service: Type[IService]) -> IService:
        try:
            service = self._storage[service]
        except KeyError:
            raise ServiceIsNotFoundException from None

        return service.get_instance()
