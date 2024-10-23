import threading
from typing import Any, Callable, List, Optional


class WrapFunction:
    """
    Wraps a function with its arguments, allowing for threaded execution and result retrieval.

    Attributes:
        _completed (threading.Event): An event to indicate task completion.
        _func (Callable): The function wrapped with bound arguments.
        _res (Optional[Any]): The result of executing the wrapped function.
    """

    def __init__(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        """
        Initializes the WrapFunction with a function and its arguments.

        Args:
            func (Callable): The function to wrap.
            *args (Any): Positional arguments for the function.
            **kwargs (Any): Keyword arguments for the function.
        """
        self._completed = threading.Event()
        self._func = self._bind_arguments(func, *args, **kwargs)
        self._res: Optional[Any] = None

    @staticmethod
    def _bind_arguments(func: Callable, *args: Any, **kwargs: Any) -> Callable:
        """
        Binds arguments to the given function.

        Args:
            func (Callable): The function to bind arguments to.
            *args (Any): Positional arguments to bind.
            **kwargs (Any): Keyword arguments to bind.

        Returns:
            Callable: A new function with bound arguments.
        """

        def bound_function(*inner_args: Any, **inner_kwargs: Any) -> Any:
            return func(*args, *inner_args, **kwargs, **inner_kwargs)

        return bound_function

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """
        Executes the wrapped function and sets the completion event.

        Args:
            *args (Any): Positional arguments for the function call.
            **kwargs (Any): Keyword arguments for the function call.
        """
        self._res = self._func(*args, **kwargs)
        self._completed.set()

    def get_result(self) -> Any:
        """
        Waits for the function execution to complete and retrieves the result.

        Returns:
            Any: The result of the function execution.
        """
        self._completed.wait()
        return self._res


class ThreadPool:
    """
    A thread pool for managing concurrent execution of tasks.

    Attributes:
        _threads (List[threading.Thread]): The list of threads in the pool.
        _tasks (List[WrapFunction]): The list of tasks to be executed.
        _lock (threading.Lock): A lock for synchronizing access.
        _condition (threading.Condition): A condition for task availability.
        _disposed (bool): Indicates if the pool has been disposed.
    """

    def __init__(self, num_threads: int) -> None:
        """
        Initializes the ThreadPool with a specified number of threads.

        Args:
            num_threads (int): The number of threads to create in the pool.

        Raises:
            ValueError: If the number of threads is less than 1.
        """
        if num_threads < 1:
            raise ValueError("Number of threads cannot be less than 1")
        self._threads: List[threading.Thread] = []
        self._tasks: List[WrapFunction] = []
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._disposed = False
        self._create_threads(num_threads)

    def _worker(self) -> None:
        """
        The worker function for threads, which waits for tasks and executes them.
        """
        while True:
            with self._condition:
                if len(self._tasks) == 0 and not self._disposed:
                    self._condition.wait()
                if self._disposed:
                    break
                task_func = self._tasks.pop(0)
            try:
                print(
                    f"Thread {threading.current_thread().ident} has received a notification and is performing the task {task_func}"
                )
                task_func()
                print(
                    f"Thread {threading.current_thread().ident} has completed working on the task"
                )
            except Exception as e:
                print(
                    f"Thread {threading.current_thread().ident} encountered an exception: {e}"
                )

    def _create_threads(self, num_thread: int) -> None:
        """
        Creates and starts the specified number of threads in the pool.

        Args:
            num_thread (int): The number of threads to create.
        """
        for _ in range(num_thread):
            thread = threading.Thread(target=self._worker)
            self._threads.append(thread)
            thread.start()

    def enqueue(self, func: Callable, *args: Any, **kwargs: Any) -> WrapFunction:
        """
        Enqueues a function with its arguments to be executed by a thread.

        Args:
            func (Callable): The function to enqueue.
            *args (Any): Positional arguments for the function.
            **kwargs (Any): Keyword arguments for the function.

        Returns:
            WrapFunction: The wrapped function that can be used to retrieve results.

        Raises:
            RuntimeError: If attempting to enqueue tasks after disposal.
        """
        if self._disposed:
            raise RuntimeError(
                "Cannot enqueue tasks after thread pool has been disposed."
            )
        wrapped_func = WrapFunction(func, *args, **kwargs)
        with self._condition:
            self._tasks.append(wrapped_func)
            self._condition.notify()
        return wrapped_func

    def dispose(self) -> None:
        """
        Disposes the thread pool, stopping all threads and cleaning up resources.
        """
        with self._condition:
            self._disposed = True
            self._condition.notify_all()
        for th in self._threads:
            th.join()
