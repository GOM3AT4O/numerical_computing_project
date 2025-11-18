import numpy  as np
from abc import  ABC , abstractmethod
from typing import  Tuple
from solution_result  import SolutionResult

class LinearSystemSolver(ABC):
    def __init__(self, A: np.ndarray ,  b: np.ndarray,precision:int= 6):
        self.A = A.copy()
        self.b = b.copy()
        self.n = len(b)
        self.precision = precision

    @abstractmethod
    def solve(self) -> SolutionResult:
        #solve the system
        pass

    def round_solution(self,x:np.ndarray) -> np.ndarray:
        #precision is callin'
        return np.round(x,self.precision)
    
    @staticmethod
    def partial_pivot(A: np.ndarray, b:np.ndarray, k: int) ->Tuple[np.ndarray, np.ndarray]:
        #pevoting
        n = len(b)
        max_idx= k+np.argmax(np.abs(A[k:,k]))
        
        if max_idx!=k:
            # Swap rows
            A[[k,max_idx]]= A[[max_idx,k]]
            b[[k,max_idx]] = b[[ max_idx,k]]
        return A, b