from typing import Generator, Tuple, Optional, Callable


def get_rgba_gen() -> Generator[Tuple[int, int, int, int], None, None]:
    """
    Generates all possible RGBA color combinations.

    Each component (R, G, B) varies from 0 to 255 (inclusive), while
    the alpha channel (A) varies from 0 to 100 in steps of 2.

    Yields:
        Tuple[int, int, int, int]: A tuple representing the RGBA color.
            - r: Red value (0-255)
            - g: Green value (0-255)
            - b: Blue value (0-255)
            - a: Alpha value (0-100, in steps of 2)
    """
    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(0, 101)
        if a % 2 == 0
    )


def get_ith_colour(index: int) -> Tuple[int, int, int, int]:
    """
    Returns the RGBA color at the specified index in the sequence.

    Args:
        index (int): The 1-based index of the desired RGBA color in the sequence.

    Returns:
        Tuple[int, int, int, int]: The RGBA color at the given index.

    Raises:
        StopIteration: If the index is out of range of the generator.
    """
    if index < 1 or index > 256**3 * 51:
        raise IndexError("Colour index out of range")
    rgba_gen = get_rgba_gen()
    for _ in range(index - 1):
        next(rgba_gen)
    return next(rgba_gen)


def prime_generator() -> Generator[int, None, None]:
    """
    A generator function that yields prime numbers in increasing order.

    Yields:
        int: The next prime number.
    """

    def is_prime(n: int) -> bool:
        """
        Checks if a number is prime.

        Args:
            n (int): The number to check for primality.

        Raises:
            TypeError: If n is not an integer.

        Returns:
            bool: True if n is a prime number, False otherwise.
        """
        if not isinstance(n, int):
            raise TypeError("Number must be an integer.")
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1


def return_kth_prime() -> (
    Callable[[Callable[[], Generator[int, None, None]]], Callable[[int], int]]
):
    """
    A decorator that modifies a generator function to return the k-th prime number
    and store the last generated prime, ensuring that the sequence is non-decreasing.

    The function can be called multiple times with increasing k.

    Returns:
        Callable: A decorator function that modifies the behavior of the input function.
    """

    def decorator(
        func: Callable[[], Generator[int, None, None]]
    ) -> Callable[[int], int]:
        """
        Decorator that modifies the generator to return the k-th prime number
        and stores the last generated prime as an attribute.

        Args:
            func (Callable): A generator function that yields prime numbers.

        Returns:
            Callable: The modified function that returns the k-th prime number
            and stores the last generated prime.
        """
        gen = func()
        last_k: int = 0
        last_prime: Optional[int] = None

        def wrapper(k: int) -> int:
            """
            The wrapper function that executes the generator and returns the k-th prime,
            ensuring that k is greater than or equal to the last requested value.

            Args:
                k (int): The position of the prime number to return.

            Returns:
                int: The k-th prime number.
            """
            nonlocal last_k, last_prime

            if k < last_k:
                raise ValueError(
                    "k must be greater than or equal to the last requested value."
                )

            for _ in range(last_k, k):
                last_prime = next(gen)

            last_k = k
            if last_prime is None:
                raise RuntimeError("Prime generator did not yield a value.")

            return last_prime

        return wrapper

    return decorator
