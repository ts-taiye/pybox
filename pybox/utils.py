__all__ = (
    'Singleton',
)


class Singleton:
    def __init__(self, class_object):
        self.class_object = class_object
        self.instance = None

    def __call__(self,*args,**kwds):
        if self.instance is None:
            self.instance = self.class_object(*args,**kwds)
        return self.instance
