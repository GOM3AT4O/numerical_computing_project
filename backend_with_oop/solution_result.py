"""
SolutionResult class to encapsulate solver results
"""

import numpy as np
from typing import Dict, Optional, Any


class SolutionResult:
    """Class to encapsulate solution results"""
    
    def __init__(self, solution: Optional[np.ndarray] = None, 
                 iterations: Optional[int] = None,
                 execution_time: float = 0.0,
                 message: str = "Solution found",
                 has_solution: bool = True):
        self.solution = solution
        self.iterations = iterations
        self.execution_time = execution_time
        self.message = message
        self.has_solution = has_solution
        
        # Optional fields for LU decomposition
        self.L = None
        self.U = None
        self.L_transpose = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON response"""
        result = {
            'has_solution': self.has_solution,
            'message': self.message,
            'execution_time': round(self.execution_time, 12) 
        }
        
        if self.solution is not None:
            result['solution'] = self.solution.tolist()
        
        if self.iterations is not None:
            result['iterations'] = self.iterations
        
        if self.L is not None:
            result['L'] = self.L
        
        if self.U is not None:
            result['U'] = self.U
        
        if self.L_transpose is not None:
            result['L_transpose'] = self.L_transpose
            
        return result