from thunderargs import Arg
from thunderargs.endpoint import Endpoint


@Endpoint
def max_int(x: Arg(int), y: Arg(int)):

    """
    You can use that, BUT you must use all params with keyword notation
    >>> max_int(x='4', y=9.0)

    if you call this function like this:
    >>> max_int('4', 9.0)

    then TypeError will be thrown.

    """

    return max(x,y)


from thunderargs.validfarm import val_gt, val_in, val_lt


@Endpoint
def max_int_valid(x: Arg(int, required=True, validators=[val_gt(0), val_lt(200)]),
                  y: Arg(int, validators=[val_in([1,10,105,124])])):
    return max(x,y)