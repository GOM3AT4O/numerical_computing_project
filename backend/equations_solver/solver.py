from abc import ABC, abstractmethod
from typing import List

import numpy as np
from equations_solver.result import Result
from equations_solver.step import Step


# base class for all solvers
class Solver(ABC):
    A: np.ndarray
    b: np.ndarray
    n: int
    precision: int
    steps: List[Step]

    def __init__(self, A: np.ndarray, b: np.ndarray, precision: int):
        self.A = A.copy()
        self.b = b.copy()
        self.n = len(b)
        self.precision = precision
        self.steps = []

    # solve the system of linear equations
    @abstractmethod
    def solve(self) -> Result:
        pass
