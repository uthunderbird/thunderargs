from thunderargs import Arg
from thunderargs.endpoint import Endpoint
from thunderargs.args import IntArg


@Endpoint(x=Arg(int), y=Arg(int))
def max_int(x, y):
    return max(x,y)


@Endpoint(x=IntArg(greater_than=0, less_than=200, required=True), y=IntArg(in_range=range(50, 100), default=76))
def max_int_valid(x, y):
    """
    Returns maximal value
    """
    return max(x, y)
