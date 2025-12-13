from typing import Callable, Dict, Any
from decimal import Decimal, InvalidOperation
from validator import FunctionValidator
from exceptions import ValidationError

# Import all finder classes here
from root_finder.finders.bisection_finder import BisectionFinder
from root_finder.finders.false_position_finder import FalsePositionFinder
from root_finder.finders.fixed_point_finder import FixedPointFinder
from root_finder.finders.newton_raphson_finder import NewtonRaphsonFinder
from root_finder.finders.secant_finder import SecantFinder
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

        x_symbol = symbols("x")

        def f(x):
            val_sympy = f_expr.subs(x_symbol, x).evalf(n=precision)

            try:
                if not val_sympy.is_real:
                    val_sympy = val_sympy.as_real_imag()[0]
                y = +Decimal(float(val_sympy))
            except (InvalidOperation, ValueError):
                raise ValueError(
                    f"calculation resulted in undefined or complex value: {val_sympy}"
                )

            return y

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
            second_guess = parameters.get("second_guess")

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

            df_expr = f_expr.diff(x_symbol)

            def df(x):
                val_sympy = df_expr.subs(x_symbol, x).evalf(n=precision)

                try:
                    if not val_sympy.is_real:
                        val_sympy = val_sympy.as_real_imag()[0]
                    y = +Decimal(float(val_sympy))
                except (InvalidOperation, ValueError):
                    raise ValueError(
                        f"calculation resulted in undefined or complex value: {val_sympy}"
                    )

                return y

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
