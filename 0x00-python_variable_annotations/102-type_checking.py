#!/usr/bin/env python3
"""duck-typed"""
from typing import Tuple, List


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """duck-typed"""
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

# Note: mypy will catch the error in the next line
zoom_3x = zoom_array(array, 3)
