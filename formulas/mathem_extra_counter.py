import sympy as sp
import numpy as np


def roundResult(nums_comma: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return round(result, nums_comma)
        return wrapper
    return decorator


def equation(equation: str) -> list[dict]:
    try:
        return sp.solve(
            sp.sympify("Eq(" + equation.replace("=", ",") + ")"),
            dict=True
        )
    except Exception as e:
        print(str(e))
        return [{'Результат': "Ошибка в написании уравнения!"}]


def equation_system(equations):
    try:
        print(equations)
        return sp.solve(
            [sp.sympify("Eq(" + equation_.replace("=", ",") + ")") for equation_ in equations],
            dict=True
        )
    except Exception as e:
        print(str(e))
        return [{'Результат': "Ошибка в написании уравнения!"}]

# print(equation('x', 'x**3 - 2 = 12 + 3'))
# print(system_equation(['x - 2 + y - 23 = 123', "x + 123 =y"]))


