#!/usr/bin/env python3
""""""
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
        Measure the total runtime of async_comprehension
        executed four times in parallel.
    """
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
