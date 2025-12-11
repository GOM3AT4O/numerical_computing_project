import time

from equations_solver.result import Result
from equations_solver.solvers.elimination_solver import EliminationSolver


class GaussEliminationSolver(EliminationSolver):
    def solve(self) -> Result:
        start_time = time.time()

        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        if self.scaling:
            self.calculating_scaling_values(A)

        for k in range(n - 1):
            A, b = self.pivot(A, b, k)

            if abs(A[k, k]) < 1e-12:
                return Result(
                    message="System doesn't have a unique solution.",
                    execution_time=time.time() - start_time,
                )

            for i in range(k + 1, n):
                if abs(A[i, k]) < 1e-12:
                    continue

                self.eliminate_row(A, b, i, k)

        if abs(A[n - 1, n - 1]) < 1e-12:
            return Result(
                message="System doesn't have a unique solution.",
                execution_time=time.time() - start_time,
            )

        # Back substitution using base methods
        x = self.back_substitution(A, b)

        execution_time = time.time() - start_time

        return Result(
            solution=x,
            steps=self.steps,
            execution_time=execution_time,
            message="Solution found using Gauss Elimination.",
        )
