import time
from decimal import Decimal
from typing import Callable, Optional

from exceptions import ValidationError
from root_finder.finder import Finder
from root_finder.result import Result
from utils import (
    calculate_absolute_relative_error,
    calculate_number_of_correct_significant_figures,
)


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
        x_new = x_curr

        try:
            f_prev = self.function(x_prev)
            f_curr = self.function(x_curr)
        except Exception as e:
            raise ValidationError(f"Error evaluating function at initial guesses: {e}")

        absolute_relative_error: Optional[Decimal] = None
        number_of_correct_significant_figures: Optional[int] = None

        # Start Iterations
        for iteration in range(1, self.number_of_iterations + 1):
            try:
                # Check for division by zero
                denominator = f_curr - f_prev
                if abs(denominator) < Decimal("1e-20"):
                    execution_time = time.time() - start_time
                    return Result(
                        root=x_curr,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=f"Secant method can't continue: Division by zero encountered at iteration {iteration}. f(x{iteration}) is too close to f(x{iteration - 1}).",
                    )

                x_new = x_curr - (f_curr * (x_curr - x_prev) / denominator)

                # Calculate relative error
                absolute_relative_error = calculate_absolute_relative_error(
                    x_new, x_curr
                )

                # 1. Check if function value is close to zero
                f_new = self.function(x_new)

                if f_new == 0:
                    if absolute_relative_error is not None:
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                    execution_time = time.time() - start_time
                    return Result(
                        root=x_new,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=f"Secant method converged after {iteration} iterations, the function at the root is zero (Absolute Relative Error: {self.absolute_relative_error})",
                    )

                # 2. Check if relative error is within tolerance
                if absolute_relative_error < self.absolute_relative_error:
                    if absolute_relative_error is not None:
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                    execution_time = time.time() - start_time
                    return Result(
                        root=x_new,
                        absolute_relative_error=absolute_relative_error,
                        number_of_correct_significant_figures=number_of_correct_significant_figures,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=f"Secant method converged after {iteration} iterations (Absolute Relative Error: {self.absolute_relative_error})",
                    )

                # Update
                x_prev = x_curr
                f_prev = f_curr
                x_curr = x_new
                f_curr = f_new
            except ValueError as e:
                execution_time = time.time() - start_time
                if absolute_relative_error is not None:
                    number_of_correct_significant_figures = (
                        calculate_number_of_correct_significant_figures(
                            absolute_relative_error, self.precision
                        )
                    )
                return Result(
                    root=x_new,
                    absolute_relative_error=absolute_relative_error,
                    number_of_correct_significant_figures=number_of_correct_significant_figures,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"Secant method can't continue: {e.args[0]}",
                )

        # If loop finishes without any return
        if absolute_relative_error is not None:
            number_of_correct_significant_figures = (
                calculate_number_of_correct_significant_figures(
                    absolute_relative_error, self.precision
                )
            )
        execution_time = time.time() - start_time
        return Result(
            root=x_curr,
            number_of_iterations=self.number_of_iterations,
            execution_time=execution_time,
            message=f"Secant method did not converge within {self.number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
        )
