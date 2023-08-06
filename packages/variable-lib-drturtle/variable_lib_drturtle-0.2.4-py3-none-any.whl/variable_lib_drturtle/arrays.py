import numpy as np
from typing import List
import re

U_RE = re.compile(r"^(?P<name>.+?)(?:\((?P<unit>.+)\))?$", flags=re.MULTILINE)


class VariableList2D:
    def __init__(self, name: str, xi=0, yi=0):
        init = np.array([xi, yi])
        self.name = name
        self.vals: List[np.ndarray] = [init]

    def append(self, x, y):
        arr = np.array([x, y])
        self.vals.append(arr)

    def add(self, arr: np.ndarray):
        self.vals.append(arr)

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
    def x_values(self):
        return np.array([x[0] for x in self.vals])

    @property
    def y_values(self):
        return np.array([x[1] for x in self.vals])
