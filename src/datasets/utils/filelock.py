# deprecated, please use the `filelock` package instead

from filelock import (  # noqa: F401 # imported for backward compatibility
    BaseFileLock,
    SoftFileLock,
    Timeout,
    UnixFileLock,
    WindowsFileLock,
)

from ._filelock import FileLock  # noqa: F401 # imported for backward compatibility
