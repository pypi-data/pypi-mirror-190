"""Log."""

import logging
from functools import cached_property, partial

from beartype import beartype
from beartype.typing import Any, Callable, Dict
from pydantic import BaseModel
from rich.console import Console
from rich.text import Text

_DEF_LEVEL = logging.ERROR


class _Styles:
    """Based on `tail-jsonl`."""

    level_error: str = 'red'
    level_warn: str = 'yellow'
    level_info: str = ''
    level_debug: str = 'blue'

    key: str = 'green'
    value: str = ''

    @cached_property
    def _level_lookup(self) -> Dict[int, str]:
        return {
            logging.ERROR: self.level_error,
            logging.WARNING: self.level_warn,
            logging.INFO: self.level_info,
            logging.DEBUG: self.level_debug,
        }


_STYLES = _Styles()


@beartype
def _log(message, *, _log_level: int, _this_level: int, _console: Console, **kwargs) -> None:
    """Default log function."""
    if _this_level >= _log_level:
        text = Text()
        text.append(message, style=_STYLES._level_lookup.get(_this_level))
        for key, value in kwargs.items():
            text.append(f' {key}:', style=_STYLES.key)
            text.append(f' {str(value): <10}', style=_STYLES.value)
        _console.print(text)


class _LogSingleton(BaseModel):
    """Store pointer to log function."""

    log: Callable[[Any], None]


_LOG_SINGLETON = _LogSingleton(log=partial(_log, _log_level=_DEF_LEVEL, _console=Console()))


class _Logger:

    @beartype
    def debug(self, message, **kwargs) -> None:
        _LOG_SINGLETON.log(message, _this_level=logging.DEBUG, **kwargs)

    @beartype
    def info(self, message, **kwargs) -> None:
        _LOG_SINGLETON.log(message, _this_level=logging.INFO, **kwargs)

    @beartype
    def warning(self, message, **kwargs) -> None:
        _LOG_SINGLETON.log(message, _this_level=logging.WARNING, **kwargs)

    @beartype
    def error(self, message, **kwargs) -> None:
        _LOG_SINGLETON.log(message, _this_level=logging.ERROR, **kwargs)

    @beartype
    def exception(self, message, **kwargs) -> None:
        _LOG_SINGLETON.log(message, _this_level=logging.EXCEPTION, **kwargs)


@beartype
def configure_logger(log_level: int = _DEF_LEVEL) -> None:
    """Configure global logger."""
    _LOG_SINGLETON.log = partial(_log, _log_level=log_level, _console=Console())


@beartype
def get_logger() -> _Logger:
    """Retrieve global logger."""
    return _Logger()
