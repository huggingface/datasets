from .logging import get_logger


logger = get_logger(__name__)


class _PatchedModuleObj:
    """Set all the modules components as attributes of the _PatchedModuleObj object."""

    def __init__(self, module):
        if module is not None:
            for key in getattr(module, "__all__", module.__dict__):
                if not key.startswith("__"):
                    setattr(self, key, getattr(module, key))


class patch_submodule:
    """
    Patch a submodule attribute of an object, by keeping all other submodules intact at all levels.

    Examples:

        >>> import importlib
        >>> from datasets.load import prepare_module
        >>> from datasets.streaming import patch_submodule, xjoin
        >>>
        >>> snli_module_path, _ = prepare_module("snli")
        >>> snli_module = importlib.import_module(snli_module_path)
        >>> patcher = patch_submodule(snli_module, "os.path.join", xjoin)
        >>> patcher.start()
        >>> assert snli_module.os.path.join is xjoin
    """

    _active_patches = []

    def __init__(self, obj, target: str, new):
        self.obj = obj
        self.target = target
        self.new = new
        self.key = target.split(".")[0]
        self.original = getattr(obj, self.key, None)

    def __enter__(self):
        *submodules, attr = self.target.split(".")
        current = self.obj
        for key in submodules:
            setattr(current, key, _PatchedModuleObj(getattr(current, key, None)))
            current = getattr(current, key)
        setattr(current, attr, self.new)

    def __exit__(self, *exc_info):
        setattr(self.obj, self.key, self.original)

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
