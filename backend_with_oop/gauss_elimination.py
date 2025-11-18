import numpy as np
import time
from base_solver  import LinearSystemSolver
from solution_result import  SolutionResult


class GaussEliminationSolver(LinearSystemSolver):

    def solve(self) -> SolutionResult:
        start_time = time.time()

        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        #forward eliminations 

        for k in range(n - 1):
            # pavoiting
            A, b = self.partial_pivot(A, b, k)

            #check for solution 

            if abs(A[k, k]) < 1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="nuh bro no solution sorry.",
                    execution_time=time.time() - start_time
                )
            #eliminating
            for i in range(k + 1, n):
                if A[k, k] != 0:
                    factor = A[i, k] / A[k, k]
                    A[i, k+1:] -= factor * A[k, k+1:] 
                    A[i, k] = 0
                    b[i] -= factor * b[k]
 

            #check for last diagonal elemnt

        if abs(A[n-1, n-1]) < 1e-12:
                return SolutionResult(
                has_solution=False,
                message="System has no unique solution singular",
                execution_time=time.time() - start_time
            )

            #back sub

        x =np.zeros(n)
        for i in range(n - 1, -1, -1):
                x[i] = b[i]

                for j in range(i + 1, n):
                    x[i] -= A[i, j] * x[j]

                x[i]= x[i]/ A[i, i]

            
                

        execution_time = time.time()-start_time
        return SolutionResult(
            solution=self.round_solution(x),
            execution_time=execution_time,
            message="we got you a solution using gauss eleimination !!!!!!"
        )
                      

       