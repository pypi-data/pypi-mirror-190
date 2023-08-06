"""Main 'shoalling' interface."""

import argparse
import sys

from beartype import beartype
from beartype.typing import List

from ._private.cli import task_help
from .tangs import registered_tangs


@beartype
def _swim(shoal_args: List[str]) -> None:
    """Run each Tang."""
    tangs = registered_tangs()

    argv = set(shoal_args)
    targets = argv.intersection(set(tangs))
    if not targets:
        raise ValueError(f'No tangs were specified in input. Excepted one of: {[*tangs]}')

    path_args = [*argv - targets]
    for target in targets:
        tangs[target].run(path_args)


@beartype
def _run() -> None:  # pragma: no cover
    """CLI Entrypoint."""
    # PLANNED: Add a flag (--debug & store_true) to print debugging information

    parser = argparse.ArgumentParser(description='shoal runner')
    parser.add_argument('-t', '--task-help', action='store_true', help='Print help for tasks')
    parser.add_argument('shoal_args', help='Arguments passed to shoal. See "-t" for more', nargs='*')
    options = parser.parse_args(sys.argv[1:])

    if options.task_help:
        task_help()
    else:
        _swim(options.shoal_args)


@beartype
def shoalling() -> None:  # pragma: no cover
    """Add to a 'shoal.py' file to run `shoal`."""
    _run()
