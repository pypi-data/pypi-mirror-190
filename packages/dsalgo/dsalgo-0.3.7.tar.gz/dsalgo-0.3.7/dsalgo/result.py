"""
inspired by Rust's Result<T, E> type.
in python, Option[T] = Union[T, None] =: T | None
while Option<T> in Rust is enum {Some(T), None}

and because Result<T, E> is enum {Ok(T), Err(E)},
Result[T, E] = Union[T, Err[E]] is fine in Python.

we don't use any Exceptions
which are starndard error handling feature in Python.
instead, Result[T, E] is defactostandard in this package.
"""

import unittest
from dataclasses import dataclass
from typing import Generic, TypeVar, Union, cast, final

from .option import unwrap

T = TypeVar("T", contravariant=True)
E = TypeVar("E", contravariant=True)
U = TypeVar("U", covariant=True)


@final
@dataclass(frozen=True)
class Err(Generic[E]):
    value: E


# wrap with Err to call is_err
Result = Union[T, Err[E]]


def is_ok(x: Result[T, E]) -> bool:
    return not is_err(x)


def is_err(x: Result[T, E]) -> bool:
    return isinstance(x, Err)


def ok(x: Result[T, E]) -> T | None:
    return cast(T, x) if is_ok(x) else None


def err(x: Result[T, E]) -> E | None:
    return cast(Err[E], x).value if is_err(x) else None


def unwrap_ok(x: Result[U, E]) -> U:
    return unwrap(ok(x))


def unwrap_err(x: Result[T, U]) -> U:
    return unwrap(err(x))


class _Tests(unittest.TestCase):
    def test(self) -> None:
        def generate_error() -> Result[int, str]:
            return Err("nothing")

        a = Err(1)
        assert not is_ok(a)
        assert ok(a) is None
        assert err(a) == 1
        assert is_err(generate_error())
        assert unwrap_err(generate_error()) == "nothing"


if __name__ == "__main__":
    import doctest

    unittest.main()

    doctest.testmod(verbose=True)
