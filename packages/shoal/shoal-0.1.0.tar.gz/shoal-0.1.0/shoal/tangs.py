"""Tangs (the collection of tasks)."""

from beartype import beartype
from beartype.typing import Dict
from pydantic import BaseModel, Field

from .tang import Tang


class Tangs(BaseModel):
    """Dynamic collection of targets."""

    targets: Dict[str, Tang] = Field(default_factory=dict)
    """All registered targets."""

    @beartype
    def add_tang(self, tang: Tang) -> None:
        """Dynamically add a new Tang to the target list."""
        if tang.target in self.targets:
            print(f'Replaceing {self.targets[tang.target]} with {tang}')
        self.targets[tang.target] = tang


_TANGS = Tangs()
"""Internal state for global tangs."""


@beartype
def register(tang: Tang) -> None:
    """Dynamically add a new Tang to the target list."""
    _TANGS.add_tang(tang)


@beartype
def registered_tangs() -> Dict[str, Tang]:
    """Retrieve the registered tangs."""
    return _TANGS.targets
