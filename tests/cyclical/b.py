from pybox.inject import InjectLazy
from pybox.service import IService

from tests.cyclical.a import A


class B(IService):
    a = InjectLazy(A)

    def who_am_i(self):
        print (f'B {id(self)}')
