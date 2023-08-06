# extension of union find


from typing import Protocol

from .len_proto import Len
from .union_find_proto import FindRoot


class UF(Len, FindRoot, Protocol):
    ...


def labels(uf: UF) -> list[int]:
    n = len(uf)
    labels = [-1] * n
    l = 0
    for i in range(n):
        r = uf.root(i)
        if labels[r] == -1:
            labels[r] = l
            l += 1
        labels[i] = labels[r]
    return labels
