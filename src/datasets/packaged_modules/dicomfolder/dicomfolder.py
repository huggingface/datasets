import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class DicomFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for DicomFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class DicomFolder(folder_based_builder.FolderBasedBuilder):
    BASE_FEATURE = datasets.Dicom
    BASE_COLUMN_NAME = "dicom"
    BUILDER_CONFIG_CLASS = DicomFolderConfig
    EXTENSIONS: list[str] = [".dcm", ".dicom"]
