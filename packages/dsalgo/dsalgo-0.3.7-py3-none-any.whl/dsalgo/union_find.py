class UnionFind:
    _root: list[int]

    def __init__(self, n: int) -> None:
        self._root = list(range(n))

    def root(self, u: int) -> int:
        r = self._root[u]
        return u if r == u else self.root(r)

    def unite(self, u: int, v: int) -> None:
        u, v = self.root(u), self.root(v)
        self._root[v] = u
