import warnings


class InvalidArgumentError(Exception):
    """不正な引数

    このパッケージがサポートしていない引数がMeCabWrapper()のargsに指定された場合に発生します。
    対応しない引数を削除して再度お試しください。
    """
    pass


def deprecated(func, message: str | None = None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    if message is None:
        message = f"{func.__name__}関数は非推奨です。"

    def newFunc(*args, **kwargs):
        warnings.warn(message, category=DeprecationWarning)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc
