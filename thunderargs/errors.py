class ThunderargsError(Exception):
    pass


class ValidationError(ThunderargsError):

    def __init__(self, message_template, *args, **kwargs):

        self.message_template = message_template
        self.args = args
        self.opt = kwargs

        super().__init__(message_template.format(*args, **kwargs))


class ArgumentRequired(ValidationError):
    pass


def customize_error(message=None, error_class=None, error_code=10000, **opt):

    def wrapper(validator):

        validator.message = message
        validator.error_class = error_class or ValidationError
        validator.error_code = error_code
        validator.opt = opt

        return validator

    return wrapper