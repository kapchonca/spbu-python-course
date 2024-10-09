import pytest
from project.decorators.currying import curry_explicit, uncurry_explicit


def test_uncurry_explicit_basic():
    # Test for basic function uncurrying
    def curried_add(a):
        return lambda b: a + b

    uncurried_add = uncurry_explicit(curried_add, 2)
    assert uncurried_add(2, 3) == 5


def test_uncurry_explicit_multiple_args():
    # Test uncurrying with multiple arguments
    def curried_multiply(a):
        return lambda b: lambda c: a * b * c

    uncurried_multiply = uncurry_explicit(curried_multiply, 3)
    assert uncurried_multiply(2, 3, 4) == 24


def test_uncurry_explicit_edge_cases():
    # Test with curried function that has 0 arguments
    def curried_constant():
        return lambda: 42

    uncurried_constant = uncurry_explicit(curried_constant, 0)
    assert uncurried_constant() == 42


def test_uncurry_explicit_arity_mismatch():
    # Test arity mismatch handling
    def curried_add(a):
        return lambda b: a + b

    uncurried_add = uncurry_explicit(curried_add, 2)

    with pytest.raises(ValueError, match="Expected 2 arguments"):
        uncurried_add(1)  # Too few arguments

    with pytest.raises(ValueError, match="Expected 2 arguments"):
        uncurried_add(1, 2, 3)  # Too many arguments


def test_uncurry_explicit_negative_arity():
    # Test for negative arity
    def dummy():
        return lambda: 0

    with pytest.raises(ValueError, match="non-negative integer"):
        uncurry_explicit(dummy, -1)


def test_combination_curry_and_uncurry():
    # Test curried and uncurried functions in combination
    def add(a, b):
        return a + b

    curried_add = curry_explicit(add, 2)
    uncurried_add = uncurry_explicit(curried_add, 2)

    assert uncurried_add(2, 3) == 5  # Check if uncurrying the curried function works
