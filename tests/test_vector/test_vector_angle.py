import pytest
from project.matrices_vectors.vector import Vector
import math


def test_angle_between_vectors():
    v1 = Vector([1, 0])
    v2 = Vector([0, 1])
    result = Vector.angle_between(v1, v2)
    assert math.isclose(result, 90.0, rel_tol=1e-6)


def test_angle_with_zero_vector():
    v1 = Vector([1, 2])
    v2 = Vector([0, 0])
    with pytest.raises(
        ValueError, match="Cannot compute angle with zero-length vector"
    ):
        Vector.angle_between(v1, v2)
