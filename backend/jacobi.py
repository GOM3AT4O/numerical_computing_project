from decimal import Decimal
import numpy as np
import time
from typing import List, Optional
from iteration import Iteration
from iterative_base import IterativeSolver
from solution_result import SolutionResult


class JacobiSolver(IterativeSolver):
    def __init__(
        self,
        A: np.ndarray,
        b: np.ndarray,
        precision: int = 6,
        initial_guess: Optional[List[Decimal]] = None,
        number_of_iterations: Optional[int] = None,
        absolute_relative_error: Optional[Decimal] = None,
    ):
        super().__init__(
            A,
            b,
            precision,
            initial_guess,
            number_of_iterations,
            absolute_relative_error,
        )

    def solve(self) -> SolutionResult:
        start_time = time.time()

        system_analysis = self.analyze_system()
        if system_analysis:
            return SolutionResult(
                message=system_analysis,
                execution_time=time.time() - start_time,
            )

        A = self.A
        b = self.b
        x = self.x0.copy()

        matrix = np.column_stack((A, b))

        # check if system might not converge
        if not self.check_diagonal_dominance():
            warning_message = "Warning: Matrix is not diagonally dominant. Thus, convergence is not really guaranteed."
        else:
            warning_message = ""

        # stopping condition
        if self.number_of_iterations is not None:
            # iterations mode
            number_of_iterations = 0

            for _ in range(self.number_of_iterations):
                x_new = np.full(self.n, +Decimal(0))

                for i in range(self.n):
                    dot_product = +Decimal(0)
                    for j in range(self.n):
                        if j != i:
                            product = A[i, j] * x[j]

                            dot_product = dot_product + product

                    numerator = b[i] - dot_product

                    x_new[i] = numerator / A[i, i]

                self.steps.append(Iteration.jacobi(matrix, x.copy(), x_new.copy()))

                x = x_new.copy()

                number_of_iterations += 1

            execution_time = time.time() - start_time
            return SolutionResult(
                solution=x,
                steps=self.steps,
                number_of_iterations=number_of_iterations,
                execution_time=execution_time,
                message=f"{warning_message} Jacobi method completed {self.number_of_iterations} iterations",
            )
        else:
            # absolute_relative_error mode
            number_of_iterations = 0
            maximum_number_of_iterations = 1000

            for _ in range(maximum_number_of_iterations):
                x_new = np.full(self.n, +Decimal(0))

                for i in range(self.n):
                    dot_product = +Decimal(0)
                    for j in range(self.n):
                        if j != i:
                            product = A[i, j] * x[j]

                            dot_product = dot_product + product

                    numerator = b[i] - dot_product

                    x_new[i] = numerator / A[i, i]

                number_of_iterations += 1

                self.steps.append(Iteration.jacobi(matrix, x.copy(), x_new.copy()))

                # check convergence
                if self.check_convergence(x_new, x):
                    execution_time = time.time() - start_time

                    return SolutionResult(
                        solution=x_new,
                        steps=self.steps,
                        number_of_iterations=number_of_iterations,
                        execution_time=execution_time,
                        message=f"{warning_message} Jacobi method converged after {number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
                    )

                x = x_new.copy()

            execution_time = time.time() - start_time

            return SolutionResult(
                solution=x,
                steps=self.steps,
                number_of_iterations=number_of_iterations,
                execution_time=execution_time,
                message=f"{warning_message} Jacobi method did not converge within {maximum_number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
            )
