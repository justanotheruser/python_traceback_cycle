"""Explicilty creating tasks prevents asyncio from storing frames after uncaught exception."""
import asyncio
from weakref import WeakSet
import gc

from py_sketches.traceback_cycle.user import User
from py_sketches.traceback_cycle.gc_check import exception_reference_cycle_watcher


USERS = WeakSet()


def raising_fn(user: User):
    full_names = {"Denis": "Denis Sleptsov", "Ivan": "Ivan Girko"}
    print(f"Hello, {full_names[user.name]}")


async def say_hello(name):
    user = User(name)
    USERS.add(user)
    raising_fn(user)


async def greet_people():
    tasks = [
        asyncio.create_task(say_hello(name))
        for name in ("Denis", "Unknown", "Another unkown")
    ]
    done, _ = await asyncio.wait(tasks)
    for task in done:
        exc = task.exception()
        if isinstance(exc, Exception):
            print(f"Exception in hello task: {exc}")


async def main():
    with exception_reference_cycle_watcher() as is_cycle_created:
        await greet_people()
        print(f"Cycle created: {is_cycle_created()}")
    print(f"User count: {User.counter}")
    for user in USERS:
        for referrer in gc.get_referrers(user):
            print(referrer)


asyncio.run(main())
