"""mmCIF (macromolecular CIF) file loader for 3D structure data.

mmCIF is the modern standard format for representing 3D macromolecular structures,
used by the Protein Data Bank (PDB) since 2014.

This implementation uses a lightweight pure Python parser for the CIF syntax,
requiring zero external dependencies.
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


# Default columns for atom_site category (most commonly used for ML)
DEFAULT_ATOM_SITE_COLUMNS = [
    "id",
    "type_symbol",
    "label_atom_id",
    "label_comp_id",
    "label_asym_id",
    "label_seq_id",
    "Cartn_x",
    "Cartn_y",
    "Cartn_z",
    "occupancy",
    "B_iso_or_equiv",
]

# Column type mapping for atom_site
ATOM_SITE_TYPES = {
    "id": pa.int32(),
    "type_symbol": pa.string(),
    "label_atom_id": pa.string(),
    "label_alt_id": pa.string(),
    "label_comp_id": pa.string(),
    "label_asym_id": pa.string(),
    "label_entity_id": pa.string(),
    "label_seq_id": pa.int32(),
    "pdbx_PDB_ins_code": pa.string(),
    "Cartn_x": pa.float32(),
    "Cartn_y": pa.float32(),
    "Cartn_z": pa.float32(),
    "occupancy": pa.float32(),
    "B_iso_or_equiv": pa.float32(),
    "pdbx_formal_charge": pa.int32(),
    "auth_seq_id": pa.int32(),
    "auth_comp_id": pa.string(),
    "auth_asym_id": pa.string(),
    "auth_atom_id": pa.string(),
    "pdbx_PDB_model_num": pa.int32(),
    "group_PDB": pa.string(),
}


@dataclass
class MmcifConfig(datasets.BuilderConfig):
    """BuilderConfig for mmCIF files.

    Args:
        features: Dataset features (optional, will be inferred if not provided).
        batch_size: Maximum number of atoms per batch.
        columns: Subset of atom_site columns to include. If None, uses default columns.
        include_hetatm: Whether to include HETATM records (ligands, water, etc.).
    """

    features: Optional[datasets.Features] = None
    batch_size: int = 100000
    columns: Optional[list[str]] = None
    include_hetatm: bool = True


class Mmcif(datasets.ArrowBasedBuilder):
    """Dataset builder for mmCIF files."""

    BUILDER_CONFIG_CLASS = MmcifConfig

    # Supported mmCIF extensions
    EXTENSIONS: list[str] = [".cif", ".mmcif"]

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

    def _tokenize_value(self, text: str, pos: int) -> tuple[str, int]:
        """Parse a single CIF value starting at position pos.

        Handles:
        - Quoted strings (single or double quotes)
        - Semicolon-delimited multi-line strings
        - Unquoted values
        """
        # Skip whitespace
        while pos < len(text) and text[pos] in " \t":
            pos += 1

        if pos >= len(text) or text[pos] == "\n":
            return "", pos

        char = text[pos]

        # Single or double quoted string
        if char in "'\"":
            end = pos + 1
            while end < len(text) and text[end] != char:
                end += 1
            value = text[pos + 1 : end]
            return value, end + 1

        # Semicolon-delimited multi-line string
        if char == ";":
            # Find closing semicolon at start of line
            end = pos + 1
            while end < len(text):
                newline_pos = text.find("\n", end)
                if newline_pos == -1:
                    break
                if newline_pos + 1 < len(text) and text[newline_pos + 1] == ";":
                    value = text[pos + 1 : newline_pos]
                    return value.strip(), newline_pos + 2
                end = newline_pos + 1
            return "", len(text)

        # Unquoted value (ends at whitespace)
        end = pos
        while end < len(text) and text[end] not in " \t\n":
            end += 1
        return text[pos:end], end

    def _parse_loop(self, lines: list[str], start_idx: int) -> tuple[dict, int]:
        """Parse a loop_ construct starting at start_idx.

        Returns:
            Tuple of (data_dict, end_index) where data_dict maps column names to value lists.
        """
        idx = start_idx + 1  # Skip 'loop_' line
        columns = []

        # Collect column names (lines starting with _)
        while idx < len(lines):
            line = lines[idx].strip()
            if not line or line.startswith("#"):
                idx += 1
                continue
            if line.startswith("_"):
                columns.append(line)
                idx += 1
            else:
                break

        # Initialize data dict
        data = {col: [] for col in columns}
        num_cols = len(columns)

        if num_cols == 0:
            return data, idx

        # Parse data values
        values = []
        while idx < len(lines):
            line = lines[idx]
            stripped = line.strip()

            # Stop conditions
            if not stripped:
                idx += 1
                continue
            if stripped.startswith("#"):
                idx += 1
                continue
            if stripped.startswith("_") or stripped.startswith("loop_") or stripped.startswith("data_"):
                break

            # Handle semicolon-delimited multi-line values
            if stripped.startswith(";"):
                # Collect until closing semicolon
                value_lines = []
                idx += 1
                while idx < len(lines):
                    if lines[idx].strip().startswith(";"):
                        idx += 1
                        break
                    value_lines.append(lines[idx])
                    idx += 1
                values.append("\n".join(value_lines).strip())
                continue

            # Parse inline values
            pos = 0
            while pos < len(line):
                # Skip whitespace
                while pos < len(line) and line[pos] in " \t":
                    pos += 1
                if pos >= len(line):
                    break

                value, pos = self._tokenize_value(line, pos)
                if value or value == "":
                    values.append(value)

            idx += 1

        # Distribute values to columns
        for i, value in enumerate(values):
            col_idx = i % num_cols
            data[columns[col_idx]].append(value)

        return data, idx

    def _parse_mmcif(self, fp) -> dict:
        """Parse mmCIF file and extract atom_site data.

        Args:
            fp: File-like object opened in text mode.

        Returns:
            Dictionary mapping column names to value lists for atom_site category.
        """
        content = fp.read()
        lines = content.split("\n")

        atom_site_data = {}
        idx = 0

        while idx < len(lines):
            line = lines[idx].strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                idx += 1
                continue

            # Look for loop_ constructs
            if line.startswith("loop_"):
                # Check if next non-empty line starts with _atom_site
                peek_idx = idx + 1
                while peek_idx < len(lines) and not lines[peek_idx].strip():
                    peek_idx += 1

                if peek_idx < len(lines) and lines[peek_idx].strip().startswith("_atom_site."):
                    data, idx = self._parse_loop(lines, idx)
                    # Merge atom_site data
                    for key, values in data.items():
                        if key.startswith("_atom_site."):
                            col_name = key.replace("_atom_site.", "")
                            atom_site_data[col_name] = values
                else:
                    idx += 1
            else:
                idx += 1

        return atom_site_data

    def _get_columns(self) -> list[str]:
        """Get the list of columns to include in output."""
        if self.config.columns is not None:
            return self.config.columns
        return DEFAULT_ATOM_SITE_COLUMNS

    def _get_schema(self, columns: list[str], available_columns: set[str]) -> pa.Schema:
        """Return Arrow schema for the selected columns."""
        fields = []
        for col in columns:
            if col in available_columns:
                dtype = ATOM_SITE_TYPES.get(col, pa.string())
                fields.append(pa.field(col, dtype))
        return pa.schema(fields)

    def _convert_value(self, value: str, dtype: pa.DataType) -> any:
        """Convert string value to appropriate Python type."""
        # Handle missing values (. or ?)
        if value in (".", "?", ""):
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
            return value

    def _generate_tables(self, files):
        """Generate Arrow tables from mmCIF files.

        Args:
            files: Iterable of file iterables from _split_generators.

        Yields:
            Tuple of (Key, pa.Table) for each batch.
        """
        requested_columns = self._get_columns()

        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            with self._open_file(file) as fp:
                atom_site_data = self._parse_mmcif(fp)

            if not atom_site_data:
                continue

            # Determine available columns
            available_columns = set(atom_site_data.keys())

            # Filter to requested columns that are available
            columns = [col for col in requested_columns if col in available_columns]

            if not columns:
                logger.warning(
                    f"No requested columns found in {file}. "
                    f"Available: {available_columns}, Requested: {requested_columns}"
                )
                continue

            # Get number of atoms
            first_col = columns[0]
            num_atoms = len(atom_site_data[first_col])

            if num_atoms == 0:
                continue

            # Filter HETATM if configured
            include_indices = None
            if not self.config.include_hetatm and "group_PDB" in atom_site_data:
                include_indices = [
                    i for i, group in enumerate(atom_site_data["group_PDB"])
                    if group == "ATOM"
                ]

            # Build schema
            schema = self._get_schema(columns, available_columns)

            # Process in batches
            batch_size = self.config.batch_size
            batch_idx = 0

            for start in range(0, num_atoms, batch_size):
                end = min(start + batch_size, num_atoms)
                batch = {}

                for col in columns:
                    dtype = ATOM_SITE_TYPES.get(col, pa.string())
                    raw_values = atom_site_data[col][start:end]

                    if include_indices is not None:
                        # Filter to only ATOM records
                        raw_values = [
                            raw_values[i - start]
                            for i in include_indices
                            if start <= i < end
                        ]

                    # Convert values
                    converted = [self._convert_value(v, dtype) for v in raw_values]
                    batch[col] = converted

                # Skip empty batches
                if not batch[columns[0]]:
                    continue

                pa_table = pa.Table.from_pydict(batch, schema=schema)
                yield Key(file_idx, batch_idx), self._cast_table(pa_table)
                batch_idx += 1
