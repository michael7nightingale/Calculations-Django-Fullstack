import dataclasses
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Iterable
from pydantic import BaseModel, Field
import sympy as sp
from functools import wraps
from sympy.abc import *

#from enum import Enum


class Literal(BaseModel):
    """
    Base model for literals, functions and constants.
    """
    literal: str
    name: str
    si: dict
    is_constant: bool = False
    is_function: bool = False
    ed: str | None = None
    value: float | None = None

    def __init__(self, **data):
        super().__init__(**data)
        self.si = defaultdict(lambda *x, **y: 1, **self.si)
        for opt, numeric in self.si.items():
            if numeric == 1:
                self.ed = opt
        if self.ed is None:
            raise ValueError("There is no main measure option~!")


class Constant(Literal):
    """Constant model (si = ed)"""
    is_constant: bool = True
    value: float


class Function(Literal):
    """Function model (si is of argument one) model"""
    is_function: bool = True
    py_name: str


class BaseFormula(ABC):
    __slots__ = ("formula", "literals", "args")
    _template: str

    def __init__(
        self,
        formula: str,
        name: str,
        **kwargs,
                 ):
        global storage
        if name in storage:
            raise AssertionError("Name is already in the storage!")
        storage[name] = self
        # literals_found = re.findall(r"", )

        self.formula: sp.Eq = sp.simplify(self._template.replace("_", ", ".join(formula.split("="))))
        self.args: str = "".join(kwargs.keys())
        self.literals: dict[str, Literal] = dict(kwargs)
    

    def __len__(self) -> int:
        return len(self.args)

    def __repr__(self) -> str:
        return str(self.formula)

    @abstractmethod
    def get_constants(self) -> Iterable[Literal]:
        pass

    @abstractmethod
    def get_formulas(self) -> Iterable[Literal]:
       pass



class Formula(BaseFormula):
    __slots__ = ()
    _template = "Eq(_)"
    
    def get_constants(self) -> Iterable[Literal]:
        return filter(
            lambda x: x.is_constant, 
            self.literals.values()
            )

    def get_formulas(self) -> Iterable[Literal]:
        return filter(
            lambda x: x.is_function, 
            self.literals.values()
            )

    def match(self, **nums):
        print(nums)
        expr = self.formula.subs(nums)
        print(expr)
        return sp.solve(expr)

    

# define storage
storage: dict[str, Formula] = {}    



 # ======================================= LITERALS ================================== # 

Impulse = Literal(si = {"kg*m/s": 1, "g*m/s": 0.001}, name = "Impulse", literal="p")
Speed = Literal(si = {"m/s": 1, "km/s": 1000}, name = "Speed", literal="V")
Mass= Literal(si = {"kg": 1, "g": 0.001}, name = "Mass", literal="m")
Way = Literal(si={"m": 1, "km": 1000, "sm": 0.01}, name='Way', literal="S")
Height = Literal(si={"m": 1, "km": 1000, "sm": 0.01}, name='Height', literal="h")
Density = Literal(si={"kg/m^3": 1}, literal="p", name="Density")
Pressure = Literal(si={"Pa": 1, "kPa": 1000, "mPa": 0.001}, name="Pressure", literal='ro')



 # ======================================= CONSTANTS ================================== # 

G = Constant(si={"m/s^2": 1}, name="Free fall acceleration", literal='g', value=9.813)



  # ======================================= FUNCTIONS ================================== # 


 # ======================================= FORMULAS ================================== # 

impulse = Formula(name='impulse', formula="p = m * V", p=Impulse, m=Mass, V=Speed)
pressure_liquid = Formula(name='pressure_liquid', formula="p = r * g * h", p=Pressure, r=Density, h=Height, g=G)