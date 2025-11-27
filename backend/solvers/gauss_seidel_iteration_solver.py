import numpy as np
from steps.iteration import Iteration
from solvers.iteration_solver import IterationSolver


class GaussSeidelIterationSolver(IterationSolver):
    @property
    def method_name(self) -> str:
        return "Gauss-Seidel Iteration"

    def iterate(self, A: np.ndarray, b: np.ndarray, x: np.ndarray) -> np.ndarray:
        x_new = x.copy()

        for i in range(self.n):
            x_new[i] = b[i]

            for j in range(self.n):
                if j != i:
                    x_new[i] -= A[i, j] * x_new[j]

            x_new[i] /= A[i, i]

        matrix = np.column_stack((A, b))

        self.steps.append(
            Iteration.gauss_seidel(
                matrix,
                x.copy(),
                x_new.copy(),
                self.calculate_absolute_relative_error(x_new, x),
            )
        )

        return x_new
