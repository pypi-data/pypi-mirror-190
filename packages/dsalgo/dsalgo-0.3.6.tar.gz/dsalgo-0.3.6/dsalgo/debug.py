def dbg(*args: object, **kwargs: object) -> None:
    import os
    import pprint

    if os.environ.get("PYTHON_DEBUG") is None:
        return

    for v in args:
        pprint.pprint(v)

    for k, v in kwargs.items():
        print(f"{k}:")
        pprint.pprint(v)


import unittest


class _Tests(unittest.TestCase):
    def test(self) -> None:
        import os

        os.environ["PYTHON_DEBUG"] = "1"
        dbg(1, 2, a=[1, 2, 3, 5, 6, 7, 8, 9, 0, 1, 1])


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    unittest.main()
