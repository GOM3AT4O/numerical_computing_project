from decimal import Decimal
import numpy as np
from typing import List, Tuple, Optional
from exceptions import ValidationError
from sympy import parse_expr, real_root, symbols, E, pi
from sympy.parsing.sympy_parser import (
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
    rationalize,
)
from sympy.core.sympify import SympifyError


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
            )  # that's the one will need to change later on for the bonus

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


class FunctionValidator:
    @staticmethod
    def validate_and_parse(equation_str: str):
        """Validates and parses a mathematical equation string into a SymPy expression."""

        # if the equation string is empty or None, raise an error
        if not equation_str or not equation_str.strip():
            raise ValidationError("Equation cannot be empty.")

        # try to parse the equation string into a SymPy expression

        x = symbols("x", real=True)

        try:
            transformations = standard_transformations + (
                implicit_multiplication_application,
                convert_xor,
                rationalize,
            )
            expr = parse_expr(
                equation_str,
                local_dict={"x": x, "e": E, "pi": pi},
                transformations=transformations,
            )

            expr = expr.replace(
                lambda x: x.is_Pow and x.exp.is_Rational and x.exp.q % 2 == 1,
                lambda x: real_root(x.base**x.exp.p, x.exp.q),
            )
        except (SympifyError, SyntaxError):
            raise ValidationError("Invalid equation format. Please check your syntax.")

        # check if the number of free symbols in the expression is only 1 or not
        free_symbols = expr.free_symbols

        if len(free_symbols) != 1:
            if len(free_symbols) == 0:
                raise ValidationError("Equation must contain a variable 'x'.")
            raise ValidationError(
                f"Equation must contain only one variable. Found: {free_symbols}"
            )

        # check if the variable is 'x' or not
        variable = list(free_symbols)[0]
        if variable.name != "x":
            raise ValidationError(f"Variable must be 'x'. Found: '{variable.name}'")

        # All validations passed, return the parsed expression
        # The return type is sympy expression
        return expr
