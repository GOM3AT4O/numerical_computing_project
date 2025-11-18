import numpy as np
import time
from base_solver import LinearSystemSolver
from solution_result import SolutionResult

class GaussJordanSolver(LinearSystemSolver):


    def solve(self)-> SolutionResult:
        start_time = time.time()
        
        A = self.A.copy()
        b =self.b.copy()
        n = self.n

        #forward eleimination 
        for k in range(n):
            A,b = self.partial_pivot(A,b,k)

            #check for singularity 

            if abs(A[k,k]) <1e-12:
                return SolutionResult(
                    has_solution= False,
                    message="System has no unique solution sorrry.",
                    execution_time=time.time()-start_time
                )
            
            pivot = A[k, k]
            A[k, :] = A[k, :] / pivot
            b[k] = b[k] / pivot

            #eliminate column k in other rows 

            for i in range(n):
                if i!= k:
                    factor = A[i, k]
                    A[i, :] -= factor * A[k, :]
                    b[i] -= factor * b[k]

        execution_time = time.time()- start_time

        return SolutionResult(
            solution=self.round_solution(b),
            execution_time=execution_time,
            message="we got you a solution using gauss-jorden yahhhhhh1"
        )
            

        

        