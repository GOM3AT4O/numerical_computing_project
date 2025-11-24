import numpy as np
from typing import List, Optional
from base_solver import LinearSystemSolver
from exceptions import ValidationError


class IterativeSolver(LinearSystemSolver):
    def __init__(
        self,
        A: np.ndarray,
        b: np.ndarray,
        precision: int = 6,
        initial_guess: Optional[List[float]] = None,
        max_iterations: Optional[int] = None,
        tolerance: Optional[float] = None,
    ):
        super().__init__(A, b, precision)

        # validate that only one stopping condition is provided!!
        if max_iterations is not None and tolerance is not None:
            raise ValidationError("Can't specify both max_iterations and tolerance.")

        if max_iterations is None and tolerance is None:
            max_iterations = 50

        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.use_iteration_limit = max_iterations is not None

        if initial_guess is not None:
            self.x0 = np.array(initial_guess, dtype=float)
            if len(self.x0) != self.n:
                raise ValidationError(
                    f"Initial guess length must match number of variables ({self.n})"
                )
        else:
            self.x0 = np.zeros(self.n)

    def check_convergence(self, x_new: np.ndarray, x_old: np.ndarray) -> bool:
        if self.tolerance is None:
            return False

        denominator = np.maximum(np.abs(x_new), 1e-10)
        relative_error = np.max(np.abs(x_new - x_old) / denominator)
        return relative_error < self.tolerance

    def check_diagonal_dominance(self) -> bool:
        for i in range(self.n):
            row_sum = np.sum(np.abs(self.A[i, :])) - np.abs(self.A[i, i])
            if np.abs(self.A[i, i]) <= row_sum:
                return False
        return True

    def analyze_system(self) -> Optional[str]:
        A = self.A
        b = self.b
        n = self.n

        zero_diagonals = []
        for i in range(n):
            if abs(A[i, i]) < 1e-12:
                zero_diagonals.append(i + 1)

        if zero_diagonals:
            return f"Can't use iterative methods: zero diagonal elements found in equations {zero_diagonals}. Reorder your equations to avoid zero diagonal elements."

        # rank analize
        try:
            # augumented matrix[A|b]
            Ab = np.column_stack((A, b))

            # check if rank(A) < rank(Ab)-inconsistent system
            rank_A = np.linalg.matrix_rank(A)
            rank_Ab = np.linalg.matrix_rank(Ab)

            if rank_A < rank_Ab:
                return f"Inconsistent system: no solution exists (rank(A) = {rank_A}<rank([A|b])={rank_Ab})"

            # chcek for infinite solutions  by cchecking rank <number of variables
            if rank_A < n:
                return f"System has infinite solutions: rank(A)= {rank_A}<number of variables = {n}"

        except np.linalg.LinAlgError:
            pass

        for i in range(n):
            if np.allclose(A[i, :], 0) and not np.isclose(b[i], 0):
                return f"Inconsistent system: equation {i + 1} is 0={b[i]}"

        return None

