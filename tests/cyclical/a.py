from pybox.inject import InjectLazy
from pybox.service import IService


class A(IService):
    b = InjectLazy('tests.cyclical.b.B')

    def who_am_i(self):
        print (f'A {id(self)}')
