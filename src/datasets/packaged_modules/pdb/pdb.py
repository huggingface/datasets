"""PdbFolder - Load PDB protein structure files from directories.

Follows ImageFolder pattern: folder names become labels, supports metadata files.
Each row in the resulting dataset contains one complete PDB structure file,
following the "one row = one structure" pattern.

Usage:
    >>> from datasets import load_dataset
    >>> dataset = load_dataset("pdb", data_dir="./structures")

With folder-based labels:
    structures/
        enzymes/
            1abc.pdb
        receptors/
            2xyz.pdb

With metadata file:
    structures/
        metadata.csv  (columns: file_name, label, resolution, ...)
        1abc.pdb
        2def.ent
"""

import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


class PdbFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for PdbFolder."""

    drop_labels: bool = None
    drop_metadata: bool = None

    def __post_init__(self):
        super().__post_init__()


class PdbFolder(folder_based_builder.FolderBasedBuilder):
    """Folder-based builder for PDB protein structure files.

    Supports PDB format (.pdb, .ent).
    Each row in the resulting dataset contains one complete structure file,
    following the "one row = one structure" pattern recommended for ML workflows.
    """

    BASE_FEATURE = datasets.ProteinStructure
    BASE_COLUMN_NAME = "structure"
    BUILDER_CONFIG_CLASS = PdbFolderConfig
    EXTENSIONS: list[str] = [".pdb", ".ent"]
