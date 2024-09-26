import math
from typing import List


class Matrix:
    """
    Represents a mathematical matrix.
    """

    values: List[List[float]]
    rows: int
    cols: int

    def __init__(self, values: List[List[float]]):
        """
        Initializes the matrix with a 2D list of values.
        """
        if not all(len(row) == len(values[0]) for row in values):
            raise ValueError("All rows must have the same length")
        self.values = values
        self.rows = len(values)
        self.cols = len(values[0])

    def _assert_dimensionality(self, other: "Matrix"):
        """
        Ensures that two matrices have the same dimensions.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions")

    def __add__(self, other: "Matrix") -> "Matrix":
        """
        Adds two matrices element-wise.
        """
        self._assert_dimensionality(other)
        return Matrix(
            [
                [self.values[i][j] + other.values[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def __sub__(self, other: "Matrix") -> "Matrix":
        """
        Subtracts two matrices element-wise.
        """
        self._assert_dimensionality(other)
        return Matrix(
            [
                [self.values[i][j] - other.values[i][j] for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def __mul__(self, scalar: float) -> "Matrix":
        """
        Multiplies the matrix by a scalar.
        """
        return Matrix(
            [
                [self.values[i][j] * scalar for j in range(self.cols)]
                for i in range(self.rows)
            ]
        )

    def transpose(self) -> "Matrix":
        """
        Returns the transposed matrix.
        """
        return Matrix(
            [[self.values[j][i] for j in range(self.rows)] for i in range(self.cols)]
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the matrix.
        """
        return f"Matrix({self.values})"
