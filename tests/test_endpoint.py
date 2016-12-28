import operator

import pytest

from thunderargs import Arg, ArgumentRequired
from thunderargs.endpoint import Endpoint, annotate

OPERATION = {'+': operator.add,
             '-': operator.sub,
             '*': operator.mul,
             '^': pow}


def test_basic():
    @Endpoint
    @annotate(x=Arg(int), y=Arg(int), op=Arg(expander=OPERATION.get))
    def calc(x, y, op):
        return op(x, y)
    assert calc(x=5, y=6, op='+') == 11


def test_basic_ordered():
    @Endpoint
    @annotate(x=Arg(int), y=Arg(int), op=Arg(expander=OPERATION.get))
    def calc(x, y, op):
        return op(x, y)
    assert calc(5, 6, '*') == 30


def test_basic_mixed():
    @Endpoint
    @annotate(x=Arg(int), y=Arg(int), op=Arg(expander=OPERATION.get))
    def calc(x, y, op):
        return op(x, y)
    assert calc(5, 6, op='*') == 30


def test_default():
    @Endpoint
    @annotate(x=Arg(int, default=2), y=Arg(int, default=2), op=Arg(expander=OPERATION.get))
    def calc(x, y, op):
        return op(x, y)
    assert calc(5, 6, op='+') == 11
    assert calc(op='+') == 4


def test_required():
    @Endpoint
    @annotate(x=Arg(int, required=True), y=Arg(int, required=True), op=Arg(expander=OPERATION.get, default="+"))
    def calc(x, y, op):
        return op(x, y)
    assert calc(5, 6, op='*') == 30
    with pytest.raises(ArgumentRequired):
        calc(op='+')


def test_direct_structure_pass():
    @Endpoint(x=Arg(int, required=True), y=Arg(int, required=True), op=Arg(expander=OPERATION.get, default="+"))
    def calc(x, y, op):
        return op(x, y)
    assert calc(5, 6, op='*') == 30
    with pytest.raises(ArgumentRequired):
        calc(op='+')
