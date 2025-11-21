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

        # forward 
        for k in range(n- 1):
            # pivoting
            A, b = self.partial_pivot(A, b, k)

            #  singular matrix
            if abs(A[k, k]) < 1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="nuh bro no solution sorry.",
                    execution_time=time.time() - start_time
                )
            
            # elimination
            for i in range(k+1,n):
                if A[k,k]!= 0:
                    factor = self.round_to_sf(A[i,k]/A[k, k])

                    update = self.round_to_sf(factor * A[k, k+1:])
                    A[i, k+1:] = self.round_to_sf(A[i, k+1:] - update)
                    A[i, k] = 0

                    b_update = self.round_to_sf(factor * b[k])
                    b[i] = self.round_to_sf(b[i] - b_update)

        # check the last diagonal element
        if abs(A[n-1,  n-1])<1e-16:
            return SolutionResult(
                has_solution=False,
                message="System has no unique solution singular",
                execution_time=time.time() - start_time
            )

        # back sub
        x = np.zeros(n)
        for i in range(n-1,-1,-1):
            x[i] = b[i]
            for j in range(i+1,n):
                subtract_val = self.round_to_sf(A[i, j] * x[j])
                x[i] = self.round_to_sf(x[i] - subtract_val)

            x[i] = self.round_to_sf(x[i] / A[i, i])

        execution_time = time.time() - start_time

        return SolutionResult(
            solution=x,  
            execution_time=execution_time,
            message="we got you a solution using gauss eleimination !!!!!!",
            has_solution=True
        )