"""PDB (Protein Data Bank) file loader for 3D structure data.

PDB is the legacy fixed-width format for representing 3D macromolecular structures.
While mmCIF is the modern standard, PDB remains widely used and many historical
datasets are in this format.

This implementation parses ATOM and HETATM records using fixed-width column positions
as defined by the official PDB format specification.
"""

import bz2
import gzip
import itertools
import lzma
from dataclasses import dataclass
from typing import Optional

import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.features.features import require_storage_cast
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


# PDB column definitions (0-indexed, end-exclusive)
# Based on https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html
PDB_ATOM_COLUMNS = {
    "record_type": (0, 6),      # ATOM or HETATM
    "atom_serial": (6, 11),     # Atom serial number
    "atom_name": (12, 16),      # Atom name
    "alt_loc": (16, 17),        # Alternate location indicator
    "residue_name": (17, 20),   # Residue name
    "chain_id": (21, 22),       # Chain identifier
    "residue_seq": (22, 26),    # Residue sequence number
    "insertion_code": (26, 27), # Code for insertions of residues
    "x": (30, 38),              # X coordinate (Angstroms)
    "y": (38, 46),              # Y coordinate (Angstroms)
    "z": (46, 54),              # Z coordinate (Angstroms)
    "occupancy": (54, 60),      # Occupancy
    "temp_factor": (60, 66),    # Temperature factor (B-factor)
    "element": (76, 78),        # Element symbol
    "charge": (78, 80),         # Charge
}

# Column type mapping
PDB_COLUMN_TYPES = {
    "record_type": pa.string(),
    "atom_serial": pa.int32(),
    "atom_name": pa.string(),
    "alt_loc": pa.string(),
    "residue_name": pa.string(),
    "chain_id": pa.string(),
    "residue_seq": pa.int32(),
    "insertion_code": pa.string(),
    "x": pa.float32(),
    "y": pa.float32(),
    "z": pa.float32(),
    "occupancy": pa.float32(),
    "temp_factor": pa.float32(),
    "element": pa.string(),
    "charge": pa.string(),
}

# Default columns for output
DEFAULT_PDB_COLUMNS = [
    "record_type",
    "atom_serial",
    "atom_name",
    "residue_name",
    "chain_id",
    "residue_seq",
    "x",
    "y",
    "z",
    "occupancy",
    "temp_factor",
    "element",
]


@dataclass
class PdbConfig(datasets.BuilderConfig):
    """BuilderConfig for PDB files.

    Args:
        features: Dataset features (optional, will be inferred if not provided).
        batch_size: Maximum number of atoms per batch.
        columns: Subset of columns to include. If None, uses default columns.
        record_types: List of record types to include ("ATOM", "HETATM", or both).
    """

    features: Optional[datasets.Features] = None
    batch_size: int = 100000
    columns: Optional[list[str]] = None
    record_types: Optional[list[str]] = None  # Default: ["ATOM", "HETATM"]


class Pdb(datasets.ArrowBasedBuilder):
    """Dataset builder for PDB files."""

    BUILDER_CONFIG_CLASS = PdbConfig

    # Supported PDB extensions
    EXTENSIONS: list[str] = [".pdb", ".ent"]

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        """Generate splits from data files."""
        if not self.config.data_files:
            raise ValueError(
                f"At least one data file must be specified, but got data_files={self.config.data_files}"
            )
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files = [dl_manager.iter_files(file) for file in files]
            splits.append(
                datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files})
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        """Cast Arrow table to configured features schema."""
        if self.config.features is not None:
            schema = self.config.features.arrow_schema
            if all(
                not require_storage_cast(feature)
                for feature in self.config.features.values()
            ):
                pa_table = pa_table.cast(schema)
            else:
                pa_table = table_cast(pa_table, schema)
            return pa_table
        return pa_table

    def _open_file(self, filepath: str):
        """Open file with automatic compression detection based on magic bytes."""
        with open(filepath, "rb") as f:
            magic = f.read(6)

        if magic[:2] == b"\x1f\x8b":  # gzip magic number
            return gzip.open(filepath, "rt", encoding="utf-8")
        elif magic[:3] == b"BZh":  # bzip2 magic number
            return bz2.open(filepath, "rt", encoding="utf-8")
        elif magic[:6] == b"\xfd7zXZ\x00":  # xz magic number
            return lzma.open(filepath, "rt", encoding="utf-8")
        else:
            return open(filepath, "r", encoding="utf-8")

    def _parse_atom_line(self, line: str) -> dict:
        """Parse a single ATOM/HETATM line using fixed-width columns.

        Args:
            line: A single line from the PDB file.

        Returns:
            Dictionary mapping column names to parsed values.
        """
        result = {}
        for col_name, (start, end) in PDB_ATOM_COLUMNS.items():
            if end <= len(line):
                value = line[start:end].strip()
            elif start < len(line):
                value = line[start:].strip()
            else:
                value = ""
            result[col_name] = value
        return result

    def _convert_value(self, value: str, dtype: pa.DataType):
        """Convert string value to appropriate Python type."""
        if not value or value == "":
            return None

        if pa.types.is_int32(dtype):
            try:
                return int(value)
            except ValueError:
                return None
        elif pa.types.is_float32(dtype):
            try:
                return float(value)
            except ValueError:
                return None
        else:
            return value if value else None

    def _get_columns(self) -> list[str]:
        """Get the list of columns to include in output."""
        if self.config.columns is not None:
            return self.config.columns
        return DEFAULT_PDB_COLUMNS

    def _get_record_types(self) -> set[str]:
        """Get the set of record types to include."""
        if self.config.record_types is not None:
            return set(self.config.record_types)
        return {"ATOM", "HETATM"}

    def _get_schema(self, columns: list[str]) -> pa.Schema:
        """Return Arrow schema for the selected columns."""
        fields = []
        for col in columns:
            dtype = PDB_COLUMN_TYPES.get(col, pa.string())
            fields.append(pa.field(col, dtype))
        return pa.schema(fields)

    def _generate_tables(self, files):
        """Generate Arrow tables from PDB files.

        Args:
            files: Iterable of file iterables from _split_generators.

        Yields:
            Tuple of (Key, pa.Table) for each batch.
        """
        requested_columns = self._get_columns()
        record_types = self._get_record_types()
        schema = self._get_schema(requested_columns)

        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            batch_idx = 0
            batch = {col: [] for col in requested_columns}
            batch_count = 0

            with self._open_file(file) as fp:
                for line in fp:
                    # Check if this is an ATOM or HETATM record
                    record_type = line[:6].strip()
                    if record_type not in record_types:
                        continue

                    # Parse the line
                    parsed = self._parse_atom_line(line)

                    # Add values to batch
                    for col in requested_columns:
                        raw_value = parsed.get(col, "")
                        dtype = PDB_COLUMN_TYPES.get(col, pa.string())
                        converted = self._convert_value(raw_value, dtype)
                        batch[col].append(converted)

                    batch_count += 1

                    # Yield batch if full
                    if batch_count >= self.config.batch_size:
                        pa_table = pa.Table.from_pydict(batch, schema=schema)
                        yield Key(file_idx, batch_idx), self._cast_table(pa_table)
                        batch = {col: [] for col in requested_columns}
                        batch_count = 0
                        batch_idx += 1

            # Yield remaining records
            if batch_count > 0:
                pa_table = pa.Table.from_pydict(batch, schema=schema)
                yield Key(file_idx, batch_idx), self._cast_table(pa_table)
