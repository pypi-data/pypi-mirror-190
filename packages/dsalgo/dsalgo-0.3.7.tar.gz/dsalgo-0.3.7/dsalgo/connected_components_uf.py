from .union_find_optimized import UnionFind


def labels(
    n: int,
    edges: list[tuple[int, int]],
) -> list[int]:
    uf = UnionFind(n)
    for u, v in edges:
        uf.unite(u, v)
    return uf.labels()
