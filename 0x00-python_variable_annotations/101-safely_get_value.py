#!/usr/bin/env python3
"""type module"""
from typing import TypeVar, Mapping, Any, Union, Optional

T = TypeVar('T')  # Type variable for the return type


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """
    Safely get a value from a mapping based on a key.

    Args:
        dct (Mapping): A mapping (e.g., dictionary)
          with keys and values.
        key (Any): The key to look up in the mapping.
        default (Union[T, None], optional):
        The default value to return
        if the key is not found. Defaults to None.

    Returns:
        Union[Any, T]: The value associated
        with the key in the mapping, or the
        default value if the key is not found.
    """
    if key in dct:
        return dct[key]
    else:
        return default
