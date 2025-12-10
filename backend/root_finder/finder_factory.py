from typing import Dict, Any
from decimal import Decimal
from validator import FunctionValidator
from exceptions import ValidationError

# Import all finder classes here
from finders.secant_finder import SecantFinder
from finders.bisection_finder import BisectionFinder
from finders.false_position_finder import FalsePositionFinder
from finders.fixed_point_finder import FixedPointFinder
from finders.newton_raphson_finder import NewtonRaphsonFinder
import math


class FinderFactory:
    @staticmethod
    def create_finder(
        function: str,
        method: str,
        absolute_relative_error: Decimal,
        number_of_iterations: int,
        parameters: Dict[str, Any],
    ):
        if method == "bisection":
            func_expr = parameters.get("function")
            xl = parameters.get("xl")
            xu = parameters.get("xu")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)

            if func_expr is None or xl is None or xu is None:
                raise ValidationError(
                    "Bisection method requires function xl and xu parameters"
                )

            try:
                xl_decimal = Decimal(str(float(xl)))
                xu_decimal = Decimal(str(float(xu)))
                epsilon_decimal = Decimal(str(float(epsilon)))
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: xl={xl}, xu={xu}, epsilon={epsilon}. Error: {str(e)}"
                )

            def func(x: Decimal) -> Decimal:
                try:
                    namespace = {
                        "x": float(x),
                        "Decimal": Decimal,
                        "abs": abs,
                        "sin": math.sin,
                        "cos": math.cos,
                        "tan": math.tan,
                        "exp": math.exp,
                        "log": math.log,
                        "sqrt": math.sqrt,
                    }
                    result = eval(func_expr, {"__builtins__": {}}, namespace)
                    if not isinstance(result, Decimal):
                        result = Decimal(str(result))
                    return result

                except Exception as e:
                    raise ValidationError(
                        f"Error evaluating function '{func_expr}': {str(e)}"
                    )

            return BisectionFinder(
                xl=xl_decimal,
                xu=xu_decimal,
                precision=precision,
                func=func,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
            )

        elif method == "false-position":
            func_expr = parameters.get("function")
            xl = parameters.get("xl")
            xu = parameters.get("xu")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)

            if func_expr is None or xl is None or xu is None:
                raise ValidationError(
                    "flase-position method requires function xl and xu parameters"
                )

            try:
                xl_decimal = Decimal(str(float(xl)))
                xu_decimal = Decimal(str(float(xu)))
                epsilon_decimal = Decimal(str(float(epsilon)))

            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: xl={xl}, xu={xu}, epsilon={epsilon}. Error: {str(e)}"
                )

            def func(x: Decimal) -> Decimal:
                try:
                    namespace = {
                        "x": float(x),
                        "Decimal": Decimal,
                        "abs": abs,
                        "sin": math.sin,
                        "cos": math.cos,
                        "tan": math.tan,
                        "exp": math.exp,
                        "log": math.log,
                        "sqrt": math.sqrt,
                    }
                    result = eval(func_expr, {"__builtins__": {}}, namespace)
                    if not isinstance(result, Decimal):
                        result = Decimal(str(result))
                    return result
                except Exception as e:
                    raise ValidationError(
                        f"Error evaluating function '{func_expr}': {str(e)}"
                    )

            return FalsePositionFinder(
                xl=xl_decimal,
                xu=xu_decimal,
                precision=precision,
                func=func,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
            )
        elif method == "secant":
            func_expr = parameters.get("function")
            x0 = parameters.get("x0")
            x1 = parameters.get("x1")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)

            if func_expr is None or x0 is None or x1 is None:
                raise ValidationError(
                    "Secant method requires function, x0, and x1 parameters"
                )

            try:
                x0_decimal = Decimal(str(float(x0)))
                x1_decimal = Decimal(str(float(x1)))
                epsilon_decimal = Decimal(str(float(epsilon)))
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"Error converting parameters: x0={x0}, x1={x1}, epsilon={epsilon}. Error: {str(e)}"
                )

            def func(x: Decimal) -> Decimal:
                try:
                    namespace = {
                        "x": float(x),
                        "Decimal": Decimal,
                        "abs": abs,
                        "sin": math.sin,
                        "cos": math.cos,
                        "tan": math.tan,
                        "exp": math.exp,
                        "log": math.log,
                        "sqrt": math.sqrt,
                    }
                    result = eval(func_expr, {"__builtins__": {}}, namespace)
                    if not isinstance(result, Decimal):
                        result = Decimal(str(result))
                    return result
                except Exception as e:
                    raise ValidationError(
                        f"Error evaluating function '{func_expr}': {str(e)}"
                    )

            return SecantFinder(
                x0=x0_decimal,
                x1=x1_decimal,
                precision=precision,
                func=func,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
            )
        elif method == "fixed-point":
            func_str = parameters.get("function")
            guess = parameters.get("guess")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)

            print(func_str, " ", guess, " ", epsilon)

            if func_str is None or guess is None:
                raise ValidationError(
                    "Fixed Point method requires 'function' and 'guess' parameters"
                )

            try:
                func_expr = FunctionValidator.validate_and_parse(func_str)
                guess_decimal = Decimal(str(float(guess)))
                epsilon_decimal = Decimal(str(float(epsilon)))

            except Exception as e:
                raise ValidationError(
                    f"Error preparing parameters for Fixed Point: {str(e)}"
                )

            return FixedPointFinder(
                guess=guess_decimal,
                func=func_expr,
                precision=precision,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
            )
        elif method == "newton-raphson":
            func_str = parameters.get("function")
            guess = parameters.get("guess")
            epsilon = parameters.get("epsilon", 0.00001)
            max_iterations = parameters.get("max_iterations", 50)
            m = parameters.get("m", 1)

            print(func_str, " ", guess, " ", epsilon)

            if func_str is None or guess is None:
                raise ValidationError(
                    "Fixed Point method requires 'function' and 'guess' parameters"
                )

            try:
                func_expr = FunctionValidator.validate_and_parse(func_str)
                guess_decimal = Decimal(str(float(guess)))
                epsilon_decimal = Decimal(str(float(epsilon)))

            except Exception as e:
                raise ValidationError(
                    f"Error preparing parameters for Fixed Point: {str(e)}"
                )

            return NewtonRaphsonFinder(
                guess=guess_decimal,
                func=func_expr,
                precision=precision,
                epsilon=epsilon_decimal,
                max_iterations=int(max_iterations),
                m=int(m),
            )

        else:
            raise ValidationError(f"Unknown method: {method}")
