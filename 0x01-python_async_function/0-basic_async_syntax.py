#!/usr/bin/env python3
""" wait random"""

from asyncio import sleep
from random import uniform


async def wait_random(max_delay=10):
    delay = uniform(0, max_delay)
    await sleep(delay)
    return delay