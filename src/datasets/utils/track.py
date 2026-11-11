from collections.abc import Iterable, Iterator
from urllib.parse import urlsplit, urlunsplit


def _sanitize_origin(origin: str) -> str:
    """Strip userinfo and query from origin URLs before embedding them in reprs/errors.

    Keeps scheme/host/path (e.g. hf://…) for debugging while avoiding leaking basic-auth
    credentials or presigned-URL query parameters into logs and tracebacks.
    """
    parts = urlsplit(origin)
    if not parts.scheme:
        return origin
    netloc = parts.netloc.rsplit("@", 1)[-1] if "@" in parts.netloc else parts.netloc
    if netloc == parts.netloc and not parts.query:
        return origin
    return urlunsplit((parts.scheme, netloc, parts.path, "", parts.fragment))


class tracked_str(str):
    origins = {}

    def set_origin(self, origin: str):
        if super().__repr__() not in self.origins:
            self.origins[super().__repr__()] = origin

    def get_origin(self):
        return self.origins.get(super().__repr__(), str(self))

    def __repr__(self) -> str:
        origin = self.origins.get(super().__repr__())
        if origin is None or origin == self:
            return super().__repr__()
        return f"{super().__repr__()} (origin={_sanitize_origin(origin)})"


class tracked_list(list):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.last_item = None

    def __iter__(self) -> Iterator:
        for x in super().__iter__():
            self.last_item = x
            yield x
        self.last_item = None

    def __repr__(self) -> str:
        if self.last_item is None:
            return super().__repr__()
        else:
            return f"{self.__class__.__name__}(current={self.last_item})"


class TrackedIterableFromGenerator(Iterable):
    """Utility class to create an iterable from a generator function, in order to reset the generator when needed."""

    def __init__(self, generator, *args):
        super().__init__()
        self.generator = generator
        self.args = args
        self.last_item = None

    def __iter__(self):
        for x in self.generator(*self.args):
            self.last_item = x
            yield x
        self.last_item = None

    def __repr__(self) -> str:
        if self.last_item is None:
            return super().__repr__()
        else:
            return f"{self.__class__.__name__}(current={self.last_item})"

    def __reduce__(self):
        return (self.__class__, (self.generator, *self.args))
