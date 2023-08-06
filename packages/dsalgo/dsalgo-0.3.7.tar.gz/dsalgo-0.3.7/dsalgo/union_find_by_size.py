class UnionFind:
    _root: list[int]
    _size: list[int]

    def __init__(self, n: int) -> None:
        self._root = list(range(n))
        self._size = [1] * n

    def root(self, u: int) -> int:
        r = self._root[u]
        return u if r == u else self.root(r)

    def unite(self, u: int, v: int) -> None:
        u, v = self.root(u), self.root(v)
        if u == v:
            return
        if self._size[u] < self._size[v]:
            u, v = v, u
        self._size[u] += self._size[v]
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
