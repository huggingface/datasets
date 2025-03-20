import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class PdfFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for ImageFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class PdfFolder(folder_based_builder.FolderBasedBuilder):
    BASE_FEATURE = datasets.Pdf
    BASE_COLUMN_NAME = "pdf"
    BUILDER_CONFIG_CLASS = PdfFolderConfig
    EXTENSIONS: list[str] = [".pdf"]
