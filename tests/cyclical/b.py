from pybox.inject import Inject
from pybox.service import IService

from tests.cyclical.a import A


class B(IService):
    a = Inject(A)

    def who_am_i(self):
        print (f'B {id(self)}')
