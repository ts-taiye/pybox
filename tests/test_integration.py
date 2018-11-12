from pybox.inject import Inject
from pybox.service import IService, ServiceMode


class SingletonService(IService):
    def who_am_i(self):
        print(f'Singleton {id(self)}')


class FactoryService(IService):
    singleton = Inject(SingletonService)

    @classmethod
    def service_mode(cls):
        return ServiceMode.FACTORY

    def who_am_i(self):
        print(f'Factory {id(self)}')


class A:
    singleton1 = Inject(SingletonService)
    singleton2 = Inject(SingletonService)
    factory1 = Inject(FactoryService)
    factory2 = Inject(FactoryService)

    def who_am_i(self):
        print(f'A {id(self)}')


if __name__ == '__main__':
    a = A()
    assert a.singleton1 is a.singleton2
    assert isinstance(a.singleton1, SingletonService)

    assert isinstance(a.factory1, FactoryService)
    assert isinstance(a.factory2, FactoryService)
    assert a.factory1 is not a.factory2

    a.factory1.who_am_i()
    a.factory2.who_am_i()
    a.singleton1.who_am_i()
    a.singleton2.who_am_i()
    a.factory1.singleton.who_am_i()
    a.factory2.singleton.who_am_i()
    a.who_am_i()
