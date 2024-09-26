from project.matrices_vectors.vector import Vector


def test_vector_length():
    v = Vector([3, 4])
    assert v.length() == 5.0


def test_zero_vector_length():
    v = Vector([0, 0, 0])
    assert v.length() == 0.0
