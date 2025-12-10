from decimal import Decimal
import numpy as np
from typing import Callable, Optional, List
import time 
from solution_result import SolutionResult
from exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP
from utils import calculating_number_of_significant_digits

class FalsePositionSolver:


    def __init__(
        self,
        xl: Decimal,
        xu: Decimal,
        precision: int = 6,
        func: Callable[[Decimal], Decimal] = None,
        epsilon: Decimal = Decimal("0.00001"),
        max_iterations: int = 50,
    ):
        
        self.xl = Decimal(xl)
        self.xu = Decimal(xu)
        self.precision = precision
        self.func = func
        self.epsilon = Decimal(epsilon)
        self.max_iterations = max_iterations
        

        if self.func is not None:
            self._validate_interval()


    def _validate_interval(self):
        if self.xl > self.xu:
            raise ValidationError("xl must be less than xu")

        f_xl = self.func(self.xl)
        f_xu = self.func(self.xu)

        if f_xl * f_xu > 0:
            raise ValidationError("f(xl) and f(xu) must have different signs")
        

    def solve(self) -> SolutionResult:

        start_time = time.time() 

        xl = self.xl
        xu = self.xu
        xr = Decimal(0)
        old_xr = Decimal(0)  

        iteration_steps = []
        relative_errors = []
        number_of_significant_digits=0


        for iteration in range(1 , self.max_iterations+1):


            f_xl = self.func(xl)
            f_xu = self.func(xu)

            if f_xl == f_xu :
                execution_time = time.time() - start_time
                return SolutionResult(
                    solution=np.array([xr]),
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"False Position method an't got no solution cannot be used sorry for that.",
                    converged=False
                )
            

            xr = (xl * f_xu - xu * f_xl) / (f_xu - f_xl)
            iteration_steps.append(str(xr))

            f_xr = self.func(xr)

            if abs(f_xr) < self.epsilon:
                execution_time = time.time() - start_time
                return SolutionResult(
                    solution=np.array([xr]),
                    number_of_iterations=iteration,
                    execution_time=execution_time,
                    message=f"False Position method converges after {iteration} iterations alright? the root was found in x = {xr:.{self.precision}f} with f(x) = 0 (tolerance: {self.epsilon})",
                    relative_errors=relative_errors,
                    significant_digits=str(self.precision),
                    converged=True,
                    iterations_steps=iteration_steps
                )

            if iteration > 1 :
                relative_error = abs((xr - old_xr)) / abs(xr) if xr != 0 else abs(xr - old_xr)
                relative_errors.append(str(relative_error))
                number_of_significant_digits= calculating_number_of_significant_digits(relative_error * Decimal("100"), self.precision)
                if relative_error < self.epsilon:
                    execution_time = time.time() - start_time
                    return SolutionResult(
                        solution=np.array([xr]),
                        number_of_iterations=iteration,
                        execution_time=execution_time,
                        message=f"False Position method converges after {iteration} iterations alright? the root was found in x = {xr:.{self.precision}f} with f(x) = 0 (tolerance: {self.epsilon})"
                        ,relative_errors=relative_errors,
                        significant_digits=str(number_of_significant_digits),
                        converged=True,
                        iterations_steps=iteration_steps
                    )
                
            old_xr = xr
                

            if f_xl * f_xr < 0:
                xu = xr

            else:
                xl = xr
            
        execution_time =time.time() - start_time
        return SolutionResult(
                solution=  np.array([xr]),
                number_of_iterations=iteration,
                execution_time=execution_time,
                message=f"False Position method didn't converge after {self.max_iterations} iterations. The root was found in x = {xr:.{self.precision}f} with f(x) = 0 (tolerance: {self.epsilon})",
                converged=False,
                relative_errors=relative_errors,
                significant_digits=str(number_of_significant_digits),
                iterations_steps=iteration_steps
            )
            








