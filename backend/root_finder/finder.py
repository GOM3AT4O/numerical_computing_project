from decimal import Decimal
from typing import Callable
from abc import ABC, abstractmethod
from result import Result


# base class for all root finding methods
class Finder(ABC):
    function: Callable[[Decimal], Decimal]
    epsilon: Decimal
    maximum_number_of_iterations: int
    precision: int

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        epsilon: Decimal,
        maximum_number_of_iterations: int,
        precision: int,
    ):
        self.function = function
        self.epsilon = epsilon
        self.maximum_number_of_iterations = maximum_number_of_iterations
        self.precision = precision

    # find the root of the function
    @abstractmethod
    def find(self) -> Result:
        pass
