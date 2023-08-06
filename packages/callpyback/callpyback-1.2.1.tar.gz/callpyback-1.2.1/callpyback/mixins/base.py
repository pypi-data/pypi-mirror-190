"""Module containing BaseCallBackMixin implementation"""

import inspect
import threading

from callpyback.utils import _default_callback

CALLBACK_LABELS = ("on_call", "on_success", "on_failure", "on_end")
CALLBACK_PARAMETER_MAP = {
    "on_call": {"func", "func_kwargs"},
    "on_success": {"func", "func_result", "func_kwargs"},
    "on_failure": {"func", "func_exception", "func_kwargs"},
    "on_end": {
        "func",
        "func_result",
        "func_exception",
        "func_kwargs",
        "func_scope_vars",
    },
}


class BaseCallBackMixin:
    """Class implementing basic callback features.

    Attributes:
        N/A

    Methods:
        validate_callbacks():
            Validates callbacks passed to class constructor.
        run_callback_func(func, func_kwargs):
            Executes given callback function with given kwargs.
        run_on_call_func(func, func_args, func_kwargs):
            Generates kwargs for given `on_call` callback function and executes
            it with generated kwargs.
        run_on_success_func(func, func_result, func_args, func_kwargs):
            Generates kwargs for given `on_success` callback function and
            executes it with generated kwargs.
        run_on_failure_func(func, func_exception, func_args, func_kwargs):
            Generates kwargs for given `on_failure` callback function and
            executes it with generated kwargs.
        run_on_end_func(func, func_result, func_exception, func_args,
        func_kwargs, func_scope_vars):
            Generates kwargs for given `on_end` callback function and executes
            it with generated kwargs.
        get_callback_kwargs(callback, **kwargs):
            Generates kwargs for given callback function.

    """

    def __init__(
        self,
        on_call=_default_callback,
        on_success=_default_callback,
        on_failure=_default_callback,
        on_end=_default_callback,
        **kwargs,
    ):
        """Class constructor. Sets instance variables.

        Args:
            on_call (Callable, optional): Called before execution.
                Defaults to DEFAULT_ON_CALL_LAMBDA.
            on_success (Callable, optional): Called after success.
                Defaults to DEFAULT_ON_SUCCESS_LAMBDA.
            on_failure (Callable, optional): Called after failed execution.
                Defaults to DEFAULT_ON_FAILURE_LAMBDA.
            on_end (Callable, optional): Called after execution.
                Defaults to DEFAULT_ON_END_LAMBDA.

        Returns:
            BaseCallBackMixin: mixin instance
        Raises:
            N/A
        """
        super().__init__(**kwargs)
        self.on_call = on_call
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_end = on_end
        self.callbacks = (
            self.on_call,
            self.on_success,
            self.on_failure,
            self.on_end,
        )

    def validate_callbacks(self):
        """Validates callbacks passed to class constructor.

        Executes following checks:
            1. Callback must be a Callable type.
            2. Callback cannot be an async coroutine.
            3. Callback must accepted some or none of the parameters specified
               in CALLBACK_PARAMETER_MAP.

        Args:
            N/A
        Returns:
            None
        Raises:
            TypeError: Raised if one of the callbacks is not Callable.
            TypeError: Raised if one of the callbacks is an async coroutine.
            AssertionError: Raised if any callbacks haves invalid parameters.
        """
        for callback_name, callback in zip(CALLBACK_LABELS, self.callbacks):
            if not callable(callback):
                raise TypeError("Callback must be a callable.")
            if inspect.iscoroutinefunction(callback):
                raise TypeError(
                    f"Callback `{callback.__name__}` cannot be a coroutine."
                )
            self.validate_callback_parameters(callback, callback_name)

    def validate_callback_parameters(self, callback, callback_name):
        """Validates callback parameters to be accepted by the callback.

        Args:
            callback (func): callback function.
            callback_name (str): name of the callback function.
        Returns:
            None
        Raises:
            AssertionError: Raised if some callback parameters are invalid.
        """
        found_params = sorted(inspect.signature(callback).parameters)
        expected_params = sorted(CALLBACK_PARAMETER_MAP[callback_name])
        if not set(found_params).issubset(set(expected_params)):
            raise AssertionError(
                f"Signature of callback `{callback_name}` is invalid.\n"
                f"Expected: No parameter or combination of: "
                f"{','.join(expected_params)}.\n"
                f"Found: {','.join(found_params)}."
            )

    def run_callback_func(self, func, func_kwargs):
        """Executes given callback function with given kwargs.
        If callback function was decorated with a `@backgroung_callback`,
        function is executed on a new thread in the background.

        Args:
            func (Callable): Callback function to be executed.
            func_kwargs (dict): Keyword arguments to be passed to the callback.
        Returns:
            None
        Raises:
            N/A
        """
        if hasattr(func, "__background_callpyback__"):
            task = threading.Thread(target=func, args=(), kwargs=func_kwargs)
            task.start()
        else:
            func(**func_kwargs)

    def run_on_call_func(self, func, func_kwargs):
        """Generates kwargs for given `on_call` callback function and executes
        it with generated kwargs.

        Args:
            func (func): decorated function
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_call_kwargs = self.get_callback_kwargs(
            callback=self.on_call, func=func, func_kwargs=func_kwargs
        )
        self.run_callback_func(self.on_call, on_call_kwargs)

    def run_on_success_func(self, func, func_result, func_kwargs):
        """Generates kwargs for given `on_success` callback function and
        executes it with generated kwargs.

        Args:
            func (func): decorated function
            func_result (Any): Result of the decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_success_kwargs = self.get_callback_kwargs(
            callback=self.on_success,
            func=func,
            func_result=func_result,
            func_kwargs=func_kwargs,
        )
        self.run_callback_func(self.on_success, on_success_kwargs)

    def run_on_failure_func(self, func, func_exception, func_kwargs):
        """Generates kwargs for given `on_failure` callback function and
        executes it with generated kwargs.

        Args:
            func (func): decorated function
            func_exception (Exception): Exception raised by decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_failure_kwargs = self.get_callback_kwargs(
            callback=self.on_failure,
            func=func,
            func_exception=func_exception,
            func_kwargs=func_kwargs,
        )
        self.run_callback_func(self.on_failure, on_failure_kwargs)

    def run_on_end_func(
        self, func, func_result, func_exception, func_kwargs, func_scope_vars
    ):
        """Generates kwargs for given `on_end` callback function and executes
        it with generated kwargs.

        Args:
            func (func): decorated function
            func_result (Any): Result of the decorated function.
            func_exception (Exception): Exception raised by decorated function.
            func_kwargs (dict): Keyword arguments for the decorated function.
            func_scope_vars (dict): Scope variables for the decorated function.
        Returns:
            None
        Raises:
            N/A
        """
        on_end_kwargs = self.get_callback_kwargs(
            callback=self.on_end,
            func=func,
            func_result=func_result,
            func_exception=func_exception,
            func_kwargs=func_kwargs,
            func_scope_vars=func_scope_vars,
        )
        self.run_callback_func(self.on_end, on_end_kwargs)

    def get_callback_kwargs(self, callback, **kwargs):
        """Generates kwargs for given callback function.
        Only kwargs specified in callback signature will be passed to callback.
        This is to allow omitting unused parameters in user created callbacks.

        Args:
            kwargs (dict): Decorated function keyword arguments.

        Returns:
            dict: Callback function keyword arguments.
        """
        callback_kwargs = {}
        params = inspect.signature(callback).parameters
        for kwarg_name, kwarg_value in kwargs.items():
            if kwarg_name in params:
                callback_kwargs[kwarg_name] = kwarg_value
        return callback_kwargs
