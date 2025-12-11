from root_finder.finders.one_guess_finder import OneGuessFinder
from decimal import Decimal


class FixedPointFinder(OneGuessFinder):
    @property
    def method_name(self) -> str:
        return "Fixed-Point"

    def iterate(self, x: Decimal) -> Decimal:
        return self.function(x)
