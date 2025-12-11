import time
from decimal import Decimal
from typing import Callable, Optional

from exceptions import ValidationError
from root_finder.finder import Finder
from root_finder.result import Result
from utils import calculating_number_of_correct_significant_figures


class SecantFinder(Finder):
    first_guess: Decimal
    second_guess: Decimal

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        absolute_relative_error: Decimal,
        number_of_iterations: int,
        precision: int,
        first_guess: Decimal,
        second_guess: Decimal,
    ):
        super().__init__(
            function, absolute_relative_error, number_of_iterations, precision
        )
        self.first_guess = first_guess
        self.second_guess = second_guess

    def find(self) -> Result:
        start_time = time.time()

        x_prev = self.first_guess
        x_curr = self.second_guess

        try:
            f_prev = self.function(x_prev)
            f_curr = self.function(x_curr)
        except Exception as e:
            raise ValidationError(f"Error evaluating function at initial guesses: {e}")

        absolute_relative_error: Optional[Decimal] = None
        number_of_correct_significant_figures: Optional[int] = None

        # Start Iterations
        for iteration in range(1, self.number_of_iterations + 1):
            # Check for division by zero
            denominator = f_curr - f_prev
            if abs(denominator) < Decimal("1e-20"):
                execution_time = time.time() - start_time
                return Result(
                    root=x_curr,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"Secant method failed: Division by zero encountered at iteration {iteration}. f(x{iteration}) is too close to f(x{iteration - 1}).",
                )

            x_new = x_curr - (f_curr * (x_curr - x_prev) / denominator)

            # Calculate relative error
            absolute_relative_error = (
                abs((x_new - x_curr)) / abs(x_new)
                if x_new != 0
                else abs(x_new - x_curr)
            )

            # 1. Check if function value is close to zero
            f_new = self.function(x_new)

            if abs(f_new) == Decimal("0"):
                if absolute_relative_error is not None:
                    number_of_correct_significant_figures = (
                        calculating_number_of_correct_significant_figures(
                            absolute_relative_error * Decimal("100"), self.precision
                        )
                    )
                execution_time = time.time() - start_time
                return Result(
                    root=x_new,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"Secant method converges after {iteration} iterations. Root found at x = {x_new:.{self.precision}f} (tolerance: {self.absolute_relative_error})",
                )

            # 2. Check if relative error is within tolerance
            if absolute_relative_error < self.absolute_relative_error:
                if absolute_relative_error is not None:
                    number_of_correct_significant_figures = (
                        calculating_number_of_correct_significant_figures(
                            absolute_relative_error * Decimal("100"), self.precision
                        )
                    )
                execution_time = time.time() - start_time
                return Result(
                    root=x_new,
                    absolute_relative_error=absolute_relative_error,
                    number_of_correct_significant_figures=number_of_correct_significant_figures,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"Secant method converges after {iteration} iterations. Root found at x = {x_new:.{self.precision}f} (tolerance: {self.absolute_relative_error})",
                )

            # Update
            x_prev = x_curr
            f_prev = f_curr
            x_curr = x_new
            f_curr = f_new

        # If loop finishes without any return
        if absolute_relative_error is not None:
            number_of_correct_significant_figures = (
                calculating_number_of_correct_significant_figures(
                    absolute_relative_error * Decimal("100"), self.precision
                )
            )
        execution_time = time.time() - start_time
        return Result(
            root=x_curr,
            number_of_iterations=self.number_of_iterations,
            execution_time=execution_time,
            message=f"Secant method didn't converge after {self.number_of_iterations} iterations. Best approximation: x = {x_curr:.{self.precision}f}",
        )
