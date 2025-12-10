import time
from abc import abstractmethod
from decimal import Decimal
from typing import Callable

from exceptions import ValidationError
from finder import Finder
from result import Result
from utils import calculating_number_of_correct_significant_figures


class IntervalFinder(Finder):
    lower_bound: Decimal
    upper_bound: Decimal

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        absolute_relative_error: Decimal,
        maximum_number_of_iterations: int,
        precision: int,
        lower_bound: Decimal,
        upper_bound: Decimal,
    ):
        super().__init__(
            function, absolute_relative_error, maximum_number_of_iterations, precision
        )
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self._validate_interval()

    def _validate_interval(self):
        if self.lower_bound > self.upper_bound:
            raise ValidationError("lower_bound must be less than upper_bound")

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

    def solve(self) -> Result:
        start_time = time.time()

        xl: Decimal = self.lower_bound
        xu: Decimal = self.upper_bound
        xr = Decimal(0)

        absolute_relative_error = Decimal("infinity")

        for iteration in range(1, self.maximum_number_of_iterations + 1):
            old_xr = xr

            f_xl = self.function(xl)
            f_xu = self.function(xu)

            try:
                xr = self.iterate(xl, xu, f_xl, f_xu)
            except ValueError as e:
                execution_time = time.time() - start_time
                return Result(
                    root=xr,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=e.args[0],
                )

            f_xr = self.function(xr)

            if iteration > 1:
                absolute_relative_error = (
                    abs((xr - old_xr)) / abs(xr) if xr != 0 else abs(xr - old_xr)
                )
                if absolute_relative_error < self.epsilon or abs(f_xr) < self.epsilon:
                    execution_time = time.time() - start_time
                    number_of_correct_significant_figures = (
                        calculating_number_of_correct_significant_figures(
                            absolute_relative_error * Decimal("100"), self.precision
                        )
                    )
                    return Result(
                        root=xr,
                        absolute_relative_error=absolute_relative_error,
                        number_of_correct_significant_figures=number_of_correct_significant_figures,
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=f"{self.method_name} method converges after {iteration} iterations alright? the root was found in x = {xr:.{self.precision}f} with f(x) = 0 (tolerance: {self.epsilon})",
                    )

            if f_xl * f_xr < 0:
                xu = xr
            elif f_xr * f_xu < 0:
                xl = xr
            else:
                execution_time = time.time() - start_time
                number_of_correct_significant_figures = (
                    calculating_number_of_correct_significant_figures(
                        absolute_relative_error * Decimal("100"), self.precision
                    )
                )
                return Result(
                    root=xr,
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"{self.method_name} method converges after {iteration} iterations alright? the root was found in x = {xr:.{self.precision}f} with f(x) = 0 (tolerance: {self.epsilon})",
                    number_of_correct_significant_figures=number_of_correct_significant_figures,
                )

        execution_time = time.time() - start_time
        number_of_correct_significant_figures = (
            calculating_number_of_correct_significant_figures(
                absolute_relative_error * Decimal("100"), self.precision
            )
        )
        return Result(
            root=xr,
            number_of_correct_significant_figures=number_of_correct_significant_figures,
            number_of_iterations=self.maximum_number_of_iterations,
            execution_time=execution_time,
            message=f"{self.method_name} method didn't converge after {self.maximum_number_of_iterations} iterations sorry the bst we got is x= {xr:.{self.precision}f} with f(x) = {self.function(xr):.{self.precision}f} tolerance is going to be : {self.epsilon})",
        )
