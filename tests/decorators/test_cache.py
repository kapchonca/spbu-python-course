import pytest
from unittest.mock import Mock
from project.decorators.caching import cache


def test_cache_fibonacci():
    @cache(max_size=3)
    def fibonacci(n):
        if n < 2:
            return n
        result = fibonacci(n - 1) + fibonacci(n - 2)
        return result

    # Calling the fibonacci function to check the caching of results
    for i in range(0, 2000):
        fibonacci(i)

    fibonacci(1999)
    fibonacci(1998)
    fibonacci(1997)
    # Checking for RecursionError when calling fibonacci with an uncached number
    with pytest.raises(RecursionError):
        fibonacci(3000)
    with pytest.raises(RecursionError):
        fibonacci(1996)


def test_no_cache_calls():
    """Test the function is called every time if caching is disabled (max_size=0)."""
    mock_func = Mock(side_effect=lambda x: x * 2)

    @cache()
    def cached_func(*args, **kwargs):
        return mock_func(*args, **kwargs)

    # Call the function multiple times with the same arguments
    cached_func(2)
    cached_func(2)
    cached_func(3)

    # The function should be called every time
    assert mock_func.call_count == 3


def test_cache_calls_with_limit():
    """Test the function is called fewer times when caching is enabled."""
    mock_func = Mock(side_effect=lambda x: x * 2)

    @cache(max_size=2)
    def cached_func(*args, **kwargs):
        return mock_func(*args, **kwargs)

    # Call the function with the same arguments
    cached_func(2)
    cached_func(2)
    cached_func(3)
    cached_func(2)  # This should hit the cache

    # The function should be called only twice, because the second call to 2 should hit the cache
    assert mock_func.call_count == 2


def test_cache_eviction():
    """Test that cache evicts the oldest entry when max_size is exceeded."""
    mock_func = Mock(side_effect=lambda x: x * 2)

    @cache(max_size=2)
    def cached_func(*args, **kwargs):
        return mock_func(*args, **kwargs)

    # Call the function with different arguments to fill the cache
    cached_func(2)  # Called, added to cache
    cached_func(3)  # Called, added to cache
    cached_func(4)  # Called, added to cache, evicts the (2,)
    cached_func(2)  # Cache miss, should call again

    # Since the cache size is 2, the first call to 2 should be evicted when 4 is added
    assert mock_func.call_count == 4


def test_cache_with_kwargs():
    """Test the function caching works correctly with keyword arguments."""
    mock_func = Mock(side_effect=lambda x: x * 2)

    @cache(max_size=2)
    def cached_func(*args, **kwargs):
        return mock_func(*args, **kwargs)

    cached_func(x=5)  # Called, added to cache
    cached_func(x=5)  # Cache hit, should not call again
    cached_func(x=6)  # Called, added to cache

    # Since both calls with x=5 should cache, the function should be called only twice
    assert mock_func.call_count == 2
