import numpy as np
from decimal import Decimal
import time
from row_operation import RowOperation
from base_solver import LinearSystemSolver
from solution_result import SolutionResult


class GaussJordanSolver(LinearSystemSolver):
    def solve(self) -> SolutionResult:
        start_time = time.time()

        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        for k in range(n):
            # pivoting
            A, b = self.partial_pivot(A, b, k)

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

                    factor = A[i, k]

                    old_matrix = np.column_stack([A, b])

                    A[i] = self.update_matrix_row(A[i], A[k], factor)

                    b[i] = self.update_vector_element(b[i], b[k], factor)

                    A[i, k] = +Decimal(0)

                    new_matrix = np.column_stack([A, b])

                    self.steps.append(
                        RowOperation.add(old_matrix, new_matrix, i, k, -factor)
                    )

        execution_time = time.time() - start_time

        return SolutionResult(
            solution=b,
            steps=self.steps,
            execution_time=execution_time,
            message="Solution found using Gauss-Jordan Elimination.",
        )
