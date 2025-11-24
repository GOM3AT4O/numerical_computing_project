from decimal import Decimal
import numpy as np
from typing import List, Tuple, Optional
from exceptions import ValidationError


class LinearSystemValidator:
    @staticmethod
    def validate_system(
        A: List[List[Decimal]], b: List[Decimal]
    ) -> Tuple[np.ndarray, np.ndarray]:
        try:
            A_matrix = np.array(A, dtype=Decimal)
            b_vector = np.array(b, dtype=Decimal)
        except (ValueError, TypeError) as e:
            raise ValidationError(
                f"Coefficients must be numbers:{str(e)}"
            )  # that's the one will need to channge later on for the bonus

        if A_matrix.ndim != 2:
            raise ValidationError("Coefficient matrix must be 2-dimensional.")

        if b_vector.ndim != 1:
            raise ValidationError("Constants vector must be 1-dimensional.")

        n_equations, n_variables = A_matrix.shape

        if n_equations != n_variables:
            raise ValidationError(
                f"Number of equations ({n_equations}) must equal number of variables ({n_variables})."
            )

        return A_matrix, b_vector

    @staticmethod
    def validate_precision(precision: Optional[int]) -> int:
        if precision is None:
            return 10  # a7la defalut

        try:
            prec = int(precision)
            if prec < 1:
                raise ValidationError("Precision must be more than 1")
            return prec
        except (ValueError, TypeError):
            raise ValidationError("Precision  must be an integer")
