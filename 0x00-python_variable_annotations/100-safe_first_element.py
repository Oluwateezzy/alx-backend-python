#!/usr/bin/env python3
"""duck-typed"""
from typing import Any, Union, Sequence, Optional


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Union[Any, Optional[None]]:
    if lst:
        return lst[0]
    else:
        return None