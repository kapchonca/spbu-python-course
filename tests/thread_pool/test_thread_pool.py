from time import sleep
from threading import Thread, active_count
from typing import Any
import pytest
from project.thread_pool.thread_pool import ThreadPool, WrapFunction


def test_task_result() -> None:
    """Test that WrapFunction correctly sets and awaits a result."""

    def set_five() -> int:
        return 5

    task = WrapFunction(set_five)

    t = Thread(target=task)
    t.start()
    t.join()

    # Await the result
    assert task.get_result() == 5


def test_enqueue_task() -> None:
    """Test that tasks are correctly enqueued and processed."""
    pool = ThreadPool(2)

    def sample_task() -> str:
        return "Task completed"

    task = pool.enqueue(sample_task)

    # Await the task completion and check the result
    result = task.get_result()
    assert result == "Task completed"

    # Clean up thread pool
    pool.dispose()


def test_enqueue_for_task_with_parameters() -> None:
    """Test that tasks are correctly enqueued and processed."""
    pool = ThreadPool(2)

    def task1(x: str, y: int):
        return x, y

    def task2(a: Any) -> Any:
        return a

    task_1 = pool.enqueue(task1, "abc", 123)
    task_2 = pool.enqueue(task2, None)

    # Await the task completion and check the result
    result1 = task_1.get_result()
    assert result1 == ("abc", 123)
    result2 = task_2.get_result()
    assert result2 is None

    # Clean up thread pool
    pool.dispose()


def test_enqueue_for_built_in_functions() -> None:
    """Test that built-in functions are correctly enqueued and processed."""
    pool = ThreadPool(2)

    task_1 = pool.enqueue(pow, 2, 10)
    task_2 = pool.enqueue(sum, [1, 2, 3, 4])

    # Await the task completion and check the result
    result1 = task_1.get_result()
    assert result1 == 1024
    result2 = task_2.get_result()
    assert result2 == 10

    # Clean up thread pool
    pool.dispose()


def test_ordered_execution_with_one_threads() -> None:
    """Test that tasks are executed in the order they were enqueued."""
    pool = ThreadPool(1)  # Single thread to ensure order

    results = []

    def task1() -> None:
        results.append(1)

    def task2() -> None:
        results.append(2)

    task_1 = pool.enqueue(task1)
    task_2 = pool.enqueue(task2)

    # Wait for tasks to complete
    task_1.get_result()
    task_2.get_result()

    # Ensure the tasks were executed in order
    assert results == [1, 2]

    # Clean up thread pool
    pool.dispose()


def test_ordered_execution_with_multiple_threads() -> None:
    """Test that the order is followed to perform tasks on multiple threads."""
    pool = ThreadPool(2)

    results = []

    def task1() -> None:
        results.append(1)

    def task2() -> None:
        sleep(1)
        results.append(2)

    def task3() -> None:
        results.append(3)

    t1 = pool.enqueue(task1)
    t2 = pool.enqueue(task2)
    t3 = pool.enqueue(task3)

    # Wait for tasks to complete and check the result
    t1.get_result()
    t2.get_result()
    t3.get_result()
    assert results == [1, 3, 2]

    # Clean up thread pool
    pool.dispose()


def test_that_cannot_add_task_after_dispose() -> None:
    """Test that after dispose a thread cannot add a task."""
    pool = ThreadPool(2)

    # Clean up thread pool
    pool.dispose()

    # Attempt to add a task
    with pytest.raises(RuntimeError):
        pool.enqueue(sum, [1, 2, 3])


def test_for_the_number_of_threads() -> None:
    """Test that cannot create a thread pool with a non-sufficient number of threads."""
    with pytest.raises(ValueError):
        ThreadPool(0)
        ThreadPool(-1)


def test_thread_count() -> None:
    """
    Test case to verify the correct number of active threads in the pool.
    Ensures that the pool has the same number of active threads as specified.
    """
    initial_active_threads = active_count()  # Count initial active threads
    pool = ThreadPool(4)  # Create a thread pool with 5 threads
    current_active_threads = active_count()  # Count current active threads

    # Pool threads
    active_threads_in_pool = current_active_threads - initial_active_threads

    assert active_threads_in_pool == 4
    pool.dispose()
