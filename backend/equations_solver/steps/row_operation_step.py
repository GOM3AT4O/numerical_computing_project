import numpy as np
from decimal import Decimal
from typing import Any, Dict, Optional
from step import Step
from utils import remove_trailing_zeros


class RowOperationStep(Step):
    operation_type: str
    old_matrix: np.ndarray
    new_matrix: np.ndarray
    target_row: int
    source_row: Optional[int]
    factor: Optional[Decimal]

    def __init__(
        self,
        operation_type: str,
        old_matrix: np.ndarray,
        new_matrix: np.ndarray,
        target_row: int,
        source_row: Optional[int] = None,
        factor: Optional[Decimal] = None,
    ):
        super().__init__("row-operation")

        self.operation_type = operation_type
        self.old_matrix = old_matrix
        self.new_matrix = new_matrix
        self.target_row = target_row
        self.source_row = source_row
        self.factor = factor

    @classmethod
    def swap(
        cls,
        old_matrix: np.ndarray,
        new_matrix: np.ndarray,
        target_row: int,
        source_row: int,
    ) -> "RowOperationStep":
        return cls(
            operation_type="swap",
            old_matrix=old_matrix,
            new_matrix=new_matrix,
            target_row=target_row,
            source_row=source_row,
        )

    @classmethod
    def scale(
        cls, old_matrix: np.ndarray, new_matrix: np.ndarray, row: int, factor: Decimal
    ) -> "RowOperationStep":
        return cls(
            operation_type="scale",
            old_matrix=old_matrix,
            new_matrix=new_matrix,
            target_row=row,
            factor=factor,
        )

    @classmethod
    def add(
        cls,
        old_matrix: np.ndarray,
        new_matrix: np.ndarray,
        target_row: int,
        source_row: int,
        factor: Decimal,
    ) -> "RowOperationStep":
        return cls(
            operation_type="add",
            old_matrix=old_matrix,
            new_matrix=new_matrix,
            target_row=target_row,
            source_row=source_row,
            factor=factor,
        )

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "step_type": self.step_type,
            "operation_type": self.operation_type,
            "old_matrix": np.vectorize(remove_trailing_zeros)(self.old_matrix).tolist(),
            "new_matrix": np.vectorize(remove_trailing_zeros)(self.new_matrix).tolist(),
            "target_row": self.target_row,
        }

        if self.source_row is not None:
            result["source_row"] = self.source_row

        if self.factor is not None:
            result["factor"] = remove_trailing_zeros(self.factor)

        return result
