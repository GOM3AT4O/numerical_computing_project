import time
from abc import abstractmethod
from decimal import Decimal
from typing import Callable, Optional

from exceptions import ValidationError
from root_finder.finder import Finder
from root_finder.result import Result
from utils import (
    calculate_absolute_relative_error,
    calculate_number_of_correct_significant_figures,
)


class IntervalFinder(Finder):
    lower_bound: Decimal
    upper_bound: Decimal

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        absolute_relative_error: Decimal,
        number_of_iterations: int,
        precision: int,
        lower_bound: Decimal,
        upper_bound: Decimal,
    ):
        super().__init__(
            function, absolute_relative_error, number_of_iterations, precision
        )
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self._validate_interval()

    def _validate_interval(self):
        if self.lower_bound > self.upper_bound:
            raise ValidationError("lower bound must be less than upper bound")

        f_xl = self.function(self.lower_bound)
        f_xu = self.function(self.upper_bound)

        if f_xl * f_xu > 0:
            raise ValidationError("f(xl) and f(xu) must have different signs")

    # the user facing name of the method, to be implemented by subclasses
    @property
    @abstractmethod
    def method_name(self) -> str:
        pass

    # perform a single iteration, to be implemented by subclasses
    @abstractmethod
    def iterate(
        self, xl: Decimal, xu: Decimal, f_xl: Decimal, f_xu: Decimal
    ) -> Decimal:
        pass

    def find(self) -> Result:
        start_time = time.time()

        xl: Decimal = self.lower_bound
        xu: Decimal = self.upper_bound
        xr = Decimal(0)

        absolute_relative_error: Optional[Decimal] = None
        number_of_correct_significant_figures: Optional[int] = None

        for iteration in range(1, self.number_of_iterations + 1):
            try:
                old_xr = xr

                f_xl = self.function(xl)
                f_xu = self.function(xu)

                try:
                    xr = self.iterate(xl, xu, f_xl, f_xu)
                except ValueError as e:
                    if absolute_relative_error is not None:
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                    execution_time = time.time() - start_time
                    return Result(
                        root=xr,
                        absolute_relative_error=absolute_relative_error,
                        number_of_correct_significant_figures=number_of_correct_significant_figures,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=e.args[0],
                    )

                f_xr = self.function(xr)

                if iteration > 1:
                    absolute_relative_error = calculate_absolute_relative_error(
                        xr, old_xr
                    )
                    if absolute_relative_error < self.absolute_relative_error:
                        execution_time = time.time() - start_time
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                        return Result(
                            root=xr,
                            absolute_relative_error=absolute_relative_error,
                            number_of_correct_significant_figures=number_of_correct_significant_figures,
                            number_of_iterations=iteration,
                            execution_time=execution_time,
                            message=f"{self.method_name} method converged after {iteration} iterations (Absolute Relative Error: {self.absolute_relative_error})",
                        )

                if f_xl * f_xr < 0:
                    xu = xr
                elif f_xr * f_xu < 0:
                    xl = xr
                else:
                    execution_time = time.time() - start_time
                    if absolute_relative_error is not None:
                        number_of_correct_significant_figures = (
                            calculate_number_of_correct_significant_figures(
                                absolute_relative_error, self.precision
                            )
                        )
                    if f_xr == 0:
                        root = xr
                    elif f_xl == 0:
                        root = xl
                    else:
                        root = xu
                    return Result(
                        root=root,
                        absolute_relative_error=absolute_relative_error,
                        number_of_correct_significant_figures=number_of_correct_significant_figures,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=f"{self.method_name} method converged after {iteration} iterations (Absolute Relative Error: {self.absolute_relative_error})",
                    )
            except ValueError as e:
                execution_time = time.time() - start_time
                if absolute_relative_error is not None:
                    number_of_correct_significant_figures = (
                        calculate_number_of_correct_significant_figures(
                            absolute_relative_error, self.precision
                        )
                    )
                return Result(
                    root=xr,
                    absolute_relative_error=absolute_relative_error,
                    number_of_correct_significant_figures=number_of_correct_significant_figures,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"{self.method_name} method can't continue: {e.args[0]}",
                )

        if absolute_relative_error is not None:
            number_of_correct_significant_figures = (
                calculate_number_of_correct_significant_figures(
                    absolute_relative_error, self.precision
                )
            )
        execution_time = time.time() - start_time
        return Result(
            root=xr,
            absolute_relative_error=absolute_relative_error,
            number_of_correct_significant_figures=number_of_correct_significant_figures,
            number_of_iterations=self.number_of_iterations,
            execution_time=execution_time,
            message=f"{self.method_name} method did not converge within {self.number_of_iterations} iterations (Absolute Relative Error: {self.absolute_relative_error})",
        )
