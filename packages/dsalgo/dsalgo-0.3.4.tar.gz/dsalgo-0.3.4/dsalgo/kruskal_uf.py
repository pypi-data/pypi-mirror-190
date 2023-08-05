"""
https://en.wikipedia.org/wiki/Kruskal%27s_algorithm

with Union Find
"""

from .union_find import UnionFind


def mst(
    n: int,
    edges: list[tuple[int, int, int]],
) -> list[int]:
    """kruskal
    edges: [(u, v, weight)]
    return: added edge indices
    """
    uf = UnionFind(n)
    eids = []
    for i, (u, v, _) in sorted(enumerate(edges), key=lambda e: e[1][2]):
        if uf.root(u) == uf.root(v):
            continue
        eids.append(i)
        uf.unite(u, v)
    return eids
