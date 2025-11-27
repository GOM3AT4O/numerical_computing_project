from decimal import Decimal
import numpy as np
import time
from steps.substitution import Substitution
from solver import Solver
from solution_result import SolutionResult
from exceptions import ValidationError


class LUDecompositionSolver(Solver):
    def __init__(
        self,
        A: np.ndarray,
        b: np.ndarray,
        precision: int = 6,
        format: str = "doolittle",
    ):
        super().__init__(A, b, precision)
        self.format = format.lower()

    def solve(self) -> SolutionResult:
        if self.format == "doolittle":
            return self._solve_doolittle()

        elif self.format == "crout":
            return self._solve_crout()

        elif self.format == "cholesky":
            return self._solve_cholesky()

        else:
            raise ValidationError(f"Unknown LU Decomposition format: {self.format}")

    def _solve_doolittle(self) -> SolutionResult:
        start_time = time.time()

        A = self.A.copy()
        b = self.b.copy()
        n = self.n
        # Pivoting
        P = np.array(
            [
                [+Decimal(1) if i == j else +Decimal(0) for j in range(n)]
                for i in range(n)
            ],
            dtype=Decimal,
        )

        for k in range(n):
            max_idx = k + np.argmax(np.abs(A[k:, k]))
            if max_idx != k:
                A[[k, max_idx]] = A[[max_idx, k]]
                P[[k, max_idx]] = P[[max_idx, k]]

                A = A
                P = P

        L = np.array(
            [
                [+Decimal(1) if i == j else +Decimal(0) for j in range(n)]
                for i in range(n)
            ],
            dtype=Decimal,
        )
        U = np.full((n, n), +Decimal(0))

        for i in range(n):
            # Upper
            for j in range(i, n):
                dot_product = +Decimal(0)
                for k in range(i):
                    product = L[i, k] * U[k, j]
                    dot_product = dot_product + product

                U[i, j] = A[i, j] - dot_product

            if abs(U[i, i]) < 1e-12:
                return SolutionResult(
                    message="System doesn't have a unique solution.",
                    execution_time=time.time() - start_time,
                )

            # Lower
            for j in range(i + 1, n):
                dot_product = +Decimal(0)
                for k in range(i):
                    product = L[j, k] * U[k, i]
                    dot_product = dot_product + product

                numerator = A[j, i] - dot_product
                L[j, i] = numerator / U[i, i]

        # permutation
        b = P @ b

        # forward sub
        y = np.full(n, +Decimal(0))
        for i in range(n):
            dot_product = +Decimal(0)
            for j in range(i):
                product = L[i, j] * y[j]
                dot_product = dot_product + product

            y[i] = b[i] - dot_product

        matrix = np.column_stack([L, b])

        self.steps.append(Substitution.forward(matrix, y))

        # back sub
        x = np.full(n, +Decimal(0))
        for i in range(n - 1, -1, -1):
            dot_product = +Decimal(0)
            for j in range(i + 1, n):
                product = U[i, j] * x[j]
                dot_product = dot_product + product

            numerator = y[i] - dot_product
            x[i] = numerator / U[i, i]

        matrix = np.column_stack([U, y])

        self.steps.append(Substitution.back(matrix, x))

        execution_time = time.time() - start_time

        result = SolutionResult(
            solution=x,
            steps=self.steps,
            execution_time=execution_time,
            message="Solution found using doolittle LU decomposition.",
        )
        # Add L and U matrices to result
        result.L = L
        result.U = U

        return result

    def _solve_crout(self) -> SolutionResult:
        start_time = time.time()
        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        L = np.full((n, n), +Decimal(0))
        U = np.array(
            [
                [+Decimal(1) if i == j else +Decimal(0) for j in range(n)]
                for i in range(n)
            ],
            dtype=Decimal,
        )

        for j in range(n):
            # lower
            for i in range(j, n):
                dot_product = +Decimal(0)
                for k in range(j):
                    product = L[i, k] * U[k, j]
                    dot_product = dot_product + product

                L[i, j] = A[i, j] - dot_product

            # check singularity
            if abs(L[j, j]) < 1e-12:
                return SolutionResult(
                    message="System doesn't have a unique solution.",
                    execution_time=time.time() - start_time,
                )

            # Upper triangular
            for i in range(j + 1, n):
                dot_product = +Decimal(0)
                for k in range(j):
                    product = L[j, k] * U[k, i]
                    dot_product = dot_product + product

                numerator = A[j, i] - dot_product
                U[j, i] = numerator / L[j, j]

        # forward sub: Ly = b
        y = np.full(n, +Decimal(0))
        for i in range(n):
            dot_product = +Decimal(0)
            for j in range(i):
                product = L[i, j] * y[j]
                dot_product = dot_product + product

            numerator = b[i] - dot_product
            y[i] = numerator / L[i, i]

        matrix = np.column_stack([L, b])

        self.steps.append(Substitution.forward(matrix, y))

        # backwar sub: Ux = y
        x = np.full(n, +Decimal(0))
        for i in range(n - 1, -1, -1):
            dot_product = +Decimal(0)

            for j in range(i + 1, n):
                product = U[i, j] * x[j]
                dot_product = dot_product + product

            x[i] = y[i] - dot_product

        matrix = np.column_stack([U, y])

        self.steps.append(Substitution.back(matrix, x))

        execution_time = time.time() - start_time

        result = SolutionResult(
            solution=x,
            steps=self.steps,
            execution_time=execution_time,
            message="Solution found using Crout LU Decomposition.",
        )
        # Add L and U matrices to result
        result.L = L
        result.U = U

        return result

    @staticmethod
    def allclose(
        a: np.ndarray, b: np.ndarray, rtol=Decimal("1e-5"), atol=Decimal("1e-8")
    ) -> bool:
        if a.shape != b.shape:
            return False

        for x, y in zip(a.flat, b.flat):
            diff = abs(x - y)
            tol = atol + rtol * abs(y)
            if diff > tol:
                return False
        return True

    def _solve_cholesky(self) -> SolutionResult:
        start_time = time.time()
        A = self.A.copy()
        b = self.b.copy()
        n = self.n

        # Check matrix symmetric or what
        if not self.allclose(A, A.T):
            return SolutionResult(
                message="Coefficients matrix is not symmetric.",
                execution_time=time.time() - start_time,
            )

        L = np.full((n, n), +Decimal(0))
        for i in range(n):
            for j in range(i + 1):
                if i == j:
                    sum_sq = +Decimal(0)
                    for k in range(j):
                        product = L[i, k] * L[i, k]
                        sum_sq = sum_sq + product
                    val = A[i, i] - sum_sq
                    if val <= 0:
                        return SolutionResult(
                            message="Coefficients matrix is not positive definite.",
                            execution_time=time.time() - start_time,
                        )

                    L[i, j] = np.sqrt(val)
                else:
                    sum_prod = +Decimal(0)
                    for k in range(j):
                        product = L[i, k] * L[j, k]
                        sum_prod = sum_prod + product
                    numerator = A[i, j] - sum_prod
                    L[i, j] = numerator / L[j, j]

        # forward sub Ly = b
        y = np.full(n, +Decimal(0))
        for i in range(n):
            dot_product = +Decimal(0)
            for j in range(i):
                product = L[i, j] * y[j]
                dot_product = dot_product + product

            numerator = b[i] - dot_product
            y[i] = numerator / L[i, i]

        matrix = np.column_stack([L, b])

        self.steps.append(Substitution.forward(matrix, y))

        # backward sub
        x = np.full(n, +Decimal(0))
        for i in range(n - 1, -1, -1):
            dot_product = +Decimal(0)
            for j in range(i + 1, n):
                product = L[j, i] * x[j]
                dot_product = dot_product + product

            numerator = y[i] - dot_product
            x[i] = numerator / L[i, i]

        matrix = np.column_stack([L.T, y])

        self.steps.append(Substitution.back(matrix, x))

        execution_time = time.time() - start_time

        result = SolutionResult(
            solution=x,
            steps=self.steps,
            execution_time=execution_time,
            message="Solution found using Cholesky LU Decomposition.",
        )
        result.L = L
        result.U = L.T

        return result
