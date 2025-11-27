import numpy as np
from decimal import Decimal
import time
from solvers.elimination_solver import EliminationSolver
from steps.row_operation import RowOperation
from solution_result import SolutionResult


class GaussJordanEliminationSolver(EliminationSolver):
    def solve(self) -> SolutionResult:
        start_time = time.time()

        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        if self.scaling:
            self.calculating_scaling_values(A)

        for k in range(n):
            # pivoting
            A, b = self.pivot(A, b, k)

            # check for singularity
            if abs(A[k, k]) < 1e-12:
                return SolutionResult(
                    message="System doesn't have a unique solution.",
                    execution_time=time.time() - start_time,
                )

            old_matrix = np.column_stack([A, b])

            pivot = A[k, k]
            for j in range(n):
                A[k, j] = A[k, j] / pivot
            b[k] = b[k] / pivot

            new_matrix = np.column_stack([A, b])

            self.steps.append(
                RowOperation.scale(old_matrix, new_matrix, k, +Decimal(1) / pivot)
            )

            for i in range(n):
                if i != k:
                    if abs(A[i, k]) < 1e-12:
                        continue

                    self.eliminate_row(A, b, i, k)

        execution_time = time.time() - start_time

        return SolutionResult(
            solution=b,
            steps=self.steps,
            execution_time=execution_time,
            message="Solution found using Gauss-Jordan Elimination.",
        )
