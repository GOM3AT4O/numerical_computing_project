from typing import Any, Dict

import numpy as np
from equations_solver.step import Step
from utils import remove_trailing_zeros


class ShowMatricesStep(Step):
    matrices: Dict[str, np.ndarray]

    def __init__(self, matrices: Dict[str, np.ndarray]):
        super().__init__("show-matrices")

        self.matrices = matrices

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "step_type": self.step_type,
            "matrices": {
                k: np.vectorize(remove_trailing_zeros)(v).tolist()
                for k, v in self.matrices.items()
            },
        }

        return result
