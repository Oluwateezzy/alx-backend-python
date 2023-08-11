#!/usr/bin/env python3
"""async await"""

from typing import List

async_gen = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    '''returns a list of rand numbers using async comprehension'''
    rand_num = [i async for i in async_gen()]
    return rand_num


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(async_comprehension()))
