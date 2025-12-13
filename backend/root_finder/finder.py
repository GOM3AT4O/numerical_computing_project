from decimal import Decimal
from typing import Callable
from abc import ABC, abstractmethod
from root_finder.result import Result


# base class for all root finding methods
class Finder(ABC):
    function: Callable[[Decimal], Decimal]
    absolute_relative_error: Decimal
    number_of_iterations: int
    precision: int

    def __init__(
        self,
        function: Callable[[Decimal], Decimal],
        absolute_relative_error: Decimal,
        number_of_iterations: int,
        precision: int,
    ):
        self.function = function
        self.absolute_relative_error = absolute_relative_error
        self.number_of_iterations = number_of_iterations
        self.precision = precision

    # find the root of the function
    @abstractmethod
    def find(self) -> Result:
        pass
