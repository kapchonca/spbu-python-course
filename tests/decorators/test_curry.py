import pytest
from project.decorators.currying import curry_explicit


def test_curry_explicit_basic():
    # Test for a basic function of 2 arguments
    def add(a, b):
        return a + b

    curried_add = curry_explicit(add, 2)
    assert curried_add(2)(3) == 5  # Curried form
    assert curried_add(2, 3) == 5  # Non-curried form


def test_curry_explicit_multiple_args():
    # Test with a function that takes 3 arguments
    def multiply(a, b, c):
        return a * b * c

    curried_multiply = curry_explicit(multiply, 3)
    assert curried_multiply(2)(3)(4) == 24
    assert curried_multiply(2, 3)(4) == 24
    assert curried_multiply(2)(3, 4) == 24
    assert curried_multiply(2, 3, 4) == 24


def test_curry_explicit_edge_cases():
    # Test with a function of 0 arguments
    def constant():
        return 42

    curried_constant = curry_explicit(constant, 0)
    assert curried_constant() == 42


def test_curry_explicit_arity_mismatch():
    # Test if too many arguments are passed
    def add(a, b):
        return a + b

    curried_add = curry_explicit(add, 2)
    with pytest.raises(TypeError, match="Too many arguments"):
        curried_add(1, 2, 3)


def test_curry_explicit_negative_arity():
    # Test for negative arity
    def dummy():
        return 0

    with pytest.raises(ValueError, match="non-negative integer"):
        curry_explicit(dummy, -1)