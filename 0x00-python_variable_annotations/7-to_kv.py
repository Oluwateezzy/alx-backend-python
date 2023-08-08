#!/usr/bin/env python3
"""complex type"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """complex type"""
    return (k, v**2)
