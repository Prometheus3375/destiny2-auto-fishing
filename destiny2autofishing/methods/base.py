import os
from collections.abc import Iterator, Set
from os.path import dirname, join
from time import sleep

from ..anti_afk import AntiAFK
from ..configurator import Config, ConfigParameter, Configurable
from ..controls import *
from ..functions import current_datetime_ms_str, current_datetime_str, locate_file


class BaseMethod(Configurable, config_group='fishing-method'):
    """
    Base method for all fishing methods.
    """

    name: str
    """
    Name of the fishing method.
    """

    file_arguments: Set[str] = frozenset()
    """
    A set of arguments names which accept file paths.
    It is used to try several possible file locations
    before supplying these arguments to constructor
    when creating a fishing method from a configuration file.
    """

    __name2cls: dict[str, type['BaseMethod']] = {}
    """
    Maps method name to its class.
    """

    # noinspection PyMethodOverriding
    def __init_subclass__(cls, /, *, name: str):
        if not (isinstance(name, str) and name):
            raise TypeError(
                f"parameter 'name' of {cls} must be a non-empty string, "
                f"got {name!r} of type {type(name)}"
                )

        present = BaseMethod.__name2cls.get(name)
        if present is not None:
            raise ValueError(f'method name {present.name!r} is already used by {present}')

        cls.name = name
        BaseMethod.__name2cls[name] = cls
        super().__init_subclass__(config_group=f'{BaseMethod.config_group}.{name}')

    __slots__ = (
        '_press',
        '_hold',
        '_interact_key',
        '_anti_afk',
        'delay_after_catch',
        'cast_duration',
        'log_file',
        )

    def __init__(
            self,
            /,
            interact_key: str,
            is_mouse_button: bool,
            delay_after_catch: float = 3.3,
            # After catch there are ~100 frames in 30 FPS video
            # before interact button appears again
            cast_duration: float = 1,
            # Interact button is held for ~11 frames in 30 FPS video to continue fishing
            # 0.6 is not enough at low FPS
            log_directory_path: str = '',
            ):
        """
        :param interact_key: a key that is used to catch fish and cast the fishing rod.
        :param is_mouse_button: should be ``True`` if ``interact_key`` is a mouse button
          and ``False`` otherwise.
        :param delay_after_catch: time in seconds to wait after catch
          before casting the fishing rod.
          Defaults to 3.3.
        :param cast_duration: time in seconds to hold interact key to cast the fishing rod.
          Defaults to 1.
        :param log_directory_path: path to a directory where log files will be stored.
          Log file is used to write debug information; its name is the current date and time.
          Defaults to the empty string which means no log directory and no current log file.
        """
        assert isinstance(interact_key, str) and interact_key
        assert isinstance(is_mouse_button, bool)
        assert isinstance(delay_after_catch, (int, float)) and delay_after_catch > 0
        assert isinstance(cast_duration, (int, float)) and cast_duration > 0
        assert isinstance(log_directory_path, str)

        self._interact_key = interact_key
        self._press = press_mouse if is_mouse_button else press_key
        self._hold = hold_mouse if is_mouse_button else hold_key
        self._anti_afk = None

        self.delay_after_catch = delay_after_catch
        self.cast_duration = cast_duration

        if log_directory_path:
            os.makedirs(log_directory_path, exist_ok=True)
            self.log_file = os.path.join(
                log_directory_path,
                current_datetime_str().replace(':', '-'),
                )
        else:
            self.log_file = None

    @property
    def anti_afk(self, /) -> AntiAFK | None:
        """
        An instance of :class:`AntiAFK` or ``None``.
        This instance is used to perform actions preventing the game to consider a player as AFK.
        If ``None``, then anti-AFK is disabled.
        """
        return self._anti_afk

    @anti_afk.setter
    def anti_afk(self, value: AntiAFK | None, /):
        """
        Sets an instance of :class:`AntiAFK`.
        This instance is used to perform actions preventing the game to consider a player as AFK.
        If ``None`` is passed, disables anti-AFK.
        """
        assert value is None or isinstance(value, AntiAFK)
        self._anti_afk = value

    def _log(self, line: str, /, *args, **kwargs):
        """
        If there is a file for logs, opens it and appends passed string with format arguments.
        The result is prepended with the current datetime and appended with line feed.
        """
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f'{current_datetime_ms_str()}    {line.format(*args, *kwargs)}\n')

    def cast(self, /):
        """
        Issues a command to cast the fishing rod.
        """
        self._hold(self._interact_key, self.cast_duration)

    def catch(self, /):
        """
        Issues a command to catch fish.
        """
        self._press(self._interact_key)

    def _start(self, /):
        """
        Starts an infinite loop of fishing.
        If fish can be successfully caught, yields ``True``.
        Yields ``False`` in any other case.
        """
        raise NotImplementedError

    def start(self, do_cast: bool, /) -> Iterator[bool]:
        """
        Starts an infinite loop of fishing.
        If fish is successfully caught, yields ``True``.
        Yields ``False`` in any other case.

        :param do_cast: if ``True``, then casts the fishing rod before entering the loop.
        """
        if do_cast:
            self.cast()
            yield False

        for do_catch in self._start():
            if do_catch:
                self.catch()
                yield True
                sleep(self.delay_after_catch)
                yield False
                self.cast()

            if self._anti_afk: self._anti_afk.act_based_on_catch(do_catch)
            yield False

    @staticmethod
    def config_parameters() -> list[ConfigParameter]:
        method_names = ', '.join(repr(sub.name) for sub in BaseMethod.__subclasses__())
        method_name_doc = f'Name of the fishing method. Possible values: {method_names}.'
        return [
            ConfigParameter('method_name', str, method_name_doc),
            *ConfigParameter.function_params(BaseMethod.__init__),
            ]

    @staticmethod
    def from_config(config: Config, /) -> 'BaseMethod':
        kwargs = config.params[BaseMethod.config_group].copy()
        method_name = kwargs.pop('method_name')
        kwargs |= kwargs.pop(method_name)
        cls = BaseMethod.__name2cls[method_name]
        for arg in cls.file_arguments:
            original_path = kwargs[arg]
            config_dir_path = join(dirname(config.path), original_path)
            located = locate_file(original_path, config_dir_path)
            if located is None:
                raise ValueError(
                    f'cannot locate a file for parameter {arg!r} '
                    f'of {method_name!r} fishing method; '
                    f'tried locations: {original_path!r} and {config_dir_path!r}'
                    )

            kwargs[arg] = located

        return cls(**kwargs)


__all__ = 'BaseMethod',
