import numpy as np
from abc import ABC, abstractmethod
from typing import List
from step import Step
from solution_result import SolutionResult


class Solver(ABC):
    A: np.ndarray
    b: np.ndarray
    n: int
    precision: int
    steps: List[Step]

    def __init__(self, A: np.ndarray, b: np.ndarray, precision: int = 6):
        self.A = A.copy()
        self.b = b.copy()
        self.n = len(b)
        self.precision = precision
        self.steps = []

    @abstractmethod
    def solve(self) -> SolutionResult:
        pass
