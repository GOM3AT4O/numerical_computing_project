import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from decimal import Decimal, getcontext
from backend.utils import calculating_number_of_significant_digits
from backend.exceptions import ValidationError
from sympy import lambdify
from sympy.core.expr import Expr

class FixedPointSolver:
    def __init__(
        self,
        guess: Decimal,
        func: Expr,        
        precision: int = 6,
        epsilon: Decimal = Decimal("0.00001"),
        max_iterations: int = 50,
    ):
        self.guess = guess
        self.precision = precision
        self.epsilon = epsilon
        self.max_iterations = max_iterations

        self.x_symbol = list(func.free_symbols)[0]

        self.g_func = lambdify(self.x_symbol, func, modules='sympy')

    def solve(self):
        """
        Performs the Fixed Point Iteration method to find a root.
        1. Sets the decimal precision for calculations.
        2. Iteratively computes the next approximation using g(x).
        3. Checks for divergence (if values become too large).
        """

        getcontext().prec = self.precision

        es : Decimal = Decimal("0")
        
        current_x = self.guess
        iterates = [str(current_x)] 

        relative_errors = []


        number_of_significant_digits=0

        try:
            for i in range(self.max_iterations):
                
                val_sympy = self.g_func(current_x)

                if hasattr(val_sympy, 'evalf'):
                    val_sympy = val_sympy.evalf(n=self.precision)

                next_x = Decimal(str(val_sympy))

                iterates.append(str(next_x))

                if next_x != 0:
                    es = abs((next_x - current_x) / next_x)
                else:
                    # avoid division by zero and this means we have converged to zero
                    # i will keep the absolute error in this case
                    es = abs(next_x - current_x)

                relative_errors.append(str(es))
                
                # (Convergence check)
                if es < self.epsilon:
                    number_of_significant_digits = calculating_number_of_significant_digits(es*100, self.precision)

                    return {
                        "root": str(next_x),
                        "iterations": i + 1,
                        "significant_digits": str(number_of_significant_digits),
                        "converged": True,
                        "steps": iterates,
                        "relative_errors": relative_errors,
                    }

                current_x = next_x

            number_of_significant_digits = calculating_number_of_significant_digits(es*100, self.precision)


            return {
                "error": "oops! Max iterations reached without convergence",
                "root": str(current_x),
                "converged": False,
                "significant_digits": str(number_of_significant_digits),
                "iterations": self.max_iterations,
                "steps": iterates,
            }
        
        except OverflowError:
            raise ValidationError("error : Divergence detected: values are growing too large.")
        except Exception as e:
            raise ValidationError(f"error : Math error during calculation: {str(e)}")