from tests.cyclical.a import A
from tests.cyclical.b import B


if __name__ == '__main__':
    a = A()
    b = B()

    assert isinstance(a.b, B)
    assert isinstance(b.a, A)

    a.who_am_i()
    b.who_am_i()
    a.b.who_am_i()
    b.a.who_am_i()
