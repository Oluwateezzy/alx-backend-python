#!/usr/bin/env python3
"""make multiplier"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """make multiplier"""
    def multiplier_function(value: float) -> float:
        return value * multiplier
    return multiplier_function
