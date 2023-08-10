#!/usr/bin/env python3
"""Write a coroutine called async_generator that takes no arguments"""

import asyncio
import random


async def async_generator():
    """async generator"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)


if __name__ == '__main__':
    async def print_yielded_values():
        result = []
        async for i in async_generator():
            result.append(i)
        print(result)

    asyncio.run(print_yielded_values())