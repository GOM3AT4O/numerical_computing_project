from decimal import Decimal
import numpy as np
from steps.substitution_step import SubstitutionStep
from solver import Solver
from typing import Tuple
from steps.row_operation_step import RowOperationStep


# base class for elimination solvers (like Gauss elimination, Gauss-Jordan elimination, etc.)
class EliminationSolver(Solver):
    scaling: bool  # whether to use scaling or not
    scaling_factors: np.ndarray  # scaling factors array

    def __init__(
        self,
        A: np.ndarray,
        b: np.ndarray,
        precision: int = 6,
        scaling: bool = False,
    ):
        super().__init__(A, b, precision)
        self.scaling = scaling

    # eliminate the element in row i using the pivot row k
    def eliminate_row(self, A: np.ndarray, b: np.ndarray, i: int, k: int):
        old_matrix = np.column_stack([A, b])

        factor = A[i, k] / A[k, k]

        # multiply pivot row by factor and subtract from current row
        for j in range(k + 1, self.n):
            A[i, j] -= factor * A[k, j]

        A[i, k] = +Decimal(0)

        b[i] -= factor * b[k]

        new_matrix = np.column_stack([A, b])

        # add elimination step
        self.steps.append(RowOperationStep.add(old_matrix, new_matrix, i, k, -factor))

    # back substitution to solve for x using the matrix A in row echelon form
    def back_substitution(self, A: np.ndarray, b: np.ndarray) -> np.ndarray:
        x = np.full(self.n, +Decimal(0))

        for i in range(self.n - 1, -1, -1):
            x[i] = b[i]
            for j in range(i + 1, self.n):
                x[i] -= A[i, j] * x[j]
            x[i] /= A[i, i]

        matrix = np.column_stack([A, b])

        # add back substitution step
        self.steps.append(SubstitutionStep.back(matrix, x))

        return x

    # for calculating the scaling values of each row in the coefficient matrix A
    def calculating_scaling_values(self, A: np.ndarray):
        n = A.shape[0]  # number of rows in A
        s = np.full(n, Decimal(0))  # initialize scaling factors array
        for i in range(n):  # iterate through each row
            s[i] = np.max(np.abs(A[i, :]))  # find the maximum absolute value in the row
        self.scaling_factors = s  # set the array of scaling factors

    # find the pivot index using partial pivoting
    def partial_pivot_index(self, A: np.ndarray, k: int) -> int:
        return int(k + np.argmax(np.abs(A[k:, k])))

    # find the pivot index using scaled partial pivoting
    def scaling_pivot_index(self, A: np.ndarray, k: int) -> int:
        ratios = (
            np.abs(A[k:, k]) / self.scaling_factors[k:]
        )  # calculate the ratio of the absolute value of the pivot element to the scaling factor for each row
        pivot_index = k + np.argmax(ratios)  # find the index of the maximum ratio
        return int(pivot_index)  # return the index of the pivot row

    def pivot(
        self, A: np.ndarray, b: np.ndarray, k: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        # choose pivoting method
        if self.scaling:
            pivot_index = self.scaling_pivot_index(A, k)
        else:
            pivot_index = self.partial_pivot_index(A, k)

        # if the pivot row is not the current row, swap them
        if pivot_index != k:
            old_matrix = np.column_stack([A, b])
            A[[k, pivot_index]] = A[[pivot_index, k]]
            b[[k, pivot_index]] = b[[pivot_index, k]]
            if self.scaling:
                self.scaling_factors[[k, pivot_index]] = self.scaling_factors[
                    [pivot_index, k]
                ]

            new_matrix = np.column_stack([A, b])

            # add row swap step
            self.steps.append(
                RowOperationStep.swap(old_matrix, new_matrix, k, int(pivot_index))
            )

        # returning the updated A and b
        return A, b
