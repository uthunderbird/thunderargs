from thunderargs.helpers import Nothing


class Transformer(object):

    def __call__(self, value):
        return self.transformer(value)

    def __init__(self, transformer, condition_or_conditions=(), description=""):
        if callable(condition_or_conditions):
            condition_or_conditions = (condition_or_conditions,)
        self.conditions = condition_or_conditions
        self.transformer = transformer
        self.description = description

    def is_acceptable(self, value):
        # TODO `all` or `any`?
        return all(condition(value) for condition in self.conditions)


def set_default_if_unset(default):
    return Transformer(lambda x: default, lambda x: x is Nothing,
                       description="Default value: {default}".format(default=default))
