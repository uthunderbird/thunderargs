from . import Arg
from .validfarm import lt, gt, val_in
from .errors import WrongArgumentConfiguration, NotImplemented


class BasicNumberArg(Arg):

    _type = (int, float)
    _convert_to = None

    def __init__(self, less_than=None, greater_than=None, in_range=None, **kwargs):

        if in_range is not None and (less_than is not None or greater_than is not None):
            raise WrongArgumentConfiguration("If you want to specify range, you should"
                                             "specify neither greater_than nor less_than")

        kwargs['convert_to'] = self._convert_to

        validators = kwargs.setdefault('validators', [])

        if in_range is not None:
            if isinstance(in_range, range):
                validators.append(val_in(in_range))
            elif (isinstance(in_range, list) or isinstance(in_range, tuple)) and len(in_range) == 2:
                greater_than = in_range[0]
                less_than = in_range[1]

        if less_than is not None:
            assert isinstance(less_than, self._type), "less_than should be {type}".format(type=self._type_name())
            validators.append(lt(less_than))
        if greater_than is not None:
            assert isinstance(greater_than, self._type), "greater_than should be {type}".format(type=self._type_name())
            validators.append(gt(greater_than))

        super().__init__(self._type, **kwargs)

    def _type_name(self):
        return self._type.__name__ or self._type


class IntArg(BasicNumberArg):
    _convert_to = int


class FloatArg(BasicNumberArg):
    _convert_to = float


class NumberArg(BasicNumberArg):
    pass