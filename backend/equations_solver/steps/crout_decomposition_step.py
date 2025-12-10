from typing import Any, Dict
import numpy as np
from utils import remove_trailing_zeros
from step import Step


class CroutDecompositionStep(Step):
    A: np.ndarray
    L: np.ndarray
    U: np.ndarray

    def __init__(self, A: np.ndarray, L: np.ndarray, U: np.ndarray):
        super().__init__("crout-decomposition")

        self.A = A
        self.L = L
        self.U = U

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "step_type": self.step_type,
            "A": np.vectorize(remove_trailing_zeros)(self.A).tolist(),
            "L": np.vectorize(remove_trailing_zeros)(self.L).tolist(),
            "U": np.vectorize(remove_trailing_zeros)(self.U).tolist(),
        }

        return result
