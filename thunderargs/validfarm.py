__author__ = 'thunder'

from .errors import customize_error


def len_gt(x):

    @customize_error("Length of `{arg_name}` must be at least {min_len}", min_len=x+1)
    def validator(val
    ue):
        return len(value) > x

    return validator


def len_lt(x):

    @customize_error("Length of `{arg_name}` must be less than {max_len}", max_len=x)
    def validator(value):
        return len(value) < x

    return validator


def len_eq(x):

    @customize_error("Length of `{arg_name}` must be {_len} symbols", _len=x)
    def validator(value):
        return len(value) == x

    return validator


def len_neq(x):

    @customize_error("Length of `{arg_name}` must be NOT {_len} symbols", _len=x)
    def validator(value):
        return len(value) != x

    return validator


def val_gt(x):

    @customize_error("Value of `{arg_name}` must be at least {max_val}", max_val=x+1)
    def validator(value):
        return value > x

    return validator


def val_lt(x):

    @customize_error("Value of `{arg_name}` must be less than {min_val}", min_val=x)
    def validator(value):
        return value < x

    return validator


def val_neq(x):

    @customize_error("Value of `{arg_name}` can't be {value}", max_len=x+1)
    def validator(value):
        return value != x

    return validator


def val_in(x):

    @customize_error("Value of `{arg_name}` must be in {possible_values}", possible_values=x)
    def validator(value):
        return value in x

    return validator


def val_nin(x):

    @customize_error("Value of `{arg_name}` can't be in {impossible_values}", impossible_values=x)
    def validator(value):
        return not value in x

    return validator