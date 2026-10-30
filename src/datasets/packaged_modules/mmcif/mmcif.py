"""MmcifFolder - Load mmCIF protein structure files from directories.

Follows ImageFolder pattern: folder names become labels, supports metadata files.
Each row in the resulting dataset contains one structure, read with biotite
into an `AtomicStructure` column.

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

from dataclasses import dataclass

import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class MmcifFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for MmcifFolder.

    Args:
        drop_labels (`bool`, *optional*):
            Whether to drop folder-name labels.
        drop_metadata (`bool`, *optional*):
            Whether to drop metadata columns.
    """

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class MmcifFolder(folder_based_builder.FolderBasedBuilder):
    """Folder-based builder for mmCIF protein structure files.

    Supports PDBx/mmCIF (.cif, .mmcif) and BinaryCIF (.bcif).
    Each row in the resulting dataset contains one complete structure file,
    following the "one row = one structure" pattern recommended for ML workflows.
    """

    BASE_FEATURE = datasets.AtomicStructure
    BASE_COLUMN_NAME = "structure"
    BUILDER_CONFIG_CLASS = MmcifFolderConfig
    EXTENSIONS: list[str] = [".cif", ".mmcif", ".bcif"]
