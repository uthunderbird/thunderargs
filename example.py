from thunderargs import Arg
from thunderargs.endpoint import Endpoint


@Endpoint(x=Arg(int), y=Arg(int))
def max_int(x, y):

    """
    You can use that, BUT you must use all params with keyword notation
    >>> max_int(x='4', y=9.0)

    if you call this function like this:
    >>> max_int('4', 9.0)

    then TypeError will be thrown.

    """

    return max(x,y)


from thunderargs.validfarm import gt, val_in, lt


@Endpoint(x=Arg(int, required=True, validators=[gt(0), lt(200)]), y=Arg(int, validators=[val_in([1,10,105,124])]))
def max_int_valid(x, y):
    return max(x, y)
