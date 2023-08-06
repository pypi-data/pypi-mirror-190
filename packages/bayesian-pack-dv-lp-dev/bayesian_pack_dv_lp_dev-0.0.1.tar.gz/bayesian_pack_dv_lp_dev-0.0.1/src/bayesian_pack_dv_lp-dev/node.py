from dataclasses import dataclass, field

@dataclass(frozen=True)
class Node():
    name: str = field()
    dependencies: list = field(default_factory=list)