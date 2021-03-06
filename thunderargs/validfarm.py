from .errors import ValidationError


class Validator(object):

    default_error_message_template = "Validation was failed in validator #{validator_no} on value `{value}`"
    default_error_class = ValidationError
    validator_no = "<UNKNOWN>"
    arg_name = "<UNSPECIFIED>"

    def __init__(self, expression, error_message_template=None, error_class=None, description_template=None, **opt):
        self.expression = expression
        self.error_message_template = error_message_template or self.default_error_message_template
        self.error_class = error_class or self.default_error_class
        if not description_template:
            if error_message_template:
                description_template = error_message_template
            else:
                description_template = "<UNDESCRIBED VALIDATOR>"
        self.description_template = description_template
        self.opt = opt

    def __call__(self, value):
        if not self.expression(value):
            self.raise_exception(value=value)

    def raise_exception(self, *args, **kwargs):
        kwargs.update(self.opt)
        kwargs['validator_no'] = self.validator_no
        kwargs['arg_name'] = self.arg_name
        raise self.error_class(self.error_message_template, *args, **kwargs)

    def get_description(self):
        return self.description_template.format(arg_name=self.arg_name, **self.opt)


def validator(*args, **kwargs):
    def decorator(func):
        return Validator(func, *args, **kwargs)
    return decorator


def len_gt(x):
    return Validator(lambda lst: len(lst) > x,
                     "Length of `{arg_name}` must be greater than `{min_len}`",
                     min_len=x)


def len_lt(x):
    return Validator(lambda lst: len(lst) < x,
                     "Length of `{arg_name}` must be less than `{min_len}`",
                     min_len=x)


def len_eq(x):
    return Validator(lambda lst: len(lst) == x,
                     "Length of `{arg_name}` must be `{len_}` symbols",
                     len_=x)


def len_neq(x):
    return Validator(lambda lst: len(lst) != x,
                     "Length of `{arg_name}` must be NOT `{len_}` symbols",
                     len_=x)


def gt(x):

    @validator("Value of `{arg_name}` must be greater than `{max_val}`", max_val=x)
    def cond(value):
        return value > x

    return cond


def lt(x):

    @validator("Value of `{arg_name}` must be less than `{min_val}`", min_val=x)
    def cond(value):
        return value < x

    return cond


def neq(x, error_class=ValidationError):

    @validator("Value of `{arg_name}` can't be `{value}`", error_class=error_class, value=x)
    def cond(value):
        return value != x

    return cond


def nis(x, error_class=ValidationError, error_template="`{arg_name}` instance can't be `{x}`"):

    @validator(error_template, error_class=error_class, x=x)
    def cond(value):
        return value is not x

    return cond


def val_in(x):

    @validator("Value of `{arg_name}` must be in `{possible_values}`", possible_values=x)
    def cond(value):
        return value in x

    return cond


def val_nin(x):

    @validator("Value of `{arg_name}` can't be in `{impossible_values}`", impossible_values=x)
    def cond(value):
        return value not in x

    return cond


class TypeValidator(Validator):

    def __call__(self, value):
        if not self.expression(value):
            self.raise_exception(given_type_name=type(value).__name__)


def type_is(t):
    return TypeValidator(lambda x: isinstance(x, t),
                         "Value of `{arg_name}` should be `{expected_type_name}`, not `{given_type_name}`",
                         description_template="Value of `{arg_name}` should be `{expected_type_name}`",
                         expected_type_name=t.__name__)


def type_in(xs):
    return TypeValidator(lambda t: any(isinstance(t, x) for x in xs),
                         "Value of `{arg_name}` should be one of `{expected_type_names}`, not `{given_type_name}`",
                         description_template="Value of `{arg_name}` should be one of `{expected_type_names}`",
                         expected_type_names=[x.__name__ for x in xs])
