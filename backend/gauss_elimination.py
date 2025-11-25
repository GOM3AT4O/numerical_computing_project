from decimal import Decimal
import numpy as np
import time
from row_operation import RowOperation
from base_solver import LinearSystemSolver
from solution_result import SolutionResult


class GaussEliminationSolver(LinearSystemSolver):
    def solve(self) -> SolutionResult:
        start_time = time.time()

        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        for k in range(n - 1):
            A, b = self.partial_pivot(A, b, k)

            if abs(A[k, k]) < 1e-12:
                return SolutionResult(
                    message="System doesn't have a unique solution.",
                    execution_time=time.time() - start_time,
                )

            for i in range(k + 1, n):
                if abs(A[i, k]) < 1e-12:
                    continue

                factor = A[i, k] / A[k, k]

                old_matrix = np.column_stack([A, b])

                A[i, k + 1 :] = self.update_matrix_row(
                    A[i, k + 1 :], A[k, k + 1 :], factor
                )

                b[i] = self.update_vector_element(b[i], b[k], factor)

                A[i, k] = +Decimal(0)

                new_matrix = np.column_stack([A, b])

                self.steps.append(
                    RowOperation.add(old_matrix, new_matrix, i, k, -factor)
                )

        if abs(A[n - 1, n - 1]) < 1e-12:
            return SolutionResult(
                message="System doesn't have a unique solution.",
                execution_time=time.time() - start_time,
            )

        # Back substitution using base methods
        x = np.full(n, +Decimal(0))
        for i in range(n - 1, -1, -1):
            sum_val = b[i]
            for j in range(i + 1, n):
                sum_val = self.update_vector_element(
                    sum_val, A[i, j] * x[j], +Decimal("1")
                )
            x[i] = self.safe_divide(sum_val, A[i, i])

        execution_time = time.time() - start_time

        return SolutionResult(
            solution=x,
            steps=self.steps,
            execution_time=execution_time,
            message="Solution found using Gauss Elimination.",
        )
