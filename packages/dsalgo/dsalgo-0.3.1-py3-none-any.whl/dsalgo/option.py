from typing import TypeVar

T = TypeVar("T")


def unwrap(x: T | None) -> T:
    assert x is not None
    return x


import unittest


class _Tests(unittest.TestCase):
    def test(self) -> None:
        def receive_int(b: int) -> None:
            ...

        a: int | None = 1

        receive_int(unwrap(a))


if __name__ == "__main__":
    import doctest

    unittest.main()

    doctest.testmod(verbose=True)
