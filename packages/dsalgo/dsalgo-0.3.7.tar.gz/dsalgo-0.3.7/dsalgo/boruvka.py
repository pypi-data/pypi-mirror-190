# https://en.wikipedia.org/wiki/Bor%C5%AFvka%27s_algorithm

# O(|E|\log{|V|})

from .connected_components_uf import labels


def boruvka(
    n: int,
    edges: list[tuple[int, int, int]],
) -> list[int]:
    m = len(edges)
    added = [False] * m
    while True:  # O(\log{|V|}) times loop.
        label = labels(
            n,
            [(u, v) for i, (u, v, _) in enumerate(edges) if added[i]],
        )
        k = max(label) + 1
        if k == 1:
            break
        min_edge = [-1] * k  # for each label.
        for i, (u, v, w) in enumerate(edges):
            u, v = label[u], label[v]
            if u == v:
                continue
            if min_edge[u] == -1 or w < edges[min_edge[u]][2]:
                min_edge[u] = i
            if min_edge[v] == -1 or w < edges[min_edge[v]][2]:
                min_edge[v] = i

        for i in min_edge:
            assert i != -1
            added[i] = True
    return [i for i, ok in enumerate(added) if ok]
