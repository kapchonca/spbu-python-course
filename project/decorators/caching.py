from functools import wraps
from collections import OrderedDict
from typing import Callable, Any, Tuple


def cache(max_size: int = 0) -> Callable[[Callable], Callable]:
    """
    Decorator for caching the results of a function with optional support for keyword arguments
    and a size limit on the cache.

    Args:
        max_size (int, optional): The maximum size of the cache. If 0, caching is disabled.
                                  If greater than 0, the oldest cache entry will be removed
                                  when the cache exceeds `max_size`.
                                  Defaults to 0 (no caching).

    Returns:
        function: The decorated function with caching applied.

    Raises:
        ValueError: If `max_size` is a negative number.
    """
    if max_size < 0:
        raise ValueError("max_size must be a non-negative integer")

    def cache_inner(function: Callable) -> Callable:
        """
        Internal function that manages the cache and its size.

        Args:
            function (Callable): The function whose results will be cached.

        Returns:
            Callable: A wrapper function that returns cached results or computes them if not cached.
        """
        cached: OrderedDict[Tuple[Any, frozenset], Any] = OrderedDict()

        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function for caching. Checks if the result is in the cache (using both positional
            and keyword arguments), otherwise computes the result and stores it in the cache.

            Args:
                *args: Positional arguments passed to the original function.
                **kwargs: Keyword arguments passed to the original function.

            Returns:
                Any: The result of the function (either from the cache or freshly computed).
            """
            cache_key: Tuple[Tuple[Any, ...], frozenset] = (
                args,
                frozenset(kwargs.items()),
            )

            if cache_key in cached:
                return cached[cache_key]

            if len(cached) == max_size and max_size > 0:
                cached.popitem(last=False)

            result = function(*args, **kwargs)
            if max_size > 0:
                cached[cache_key] = result

            return result

        return wrapper

    return cache_inner
