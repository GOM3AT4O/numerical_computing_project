import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple
from solution_result import SolutionResult


class LinearSystemSolver(ABC):
    #abstract base class for linear system solvers
    
    def __init__(self, A: np.ndarray, b: np.ndarray, precision: int = 6):
        self.A = A.copy()
        self.b = b.copy()
        self.n = len(b)
        self.precision = precision
    
    @abstractmethod
    def solve(self) -> SolutionResult:
        
        pass
    
    def round_to_sf(self, x):
        
        def round_single(num):
            if num == 0:
                return 0 
            
            order = np.floor(np.log10(abs(num)))
            scale = 10 ** (self.precision - 1 - order)
            return round(num * scale) / scale
        
        if isinstance(x, np.ndarray):
            return np.vectorize(round_single)(x)
        else:
            return round_single(x)
        
    def round_solution(self, x: np.ndarray) -> np.ndarray:
        return self.round_to_sf(x)
        
    
    @staticmethod
    def partial_pivot(A: np.ndarray, b: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        #apply pivoting
        n = len(b)
        max_idx = k + np.argmax(np.abs(A[k:, k]))
        
        if max_idx != k:
            # Swap rows
            A[[k, max_idx]] = A[[max_idx, k]]
            b[[k, max_idx]] = b[[max_idx, k]]
        
        return A, b