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
            A = self.round_to_sf(A)
            b = self.round_to_sf(b)




            #check for singularity 

            if abs(A[k,k]) <1e-12:
                return SolutionResult(
                    has_solution= False,
                    message="System has no unique solution sorrry.",
                    execution_time=time.time()-start_time
                )
            
            pivot = A[k, k]
            for j in range(n):
                A[k,j]= self.round_to_sf(A[k,j]/pivot)

            b[k] = self.round_to_sf(b[k]/pivot)


            #eliminate column k in other rows 

            for i in range(n):
                if i!= k:
                    factor = A[i, k]
                    for j in range(n):
                        product = self.round_to_sf(factor*A[k,j])
                        A[i,j] =self.round_to_sf(A[i,j]-product)

                    product_b=self.round_to_sf(factor*b[k])
                    b[i]=self.round_to_sf(b[i]-product_b)

        execution_time = time.time()- start_time

        return SolutionResult(
            solution=self.round_solution(b),
            execution_time=execution_time,
            message="we got you a solution using gauss-jorden yahhhhhh1",
            has_solution=True
        )
            

        

        