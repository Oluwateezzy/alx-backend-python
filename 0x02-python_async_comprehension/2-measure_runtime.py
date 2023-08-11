#!/usr/bin/env python3
"""Async await"""

import asyncio
import time


async def measure_runtime() -> float:
    """
        Measure the total runtime of async_comprehension
        executed four times in parallel.
    """
    async_comprehension = __import__('1-async_comprehension').async_comprehension

    start = time.time()
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )
    return time.time() - start


if __name__ == '__main__':
    print(asyncio.run(measure_runtime()))
