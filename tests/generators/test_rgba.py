import pytest
from project.generators.generators import get_rgba_gen, get_ith_colour


@pytest.mark.parametrize(
    "index, expected_rgba",
    [
        (1, (0, 0, 0, 0)),
        (2, (0, 0, 0, 2)),
        (52, (0, 0, 1, 0)),
    ],
)
def test_get_rgba_gen_indexed(index, expected_rgba):
    """Test the RGBA generator at specific indices."""
    rgba_gen = get_rgba_gen()
    for _ in range(index - 1):
        next(rgba_gen)
    assert next(rgba_gen) == expected_rgba


@pytest.mark.parametrize(
    "index, expected_rgba",
    [
        (1, (0, 0, 0, 0)),
        (161024, (0, 12, 85, 32)),
        (-1, IndexError),
        (10e8, IndexError),
    ],
)
def test_get_ith_colour(index, expected_rgba):
    """Test the getter of i-th element at specific indices."""
    if isinstance(expected_rgba, type) and issubclass(expected_rgba, Exception):
        with pytest.raises(expected_rgba):
            get_ith_colour(index)
    else:
        assert get_ith_colour(index) == expected_rgba
