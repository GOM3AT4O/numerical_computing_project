from decimal import Decimal
from typing import Dict, Optional, Any


class Result:
    root: Optional[Decimal]
    absolute_relative_error: Optional[Decimal]
    number_of_correct_significant_figures: Optional[int]
    number_of_iterations: Optional[int]
    execution_time: float
    message: str

    def __init__(
        self,
        root: Optional[Decimal] = None,
        absolute_relative_error: Optional[Decimal] = None,
        number_of_correct_significant_figures: Optional[int] = None,
        number_of_iterations: Optional[int] = None,
        execution_time: float = 0.0,
        message: str = "Solution found",
    ):
        self.root = root
        self.absolute_relative_error = absolute_relative_error
        self.number_of_correct_significant_figures = (
            number_of_correct_significant_figures
        )
        self.number_of_iterations = number_of_iterations
        self.execution_time = execution_time
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "message": self.message,
            "execution_time": round(self.execution_time, 12),
        }

        if self.root is not None:
            result["root"] = self.root

        if self.absolute_relative_error is not None:
            result["absolute_relative_error"] = self.absolute_relative_error

        if self.number_of_correct_significant_figures is not None:
            result["number_of_correct_significant_figures"] = (
                self.number_of_correct_significant_figures
            )

        if self.number_of_iterations is not None:
            result["number_of_iterations"] = self.number_of_iterations

        return result
