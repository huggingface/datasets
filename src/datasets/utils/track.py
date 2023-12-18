from collections.abc import Iterator
from typing import Iterable


class tracked_str(str):
    origins = {}

    def set_origin(self, origin: str):
        if super().__repr__() not in self.origins:
            self.origins[super().__repr__()] = origin

    def get_origin(self):
        return self.origins.get(super().__repr__(), str(self))

    def __repr__(self) -> str:
        if super().__repr__() not in self.origins or self.origins[super().__repr__()] == self:
            return super().__repr__()
        else:
            return f"{str(self)} (origin={self.origins[super().__repr__()]})"


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


class TrackedIterable(Iterable):
    def __init__(self) -> None:
        super().__init__()
        self.last_item = None

    def __repr__(self) -> str:
        if self.last_item is None:
            super().__repr__()
        else:
            return f"{self.__class__.__name__}(current={self.last_item})"
