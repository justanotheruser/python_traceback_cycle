"""No exception reference cycle, but still a memory leak - frames are stored somewhere in asyncio."""
import asyncio
from weakref import WeakSet
import gc

from traceback_cycle.user import User
from traceback_cycle.gc_check import exception_reference_cycle_watcher


USERS = WeakSet()


def raising_fn(user: User):
    full_names = {"Denis": "Denis Sleptsov", "Ivan": "Ivan Girko"}
    print(f"Hello, {full_names[user.name]}")


async def say_hello(name):
    user = User(name)
    USERS.add(user)
    raising_fn(user)


async def greet_people():
    results = await asyncio.gather(
        say_hello("Denis"),
        say_hello("Unknown"),
        say_hello("Another unkown"),
        return_exceptions=True,
    )
    for exc in [r for r in results if isinstance(r, BaseException)]:
        print(f"Exception in hello task: {exc}")
        exc.__traceback__ = None  # This doesn't help
        del exc  # Neither does this
    del results  # or even this


async def main():
    with exception_reference_cycle_watcher() as is_cycle_created:
        await greet_people()
        print(f"Cycle created: {is_cycle_created()}")
    print(f"User count: {User.counter}")
    for user in USERS:
        for referrer in gc.get_referrers(user):
            print(referrer)


asyncio.run(main())
