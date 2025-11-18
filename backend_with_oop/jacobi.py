import numpy as np
import time
from iterative_base import IterativeSolver
from solution_result import SolutionResult

class JacobiSolver(IterativeSolver):
    def solve(self) -> SolutionResult:
        start_time = time.time()
        A = self.A
        b = self.b
        x = self.x0.copy()

        #check diagonal dominance like me dominant
        for i in range(self.n):
            if abs(A[i,i]) <1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="Matrix has zero on diagonal (cannot use Jacobi method)",
                    execution_time=time.time() -start_time
                )
        for iteration in range(self.max_iterations):
            x_new = np.zeros(self.n)

            for i in range(self.n):
                sum_val= np.dot(A[i,:], x)- A[i, i] * x[i]
                x_new[i]= (b[i]-sum_val) /A[i, i]

            if self.check_convergence(x_new,x):
                execution_time =time.time()-start_time
                return SolutionResult(
                    solution=self.round_solution(x_new),
                    iterations=iteration +1,
                    execution_time=execution_time,
                    message=f"Solution converged using Jacobi method"
                )
            
            x = x_new.copy()

        
        execution_time = time.time()- start_time
        return SolutionResult(
            has_solution=False,
            message=f"jacobi method did not converge after {self.max_iterations} iterations ma3l4",
            execution_time=execution_time
        )