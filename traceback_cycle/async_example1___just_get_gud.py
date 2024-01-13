"""One way to avoid exception reference cycle problem in async world -
    never let exceptions bubble up from task."""
import asyncio
import traceback

from traceback_cycle.user import User
from traceback_cycle.gc_check import exception_reference_cycle_watcher


def raising_fn(user: User):
    full_names = {"Denis": "Denis Sleptsov", "Ivan": "Ivan Girko"}
    print(f"Hello, {full_names[user.name]}")


async def say_hello(name):
    user = User(name)
    try:
        raising_fn(user)
    except Exception as e:
        print(f"Raised exception: {e}")


async def say_hello2(name):
    user = User(name)
    try:
        raising_fn(user)
    except Exception as e:
        result = e
        print(f"Raised exception: {e}")
        traceback.print_exc(limit=5)


async def say_hello3(name):
    user = User(name)
    try:
        raising_fn(user)
    except Exception as e:
        result = e
        print(f"Raised exception: {e}")
        result.__traceback__ = None


async def greet_people(greeter):
    results = await asyncio.gather(
        greeter("Denis"), greeter("Unkown"), return_exceptions=True
    )
    for exc in [r for r in results if isinstance(r, BaseException)]:
        print(f"Exception in hello task: {exc}")


async def main():
    with exception_reference_cycle_watcher() as is_cycle_created:
        await greet_people(say_hello3)
        print(f"Cycle created: {is_cycle_created()}")
    print(f"User count: {User.counter}")


asyncio.run(main())
