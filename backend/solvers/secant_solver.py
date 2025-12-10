from decimal import Decimal
import numpy as np
import time
from typing import Callable
from solution_result import SolutionResult
from exceptions import ValidationError

class SecantSolver:
    def __init__(
        self,
        x0: Decimal,
        x1: Decimal,
        precision: int = 6,
        func: Callable[[Decimal], Decimal] = None,
        epsilon: Decimal = Decimal("0.00001"),
        max_iterations: int = 50,
    ):
        self.x0 = Decimal(x0)
        self.x1 = Decimal(x1)
        self.precision = precision
        self.func = func
        self.epsilon = Decimal(epsilon)
        self.max_iterations = max_iterations

        # Check if function is provided
        if self.func is None:
            raise ValidationError("Function definition is required for Secant Method")

    def solve(self) -> SolutionResult:
        start_time = time.time()

        
        x_prev = self.x0  
        x_curr = self.x1  
        
        iter_count = 0
        
        
        try:
            f_prev = self.func(x_prev)
            f_curr = self.func(x_curr)
        except Exception as e:
            raise ValidationError(f"Error evaluating function at initial guesses: {e}")

        # Start Iterations
        for i in range(1, self.max_iterations + 1):
            iter_count = i
            
            # Check for division by zero
            denominator = f_curr - f_prev
            if abs(denominator) < Decimal("1e-20"):
                execution_time = time.time() - start_time
                return SolutionResult(
                    solution=np.array([x_curr]),
                    number_of_iterations=iter_count,
                    execution_time=execution_time,
                    message=f"Secant method failed: Division by zero encountered at iteration {i}. f(x{i}) is too close to f(x{i-1})."
                )

            
            x_new = x_curr - (f_curr * (x_curr - x_prev) / denominator)

            # Calculate relative error
            if x_new != 0:
                relative_error = abs((x_new - x_curr) / x_new)
            else:
                relative_error = abs(x_new - x_curr)

            
            # 1. Check if function value is close to zero
            f_new = self.func(x_new)
            if abs(f_new) < self.epsilon:
                execution_time = time.time() - start_time
                return SolutionResult(
                    solution=np.array([x_new]),
                    number_of_iterations=iter_count,
                    execution_time=execution_time,
                    message=f"Secant method converges after {iter_count} iterations. Root found at x = {x_new:.{self.precision}f} (tolerance: {self.epsilon})"
                )
            
            # 2. Check if relative error is within tolerance
            if relative_error < self.epsilon:
                execution_time = time.time() - start_time
                return SolutionResult(
                    solution=np.array([x_new]),
                    number_of_iterations=iter_count,
                    execution_time=execution_time,
                    message=f"Secant method converges after {iter_count} iterations. Root found at x = {x_new:.{self.precision}f} (tolerance: {self.epsilon})"
                )

            # Update
            x_prev = x_curr
            f_prev = f_curr
            x_curr = x_new
            f_curr = f_new

        # If loop finishes without any return 
        execution_time = time.time() - start_time
        return SolutionResult(
            solution=np.array([x_curr]),
            number_of_iterations=iter_count,
            execution_time=execution_time,
            message=f"Secant method didn't converge after {self.max_iterations} iterations. Best approximation: x = {x_curr:.{self.precision}f}"
        )