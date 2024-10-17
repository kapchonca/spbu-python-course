import pytest
from project.decorators.smart_args import Isolated, Evaluated, smart_args


def call_counter():
    """
    Function that counts the number of its own calls.
    """
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter


def test_combination_isolated_evaluated():
    # Checking that Evaluated cannot be called from Isolated and vice versa
    with pytest.raises(TypeError):
        Isolated(Evaluated(call_counter()))
    with pytest.raises(TypeError):
        Evaluated(Isolated())


def test_only_kwargs_isolation():
    @smart_args
    def check_isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    no_mutable = {"a": 10}
    # Checking that no_mutable has not changed during transmission via Isolated()
    assert check_isolation(d=no_mutable) == {"a": 0}
    assert no_mutable == {"a": 10}


def test_only_kwargs_evaluated():
    counter_function = call_counter()

    @smart_args
    def check_evaluation(*, x=counter_function(), y=Evaluated(counter_function)):
        return x, y

    # Checking that Evaluated is triggered without passing an argument
    res1 = check_evaluation()
    res2 = check_evaluation()

    assert res1[0] == 1
    assert res1[1] == 2  # Evaluated calls the function during decoration
    assert res2[0] == 1  # Stored result from the first call
    assert res2[1] == 3  # Also calls the function during decoration


def test_only_kwargs_isolated_evaluation():
    counter_function = call_counter()

    @smart_args
    def check_isolated_evaluation(*, x=Isolated(), y=Evaluated(counter_function)):
        x["a"] = 0
        return x, y

    # Checking that Evaluated and Isolated can be parameters of the same function
    no_mutable = {"a": 10}
    res1 = check_isolated_evaluation(x=no_mutable)
    res2 = check_isolated_evaluation(x=no_mutable, y=150)

    assert res1[0] == {"a": 0}
    assert no_mutable == {"a": 10}
    assert res2[1] == 150
