"""Run shell commands."""

import shlex
import subprocess  # noqa: S404  # nosec
import sys
from io import BufferedReader
from pathlib import Path

from beartype import beartype
from beartype.typing import Callable, Optional


@beartype
def capture_shell(cmd: str, *, cwd: Optional[Path] = None, printer: Optional[Callable[[str], None]] = None) -> str:
    """Run shell command and return the output.

    Inspired by: https://stackoverflow.com/a/38745040/3219667

    Args:
        cmd: shell command
        cwd: optional path for shell execution
        printer: optional callable to output the lines in real time

    Returns:
        str: stripped output

    Raises:
        CalledProcessError: if return code is non-zero

    """
    lines = []
    with subprocess.Popen(  # noqa: DUO116  # nosec  # nosemgrep
        shlex.split(cmd), cwd=cwd,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
        shell=True,  # noqa: S602
    ) as proc:
        stdout: BufferedReader = proc.stdout  # type: ignore[assignment]
        return_code = None
        while return_code is None:
            if line := stdout.readline():
                lines.append(line)
                if printer:
                    printer(line.rstrip())  # type: ignore[arg-type]
            else:
                return_code = proc.poll()

    output = ''.join(lines)  # type: ignore[unreachable]
    if return_code != 0:
        raise subprocess.CalledProcessError(returncode=return_code, cmd=cmd, output=output)
    return output


@beartype
def shell(cmd: str, *, cwd: Optional[Path] = None) -> None:
    """Run shell command with buffering output.

    Args:
        cmd: shell command
        cwd: optional path for shell execution

    Raises:
        CalledProcessError: if return code is non-zero

    """
    subprocess.run(
        shlex.split(cmd), cwd=cwd,
        stdout=sys.stdout, stderr=sys.stderr, check=True,
        shell=True,  # noqa: DUO116,S602  # nosec  # nosemgrep
    )
