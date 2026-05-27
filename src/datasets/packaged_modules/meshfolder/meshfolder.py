import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class MeshFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for MeshFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class MeshFolder(folder_based_builder.FolderBasedBuilder):
    BASE_FEATURE = datasets.Mesh
    BASE_COLUMN_NAME = "mesh"
    BUILDER_CONFIG_CLASS = MeshFolderConfig
    EXTENSIONS: list[str]  # definition at the bottom of the script


MESH_EXTENSIONS = [
    ".glb",
    ".ply",
    ".stl",
]
MeshFolder.EXTENSIONS = MESH_EXTENSIONS
