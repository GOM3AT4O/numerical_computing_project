import numpy as np
import time
from iterative_base import IterativeSolver
from solution_result import SolutionResult

class GaussSeidelSolver(IterativeSolver):

    def solve(self)-> SolutionResult:
        start_time =time.time()
        A = self.A
        b = self.b
        x = self.x0.copy()
        
        #check the same idea of the diagonal elements
        for i in range(self.n):
            if abs(A[i, i])<1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="Matrix has zero on diagonal try sth else then",
                    execution_time=time.time()-start_time

                )
            for iteration in range(self.max_iterations):
                x_old = x.copy()

                for i in range(self.n):
                    sum_val= np.dot(A[i,:i], x[:i]) + np.dot(A[i, i+1:], x[i+1:])
                    x[i] =(b[i] -sum_val) /A[i, i]

                if self.check_convergence(x,x_old):
                    execution_time = time.time()- start_time
                    return SolutionResult(
                        solution=self.round_solution(x),
                        iterations=iteration + 1,
                        execution_time=execution_time,
                        message=f"Solution converged using Gauss-Seidel method inshallah"
                    )
        
        
        execution_time = time.time() - start_time
        return SolutionResult(
            has_solution=False,
            message=f"gauss sedial method did not converge after {self.max_iterations} iterations sorry we tried",
            execution_time=execution_time
        )