import traceback

from py_sketches.traceback_cycle.user import User
from py_sketches.traceback_cycle.gc_check import exception_reference_cycle_watcher


def raising_fn(user: User):
    full_names = {"Denis": "Denis Sleptsov", "Ivan": "Ivan Girko"}
    print(f"Hello, {full_names[user.name]}")


def say_hello():
    """No cycle because e is not stored anywhere."""
    user = User("Unknown name")
    try:
        raising_fn(user)
    except Exception as e:
        print(f"Raised exception: {e}")


def say_hello2():
    """Cycle because e is stored in result, result is part of frame, and frame is part of traceback of e."""
    user = User("Unknown name")
    try:
        raising_fn(user)
    except Exception as e:
        result = e
        print(f"Raised exception: {e}")
        traceback.print_exc(limit=5)


def say_hello3():
    """No cycle because traceback is explicitly deleted"""
    user = User("Unknown name")
    try:
        raising_fn(user)
    except Exception as e:
        result = e
        print(f"Raised exception: {e}")
        result.__traceback__ = None


def main():
    with exception_reference_cycle_watcher() as is_cycle_created:
        say_hello2()
        print(f"Cycle created: {is_cycle_created()}")
    print(f"User count: {User.counter}")


main()
