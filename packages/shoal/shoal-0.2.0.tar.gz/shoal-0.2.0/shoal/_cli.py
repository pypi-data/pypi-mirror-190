"""CLI helpers."""


from beartype import beartype

from . import __version__
from ._tangs import registered_tangs


@beartype
def task_help() -> None:
    """Print the help text."""
    print(f'shoal ({__version__}): python-first task runner 🐠')

    tangs = registered_tangs().values()
    if tangs:
        print('')

    for tang in tangs:
        # TODO: Pretty-print help with rich
        print(f'{tang.target}\n\t{tang.description}')

    print('')
