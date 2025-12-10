from decimal import Decimal

from finders.interval_finder import IntervalFinder


class FalsePositionSolver(IntervalFinder):
    @property
    def method_name(self) -> str:
        return "False-Position"

    def iterate(
        self, xl: Decimal, xu: Decimal, f_xl: Decimal, f_xu: Decimal
    ) -> Decimal:
        if f_xl == f_xu:
            raise ValueError(
                f"{self.method_name} method failed: f(xl) and f(xu) cannot be equal"
            )

        return (xl * f_xu - xu * f_xl) / (f_xu - f_xl)
