import math
from typing import List


class Vector:
    """
    Represents a mathematical vector.
    """

    values: List[float]

    def __init__(self, values: List[float]):
        """
        Initializes the vector with a list of values.
        """
        self.values = values

    def __add__(self, other: "Vector") -> "Vector":
        """
        Adds two vectors element-wise.
        """
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must be of the same length")
        return Vector([x + y for x, y in zip(self.values, other.values)])

    def __sub__(self, other: "Vector") -> "Vector":
        """
        Subtracts two vectors element-wise.
        """
        if len(self.values) != len(other.values):
            raise ValueError("Vectors must be of the same length")
        return Vector([x - y for x, y in zip(self.values, other.values)])

    @staticmethod
    def dot(v1: "Vector", v2: "Vector") -> float:
        """
        Computes the dot product of two vectors.
        """
        if len(v1.values) != len(v2.values):
            raise ValueError("Vectors must be of the same length")
        return sum(x * y for x, y in zip(v1.values, v2.values))

    def length(self) -> float:
        """
        Returns the Euclidean length of the vector.
        """
        return math.sqrt(sum(x**2 for x in self.values))

    @staticmethod
    def angle_between(v1: "Vector", v2: "Vector") -> float:
        """
        Returns the angle in radians between two vectors.
        """
        if v1.length() == 0 or v2.length() == 0:
            raise ValueError("Cannot compute angle with zero-length vector")
        cos_theta = Vector.dot(v1, v2) / (v1.length() * v2.length())
        return math.acos(cos_theta)

    def __repr__(self) -> str:
        """
        Returns a string representation of the vector.
        """
        return f"Vector({self.values})"
