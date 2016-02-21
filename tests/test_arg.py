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

