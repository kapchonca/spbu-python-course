import pytest
from project.matrices_vectors.vector import Vector


def test_dot_product():
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    result = Vector.dot(v1, v2)
    assert result == 32


def test_dot_product_unequal_lengths():
    v1 = Vector([1, 2])
    v2 = Vector([1, 2, 3])
    with pytest.raises(ValueError, match="Vectors must be of the same length"):
        Vector.dot(v1, v2)
