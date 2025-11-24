import numpy as np
import time
from base_solver import LinearSystemSolver
from solution_result import SolutionResult
from exceptions import ValidationError

class LUDecompositionSolver(LinearSystemSolver):

    def __init__(self, A: np.ndarray, b: np.ndarray, precision: int = 6,form: str= "doolittle"):
        super().__init__(A, b, precision)
        self.form = form.lower()

    def solve(self) -> SolutionResult:
        """Main solve method - delegates to specific forms"""
        if self.form == "doolittle":
            return self._solve_doolittle()
        
        elif self.form == "crout":
            return self._solve_crout()
        
        elif self.form == "cholesky":
            return self._solve_cholesky()
        
        else:
            raise ValidationError(f"Unknown form why don't u choose a correct LU form maybe: {self.form}")
    def _solve_doolittle(self) -> SolutionResult:
        start_time =time.time()

        A = self.A.copy()
        b =self.b.copy()
        n = self.n
        # Pivoting
        P = np.eye(n)  

        for k in range(n):
            max_idx=k + np.argmax(np.abs(A[k:, k]))
            if max_idx != k:
                A[[k,max_idx]]= A[[max_idx, k]]
                P[[k,max_idx]] =P[[max_idx, k]]

                A = self.round_to_sf(A)
                P= self.round_to_sf(P)


        L = np.eye(n)
        U = np.zeros((n, n))

        for i in range(n):
            # Upper
            for j in range(i, n):
                dot_product = 0
                for k in range(i):
                    product = self.round_to_sf(L[i,k]* U[k,j])
                    dot_product = self.round_to_sf(dot_product + product)

                U[i, j] = self.round_to_sf(A[i,j]-dot_product)

            if abs(U[i, i]) < 1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="No unique solution sorry find sth else to do",
                    execution_time=time.time() - start_time
                )


            # Lower
            for j in range(i+1,n):
                dot_product = 0
                for k in range(i):
                    product = self.round_to_sf(L[j,k]* U[k,i])
                    dot_product = self.round_to_sf(dot_product + product)

                numerator = self.round_to_sf(A[j, i] - dot_product)
                L[j, i] = self.round_to_sf(numerator / U[i, i])



              

        #permutation
        b = P @ b

        # forward sub
        y = np.zeros(n)
        for i in range(n):
            dot_product = 0
            for j in range(i):
                product = self.round_to_sf(L[i, j] * y[j])
                dot_product = self.round_to_sf(dot_product + product)
                
            y[i] = self.round_to_sf(b[i] - dot_product)


        # back sub
        x = np.zeros(n)
        for i in range(n-1,-1, -1):
            dot_product =0

            for j in range(i+ 1, n):
                product= self.round_to_sf(U[i,j]* x[j])
                dot_product= self.round_to_sf(dot_product +product)
            
            numerator =self.round_to_sf(y[i] -dot_product)
            x[i] =self.round_to_sf(numerator/ U[i,i])
        
        execution_time = time.time()-start_time

        result = SolutionResult(
            solution=self.round_solution(x),
            execution_time=execution_time,
            message="we got a solution using LU doolittle ?!",
            has_solution=True
        )
        # Add L and U matrices to result
        result.L= self.round_to_sf(L).tolist()
        result.U =self.round_to_sf(U).tolist()
        result.P =self.round_to_sf(P).tolist()
        
        return result
    def _solve_crout(self) -> SolutionResult:
        start_time = time.time()
        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        L = np.zeros((n,n))
        U = np.eye(n)

        for j in range(n):
            #lower 
            for i in range(j, n):
                dot_product =0
                for k in range(j):
                    product = self.round_to_sf(L[i,k]*U[k,j])
                    dot_product =self.round_to_sf(dot_product +product)

                L[i, j] = self.round_to_sf(A[i, j] - dot_product)


            #check singularity
            if abs(L[j, j]) < 1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="System has no unique solution singular ya bro",
                    execution_time=time.time()-start_time
                )
            
            # Upper triangular
            for i in range(j+ 1, n):
                dot_product = 0
                for k in range(j):
                    product = self.round_to_sf(L[j, k]* U[k, i])
                    dot_product = self.round_to_sf(dot_product+ product)

                numerator = self.round_to_sf(A[j, i] - dot_product)
                U[j,i] =self.round_to_sf(numerator/ L[j, j])

            

                

        #forward sub: Ly = b
        y = np.zeros(n)
        for i in range(n):
            dot_product = 0
            for j in range(i):
                product = self.round_to_sf(L[i, j] * y[j])
                dot_product = self.round_to_sf(dot_product + product)

            numerator = self.round_to_sf(b[i] - dot_product)
            y[i] = self.round_to_sf(numerator / L[i, i])

        
        # backwar sub: Ux = y
        x = np.zeros(n)
        for i in range(n-1,-1, -1):
            dot_product = 0

            for j in range(i + 1, n):
                product = self.round_to_sf(U[i,j]*x[j])
                dot_product=self.round_to_sf(dot_product +product)

            x[i] =self.round_to_sf(y[i]-dot_product)

        execution_time = time.time()- start_time

        result = SolutionResult(
            solution=self.round_solution(x),
            execution_time=execution_time,
            message="we got a solution using LU crout good for you!"
        )
        # Add L and U matrices to result
        result.L =np.round(L,self.precision).tolist()
        result.U= np.round(U,self.precision).tolist()
        
        return result
    
    def _solve_cholesky(self) -> SolutionResult:
        start_time = time.time()
        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        # Check matrix symmetric or what 
        if not np.allclose(A, A.T):
            return SolutionResult(
                has_solution=False,
                message="sorry not symmetric no solution try sth else.",
                execution_time=time.time()- start_time
            )
        
        L = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1):
                if i == j:
                    sum_sq = 0
                    for k in range(j):
                        product = self.round_to_sf(L[i,k]* L[i, k])
                        sum_sq = self.round_to_sf(sum_sq+ product)
                    val = self.round_to_sf(A[i,i] -sum_sq)
                    if val <= 0:
                        
                        return SolutionResult(
                             has_solution=False,
                            message="Matrix is not positive definite",
                            execution_time=time.time()- start_time
                        )
                        
                    L[i,j] =self.round_to_sf(np.sqrt(val))
                else:
                    sum_prod = 0
                    for k in range(j):
                        product = self.round_to_sf(L[i,k]*L[j,k])
                        sum_prod =self.round_to_sf(sum_prod+product)
                    numerator = self.round_to_sf(A[i,j] -sum_prod)
                    L[i, j] = self.round_to_sf(numerator/ L[j, j])

                

        
        #forward sub Ly = b
        y = np.zeros(n)
        for i in range(n):
            dot_product = 0
            for j in range(i):
                product = self.round_to_sf(L[i,j]* y[j])
                dot_product = self.round_to_sf(dot_product+ product)

            numerator = self.round_to_sf(b[i]- dot_product)
            y[i] = self.round_to_sf(numerator/ L[i,i])

        #backward sub 
        x = np.zeros(n)
        for i in range(n-1,-1,-1):
            dot_product = 0
            for j in range(i+1,n):
                product = self.round_to_sf(L[j, i] * x[j])
                dot_product = self.round_to_sf(dot_product + product)
            
            numerator = self.round_to_sf(y[i] - dot_product)
            x[i] = self.round_to_sf(numerator / L[i,i])


        
        execution_time=time.time()-start_time

        result =SolutionResult(
            solution=self.round_solution(x),
            execution_time=execution_time,
            message="we got a solution using LU cholesky",
            has_solution=True
        )
        result.L = self.round_to_sf(L).tolist()
        result.U = self.round_to_sf(L.T).tolist()
        
        return result