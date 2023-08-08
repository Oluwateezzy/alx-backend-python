#!/usr/bin/env python3
from typing import Iterable, Sequence, List, Tuple
"""length"""


def element_length(lst: Iterable[Sequence])-> List[Tuple[Sequence]]:
    return [(i, len(i)) for i in lst]