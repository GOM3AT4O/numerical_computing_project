import time
from decimal import Decimal
from typing import Callable, Optional

from root_finder.finder import Finder
from root_finder.result import Result
from utils import (
    calculate_absolute_relative_error,
    calculate_number_of_correct_significant_figures,
)


class FixedPointFinder(Finder):
    guess: Decimal

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        absolute_relative_error: Decimal,
        number_of_iterations: int,
        precision: int,
        guess: Decimal,
    ):
        super().__init__(
            function, absolute_relative_error, number_of_iterations, precision
        )
        self.guess = guess

    def find(self) -> Result:
        start_time = time.time()

        x = self.guess
        new_x = x

        absolute_relative_error: Optional[Decimal] = None
        number_of_correct_significant_figures: Optional[int] = None

        for iteration in range(1, self.number_of_iterations + 1):
            try:
                new_x = self.function(x)

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
                            message=f"Fixed-Point method converged after {iteration} iterations (Absolute Relative Error: {self.absolute_relative_error})",
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
                    message=f"Fixed-Point method can't continue: {e.args[0]}",
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
            message=f"Fixed-Point method did not converge within {self.number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
        )
