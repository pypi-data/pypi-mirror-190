def scc(graph: list[list[int]]) -> list[int]:
    n = len(graph)
    order = [-1] * n
    labels = [-1] * n
    stack_0: list[int] = []
    stack_1: list[int] = []
    ord = 0
    label = 0

    def dfs(u: int) -> None:
        nonlocal ord, label
        order[u] = ord
        ord += 1
        stack_0.append(u)
        stack_1.append(u)
        for v in graph[u]:
            if order[v] == -1:
                dfs(v)
            elif labels[v] == -1:
                # v is start of a scc.
                while order[stack_0[-1]] > order[v]:
                    stack_0.pop()

        if stack_0[-1] != u:
            return
        while True:
            v = stack_1.pop()
            labels[v] = label
            print(u, v)
            if v == u:
                break
        label += 1
        stack_0.pop()

    for i in range(n):
        if order[i] == -1:
            dfs(i)

    return labels


import unittest


class _Tests(unittest.TestCase):
    def test(self) -> None:
        graph: list[list[int]] = [[1, 3], [2], [3], []]
        labels = scc(graph)
        self.assertEqual(
            labels,
            [3, 2, 1, 0],
        )


if __name__ == "__main__":
    import doctest

    unittest.main()

    doctest.testmod(verbose=True)
