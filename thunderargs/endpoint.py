from . import Parser
from .helpers import wraps


class Endpoint(object):

    """
    Класс для оборачивания целевых функций и передачи им
    уже обработанных аргументов вместо сырых

    >>> plus = Endpoint(plus)
    >>> plus(5.0, "4")
    9
    """

    def __call__(self, *args, **kwargs):
        return self.callable(*args, **kwargs)

    def _decorate(self, func):
        if func._arg_description:
            self.parser = Parser(func._arg_description, func.__code__.co_varnames)
            # self.__arg_description_help = self.parser.prepare_hints()
            # Делаем инстансы данного класса вызываемыми.
            # Целевая функция оборачивается в декоратор, который
            # описн ниже
            self.callable = self._wrap_callable(func)
        else:
            self.callable = func

    def __init__(self, func=None, **structure):

        # I can use `wraps` here, right?
        # self.__name__ = func.__name__
        # self.__code__ = func.__code__
        # self.__defaults__ = func.__defaults__
        # self.__kwdefaults__ = func.__kwdefaults__

        wraps(func)(self)  # TODO check

        if not callable(func) and structure:
            def first_call(func):
                self._decorate(annotate(**structure)(func))
                return self
            self.callable = first_call
        else:
            self.__arg_description = func._arg_description
            self._decorate(func)

    def _wrap_callable(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Обертка принимает все аргументы, предназначенные
            # для целефой функции, и передаёт в парсер именованные.
            args, kwargs = self.parser(args, kwargs)
            return func(*args, **kwargs)
        return wrapper


def annotate(**structure):
    def decorator(func):
        func._arg_description = structure
        return func
    return decorator


def annotate_from(source_func):
    def decorator(func):
        func._arg_description.update(source_func._arg_description)
        return func
    return decorator
