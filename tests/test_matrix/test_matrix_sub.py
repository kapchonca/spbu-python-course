import pytest
from project.matrices_vectors.matrix import Matrix


def test_matrix_subtraction():
    m1 = Matrix([[5, 7], [9, 11]])
    m2 = Matrix([[1, 2], [3, 4]])
    result = m1 - m2
    assert result.values == [[4, 5], [6, 7]]


def test_matrix_subtraction_unequal_dimensions():
    m1 = Matrix([[1, 2]])
    m2 = Matrix([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="Matrices must have the same dimensions"):
        m1 - m2
