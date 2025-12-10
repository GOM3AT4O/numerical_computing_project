import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from solution_result import SolutionResult
from decimal import Decimal, getcontext
from backend.utils import calculating_number_of_significant_digits
from backend.exceptions import ValidationError
from sympy import lambdify
from sympy.core.expr import Expr
import time
import numpy as np

class NewtonRaphsonSolver:
    def __init__(
        self,
        guess: Decimal,
        func: Expr,        
        precision: int = 6,
        epsilon: Decimal = Decimal("0.00001"),
        max_iterations: int = 50,
        m:int = 1
    ):
        self.guess = guess
        self.precision = precision
        self.epsilon = epsilon
        self.max_iterations = max_iterations
        self.m = m

        self.x_symbol = list(func.free_symbols)[0]

        # self.f_func = lambdify(self.x_symbol, func, modules='sympy')

        # derivative_expr = func.diff(self.x_symbol)

        # self.f_driff_func = lambdify(self.x_symbol, derivative_expr, modules='sympy')

        self.f_func = func
        self.f_driff_func = func.diff(self.x_symbol)

    def solve(self) -> SolutionResult:

        start_time = time.time()
        """
        Performs the Newton-Raphson method to find a root.
        1. Sets the decimal precision for calculations.
        2. Iteratively computes the next approximation using f(x) and f'(x).
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

                
                f_value_sympy = self.f_func.subs(self.x_symbol, current_x).evalf(n=self.precision)
                f_driff_value_sympy = self.f_driff_func.subs(self.x_symbol, current_x).evalf(n=self.precision)

                # if hasattr(f_value_sympy, 'evalf'):
                #     f_value_sympy = f_value_sympy.evalf(n=self.precision)
                # if hasattr(f_driff_value_sympy, 'evalf'):
                #     f_driff_value_sympy = f_driff_value_sympy.evalf(n=self.precision)

                if not f_value_sympy.is_real:
                        f_value_sympy = f_value_sympy.as_real_imag()[0]
                    
                if not f_driff_value_sympy.is_real:
                        f_driff_value_sympy = f_driff_value_sympy.as_real_imag()[0]

                f_value = Decimal(str(f_value_sympy))
                f_driff_value = Decimal(str(f_driff_value_sympy))

                print( f_value," ",f_driff_value)

                if f_value == Decimal("0"):
                    number_of_significant_digits = calculating_number_of_significant_digits(es * Decimal("100"), self.precision)
                    execution_time = time.time() - start_time
                    return SolutionResult(
                        solution=np.array([current_x]),
                        iterations_steps=iterates,
                        relative_errors=relative_errors,
                        number_of_iterations=i+1,
                        significant_digits=str(number_of_significant_digits),
                        converged=True,
                        execution_time=execution_time,
                        message=f"Newton-Raphson method converges. Root was found successfully ",
                    )

                if abs(f_driff_value) == Decimal("0"):
                    execution_time = time.time() - start_time
                    return SolutionResult(
                        solution=np.array([current_x]),
                        number_of_iterations=i+1,
                        execution_time=execution_time,
                        message=f"Newton-Raphson method failed: Derivative too close to zero at iteration {i+1}."
                    )

                next_x = current_x - (f_value / f_driff_value)*self.m

                iterates.append(str(next_x))

                # Calculate relative error
                # Avoid division by zero so i will use absolute error in this case for now.
                if next_x == 0:
                    es = abs(next_x - current_x)
                else:
                    es = abs((next_x - current_x) / next_x)

                relative_errors.append(str(es))

                # (Convergence check)
                if es < self.epsilon:
                    number_of_significant_digits = calculating_number_of_significant_digits(es * Decimal("100"), self.precision)
                    execution_time = time.time() - start_time
                    return SolutionResult(
                        solution=np.array([next_x]),
                        iterations_steps=iterates,
                        relative_errors=relative_errors,
                        number_of_iterations=i+1,
                        significant_digits=str(number_of_significant_digits),
                        converged=True,
                        execution_time=execution_time,
                        message=f"Newton-Raphson method converges. Root was approximately found successfully",
                    )
                current_x = next_x
            number_of_significant_digits = calculating_number_of_significant_digits(es * Decimal("100"), self.precision)
            execution_time = time.time() - start_time
            return SolutionResult(
                solution=np.array([next_x]),
                iterations_steps=iterates,
                relative_errors=relative_errors,
                number_of_iterations=self.max_iterations,
                significant_digits=str(number_of_significant_digits),
                converged=False,
                execution_time=execution_time,
                message=f"Newton-Raphson method did not converge within the maximum number of iterations.",
            )
        except OverflowError:
            raise ValidationError("error : Divergence detected: values are growing too large.")
        except Exception as e:
            raise ValidationError(f"error : Math error during calculation: {str(e)}")