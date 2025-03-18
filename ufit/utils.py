from functools import wraps
import inspect
import time
import bpy


def ensure_mode(mode: bpy.ops._ModuleType) -> bool:
    """
    Ensure that the current mode is the given mode.
    If the current mode is not the given mode, switch to the given mode.

    :param mode: The mode to ensure.
    :return: True if the mode was changed, False otherwise.
    """
    if bpy.context.mode != mode:
        bpy.ops.object.mode_set(mode=mode)
        return True
    return False


class ThrottleDecorator:
    """
    Decorator that limits how often a function can be called.
    Only executes the function if enough time has passed since the last call.
    """
    def __init__(self, func, interval: float):
        self.func = func
        self.interval = interval
        self.last_run = 0

        # Get function signature information
        self.signature = inspect.signature(func)
        self.params = list(self.signature.parameters.keys())

    def _prepare_args(self, args, kwargs):
        """Prepare arguments according to function signature"""
        try:
            bound_args = self.signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            return bound_args.args, bound_args.kwargs
        except TypeError as e:
            if len(args) > len(self.params):
                args = args[:len(self.params)]
                return self._prepare_args(args, kwargs)
            raise e

    def __call__(self, *args, **kwargs):
        now = time.time()
        delta = now - self.last_run

        # Prepare current arguments
        args, kwargs = self._prepare_args(args, kwargs)

        # If enough time has passed, execute immediately
        if delta >= self.interval:
            self.last_run = now
            return self.func(*args, **kwargs)


def throttle(interval: float):
    def apply_decorator(func):
        decorator = ThrottleDecorator(func=func, interval=interval)
        return wraps(func)(decorator)
    return apply_decorator
