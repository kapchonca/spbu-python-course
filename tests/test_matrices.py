import pytest
from project.matrices_vectors.matrix import Matrix
from project.matrices_vectors.vector import Vector


# Test Vector Class
def test_vector_addition():
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    result = v1 + v2
    assert result.values == [5, 7, 9]


def test_vector_subtraction():
    v1 = Vector([4, 5, 6])
    v2 = Vector([1, 2, 3])
    result = v1 - v2
    assert result.values == [3, 3, 3]


def test_vector_dot_product():
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    result = Vector.dot(v1, v2)
    assert result == 32


def test_vector_length():
    v = Vector([3, 4])
    result = v.length()
    assert result == 5


def test_vector_angle_between():
    v1 = Vector([1, 0])
    v2 = Vector([0, 1])
    result = Vector.angle_between(v1, v2)
    assert pytest.approx(result, 0.01) == 1.5708  # approx π/2 radians (90 degrees)


# Test Matrix Class
def test_matrix_addition():
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    result = m1 + m2
    assert result.values == [[6, 8], [10, 12]]


def test_matrix_subtraction():
    m1 = Matrix([[5, 6], [7, 8]])
    m2 = Matrix([[1, 2], [3, 4]])
    result = m1 - m2
    assert result.values == [[4, 4], [4, 4]]


def test_matrix_scalar_multiplication():
    m = Matrix([[1, 2], [3, 4]])
    result = m * 3
    assert result.values == [[3, 6], [9, 12]]


def test_matrix_transpose():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    result = m.transpose()
    assert result.values == [[1, 4], [2, 5], [3, 6]]
