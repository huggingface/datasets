import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class NiftiFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for NiftiFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class NiftiFolder(folder_based_builder.FolderBasedBuilder):
    BASE_FEATURE = datasets.Nifti
    BASE_COLUMN_NAME = "nifti"
    BUILDER_CONFIG_CLASS = NiftiFolderConfig
    EXTENSIONS: list[str] = [".nii", ".nii.gz"]
