import time
from decimal import Decimal
from typing import Callable, Optional

from root_finder.finder import Finder
from root_finder.result import Result
from utils import (
    calculate_absolute_relative_error,
    calculate_number_of_correct_significant_figures,
)


class NewtonRaphsonFinder(Finder):
    derivative: Callable[[Decimal], Decimal]
    guess: Decimal
    multiplicity: int

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        absolute_relative_error: Decimal,
        number_of_iterations: int,
        precision: int,
        derivative: Callable[[Decimal], Decimal],
        guess: Decimal,
        multiplicity: int = 1,
    ):
        super().__init__(
            function, absolute_relative_error, number_of_iterations, precision
        )
        self.derivative = derivative
        self.guess = guess
        self.multiplicity = multiplicity

    def find(self) -> Result:
        start_time = time.time()

        x = self.guess
        new_x = x

        absolute_relative_error: Optional[Decimal] = None
        number_of_correct_significant_figures: Optional[int] = None

        for iteration in range(1, self.number_of_iterations + 1):
            try:
                derivative_value = self.derivative(x)

                if derivative_value == 0:
                    if absolute_relative_error is not None:
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                    execution_time = time.time() - start_time
                    return Result(
                        root=x,
                        absolute_relative_error=absolute_relative_error,
                        number_of_correct_significant_figures=number_of_correct_significant_figures,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message="Newton-Raphson method can't continue: Derivative is too close to zero",
                    )

                new_x = x - (self.function(x) / derivative_value) * self.multiplicity

                if iteration > 1:
                    # Calculate relative error
                    # Avoid division by zero so i will use absolute error in this case for now.
                    absolute_relative_error = calculate_absolute_relative_error(
                        new_x, x
                    )

                    # (Convergence check)
                    if absolute_relative_error < self.absolute_relative_error:
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                        execution_time = time.time() - start_time
                        return Result(
                            root=new_x,
                            absolute_relative_error=absolute_relative_error,
                            number_of_correct_significant_figures=number_of_correct_significant_figures,
                            number_of_iterations=iteration,
                            execution_time=execution_time,
                            message=f"Newton-Raphson method converged after {iteration} iterations (Absolute Relative Error: {self.absolute_relative_error})",
                        )

                f_new_x = self.function(new_x)

                if f_new_x == 0:
                    if absolute_relative_error is not None:
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                    execution_time = time.time() - start_time
                    return Result(
                        root=new_x,
                        absolute_relative_error=absolute_relative_error,
                        number_of_correct_significant_figures=number_of_correct_significant_figures,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=f"Newton-Raphson method converged after {iteration} iterations (Absolute Relative Error: {self.absolute_relative_error})",
                    )

                x = new_x
            except ValueError as e:
                execution_time = time.time() - start_time
                if absolute_relative_error is not None:
                    number_of_correct_significant_figures = (
                        calculate_number_of_correct_significant_figures(
                            absolute_relative_error, self.precision
                        )
                    )
                return Result(
                    root=new_x,
                    absolute_relative_error=absolute_relative_error,
                    number_of_correct_significant_figures=number_of_correct_significant_figures,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"Newton-Raphson method can't continue: {e.args[0]}",
                )
        if absolute_relative_error is not None:
            number_of_correct_significant_figures = (
                calculate_number_of_correct_significant_figures(
                    absolute_relative_error, self.precision
                )
            )
        execution_time = time.time() - start_time
        return Result(
            root=new_x,
            absolute_relative_error=absolute_relative_error,
            number_of_correct_significant_figures=number_of_correct_significant_figures,
            number_of_iterations=self.number_of_iterations,
            execution_time=execution_time,
            message=f"Newton-Raphson method did not converge within {self.number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
        )
