#!/usr/bin/env python3
""" wait random"""

from asyncio import sleep
from random import random


async def wait_random(max_delay=10):
    """ wait random"""

    delay = random() * max_delay
    await sleep(delay)
    return delay
