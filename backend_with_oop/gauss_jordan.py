import numpy as np
import time
from base_solver import LinearSystemSolver
from solution_result import SolutionResult

class GaussJordanSolver(LinearSystemSolver):
    def solve(self) -> SolutionResult:
        start_time = time.time()
        
        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        for k in range(n):
            # pivoting
            A, b = self.partial_pivot(A,b,k)

            #check for singularity
            if abs(A[k,k]) <1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="system an't got no unique solution.",
                    execution_time=time.time()-start_time
                )
            
            
            pivot = A[k, k]
            for j in range(n):
                A[k, j] = self.safe_divide(A[k, j], pivot)
            b[k] = self.safe_divide(b[k], pivot)

            
            for i in range(n):
                if i != k:
                    factor = A[i,k]  
                    
                    
                    A[i]=self.update_matrix_row(A[i], A[k], factor)
                    

                    b[i] = self.update_vector_element(b[i], b[k], factor)

        execution_time = time.time()- start_time

        return SolutionResult(
            solution=self.round_solution(b),
            execution_time=execution_time,
            message="solution found using Gauss-Jordan elimination yaaaahhh",
            has_solution=True
        )