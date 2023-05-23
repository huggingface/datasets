from fsspec.implementations.local import LocalFileSystem


class FuseFileSystem(LocalFileSystem):
    """
    `datasets.filesystems.FuseFileSystem` is a subclass of `fsspec`'s [`LocalFileSystem`](https://filesystem-spec.readthedocs.io/en/latest/api.html#fsspec.implementations.local.LocalFileSystem).

    Users can use this class to access FUSE-mounted files. The `datasets` library treats this class as a remote file
    system to make file moving and renaming more efficient.
    """


def create_fuse_file_system(fs: LocalFileSystem):
    """Creates a FuseFileSystem by copying over attributes from an `LocalFileSystem`."""
    fuse_fs = FuseFileSystem()
    fuse_fs.__dict__.update(fs.__dict__)
