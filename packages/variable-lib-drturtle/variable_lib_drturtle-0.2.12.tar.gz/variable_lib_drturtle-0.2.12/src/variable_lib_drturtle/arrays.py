import numpy as np
from typing import List
import re
import matplotlib.pyplot as plt
from variable_lib_drturtle.variables import *


U_RE = re.compile(r"^(?P<name>.+?)(?:\((?P<unit>.+)\))?$", flags=re.MULTILINE)


class VariableList2D:
    def __init__(self, name: str, xi=0, yi=0):
        match = U_RE.match(name)
        self.unit = (match.group("unit") or "").strip()
        self.var_name = match.group("name").strip()
        self.name = f'{self.var_name}{f" ({self.unit})" if self.unit else ""}'.strip()

        initial = np.array([xi, yi])
        self.vals: np.ndarray[np.ndarray] = np.array([initial])

    def append(self, x, y):
        arr = np.array([x, y])
        self.add(arr)

    def add(self, arr: np.ndarray):
        self.vals = np.vstack((self.vals, arr))

    def __iadd__(self, other):
        """Adds other to the last value, then appends"""
        if not isinstance(other, np.ndarray):
            raise ValueError("Other must be ndarray")
        self.add(other + self.vals[-1])
        return self

    def __isub__(self, other):
        if not isinstance(other, np.ndarray):
            raise ValueError("Other must be ndarray")
        self.add(other + self.vals[-1])
        return self

    def __add__(self, other):
        return other + self.value

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __div__(self, other):
        return self.value / other

    def __pow__(self, other):
        return self.value**other

    def __getitem__(self, key: int):
        return self.vals[key]

    def __setitem__(self, key: int, val: np.ndarray):
        self.vals[key] = val

    def __delitem__(self, key: int):
        del self.vals[key]

    @classmethod
    def from_array(cls, name, arr: np.ndarray):
        return cls(name, arr[0], arr[1])

    @property
    def value(self):
        return self.vals[-1]

    @property
    def x_values(self):
        return np.array([x[0] for x in self.vals])

    @property
    def x_name(self):
        return f"X {self.name}"

    @property
    def y_values(self):
        return np.array([x[1] for x in self.vals])

    @property
    def y_name(self):
        return f"Y {self.name}"

    @property
    def magnitude(self):
        return np.linalg.norm(self.value)


def scatter_2d(x_list, y_list):
    if isinstance(x_list, VariableList):
        x_name = x_list.name
        x_vals = x_list
    elif isinstance(x_list, VariableList2D):
        x_name = x_list.x_name
        x_vals = x_list.x_values

    if isinstance(y_list, VariableList):
        y_name = y_list.name
        y_vals = y_vals
    elif isinstance(y_list, VariableList2D):
        y_name = y_list.y_name
        y_vals = y_list.y_values

    plt.scatter(x_vals, y_vals)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(f"{x_name} vs {y_name}")

    return plt
