#!/usr/bin/env python3
import asyncio
"""
A module for creating asyncio Tasks that run asynchronous functions.
"""

wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
        A module for creating asyncio Tasks that run asynchronous functions.
    """
    return asyncio.create_task(wait_random(max_delay))
