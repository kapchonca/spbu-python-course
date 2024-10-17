import pytest
from project.generators.generators import return_kth_prime, prime_generator


@pytest.mark.parametrize(
    "count,expected_primes",
    [
        (5, [2, 3, 5, 7, 11]),
        (10, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]),
    ],
)
def test_prime_generator(count, expected_primes):
    gen = prime_generator()
    primes = [next(gen) for _ in range(count)]
    assert primes == expected_primes


@pytest.mark.parametrize(
    "k,expected",
    [
        (1, 2),
        (5, 11),
        (100, 541),
    ],
)
def test_kth_prime(k, expected):
    @return_kth_prime(k)
    def decorated_prime_generator():
        return prime_generator()

    assert decorated_prime_generator() == expected


@pytest.mark.parametrize(
    "invalid_k",
    [
        -1,
        0,
        1.5,
        "three",
        None,
    ],
)
def test_invalid_k(invalid_k):
    with pytest.raises((TypeError, ValueError)):

        @return_kth_prime(invalid_k)
        def decorated_prime_generator():
            return prime_generator()

        decorated_prime_generator()
