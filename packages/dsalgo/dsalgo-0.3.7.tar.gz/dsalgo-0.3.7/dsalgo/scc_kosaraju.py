def _transpose_graph(graph: list[list[int]]) -> list[list[int]]:
    n = len(graph)
    new_graph: list[list[int]] = [[] for _ in range(n)]
    for u in range(n):
        for v in graph[u]:
            new_graph[v].append(u)
    return new_graph


def scc(graph: list[list[int]]) -> list[int]:
    """
    g: adjacency list
    return: component ids
    """
    n = len(graph)
    visited = [False] * n
    que: list[int] = []
    t_graph = _transpose_graph(graph)
    labels = [-1] * n
    label = 0

    def dfs(u: int) -> None:
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
        que.append(u)

    def rev_dfs(u: int, label: int) -> None:
        labels[u] = label
        for v in t_graph[u]:
            if labels[v] == -1:
                rev_dfs(v, label)

    for u in range(n):
        if not visited[u]:
            dfs(u)
    for u in que[::-1]:
        if labels[u] != -1:
            continue
        rev_dfs(u, label)
        label += 1
    return labels


import unittest


class _Tests(unittest.TestCase):
    def test(self) -> None:
        graph: list[list[int]] = [[1, 3], [2], [3], []]
        labels = scc(graph)
        self.assertEqual(
            labels,
            [0, 1, 2, 3],
        )


if __name__ == "__main__":
    import doctest

    unittest.main()

    doctest.testmod(verbose=True)
