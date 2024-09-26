import pytest
from project.matrices_vectors.vector import Vector


def test_vector_subtraction():
    v1 = Vector([5, 7, 9])
    v2 = Vector([4, 5, 6])
    result = v1 - v2
    assert result.values == [1, 2, 3]


def test_vector_subtraction_unequal_lengths():
    v1 = Vector([1, 2])
    v2 = Vector([1, 2, 3])
    with pytest.raises(ValueError, match="Vectors must be of the same length"):
        v1 - v2
