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

from dataclasses import dataclass

import datasets

from ..folder_based_builder import folder_based_builder


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class PdbFolderConfig(folder_based_builder.FolderBasedBuilderConfig):
    """BuilderConfig for PdbFolder.

    Args:
        drop_labels (`bool`, *optional*):
            Whether to drop folder-name labels.
        drop_metadata (`bool`, *optional*):
            Whether to drop metadata columns.
        include_hetatm (`bool`, defaults to `True`):
            Whether to include HETATM records (ligands, water, …) when decoding each structure.
        columns (`list[str]`, *optional*):
            Subset of PDBx/mmCIF atom columns to return per structure. Defaults to all columns.
    """

    drop_labels: bool = None
    drop_metadata: bool = None
    include_hetatm: bool = True
    columns: list[str] = None

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

    def _base_feature(self):
        return self.BASE_FEATURE(include_hetatm=self.config.include_hetatm, columns=self.config.columns)
