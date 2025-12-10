import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from result import Result
from decimal import Decimal, InvalidOperation, getcontext
from backend.utils import calculating_number_of_significant_digits
from backend.exceptions import ValidationError
from sympy import lambdify
from sympy.core.expr import Expr
import time
import numpy as np

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

        self.g_func = func

    def solve(self) -> Result:

        start_time = time.time()
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
                
                val_sympy = self.g_func.subs(self.x_symbol, current_x).evalf(n=self.precision, chop=True)

                    # if hasattr(val_sympy, 'evalf'):
                    #     val_sympy = val_sympy.evalf(n=self.precision)

                try:
                    if not val_sympy.is_real:
                        
                        val_sympy = val_sympy.as_real_imag()[0]
                    
                    next_x = Decimal(str(val_sympy))
                    
                except (InvalidOperation, ValueError):
                    raise ValidationError(f"Calculation Error: Resulted in undefined or complex value: {val_sympy}")

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
                    execution_time = time.time() - start_time

                    return Result(
                        solution=np.array([next_x]),
                        number_of_iterations=i + 1,
                        execution_time=execution_time,
                        message=f"Fixed Point method converges. Root was found successfully",
                        significant_digits=str(number_of_significant_digits),
                        converged=True,
                        iterations_steps=iterates,
                        relative_errors=relative_errors
                    )
                    # return {
                    #     "root": str(next_x),
                    #     "iterations": i + 1,
                    #     "significant_digits": str(number_of_significant_digits),
                    #     "execution_time": execution_time,
                    #     "converged": True,
                    #     "steps": iterates,
                    #     "relative_errors": relative_errors,
                    # }

                current_x = next_x

            number_of_significant_digits = calculating_number_of_significant_digits(es*100, self.precision)
            execution_time = time.time() - start_time
            # If we reach here, it means we didn't converge


            return Result(                
                solution=np.array([current_x]),
                number_of_iterations=self.max_iterations,
                execution_time=execution_time,
                message=f"Fixed Point method didn't converge",
                significant_digits=str(number_of_significant_digits),
                converged=False,
                iterations_steps=iterates,
                relative_errors=relative_errors
            )

            # return {
            #     "error": "oops! Max iterations reached without convergence",
            #     "root": str(current_x),
            #     "converged": False,
            #     "significant_digits": str(number_of_significant_digits),
            #     "execution_time": execution_time,
            #     "iterations": self.max_iterations,
            #     "steps": iterates,
            # }
        
        except OverflowError:
            raise ValidationError("error : Divergence detected: values are growing too large.")
        except Exception as e:
            raise ValidationError(f"error : Math error during calculation: {str(e)}")
