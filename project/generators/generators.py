from typing import Generator, Tuple


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
        for a in range(0, 101, 2)
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
