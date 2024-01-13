import contextlib
import gc
import types


# Thanks to aaron from 
# https://stackoverflow.com/questions/67157372/how-to-test-for-a-reference-cycle-caused-by-saved-exception
def get_exception_ids_with_reference_cycle(exclude_ids=None):
    exclude_ids = () if exclude_ids is None else exclude_ids
    exceptions = [
        o
        for o in gc.get_objects(generation=0)
        if isinstance(o, Exception) and id(o) not in exclude_ids
    ]
    exception_ids = [
        id(e)
        for e in exceptions
        if len(gc.get_referrers(e)) == 2
        and all(
            isinstance(r, types.FrameType) or r is exceptions
            for r in gc.get_referrers(e)
        )
    ]
    return exception_ids


@contextlib.contextmanager
def exception_reference_cycle_watcher():
    exception_ids = get_exception_ids_with_reference_cycle()
    yield lambda: bool(
        get_exception_ids_with_reference_cycle(exclude_ids=exception_ids)
    )
