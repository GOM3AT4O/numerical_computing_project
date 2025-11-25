from decimal import Decimal
import numpy as np
from abc import ABC, abstractmethod
from typing import List, Tuple
from row_operation import RowOperation
from step import Step
from solution_result import SolutionResult


class LinearSystemSolver(ABC):
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

    def safe_divide(self, numerator: Decimal, denominator: Decimal) -> Decimal:
        if abs(denominator) < 1e-12:
            raise ZeroDivisionError("Divison by zero encountered")
        return numerator / denominator

    def update_matrix_row(
        self, target_row: np.ndarray, source_row: np.ndarray, factor: Decimal
    ) -> np.ndarray:
        updated_row = target_row.copy()
        for j in range(len(target_row)):
            elimination_term = factor * source_row[j]
            updated_row[j] = target_row[j] - elimination_term
        return updated_row

    def update_vector_element(
        self, target: Decimal, source: Decimal, factor: Decimal
    ) -> Decimal:
        elimination_term = factor * source
        return target - elimination_term

    def partial_pivot(
        self, A: np.ndarray, b: np.ndarray, k: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        max_idx = k + np.argmax(np.abs(A[k:, k]))
        if max_idx != k:
            old_matrix = np.column_stack([A, b])
            A[[k, max_idx]] = A[[max_idx, k]]
            b[[k, max_idx]] = b[[max_idx, k]]
            new_matrix = np.column_stack([A, b])
            step = RowOperation.swap(old_matrix, new_matrix, k, int(max_idx))
            self.steps.append(step)
        return A, b
