from importlib import import_module

from .logging import get_logger


logger = get_logger(__name__)


class _PatchedModuleObj:
    """Set all the modules components as attributes of the _PatchedModuleObj object."""

    def __init__(self, module, attrs=None):
        attrs = attrs or []
        if module is not None:
            for key in module.__dict__:
                if key in attrs or not key.startswith("__"):
                    setattr(self, key, getattr(module, key))


class patch_submodule:
    """
    Patch a submodule attribute of an object, by keeping all other submodules intact at all levels.

    Example::

        >>> import importlib
        >>> from datasets.load import dataset_module_factory
        >>> from datasets.streaming import patch_submodule, xjoin
        >>>
        >>> dataset_module = dataset_module_factory("snli")
        >>> snli_module = importlib.import_module(dataset_module.module_path)
        >>> patcher = patch_submodule(snli_module, "os.path.join", xjoin)
        >>> patcher.start()
        >>> assert snli_module.os.path.join is xjoin
    """

    _active_patches = []

    def __init__(self, obj, target: str, new, attrs=None):
        self.obj = obj
        self.target = target
        self.new = new
        self.key = target.split(".")[0]
        self.original = {}
        self.attrs = attrs or []

    def __enter__(self):
        *submodules, target_attr = self.target.split(".")
        # Patch modules
        # e.g. to patch "os.path.join" we need to patch "os" and "os.path"
        for i in range(len(submodules)):
            submodule = import_module(".".join(submodules[: i + 1]))
            for attr in self.obj.__dir__():
                if getattr(self.obj, attr) is submodule:
                    self.original[attr] = getattr(self.obj, attr)
                    # patch at top level
                    setattr(self.obj, attr, _PatchedModuleObj(submodule, attrs=self.attrs))
                    patched = getattr(self.obj, attr)
                    # construct lower levels patches
                    for key in submodules[i + 1 :]:
                        setattr(patched, key, _PatchedModuleObj(getattr(patched, key, None), attrs=self.attrs))
                        patched = getattr(patched, key)
                    # finally set the target attribute
                    setattr(patched, target_attr, self.new)
        # Patch attribute itself
        # e.g. to patch "os.path.join" we may also need to patch "join"
        # itself if it was imported as "from os.path import join"
        # It can also be a builtin object
        attr_value = (
            getattr(import_module(".".join(submodules)), target_attr)
            if submodules
            else globals()["__builtins__"][target_attr]
        )
        for attr in self.obj.__dir__():
            if getattr(self.obj, attr) is attr_value:
                self.original[attr] = getattr(self.obj, attr)
                setattr(self.obj, attr, self.new)

    def __exit__(self, *exc_info):
        for attr in list(self.original):
            setattr(self.obj, attr, self.original.pop(attr))

    def start(self):
        """Activate a patch."""
        self.__enter__()
        self._active_patches.append(self)

    def stop(self):
        """Stop an active patch."""
        try:
            self._active_patches.remove(self)
        except ValueError:
            # If the patch hasn't been started this will fail
            return None

        return self.__exit__()
