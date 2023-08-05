# import typing


class UnionFind:
    _data: list[int]  # root: neg-size, other: parent

    def __init__(self, n: int) -> None:
        self._data = [-1] * n

    def size(self) -> int:
        return len(self._data)

    def root(self, u: int) -> int:
        if self._data[u] < 0:
            return u
        p = self.root(self._data[u])
        self._data[u] = p
        return p

    def unite(self, u: int, v: int) -> None:
        u, v = self.root(u), self.root(v)
        if u == v:
            return
        if self._data[u] > self._data[v]:
            u, v = v, u
        self._data[u] += self._data[v]
        self._data[v] = u

    def size_of(self, u: int) -> int:
        return -self._data[self.root(u)]

    def same(self, u: int, v: int) -> bool:
        return self.root(u) == self.root(v)

    def labels(self) -> list[int]:
        n = self.size()
        labels = [-1] * n
        l = 0
        for i in range(n):
            r = self.root(i)
            if labels[r] == -1:
                labels[r] = l
                l += 1
            labels[i] = labels[r]
        return labels

    def groups(self) -> list[list[int]]:
        labels = self.labels()
        g: list[list[int]] = [[] for _ in range(max(labels) + 1)]
        for i, l in enumerate(labels):
            g[l].append(i)
        return g


import unittest


# TODO:
class _Tests(unittest.TestCase):
    def test(self) -> None:
        ...


if __name__ == "__main__":
    import doctest

    unittest.main()

    doctest.testmod(verbose=True)
