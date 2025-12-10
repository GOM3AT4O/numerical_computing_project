from abc import abstractmethod
from decimal import Decimal
import numpy as np
from solver import Solver
from exceptions import ValidationError
import time
from result import Result


# base class for iterative solvers (like Jacobi, Gauss-Seidel, etc.)
class IterationSolver(Solver):
    x0: np.ndarray
    number_of_iterations: int
    absolute_relative_error: Decimal

    def __init__(
        self,
        A: np.ndarray,
        b: np.ndarray,
        precision,
        initial_guess,
        number_of_iterations,
        absolute_relative_error,
    ):
        super().__init__(A, b, precision)

        self.number_of_iterations = number_of_iterations
        self.absolute_relative_error = Decimal(absolute_relative_error)

        if initial_guess is not None:
            self.x0 = np.array([+Decimal(x) for x in initial_guess], dtype=Decimal)
            if len(self.x0) != self.n:
                raise ValidationError(
                    f"Initial guess length must match number of variables ({self.n})"
                )
        else:
            self.x0 = np.full(self.n, +Decimal(0))

    # calculate absolute relative error for convergence checking
    @staticmethod
    def calculate_absolute_relative_error(
        x_new: np.ndarray, x_old: np.ndarray
    ) -> Decimal:
        # make sure we don't divide by zero
        denominator = np.vectorize(lambda x: max(abs(x), Decimal("1e-10")))(
            np.abs(x_new)
        )
        return np.max(np.abs(x_new - x_old) / denominator)

    # check if the coefficients matrix is diagonally dominant
    def check_diagonal_dominance(self) -> bool:
        # keep track if at least one row is strictly diagonally dominant
        at_least_one_strict = False

        for i in range(self.n):
            row_sum = np.sum(np.abs(self.A[i, :])) - np.abs(self.A[i, i])
            if np.abs(self.A[i, i]) < row_sum:
                # the inequality is not satisfied for this row
                return False
            elif np.abs(self.A[i, i]) > row_sum:
                # this row is strictly diagonally dominant
                at_least_one_strict = True
        return at_least_one_strict

    # the user facing name of the method, to be implemented by subclasses
    @property
    @abstractmethod
    def method_name(self) -> str:
        pass

    # perform a single iteration, to be implemented by subclasses
    @abstractmethod
    def iterate(self, A: np.ndarray, b: np.ndarray, x: np.ndarray) -> np.ndarray:
        pass

    def solve(self) -> Result:
        start_time = time.time()

        A = self.A
        b = self.b
        n = self.n
        x = self.x0.copy()

        # check if there is any zero diagonal element, since iterative
        # methods can't work in that case

        zero_diagonals = []
        for i in range(n):
            if abs(A[i, i]) < 1e-12:
                zero_diagonals.append(i + 1)

        if zero_diagonals:
            return Result(
                message=f"Can't use iterative methods: zero diagonal elements found in equations {zero_diagonals}. Reorder your equations to avoid zero diagonal elements.",
                execution_time=time.time() - start_time,
            )

        # check if system might not converge
        if not self.check_diagonal_dominance():
            warning_message = "Warning: Matrix is not diagonally dominant. Thus, convergence is not really guaranteed."
        else:
            warning_message = ""

        number_of_iterations = 0
        maximum_number_of_iterations = self.number_of_iterations

        # iterate until we reach maximum number of iterations specified
        for _ in range(maximum_number_of_iterations):
            # do an iteration
            x_new = self.iterate(A, b, x)

            number_of_iterations += 1

            # calculate absolute relative error
            absolute_relative_error = self.calculate_absolute_relative_error(x_new, x)

            # check convergence
            if absolute_relative_error < self.absolute_relative_error:
                # we reached convergence, return early
                execution_time = time.time() - start_time

                return Result(
                    solution=x_new,
                    steps=self.steps,
                    number_of_iterations=number_of_iterations,
                    execution_time=execution_time,
                    message=f"{warning_message} {self.method_name} method converged after {number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
                )

            x = x_new.copy()

        execution_time = time.time() - start_time

        # we did not converge within the maximum number of iterations
        return Result(
            solution=x,
            steps=self.steps,
            number_of_iterations=number_of_iterations,
            execution_time=execution_time,
            message=f"{warning_message} {self.method_name} method did not converge within {maximum_number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
        )
