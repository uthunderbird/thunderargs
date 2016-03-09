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

    def __init__(self, func, default_source=None):

        self.__annotations__ = func.__annotations__
        self.__name__ = func.__name__
        self.__code__ = func.__code__
        self.__defaults__ = func.__defaults__
        self.__kwdefaults__ = func.__kwdefaults__

        # for arg_obj in self.__annotations__.values():
        #     arg_obj.source = arg_obj.source or default_source

        if func.__annotations__:
            # Создаём парсер для данной структуры данных
            self.parser = Parser(func.__annotations__, func.__code__.co_varnames)
            self.__annotations__ = self.parser.prepare_hints()
            # Делаем инстансы данного класса вызываемыми.
            # Целевая функция оборачивается в декоратор, который
            # описн ниже
            self.callable = self._wrap_callable(func)
        else:
            self.callable = func

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
        func.__annotations__ = structure
        return func
    return decorator


def annotate_from(source_func):
    def decorator(func):
        func.__annotations__.update(source_func.__annotations__)
        return func
    return decorator
