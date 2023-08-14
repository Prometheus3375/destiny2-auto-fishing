from collections.abc import Callable
from inspect import Parameter, signature
from tomllib import load
from typing import Any, NamedTuple, Self, final

from destiny2autofishing.functions import extract_param_docs

CONFIG_COMMENT = '# '
CONFIG_LINE_LIMIT = 70
CONFIG_PLACEHOLDER = '???'

annotation2description = {
    bool:        'A boolean',
    int:         'An integer',
    float:       'A decimal',
    int | float: 'A decimal',
    str:         'A string',
    }
"""
Maps basic types to their descriptions.
"""


def format_comment(comment: str, /) -> str:
    """
    Takes a comment string and formats it to satisfy
    comment prefix and line limit of configuration. In addition, replaces all
    ``True`` and ``False`` mentions in reStructuredText with appropriate analogs.
    """
    comment = comment.replace('``True``', '``true``').replace('``False``', '``false``')
    comment = ' '.join(comment.split())

    lines = []
    while len(comment) >= CONFIG_LINE_LIMIT:
        space_pos = comment.rfind(' ', 0, CONFIG_LINE_LIMIT)
        if space_pos == -1:
            space_pos = comment.find(' ')
            if space_pos == -1: break

        lines.append(CONFIG_COMMENT)
        lines.append(comment[:space_pos])
        lines.append('\n')
        comment = comment[space_pos + 1:]

    lines.append(CONFIG_COMMENT)
    lines.append(comment)
    return ''.join(lines)


class ConfigParameter(NamedTuple):
    """
    A data holder of configuration parameter.
    """
    name: str
    annotation: type[bool | int | float | str]
    docs: str
    default: Any = Parameter.empty

    @classmethod
    def function_params(cls, func: Callable, /) -> list[Self]:
        """
        Takes a function and returns a list of its parameters
        wrapped over :class:`ConfigParameter`.
        **Note**: undocumented parameters are not included.
        """
        params = signature(func).parameters
        descriptions = extract_param_docs(func)
        return [
            cls(name, params[name].annotation, descriptions[name], params[name].default)
            # Do not use intersection with key sets.
            # Use if check instead to preserve parameter order.
            for name in params
            if name in descriptions
            ]

    def to_config_text(self, /) -> str:
        """
        Converts this instance to appropriate configuration text.
        """
        if self.default is Parameter.empty:
            requirement_note = 'must be specified'
            default = CONFIG_PLACEHOLDER
        else:
            requirement_note = 'optional'
            default = self.default
            default = str(default).lower() if isinstance(default, bool) else repr(default)

        short_comment = f'{annotation2description[self.annotation]}, {requirement_note}.'
        return (
            f'{self.name} = {default}\n'
            f'{CONFIG_COMMENT}{short_comment}\n'
            f'{format_comment(self.docs)}\n'
        )


class Configurable:
    """
    Base class for all configurable classes.

    Subclasses must implement method ``config_parameters`` and
    specify parameter ``config_group`` on subclassing.
    """

    config_group: str
    """
    Name of the configuration group used by the class.
    The empty string means the root group.
    """

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, *, config_group: str):
        if not isinstance(config_group, str):
            raise TypeError(
                f"parameter 'config_group' of {cls} must be a string, "
                f"got {config_group!r} of type {type(config_group)}"
                )

        cls.config_group = config_group

    __slots__ = ()

    @staticmethod
    def config_parameters() -> list[ConfigParameter]:
        """
        Returns a list of :class:`ConfigParameter` necessary to customize this class.
        """
        raise NotImplementedError

    @classmethod
    @final
    def config_text(cls, /) -> str:
        """
        Returns a configuration text for this class and its subclasses.
        """
        parameters = cls.config_parameters()
        parameters_str = '\n'.join(map(ConfigParameter.to_config_text, parameters))
        if cls.config_group:
            text = [f'\n\n[{cls.config_group}]\n\n{parameters_str}']
        else:
            text = [f'{parameters_str}']

        for sub in cls.__subclasses__():
            text.append(sub.config_text())

        return ''.join(text)


_config_header = f"""
# Welcome to auto-generated configuration file!
# Anything after # character is a comment.
# Types used in this config:
# A boolean -- true or false.
# An integer -- 0, 1, -1, etc.
# A decimal -- 1.2, 1.3, etc.
# A string -- 'anything here' or "anything here".
# Any {CONFIG_PLACEHOLDER} must be replaced with a value of respective type.
# Any optional parameter can be removed from this configuration.


""".lstrip()


def generate_config(path_to_config: str, /):
    """
    Generates a sample configuration file saving it to the specified path.
    """
    # Import fisher module to import all other Configurable subclasses
    # noinspection PyUnresolvedReferences
    import destiny2autofishing.fisher

    with open(path_to_config, 'w', encoding='utf-8') as f:
        f.write(_config_header)

        # Reverse order to make Fisher in the first place
        for cls in reversed(Configurable.__subclasses__()):
            f.write(cls.config_text())


def parse_config(path_to_config: str, /) -> dict[str, Any]:
    """
    Parses configuration file to configuration dictionary.
    """
    with open(path_to_config, 'rb') as f:
        return load(f)


__all__ = 'ConfigParameter', 'Configurable', 'generate_config', 'parse_config'