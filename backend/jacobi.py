import numpy as np
import time
from typing import List, Optional
from iterative_base import IterativeSolver
from solution_result import SolutionResult


class JacobiSolver(IterativeSolver):
    def __init__(
        self,
        A: np.ndarray,
        b: np.ndarray,
        precision: int = 6,
        initial_guess: Optional[List[float]] = None,
        max_iterations: Optional[int] = None,
        tolerance: Optional[float] = None,
    ):
        super().__init__(A, b, precision, initial_guess, max_iterations, tolerance)

    def solve(self) -> SolutionResult:
        start_time = time.time()

        system_analysis = self.analyze_system()
        if system_analysis:
            return SolutionResult(
                has_solution=False,
                message=system_analysis,
                execution_time=time.time() - start_time,
            )

        A = self.A
        b = self.b
        x = self.x0.copy()

        # check if system might not converge
        if not self.check_diagonal_dominance():
            warning_msg = "Warning: Matrix is not diagonally dominant. Thus, convergence is not really guaranteed."
        else:
            warning_msg = ""

        # stopping condition
        if self.use_iteration_limit:
            # iterations mode
            iteration_count = 0

            for iteration in range(self.max_iterations):
                x_new = np.zeros(self.n)

                for i in range(self.n):
                    dot_product = 0
                    for j in range(self.n):
                        if j != i:
                            product = self.round_to_sf(A[i, j] * x[j])

                            dot_product = self.round_to_sf(dot_product + product)

                    numerator = self.round_to_sf(b[i] - dot_product)

                    x_new[i] = self.round_to_sf(numerator / A[i, i])

                x = x_new.copy()

                iteration_count += 1

            execution_time = time.time() - start_time
            return SolutionResult(
                solution=self.round_solution(x),
                iterations=iteration_count,
                execution_time=execution_time,
                message=f"{warning_msg} Jacobi method completed {self.max_iterations} iterations",
                has_solution=True,
            )
        else:
            # tolerance mode
            iteration_count = 0
            max_safe_iterations = 1000

            for iteration in range(max_safe_iterations):
                x_new = np.zeros(self.n)

                for i in range(self.n):
                    dot_product = 0
                    for j in range(self.n):
                        if j != i:
                            product = self.round_to_sf(A[i, j] * x[j])

                            dot_product = self.round_to_sf(dot_product + product)

                    numerator = self.round_to_sf(b[i] - dot_product)

                    x_new[i] = self.round_to_sf(numerator / A[i, i])

                iteration_count += 1

                # check convergence
                if self.check_convergence(x_new, x):
                    execution_time = time.time() - start_time

                    return SolutionResult(
                        solution=self.round_solution(x_new),
                        iterations=iteration_count,
                        execution_time=execution_time,
                        message=f"{warning_msg} Jacobi method converged after {iteration_count} iterations ( tolerance:{self.tolerance})",
                        has_solution=True,
                    )

                x = x_new.copy()

            execution_time = time.time() - start_time

            return SolutionResult(
                solution=self.round_solution(x_new),
                iterations=iteration_count,
                execution_time=execution_time,
                message=f"{warning_msg} Jacobi method did not converge within {max_safe_iterations} iterations ( tolerance:{self.tolerance})",
                has_solution=True,
            )
