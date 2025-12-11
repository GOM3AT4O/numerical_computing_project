from typing import Any, Dict

import numpy as np
from equations_solver.step import Step
from utils import remove_trailing_zeros


class SubstitutionStep(Step):
    substitution_type: str
    matrix: np.ndarray
    result: np.ndarray

    def __init__(self, substitution_type: str, matrix: np.ndarray, result: np.ndarray):
        super().__init__("substitution")

        self.substitution_type = substitution_type
        self.matrix = matrix
        self.result = result

    @classmethod
    def forward(cls, matrix: np.ndarray, result: np.ndarray) -> "SubstitutionStep":
        return cls(
            substitution_type="forward",
            matrix=matrix,
            result=result,
        )

    @classmethod
    def back(cls, matrix: np.ndarray, result: np.ndarray) -> "SubstitutionStep":
        return cls(
            substitution_type="back",
            matrix=matrix,
            result=result,
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "step_type": self.step_type,
            "substitution_type": self.substitution_type,
            "matrix": np.vectorize(remove_trailing_zeros)(self.matrix).tolist(),
            "result": np.vectorize(remove_trailing_zeros)(self.result).tolist(),
        }

        return result
