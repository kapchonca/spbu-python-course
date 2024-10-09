from project.matrices_vectors.matrix import Matrix


def test_matrix_transpose():
    m = Matrix([[1, 2], [3, 4]])
    result = m.transpose()
    assert result.values == [[1, 3], [2, 4]]


def test_matrix_transpose_non_square():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    result = m.transpose()
    assert result.values == [[1, 4], [2, 5], [3, 6]]
