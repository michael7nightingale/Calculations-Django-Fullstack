import dataclasses

storage = {}
import sympy as sp
from sympy.abc import *


ex = sp.simplify("Eq(x, y * z * w)")
ex: sp.Eq = ex
ex2 = ex.subs({y: 12, x: 2, z: 9})
print(sp.solve(ex2))


class Literal:
    def __init__(self, si: dict,
                 name: str,
                 ed: str,
                 literal: str):
        self.si = si
        self.name = name
        self.literal = literal
        self.ed = ed





ImpulseLiteral = Literal(si = {"kg*m/s": 1,
                               "g*m/s": 0.001,},
                         name = "Impulse",
                         ed = "kg*m/s",
                         literal="p")

SpeedLiteral = Literal(si = {"m/s": 1,
                               "km/s": 1000,},
                         name = "Speed",
                         ed = "m/s",
                         literal="V")


MassLiteral = Literal(si = {"kg": 1,
                               "g": 0.001,},
                         name = "Mass",
                         ed = "kg",
                         literal="m")


def storeByAttribute(cls):
    def inner(*_, **__):
        global storage
        instance = cls(*_, **__)
        attr_name = "name"
        if hasattr(instance, attr_name):
            attr_value = getattr(instance, attr_name)
            assert attr_value in storage, f"{attr_name} у {instance.__class__.__name__} уже есть"
            storage[attr_value] = instance
        return instance
    return inner


@storeByAttribute
class Formula:
    def __init__(self, pattern: str,
                 formula: str,
                 name: str,
                 **kwargs,
                 ):
        self.pattern = pattern
        self.formula = formula
        self.args = str(kwargs.keys())
        self.literals = dict(kwargs)

    def __len__(self):
        return len(self.args)

    def __repr__(self):
        return self.formula





# res = sp.solve(ex, [z])
# expr = res[0]
# asd = ex.subs({x: 12, z: 6, w: 2, y: 0})
# print(asd)
# print(dir(res[0]))


def register(slug: str):
    def decorator(cls):
        def inner(*args, **kwargs):
            assert slug not in storage, f"{slug} уже зарегистрирована."
            storage[slug] = cls
            return cls(*args, **kwargs)
        return inner
    return decorator


def Formula(cls):
    def inner(*_, **__):
        return cls(*_, **__)
    # cls.__mro__ =
    storage.update({cls: cls})
    return inner



class BaseFormula:
    def __new__(cls, *args, **kwargs):
        print("New called")
        return super().__new__(cls)

    def match_pattern(self):
        pass


@Formula
class Formula:
    pass


class Formulaaa():
    x = "p"
    y = "_V_"
    z = "m"
    pattern = "pattern"


