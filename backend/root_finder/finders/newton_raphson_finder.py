from decimal import Decimal
from typing import Callable
from finders.one_guess_finder import OneGuessFinder


class NewtonRaphsonSolver(OneGuessFinder):
    derivative: Callable[[Decimal], Decimal]
    multiplicity: int

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        absolute_relative_error: Decimal,
        maximum_number_of_iterations: int,
        precision: int,
        guess: Decimal,
        derivative: Callable[[Decimal], Decimal],
        multiplicity: int = 1,
    ):
        super().__init__(
            function,
            absolute_relative_error,
            maximum_number_of_iterations,
            precision,
            guess,
        )
        self.derivative = derivative
        self.multiplicity = multiplicity

    @property
    def method_name(self) -> str:
        return "Newton-Raphson"

    def iterate(self, x: Decimal) -> Decimal:
        derivative_value = self.derivative(x)

        if derivative_value == Decimal("0"):
            raise ValueError(
                f"{self.method_name} method failed: Derivative too close to zero"
            )

        return x - (self.function(x) / derivative_value) * self.multiplicity
