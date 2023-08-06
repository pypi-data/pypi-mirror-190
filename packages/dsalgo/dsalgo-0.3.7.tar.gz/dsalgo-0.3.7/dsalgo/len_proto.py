from typing import Protocol


class Len(Protocol):
    def __len__(self) -> int:
        ...
