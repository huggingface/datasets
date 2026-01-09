"""MmcifFolder - Load mmCIF protein structure files from directories.

Follows ImageFolder pattern: folder names become labels, supports metadata files.
Each row in the resulting dataset contains one complete mmCIF structure file,
following the "one row = one structure" pattern.

Usage:
    >>> from datasets import load_dataset
    >>> dataset = load_dataset("mmcif", data_dir="./structures")

With folder-based labels:
    structures/
        enzymes/
            1abc.cif
        receptors/
            2xyz.mmcif

With metadata file:
    structures/
        metadata.csv  (columns: file_name, label, resolution, ...)
        1abc.cif
        2def.mmcif
"""

import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class MmcifFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for MmcifFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class MmcifFolder(folder_based_builder.FolderBasedBuilder):
    """Folder-based builder for mmCIF protein structure files.

    Supports mmCIF format (.cif, .mmcif).
    Each row in the resulting dataset contains one complete structure file,
    following the "one row = one structure" pattern recommended for ML workflows.
    """

    BASE_FEATURE = datasets.ProteinStructure
    BASE_COLUMN_NAME = "structure"
    BUILDER_CONFIG_CLASS = MmcifFolderConfig
    EXTENSIONS: list[str] = [".cif", ".mmcif"]
