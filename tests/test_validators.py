import pytest

from thunderargs.validfarm import Validator, len_gt, ValidationError


def test_basic():
    validator = Validator(lambda x: 5 < x < 100)
    print(validator)
    assert validator(10) is None
    with pytest.raises(ValidationError):
        validator(4)
        validator(1000)
    assert validator(99) is None


def test_fabric_and_exception():
    len_gt_5 = len_gt(5)
    try:
        len_gt_5('lol')
    except ValidationError as e:
        assert e.opt['min_len'] == 5
    assert len_gt_5('asdfqq') is None

