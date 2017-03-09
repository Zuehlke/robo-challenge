# -*- coding: utf-8 -*-


def min(min_value):
    def min_decorator(func):
        def func_wrapper(self, value):
            if value < min_value:
                raise ValueError("{0} value is less than {1}".format(value, min_value))
            return func(self, value)
        return func_wrapper
    return min_decorator


def max(max_value):
    def max_decorator(func):
        def func_wrapper(self, value):
            if value > max_value:
                raise ValueError("{0} value is greater than {1}".format(value, max_value))
            return func(self, value)
        return func_wrapper
    return max_decorator


def check_int(func):
    def func_wrapper(self, value):
        if not isinstance(value, int):
            raise ValueError("{0} is not an integer".format(value))
        return func(self, value)
    return func_wrapper

