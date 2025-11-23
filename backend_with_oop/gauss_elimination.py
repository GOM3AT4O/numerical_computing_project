import numpy as np
import time
from base_solver import LinearSystemSolver
from solution_result import SolutionResult

class GaussEliminationSolver(LinearSystemSolver):
    def solve(self) -> SolutionResult:
        start_time = time.time()

        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        for k in range(n -1):
            A, b = self.partial_pivot(A,b, k)

            if abs(A[k,k]) <1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="No unique solution exists.",
                    execution_time=time.time() - start_time
                )
            
            for i in range(k + 1,n):
                factor = self.safe_divide(A[i,k],A[k,k])
                

                A[i,k+1:] = self.update_matrix_row(A[i,k+1:],A[k,k+1:],factor)
                
                b[i]=self.update_vector_element(b[i], b[k], factor)
                
                A[i,k] = 0  

        if abs(A[n-1, n-1]) < 1e-12:
            return SolutionResult(
                has_solution=False,
                message="system has no unique solution sorry.",
                execution_time=time.time() - start_time
            )

        # Back substitution using base methods
        x = np.zeros(n)
        for i in range(n -1,-1, -1):
            sum_val = b[i]
            for j in range(i+1, n):
                sum_val = self.update_vector_element(sum_val,A[i,j]*x[j], 1.0)
            x[i] = self.safe_divide(sum_val,A[i,i])

        execution_time = time.time()-start_time
        
        return SolutionResult(
            solution=self.round_solution(x),
            execution_time=execution_time,
            message="solution  found using Gauss Elimination finally,",
            has_solution=True
        )