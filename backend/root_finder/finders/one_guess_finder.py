import time
from abc import abstractmethod
from decimal import Decimal
from typing import Callable, Optional

from finder import Finder
from result import Result
from utils import calculating_number_of_correct_significant_figures


class OneGuessFinder(Finder):
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

    # the user facing name of the method, to be implemented by subclasses
    @property
    @abstractmethod
    def method_name(self) -> str:
        pass

    # perform a single iteration, to be implemented by subclasses
    @abstractmethod
    def iterate(self, x: Decimal) -> Decimal:
        pass

    def find(self) -> Result:
        start_time = time.time()

        x = self.guess
        new_x = x

        absolute_relative_error: Optional[Decimal] = None
        number_of_correct_significant_figures: Optional[int] = None

        for iteration in range(1, self.number_of_iterations + 1):
            try:
                new_x = self.iterate(x)
            except ValueError as e:
                if absolute_relative_error is not None:
                    number_of_correct_significant_figures = (
                        calculating_number_of_correct_significant_figures(
                            absolute_relative_error * Decimal("100"), self.precision
                        )
                    )
                execution_time = time.time() - start_time
                return Result(
                    root=x,
                    absolute_relative_error=absolute_relative_error,
                    number_of_correct_significant_figures=number_of_correct_significant_figures,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=e.args[0],
                )

            if iteration > 1:
                # Calculate relative error
                # Avoid division by zero so i will use absolute error in this case for now.
                absolute_relative_error = (
                    abs((new_x - x)) / abs(new_x) if new_x != 0 else abs(new_x - x)
                )

                # (Convergence check)
                if absolute_relative_error < self.absolute_relative_error:
                    number_of_correct_significant_figures = (
                        calculating_number_of_correct_significant_figures(
                            absolute_relative_error * Decimal("100"), self.precision
                        )
                    )
                    execution_time = time.time() - start_time
                    return Result(
                        root=new_x,
                        absolute_relative_error=absolute_relative_error,
                        number_of_correct_significant_figures=number_of_correct_significant_figures,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message="Newton-Raphson method converges. Root was approximately found successfully",
                    )

            f_new_x = self.function(new_x)

            if f_new_x == "0":
                if absolute_relative_error is not None:
                    number_of_correct_significant_figures = (
                        calculating_number_of_correct_significant_figures(
                            absolute_relative_error * Decimal("100"), self.precision
                        )
                    )
                execution_time = time.time() - start_time
                return Result(
                    root=new_x,
                    absolute_relative_error=absolute_relative_error,
                    number_of_correct_significant_figures=number_of_correct_significant_figures,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message="Newton-Raphson method converges. Root was approximately found successfully",
                )

            x = new_x
        if absolute_relative_error is not None:
            number_of_correct_significant_figures = (
                calculating_number_of_correct_significant_figures(
                    absolute_relative_error * Decimal("100"), self.precision
                )
            )
        execution_time = time.time() - start_time
        return Result(
            root=new_x,
            absolute_relative_error=absolute_relative_error,
            number_of_correct_significant_figures=number_of_correct_significant_figures,
            number_of_iterations=self.number_of_iterations,
            execution_time=execution_time,
            message="Newton-Raphson method did not converge within the maximum number of iterations.",
        )
