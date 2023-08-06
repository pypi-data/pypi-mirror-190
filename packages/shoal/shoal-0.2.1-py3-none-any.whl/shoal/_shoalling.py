"""Main 'shoalling' interface."""

import argparse
import logging
import sys

from beartype import beartype
from beartype.typing import List
from pydantic import BaseModel

from ._cli import task_help
from ._log import configure_logger
from ._tangs import registered_tangs


@beartype
def _run_tangs(shoal_args: List[str]) -> None:
    """Run each Tang."""
    tangs = registered_tangs()

    argv = set(shoal_args)
    targets = argv.intersection(set(tangs))
    if not targets:
        raise ValueError(
            f'No tangs were specified in input. Excepted one of: {[*tangs]}',
        )

    path_args = [*argv - targets]
    for target in targets:
        tangs[target].run(path_args)


class _CLIOptions(BaseModel):
    """CLI Options."""

    debug: bool
    task_help: bool
    shoal_args: List[str]


@beartype
def _run(options: _CLIOptions) -> None:
    """Internal entrypoint for testing."""
    configure_logger(logging.DEBUG if options.debug else logging.INFO)

    if options.task_help:
        task_help()
    else:
        _run_tangs(options.shoal_args)


@beartype
def shoalling() -> None:  # pragma: no cover
    """Main CLI and script Entrypoint."""
    parser = argparse.ArgumentParser(description='shoal runner')
    parser.add_argument('-d', '--debug', action='store_true', help='Show debug-level logging')
    parser.add_argument('-t', '--task-help', action='store_true', help='Print help for tasks')
    parser.add_argument('shoal_args', help='Arguments passed to shoal. See "-t" for more', nargs='*')
    args = parser.parse_args(sys.argv[1:])

    _run(_CLIOptions(**vars(args)))
