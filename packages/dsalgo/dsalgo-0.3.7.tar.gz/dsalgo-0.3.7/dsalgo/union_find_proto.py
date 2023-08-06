# basic protocols of union find


from typing import Protocol


class FindRoot(Protocol):
    def root(self, u: int) -> int:
        ...


class Unite(Protocol):
    def unite(self, u: int, v: int) -> None:
        ...


class SizeOf(Protocol):
    def size_of(self, u: int) -> int:
        ...
