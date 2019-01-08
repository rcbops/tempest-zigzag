from __future__ import absolute_import
import functools


def lazy_load(attribute_name, exceptions=(), value_on_exception=None, initial_value=None):
    def decorator_lazy_load(func):
        @functools.wraps(func)
        def wrapper_lazy_load(self, *args, **kwargs):
            try:
                if getattr(self, attribute_name) is initial_value:
                    setattr(self, attribute_name, func(self, *args, **kwargs))
            except tuple(exceptions):
                setattr(self, attribute_name, value_on_exception)
            return getattr(self, attribute_name)
        return wrapper_lazy_load
    return decorator_lazy_load
