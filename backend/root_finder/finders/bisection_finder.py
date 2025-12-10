from decimal import Decimal

from finders.interval_finder import IntervalFinder


class BisectionFinder(IntervalFinder):
    @property
    def method_name(self) -> str:
        return "Bisection"

    def iterate(
        self, xl: Decimal, xu: Decimal, f_xl: Decimal, f_xu: Decimal
    ) -> Decimal:
        return (xl + xu) / Decimal("2")
