"""Tang (task model).

```sh
  _
><_>
```

"""

from beartype.typing import Callable, List
from beartype import beartype
from pydantic import BaseModel


class Tang(BaseModel):
    """A singular task (named after the Tang fish).

    The inner naming and logic derives from Makefiles: https://www.gnu.org/software/make/manual/html_node/Introduction.html

    ```sh
    .PHONY target
    target: prerequisites
    <TAB> recipe
    ```

    """

    target: str
    """Name of the task."""

    recipe: List[Callable[[List[str]], None]]
    """Steps in the task."""

    description: str = ''
    """Optional help text."""

    # > PLANNED: Add support for these additional arguments

    # prerequisities: List[str] = Field(default_factory=list)
    # """Optional task and/or file prerequisities."""

    # phony: bool = False
    # """Set to True if the `target` should *not* be included in the file preqreuisites.
    #
    # By default, assumes that the target name is associated with the matching file.
    #
    # https://stackoverflow.com/a/2145605/3219667
    #
    # """

    @beartype
    def run(self, args: List[str]) -> None:
        for step in self.recipe:
            step(args)
