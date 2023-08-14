from datetime import datetime
from os.path import isfile


def current_datetime_ms_str() -> str:
    """
    Takes current date and time and converts to a string.
    The result always have 3 digits for fraction part of seconds.
    """
    dt = datetime.now()
    ms = dt.microsecond // 1000
    dt = dt.replace(microsecond=0)
    return f'{dt}.{ms:03}'


def current_datetime_str() -> str:
    """
    Takes current date and time, sets microseconds to zero and converts to a string.
    """
    return str(datetime.now().replace(microsecond=0))


def extract_param_docs(obj: object, /) -> dict[str, str]:
    """
    Parses ``__doc__`` attribute of passed object and returns a mapping
    with a correspondence between parameter names and their descriptions.
    """
    if (docs := obj.__doc__) is None: return {}

    docs = docs.strip('\n')
    indent_size = 0
    while docs[indent_size] == ' ':
        indent_size += 1

    param_name = ''
    param_doc = []
    params = {}
    for line in docs.split('\n'):
        if line.startswith('  ', indent_size):
            param_doc.append(' '.join(line.split()))
        elif param_name:
            params[param_name] = ' '.join(param_doc)
            param_name = ''
            param_doc = []

        if line.startswith(':param', indent_size):
            name, doc = line.lstrip()[6:].split(':', 1)
            param_name = name.strip()
            param_doc.append(' '.join(doc.split()))

    return params


def locate_file(*paths: str) -> str | None:
    """
    For every passed path checks if it is a file.
    Returns the first path which is a file.
    If none of passed paths is a file, returns ``None``.
    """
    for path in paths:
        if isfile(path): return path


__all__ = (
    'current_datetime_ms_str',
    'current_datetime_str',
    'extract_param_docs',
    'locate_file',
    )
