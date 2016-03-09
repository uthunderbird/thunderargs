from functools import reduce

from thunderargs.helpers import Nothing
from .errors import ValidationError, ArgumentRequired
from .transfarm import set_default_if_unset, Transformer
from .validfarm import Validator, type_is, type_in, neq

__author__ = 'thunder'
__version__ = '0.4.0a'


class BaseArg(object):

    def __call__(self, value):
        return self.validated(value)

    def __init__(self, validators=(), transform_before=(), transform_after=(), arg_name=None, safe=set()):

        if not all([isinstance(validator, Validator) for validator in validators]):
            raise TypeError("All validators should be `Validator` instances")

        if not all([isinstance(transformer, Transformer) for transformer in transform_before]) or\
           not all([isinstance(transformer, Transformer) for transformer in transform_after]):
            raise TypeError("All transformers should be callable")

        self.validators = validators
        self.transform_before = transform_before
        self.transform_after = transform_after
        self.arg_name = arg_name
        self.safe = safe
        self.configure_validators()

    def configure_validators(self):
        for number, validator in enumerate(self.validators):
            validator.arg_name = self.arg_name
            validator.validator_no = number

    def _validate(self, value):
        value = reduce(lambda x, y: y(x), filter(lambda x: x.is_acceptable(value), self.transform_before), value)
        if value in self.safe:
            return value
        if self.validators:
            for validator in self.validators:
                validator(value)
        value = reduce(lambda x, y: y(x), filter(lambda x: x.is_acceptable(value), self.transform_after), value)
        return value

    def validated(self, value):
        return self._validate(value)


class Arg(BaseArg):

    """
    Argument class
    """

    def __init__(self, expected_type_or_types=(str,), convert_to=None, default=Nothing, required=False,
                 validators=None, expander=None, safe=None, **kwargs):

        if required and default is not Nothing:
            raise ValueError("Argument can't have default value and be required at same time")

        if expander and not (callable(expander) or type(expander) is dict):
            raise ValueError("Expander must be callable or dict")

        if not validators:
            validators = []

        transform_before = []
        transform_after = []
        if safe is None:
            safe = set()

        if isinstance(expected_type_or_types, type):
            validators.insert(0, type_is(expected_type_or_types))
        elif isinstance(expected_type_or_types, (list, tuple)):
            validators.insert(0, type_in(expected_type_or_types))
        elif expected_type_or_types is not None:
            raise TypeError("You should specify expected types or set it to None")

        self.acceptable = expected_type_or_types

        if default is not Nothing:
            transform_before.append(set_default_if_unset(default))
            safe.add(default)

        if convert_to is not None:
            transform_before.append(Transformer(convert_to, lambda x: not isinstance(x, convert_to)))

        if required:
            validators.insert(0, neq(Nothing, ArgumentRequired))

        if isinstance(expander, dict):
            transform_after.append(Transformer(lambda x: expander.__getitem__))
        elif callable(expander):
            transform_after.append(Transformer(expander))
        elif expander is not None:
            raise TypeError("Expander should be callable or dict")

        super().__init__(validators, transform_before, transform_after, safe=safe, **kwargs)


class Parser(object):

    def __call__(self, args, kwargs):
        """
        Just for simplify
        """
        return self.validated(args, kwargs)

    def __init__(self, structure, ordered_names):
        self.structure = structure
        self.ordered_names = ordered_names
        for name, arg in structure.items():
            arg.arg_name = arg.arg_name or name

    def prepare_hints(self):
        return {k: v.acceptable for k, v in self.structure.items()}

    def validated(self, args, dct):
        args = dict(zip(self.ordered_names, args))
        for key, arg_instance in self.structure.items():
            if key in args:
                args[key] = arg_instance(args.get(key, Nothing))
            else:
                dct[key] = arg_instance(dct.get(key, Nothing))
        return [x[1] for x in sorted(args.items(), key=lambda x: self.ordered_names.index(x[0]))], dct
