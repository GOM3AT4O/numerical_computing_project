import numpy as np
from typing import Any, Dict
from utils import remove_trailing_zeros
from step import Step


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
