import operator

import pytest

from thunderargs import Arg
from thunderargs.endpoint import Endpoint

OPERATION = {'+': operator.add,
             '-': operator.sub,
             '*': operator.mul,
             '^': pow}


def test_basic():
    @Endpoint
    def calc(x: Arg(int), y: Arg(int), op: Arg(expander=OPERATION.get)):
        return op(x, y)
    assert calc(x=5, y=6, op='+') == 11


def test_basic_ordered():
    @Endpoint
    def calc(x: Arg(int), y: Arg(int), op: Arg(expander=OPERATION.get)):
        return op(x, y)
    assert calc(5, 6, '*') == 30
