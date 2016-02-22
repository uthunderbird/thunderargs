import pytest
from thunderargs import Arg, Nothing, ArgumentRequired


def test_type():
    assert Arg().validated(4) == '4'
    assert Arg(float).validated(2) == 2.0


def test_default():
    assert Arg(default="Lol").validated(Nothing) == "Lol"
    arg = Arg(int, default=10)
    assert arg.validated(4) == 4
    assert arg.validated(Nothing) == 10
    assert Arg(default=None).validated(Nothing) is None


def test_required():
    # Argument can't be required and contain default value, it's just meanless
    with pytest.raises(ValueError):
        Arg(default="Lol", required=True)

    with pytest.raises(ArgumentRequired):
        Arg(required=True).validated(Nothing)

    assert Arg(required=True).validated("asdf") == 'asdf'
    assert Arg(required=True).validated(None) is None

    # with pytest.raises(TypeError):
    #     Arg(required=True).validated(4)
