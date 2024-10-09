import pytest
from project.matrices_vectors.matrix import Matrix


def test_matrix_multiplication():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    result = m1.matrix_multiply(m2)
    assert result.values == [[19, 22], [43, 50]]


def test_matrix_multiplication_non_square():
    m1 = Matrix([[1, 2, 3], [4, 5, 6]])
    m2 = Matrix([[7, 8], [9, 10], [11, 12]])
    result = m1.matrix_multiply(m2)
    assert result.values == [[58, 64], [139, 154]]


def test_matrix_multiplication_incompatible_dimensions():
    m1 = Matrix([[1, 2]])
    m2 = Matrix([[3, 4], [5, 6], [7, 8]])
    with pytest.raises(
        ValueError,
        match="Number of columns in the first matrix must equal the number of rows in the second matrix",
    ):
        m1.matrix_multiply(m2)
