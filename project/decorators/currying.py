from typing import Callable, Any


def curry_explicit(function: Callable, arity: int) -> Callable:
    """
    Transforms a function into its curried version with a specified arity.

    A curried function allows partial application of arguments. When enough
    arguments (equal to the function's arity) are supplied, the function is
    executed. Otherwise, it returns another function that accepts the remaining arguments.

    Args:
        function (Callable): The function to be curried.
        arity (int): The number of arguments the function expects (its arity).

    Returns:
        Callable: A curried version of the input function.

    Raises:
        ValueError: If the arity is a negative number.
        TypeError: If too many arguments are supplied.
    """
    if arity < 0:
        raise ValueError("Arity must be a non-negative integer")

    def inner_curry(*args: Any) -> Any:
        if len(args) > arity:
            raise TypeError(
                f"Too many arguments: expected {arity}, but got {len(args)}"
            )

        if len(args) == arity:
            return function(*args)
        return lambda *args2: inner_curry(*(args + args2))

    return inner_curry


def uncurry_explicit(function: Callable, arity: int) -> Callable:
    """
    Transforms a curried function into its uncurried version with a specified arity.

    An uncurried function takes all its arguments at once, rather than one by one,
    as a curried function would.

    Args:
        function (Callable): The curried function to be uncurried.
        arity (int): The number of arguments the function expects (its arity).

    Returns:
        Callable: An uncurried version of the input curried function.

    Raises:
        ValueError: If the arity is a negative number or the number of arguments does not match.
        TypeError: If the provided arguments do not match the function's expectations.
    """
    if arity < 0:
        raise ValueError("Arity must be a non-negative integer")
    if arity == 0:
        return function()

    def inner_uncurry(*args: Any) -> Any:
        if len(args) != arity:
            raise ValueError(f"Expected {arity} arguments, but got {len(args)}")

        result = function
        for arg in args:
            result = result(arg)
        return result

    return inner_uncurry
