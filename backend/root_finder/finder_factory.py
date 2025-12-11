from typing import Callable, Dict, Any
from decimal import Decimal
from validator import FunctionValidator
from exceptions import ValidationError

# Import all finder classes here
from finders.bisection_finder import BisectionFinder
from finders.false_position_finder import FalsePositionFinder
from finders.fixed_point_finder import FixedPointFinder
from finders.newton_raphson_finder import NewtonRaphsonFinder
from finders.secant_finder import SecantFinder
from sympy import Expr, symbols, lambdify


class FinderFactory:
    @staticmethod
    def create_finder(
        function: str,
        method: str,
        absolute_relative_error: Decimal,
        number_of_iterations: int,
        precision: int,
        parameters: Dict[str, Any],
    ):
        f_expr: Expr = FunctionValidator.validate_and_parse(function)

        x = symbols("x")

        f: Callable[[Decimal], Decimal] = lambdify(x, f_expr, "math")

        if method == "bisection":
            lower_bound = parameters.get("lower_bound")
            second_guess = parameters.get("upper_bound")

            if lower_bound is None or second_guess is None:
                raise ValidationError(
                    "Bisection method requires function lower bound and upper bound parameters"
                )

            try:
                lower_bound = Decimal(lower_bound)
                second_guess = Decimal(second_guess)
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: lower bound={lower_bound}, upper bound={second_guess}, absolute_relative_error={absolute_relative_error}. Error: {str(e)}"
                )

            return BisectionFinder(
                function=f,
                absolute_relative_error=absolute_relative_error,
                number_of_iterations=number_of_iterations,
                precision=precision,
                lower_bound=lower_bound,
                upper_bound=second_guess,
            )

        elif method == "false-position":
            lower_bound = parameters.get("lower_bound")
            second_guess = parameters.get("upper_bound")

            if lower_bound is None or second_guess is None:
                raise ValidationError(
                    "False-Position method requires lower bound and upper bound parameters"
                )

            try:
                lower_bound = Decimal(lower_bound)
                second_guess = Decimal(second_guess)
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: lower bound={lower_bound}, upper bound={second_guess}. Error: {str(e)}"
                )

            return FalsePositionFinder(
                function=f,
                absolute_relative_error=absolute_relative_error,
                number_of_iterations=number_of_iterations,
                precision=precision,
                lower_bound=lower_bound,
                upper_bound=second_guess,
            )
        elif method == "secant":
            first_guess = parameters.get("first_guess")
            second_guess = parameters.get("upper_bound")

            if first_guess is None or second_guess is None:
                raise ValidationError(
                    "Secant method requires first guess and second guess parameters"
                )

            try:
                first_guess = Decimal(first_guess)
                second_guess = Decimal(second_guess)
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: first guess={first_guess}, second guess={second_guess}. Error: {str(e)}"
                )

            return SecantFinder(
                function=f,
                absolute_relative_error=absolute_relative_error,
                number_of_iterations=number_of_iterations,
                precision=precision,
                first_guess=first_guess,
                second_guess=second_guess,
            )
        elif method == "fixed-point":
            guess = parameters.get("guess")

            if guess is None:
                raise ValidationError("Fixed-Point method requires guess parameter")

            try:
                guess = Decimal(guess)
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: guess={guess}. Error: {str(e)}"
                )

            return FixedPointFinder(
                function=f,
                absolute_relative_error=absolute_relative_error,
                number_of_iterations=number_of_iterations,
                precision=precision,
                guess=guess,
            )
        elif method == "newton-raphson" or method == "modified-newton-raphson":
            guess = parameters.get("guess")
            multiplicity = parameters.get("multiplicity", 1)

            if guess is None:
                raise ValidationError("Newton-Raphson method requires guess parameter")

            try:
                guess = Decimal(guess)
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: guess={guess}. Error: {str(e)}"
                )

            df_expr = f_expr.diff(x)
            df: Callable[[Decimal], Decimal] = lambdify(x, df_expr, "math")

            return NewtonRaphsonFinder(
                function=f,
                absolute_relative_error=absolute_relative_error,
                number_of_iterations=number_of_iterations,
                precision=precision,
                guess=guess,
                derivative=df,
                multiplicity=multiplicity,
            )

        else:
            raise ValidationError(f"Unknown method: {method}")
