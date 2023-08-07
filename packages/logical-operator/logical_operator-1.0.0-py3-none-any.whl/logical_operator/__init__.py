"""Normalized logical operators as functions.

The ``and``, ``or``, and ``not`` operators implemented as free-standing
functions.

Author: Braedyn L
Version: 1.0.0
Documentation: https://github.com/braedynl/logical_operator
"""

from typing import Any

__all__ = [
    "logical_and",
    "logical_or",
    "logical_not",
]


def logical_and(a: Any, b: Any, /) -> bool:
    """Return the logical AND of two objects"""
    return (not not a) and (not not b)


def logical_or(a: Any, b: Any, /) -> bool:
    """Return the logical OR of two objects"""
    return (not not a) or (not not b)


def logical_not(a: Any, /) -> bool:
    """Return the logical NOT of an object"""
    return not a
