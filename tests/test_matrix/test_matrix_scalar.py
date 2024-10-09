from project.matrices_vectors.matrix import Matrix


def test_matrix_scalar_multiplication():
    m = Matrix([[1, 2], [3, 4]])
    result = m * 2
    assert result.values == [[2, 4], [6, 8]]


def test_matrix_scalar_multiplication_by_zero():
    m = Matrix([[1, 2], [3, 4]])
    result = m * 0
    assert result.values == [[0, 0], [0, 0]]
