import pytest
from project.matrices_vectors.matrix import Matrix


def test_matrix_addition():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    result = m1 + m2
    assert result.values == [[6, 8], [10, 12]]


def test_matrix_addition_unequal_dimensions():
    m1 = Matrix([[1, 2]])
    m2 = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="Matrices must have the same dimensions"):
        m1 + m2
