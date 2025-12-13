from decimal import Decimal

import numpy as np
from equations_solver.solvers.iteration_solver import IterationSolver
from equations_solver.steps.iteration_step import IterationStep


class JacobiIterationSolver(IterationSolver):
    @property
    def method_name(self) -> str:
        return "Jacobi Iteration"

    def iterate(self, A: np.ndarray, b: np.ndarray, x: np.ndarray) -> np.ndarray:
        # the new x values, computed using only the old x values
        x_new = np.full(self.n, +Decimal(0))

        for i in range(self.n):
            x_new[i] = b[i]

            for j in range(self.n):
                if j != i:
                    x_new[i] -= A[i, j] * x[j]

            x_new[i] /= A[i, i]

        matrix = np.column_stack((A, b))

        # add iteration step

        self.steps.append(
            IterationStep.jacobi(
                matrix,
                x.copy(),
                x_new.copy(),
                self.calculate_absolute_relative_error(x_new, x),
            )
        )

        return x_new
