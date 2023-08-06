class UnionFind:
    _root: list[int]
    _rank: list[int]

    def __init__(self, n: int) -> None:
        self._root = list(range(n))
        self._rank = [1] * n

    def root(self, u: int) -> int:
        r = self._root[u]
        return u if r == u else self.root(r)

    def unite(self, u: int, v: int) -> None:
        u, v = self.root(u), self.root(v)
        if u == v:
            return
        if self._rank[u] < self._rank[v]:
            u, v = v, u
        if self._rank[u] == self._rank[v]:
            self._rank[u] += 1
        self._root[v] = u


import unittest


# TODO:
class _Tests(unittest.TestCase):
    def test(self) -> None:
        ...


if __name__ == "__main__":
    import doctest

    unittest.main()

    doctest.testmod(verbose=True)
