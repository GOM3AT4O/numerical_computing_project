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

        L = np.eye(n)
        U = np.zeros((n, n))

        for i in range(n):
            # Upper
            for j in range(i, n):
                U[i, j] = A[i, j] -np.dot(L[i,:i], U[:i, j])

            if abs(U[i,i]) < 1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="no unique solution sorrry",
                    execution_time=time.time()-start_time
                )

            # Lower
            for j in range(i+1,n):
                L[j,i]= (A[j,i]- np.dot(L[j,:i],U[:i,i])) / U[i, i]

        #permutation
        b = P @ b

        # forward sub
        y = np.zeros(n)
        for i in range(n):
            y[i] = b[i] - np.dot(L[i,:i], y[:i])

        # back sub
        x = np.zeros(n)
        for i in range(n- 1, -1, -1):
            x[i] = (y[i] -np.dot(U[i, i+1:], x[i+1:]))/ U[i, i]
        
        execution_time = time.time()- start_time

        result = SolutionResult(
            solution=self.round_solution(x),
            execution_time=execution_time,
            message="we got a solution using LU doolittle ?!"
        )
        # Add L and U matrices to result
        result.L = np.round(L, self.precision).tolist()
        result.U = np.round(U,self.precision).tolist()
        result.P = np.round(P, self.precision).tolist()
        
        return result
    def _solve_crout(self) -> SolutionResult:
        start_time = time.time()
        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        L = np.zeros((n,n))
        U = np.eye(n)

        for j in range(n):
            # Lower triangular
            for i in range(j, n):
                L[i, j] = A[i,j] - np.dot(L[i,:j],U[:j,j])

            # Check for singularity
            if abs(L[j, j]) < 1e-12:
                return SolutionResult(
                    has_solution=False,
                    message="System has no unique solution singular ya bro",
                    execution_time=time.time()-start_time
                )
            
            # Upper triangular
            for i in range(j+ 1, n):
                U[j, i] =(A[j,i]- np.dot(L[j, :j], U[:j, i])) / L[j, j]

        # Forward substitution: Ly = b
        y = np.zeros(n)
        for i in range(n):
            y[i] = (b[i] -np.dot(L[i, :i], y[:i])) / L[i, i]
        
        # Backward substitution: Ux = y
        x = np.zeros(n)
        for i in range(n-1,-1, -1):
            x[i] = y[i] - np.dot(U[i,i+1:], x[i+1:])

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
                    sum_sq = np.dot(L[i, :j], L[i, :j])
                    val = A[i, i] - sum_sq
                    if val <= 0:
                        return SolutionResult(
                            has_solution=False,
                            message="matrix is not positive definite sorry try sth else then",
                            execution_time=time.time() - start_time
                        )
                    L[i, j] = np.sqrt(val)
                else:
                    sum_prod = np.dot(L[i, :j], L[j, :j])
                    L[i, j] = (A[i, j] - sum_prod) / L[j, j]
        
        #forward sub Ly = b
        y = np.zeros(n)
        for i in range(n):
            y[i]= (b[i] -np.dot(L[i,:i],y[:i])) /L[i, i]

        #backward sub L^T x = y
        x = np.zeros(n)
        for i in range(n- 1,-1, -1):
            x[i] = (y[i]- np.dot(L[i+1:,i],x[i+1:])) /L[i, i]
        
        execution_time=time.time()-start_time

        result =SolutionResult(
            solution=self.round_solution(x),
            execution_time=execution_time,
            message="we got a solution using LU (Cholesky)"
        )
        result.L = np.round(L, self.precision).tolist()
        result.U = np.round(L.T, self.precision).tolist()
        
        return result