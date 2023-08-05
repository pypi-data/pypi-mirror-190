import types
from functools import wraps

class Profiled:
    def __init__(self):
        self.ncalls = []

    def __call__(self, a=0):
        def doc(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.ncalls.append(func.__name__)
            return wrapper
        return doc


    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

p = Profiled()
@p(a=0)
def f1():
    print(1)
@p()
def f2(b):
    print(b)

# f1()
# f2(3)
print(p.ncalls)
# print(f1.ncalls)
