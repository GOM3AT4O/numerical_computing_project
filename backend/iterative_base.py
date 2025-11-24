from decimal import Decimal
import numpy as np
from typing import List, Optional
from base_solver import LinearSystemSolver
from exceptions import ValidationError


class IterativeSolver(LinearSystemSolver):
    def __init__(
        self,
        A: np.ndarray,
        b: np.ndarray,
        precision: int = 10,
        initial_guess: Optional[List[Decimal]] = None,
        number_of_iterations: Optional[int] = None,
        absolute_relative_error: Optional[Decimal] = None,
    ):
        super().__init__(A, b, precision)

        # validate that only one stopping condition is provided!!
        if number_of_iterations is not None and absolute_relative_error is not None:
            raise ValidationError(
                "Can't specify both number_of_iterations and absolute_relative_error."
            )

        if number_of_iterations is None and absolute_relative_error is None:
            number_of_iterations = 50

        self.number_of_iterations = number_of_iterations
        if absolute_relative_error is not None:
            self.absolute_relative_error = Decimal(absolute_relative_error)

        if initial_guess is not None:
            self.x0 = np.array([+Decimal(x) for x in initial_guess], dtype=Decimal)
            if len(self.x0) != self.n:
                raise ValidationError(
                    f"Initial guess length must match number of variables ({self.n})"
                )
        else:
            self.x0 = np.full(self.n, +Decimal(0))

    def check_convergence(self, x_new: np.ndarray, x_old: np.ndarray) -> bool:
        if self.absolute_relative_error is None:
            return False

        denominator = np.vectorize(lambda x: max(abs(x), Decimal("1e-10")))(
            np.abs(x_new)
        )
        relative_error = np.max(np.abs(x_new - x_old) / denominator)
        return relative_error < self.absolute_relative_error

    def check_diagonal_dominance(self) -> bool:
        at_least_one_strict = False
        for i in range(self.n):
            row_sum = np.sum(np.abs(self.A[i, :])) - np.abs(self.A[i, i])
            if np.abs(self.A[i, i]) < row_sum:
                return False
            elif np.abs(self.A[i, i]) > row_sum:
                at_least_one_strict = True
        return at_least_one_strict

    def analyze_system(self) -> Optional[str]:
        A = self.A
        n = self.n

        zero_diagonals = []
        for i in range(n):
            if abs(A[i, i]) < 1e-12:
                zero_diagonals.append(i + 1)

        if zero_diagonals:
            return f"Can't use iterative methods: zero diagonal elements found in equations {zero_diagonals}. Reorder your equations to avoid zero diagonal elements."
