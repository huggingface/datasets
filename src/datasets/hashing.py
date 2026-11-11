"""Control how the functions passed to `Dataset.map` and `Dataset.filter` are hashed for caching."""

from typing import Callable, Optional


# Name of the function attribute that stores the `fn_kwargs` keys to leave out of the fingerprint.
IGNORE_KWARGS_ATTRIBUTE = "_datasets_fingerprint_ignore_kwargs"


def register(ignore_kwargs: list[str]) -> Callable[[Callable], Callable]:
    """Register how a processing function is hashed by [`Dataset.map`] and [`Dataset.filter`].

    The keys of `fn_kwargs` listed in `ignore_kwargs` are not used to compute the fingerprint of the
    resulting dataset, so changing their values doesn't invalidate the cache. Use it for arguments that
    don't change the output of the function, e.g. a logging flag or an object that can't be hashed.

    Args:
        ignore_kwargs (`list[str]`):
            Names of the keyword arguments of the function to leave out of the fingerprint.

    Example:

    ```py
    >>> import datasets
    >>> @datasets.hashing.register(ignore_kwargs=["verbose"])
    ... def add_length(example, verbose=False):
    ...     if verbose:
    ...         print(example)
    ...     return {"length": len(example["text"])}
    >>> ds = ds.map(add_length, fn_kwargs={"verbose": True})  # same fingerprint and cache as with verbose=False
    ```
    """
    if not isinstance(ignore_kwargs, (list, tuple)) or not all(isinstance(name, str) for name in ignore_kwargs):
        raise TypeError(f"ignore_kwargs should be a list of argument names, but got {ignore_kwargs!r}.")

    def decorator(function: Callable) -> Callable:
        setattr(function, IGNORE_KWARGS_ATTRIBUTE, sorted(set(ignore_kwargs)))
        return function

    return decorator


def get_ignore_kwargs(function: Optional[Callable]) -> list[str]:
    """Return the `fn_kwargs` keys registered with [`register`] for `function`, or an empty list."""
    return getattr(function, IGNORE_KWARGS_ATTRIBUTE, [])
