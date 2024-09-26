from project.matrices_vectors.matrix import Matrix


def test_single_row_by_single_column():
    m1 = Matrix([[1, 2, 3]])
    m2 = Matrix([[4], [5], [6]])
    result = m1.matrix_multiply(m2)
    assert result.values == [[32]]


def test_single_element_multiplication():
    m1 = Matrix([[2]])
    m2 = Matrix([[3]])
    result = m1.matrix_multiply(m2)
    assert result.values == [[6]]


def test_multiplication_by_zero_matrix():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[0, 0], [0, 0]])
    result = m1.matrix_multiply(m2)
    assert result.values == [[0, 0], [0, 0]]
