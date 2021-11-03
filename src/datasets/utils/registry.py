from inspect import isclass
from typing import Any, Callable, Optional

from catalogue import InFunc, Registry

from datasets.utils.py_utils import get_qualname_from_cls


class DatasetsRegistry(Registry):
    """The original catalogue.Registry is restricted to using strings as the registry key.
    In our case we want to extend this to classes specifically. This allows users to register
    specific functions that have to be used to hash objects with a specific class.

    To make this work consistently, we get the full module name + the class' qualname of the object
    (py_utils.get_qualname_from_cls), which allows us to later retrieve the class
    (py_utils.get_cls_from_qualname).
    """

    # TODO: also incorporate other functions: get_all, get_entry_points, get_entry_point
    # Do not think find() is necessary as it calls get() anyway
    @staticmethod
    def get_arg_as_str(name: Any) -> str:
        if isclass(name):
            name = get_qualname_from_cls(name)
        elif not isinstance(name, str):
            name = repr(name)
        return name

    def __contains__(self, name: Any) -> bool:
        return super().__contains__(self.get_arg_as_str(name))

    def __call__(self, name: Any, func: Optional[Any] = None) -> Callable[[InFunc], InFunc]:
        return super().__call__(self.get_arg_as_str(name), func=func)

    def register(self, name: Any, *, func: Optional[Any] = None) -> Callable[[InFunc], InFunc]:
        return super().register(self.get_arg_as_str(name), func=func)

    def get(self, name: Any) -> Any:
        return super().get(self.get_arg_as_str(name))


hashers = DatasetsRegistry(("datasets_registry", "hashers"))
