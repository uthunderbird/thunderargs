from thunderargs import Arg
from thunderargs.endpoint import Endpoint
from thunderargs.validfarm import gt, val_in, lt


@Endpoint(x=Arg(int), y=Arg(int))
def max_int(x, y):
    return max(x,y)


@Endpoint(x=Arg(int, required=True, validators=[gt(0), lt(200)]), y=Arg(int, validators=[val_in([1,10,105,124])]))
def max_int_valid(x, y):
    return max(x, y)
