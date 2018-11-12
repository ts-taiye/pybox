from pybox.inject import InjectFromString
from pybox.service import IService


class A(IService):
    b = InjectFromString('tests.cyclical.b.B')

    def who_am_i(self):
        print (f'A {id(self)}')
