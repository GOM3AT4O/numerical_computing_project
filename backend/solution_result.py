import numpy as np
from typing import Dict, Optional, Any
from decimal import Decimal


class SolutionResult:
    solution: Optional[np.ndarray]
    iterations: Optional[int]
    execution_time: float
    message: str
    has_solution: bool
    L: Optional[np.ndarray]
    U: Optional[np.ndarray]

    def __init__(
        self,
        solution: Optional[np.ndarray] = None,
        iterations: Optional[int] = None,
        execution_time: float = 0.0,
        message: str = "Solution found",
        has_solution: bool = True,
    ):
        self.solution = solution
        self.iterations = iterations
        self.execution_time = execution_time
        self.message = message
        self.has_solution = has_solution

        # optional fields for LU decomposition
        self.L = None
        self.U = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "has_solution": self.has_solution,
            "message": self.message,
            "execution_time": round(self.execution_time, 12),
        }

        def remove_exponent(value: Decimal):
            value = value.normalize()
            if value == value.to_integral_value():
                return value.to_integral_value()
            return value

        if self.solution is not None:
            result["solution"] = np.vectorize(remove_exponent)(self.solution).tolist()

        if self.iterations is not None:
            result["iterations"] = self.iterations

        if self.L is not None:
            result["L"] = np.vectorize(remove_exponent)(self.L).tolist()

        if self.U is not None:
            result["U"] = np.vectorize(remove_exponent)(self.U).tolist()

        return result
