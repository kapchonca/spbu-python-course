from copy import deepcopy
from inspect import signature
from typing import Any, Callable


class Isolated:
    """Marker class to indicate that the argument should be deeply copied."""

    pass


class Evaluated:
    """
    Wrapper class that ensures the function passed is evaluated
    when called. Raises a TypeError if an Isolated class is passed to it.
    """

    def __init__(self, function: Callable[..., Any]) -> None:
        """
        Initialize with a function. Raises an error if the function
        is an instance of the Isolated class.

        Args:
            function: A callable to be wrapped.

        Raises:
            TypeError: If the function is an instance of Isolated.
        """
        if isinstance(function, Isolated):
            raise TypeError("Oops! Cannot mix Evaluated and Isolated classes")
        self.function = function

    def __call__(self) -> Any:
        """
        Call the wrapped function.

        Returns:
            The result of the function call.
        """
        return self.function()


def smart_args(function: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that processes the arguments passed to the function, handling
    special behavior for Isolated and Evaluated instances.

    For arguments marked as Isolated, they are deeply copied.
    For arguments marked as Evaluated, the wrapped function is called.

    Args:
        function: The function to be wrapped.

    Returns:
        The wrapped function with smart argument processing.
    """

    def wrapper(**kwargs: Any) -> Any:
        """
        Processes the arguments of the wrapped function, ensuring deep copying
        for Isolated and evaluation for Evaluated arguments.

        Args:
            kwargs: Keyword arguments to pass to the wrapped function.

        Raises:
            ValueError: If an argument marked as Isolated is not provided.

        Returns:
            The result of the wrapped function.
        """
        sign = signature(function)

        for key, value in sign.parameters.items():
            if isinstance(value.default, Isolated):
                if key not in kwargs:
                    raise ValueError(
                        f"Argument '{key}' must be provided when using Isolated()"
                    )
                kwargs[key] = deepcopy(kwargs[key])
            if isinstance(value.default, Evaluated):
                if key not in kwargs:
                    kwargs[key] = value.default()

        return function(**kwargs)

    return wrapper
