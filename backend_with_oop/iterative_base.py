import numpy as np
from typing import List, Optional
from base_solver import LinearSystemSolver
from exceptions import ValidationError

class IterativeSolver(LinearSystemSolver):
    def __init__(self,A:np.ndarray, b: np.ndarray, precision:int = 6,
                initial_guess:Optional[List[float]] = None,
                max_iterations:int = 50,
                tolerance: float= 1e-6):
        super().__init__(A,b,precision)
        
        if initial_guess is not None:

            self.x0 = np.array(initial_guess,dtype=float)
            if len(self.x0)!= self.n:
                raise ValidationError(f"initail guess length must match number of variables which is  ({self.n})")
            else:
            
                self.x0 = np.zeros(self.n)
            
            self.max_iterations = max_iterations
            self.tolerance = tolerance

    def check_convergence(self, x_new: np.ndarray, x_old: np.ndarray) -> bool:
            #avoid zero division 
            denominator =np.maximum(np.abs(x_new),1e-10)
            relative_error= np.max(np.abs(x_new - x_old)/ denominator)
            return relative_error< self.tolerance
