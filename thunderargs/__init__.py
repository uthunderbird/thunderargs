__author__ = 'thunder'
__version__ = '0.3.1a5'

from .errors import ValidationError, ArgumentRequired


class Arg(object):

    """
    Basic argument class
    """

    DEFAULT_SOURCE = None

    def __call__(self, value):
        return self.validated(value)

    def __init__(self, p_type=str, default=None, multiple=False, required=False,
                 validators=[], expander=None, suppress_expanding_check=False,
                 source=None, arg_name=None):

        if required and default is not None:
            raise ValueError("Argument can't have default value and be required at same time")

        if validators:
            for validator in validators:
                if not callable(validator):
                    raise ValueError("All validators must be callable")

        if expander and not (callable(expander) or type(expander) is dict):
            raise ValueError("Expander must be callable or dict")

        if validators and default:

            if multiple:
                for i, value in enumerate(default):
                    for j, validator in enumerate(validators):

                        if not isinstance(value, p_type) and not value == None:
                            raise ValueError("{} is not {} instance".format(value, p_type.__name__))

                        if not validator(value):
                            raise ValueError("Default value {} is not passed validator #{}".format(
                                value, j
                            ))
            else:

                if not isinstance(default, p_type):
                    raise ValueError("{} is not {} instance".format(default, p_type.__name__))

                for i, validator in enumerate(validators):
                    if not validator(default):
                        raise ValueError("Default value {} is not passed validator #{}".format(
                                default, i
                            ))

        self.type = p_type
        self.default = default
        self.multiple = multiple
        self.required = required
        self.validators = validators
        self.expander = expander
        self.check_expanding = not suppress_expanding_check
        self.source = source or self.DEFAULT_SOURCE
        self.__name__ = arg_name

    def _validate(self, value):
        """Perform conversion and validation on ``value``."""

        if not isinstance(value, self.type) and value is not None:
            try:
                typed_value = self.type(value)
            except TypeError:
                raise TypeError("Argument {} must be `{}`, not `{}`".format(self.__name__,
                                                                            self.type.__name__,
                                                                            type(value).__name__))

        elif value is None and self.default is not None:
            typed_value = self.default

        else:
            typed_value = value

        if self.validators and value is not None:
            for validator_no, validator in enumerate(self.validators):
                if not validator(typed_value):
                    template = getattr(validator, 'message',
                                       "Argument {arg_name} failed at validator #{validator_no}."
                                       "Given value: {value}")

                    error_class = getattr(validator, 'error_class', ValidationError)

                    error_code = getattr(validator, 'error_code', 10000)

                    opt = getattr(validator, 'opt', {})

                    raise error_class(message_template=template, error_code=error_code,
                                      arg_name=self.__name__, value=value,
                                      validator_no=validator_no, **opt)

        if self.expander:
            if isinstance(self.expander, dict):

                if not typed_value in self.expander and self.check_expanding:
                    raise KeyError("Can't find %s in expander" % typed_value)

                else:
                    return self.expander.get(typed_value)

            else:
                return self.expander(typed_value)

        return typed_value

    def validated(self, value):
        """
        Convert and validate the given value according to the ``p_type``
        Sets default if value is None
        """

        if self.multiple:
            if self.required and value == []:
                raise ArgumentRequired("Argument {} is required".format(self.__name__))
            return map(self._validate, value)

        if value is None:
            if self.required:
                raise ArgumentRequired("Argument {} is required".format(self.__name__))

        return self._validate(value)


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
            arg.__name__ = arg.__name__ or name

    def validated(self, args, dct):
        args = {k: v for k, v in zip(self.ordered_names, args)}
        for key, arg_instance in self.structure.items():
            if key in args:
                args[key] = arg_instance(args.get(key, None))
            else:
                dct[key] = arg_instance(dct.get(key, None))
        return [x[1] for x in sorted(args.items(), key=lambda x: self.ordered_names.index(x[0]))], dct
