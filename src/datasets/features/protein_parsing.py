"""Dependency-free parsers for protein 3D structure files (PDB and mmCIF).

Both formats are parsed into a *struct-of-arrays* keyed by
[PDBx/mmCIF dictionary](https://mmcif.wwpdb.org/) ``_atom_site`` column names, so
that PDB- and mmCIF-derived datasets expose the same column vocabulary. PDB
fixed-width records are mapped onto the mmCIF-native names; mmCIF ``_atom_site``
loops are read directly.

The schema (column names and Arrow dtypes) lives in a single mapping,
[`PROTEIN_ATOM_TYPES`], reused by both parsers and by the
[`~datasets.ProteinStructure`] feature — there is no per-format duplication of
the column list or its types.
"""

from __future__ import annotations

import pyarrow as pa


# Canonical column -> Arrow dtype table (PDBx/mmCIF `_atom_site` dictionary names).
# Single source of truth for both parsers and the ProteinStructure feature.
PROTEIN_ATOM_TYPES: dict[str, pa.DataType] = {
    "group_PDB": pa.string(),  # "ATOM" / "HETATM"; drives include_hetatm, not emitted by default
    "id": pa.int32(),
    "type_symbol": pa.string(),
    "label_atom_id": pa.string(),
    "label_comp_id": pa.string(),
    "label_asym_id": pa.string(),
    "label_seq_id": pa.int32(),
    "Cartn_x": pa.float32(),
    "Cartn_y": pa.float32(),
    "Cartn_z": pa.float32(),
    "occupancy": pa.float32(),
    "B_iso_or_equiv": pa.float32(),
}

# Default emitted columns (everything except the internal record-group flag).
DEFAULT_ATOM_COLUMNS: list[str] = [col for col in PROTEIN_ATOM_TYPES if col != "group_PDB"]

# PDB fixed-width column ranges (0-indexed, end-exclusive), per the wwPDB
# format-33 spec, expressed against the canonical mmCIF column names.
# https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html
PDB_FIELD_SPANS: dict[str, tuple[int, int]] = {
    "group_PDB": (0, 6),
    "id": (6, 11),
    "label_atom_id": (12, 16),
    "label_comp_id": (17, 20),
    "label_asym_id": (21, 22),
    "label_seq_id": (22, 26),
    "Cartn_x": (30, 38),
    "Cartn_y": (38, 46),
    "Cartn_z": (46, 54),
    "occupancy": (54, 60),
    "B_iso_or_equiv": (60, 66),
    "type_symbol": (76, 78),
}

_MMCIF_RECORD_GROUP = "group_PDB"
_ATOM_RECORD = "ATOM"


def _convert(value: str, dtype: pa.DataType):
    """Coerce a raw string token to the Arrow dtype's Python type, or None if empty/invalid.

    mmCIF uses ``.`` and ``?`` for missing values; both map to None.
    """
    if value is None or value == "" or value in (".", "?"):
        return None
    if pa.types.is_integer(dtype):
        try:
            return int(value)
        except ValueError:
            return None
    if pa.types.is_floating(dtype):
        try:
            return float(value)
        except ValueError:
            return None
    return value


def _resolve_columns(columns: list[str] | None) -> list[str]:
    """Validate a requested column subset against the canonical schema.

    Returns the default columns when ``columns`` is None. Raises ValueError on any
    unknown name rather than silently dropping it.
    """
    if columns is None:
        return list(DEFAULT_ATOM_COLUMNS)
    unknown = [c for c in columns if c not in PROTEIN_ATOM_TYPES]
    if unknown:
        raise ValueError(f"Unknown protein atom column(s) {unknown}. Valid columns are: {sorted(PROTEIN_ATOM_TYPES)}")
    return list(columns)


def parse_pdb_atoms(text: str, columns: list[str] | None = None, include_hetatm: bool = True) -> dict[str, list]:
    """Parse PDB ATOM/HETATM records into a struct-of-arrays.

    Args:
        text (`str`):
            Raw PDB file content.
        columns (`list[str]`, *optional*):
            Subset of [`PROTEIN_ATOM_TYPES`] columns to return. Defaults to
            [`DEFAULT_ATOM_COLUMNS`].
        include_hetatm (`bool`, defaults to `True`):
            Whether to include HETATM records (ligands, water, …). When `False`,
            only `ATOM` records are kept.

    Returns:
        `dict[str, list]`: Mapping of column name to a list of per-atom values.
    """
    requested = _resolve_columns(columns)
    atoms: dict[str, list] = {col: [] for col in requested}

    for line in text.splitlines():
        record = line[slice(*PDB_FIELD_SPANS[_MMCIF_RECORD_GROUP])].strip()
        if record not in ("ATOM", "HETATM"):
            continue
        if not include_hetatm and record != _ATOM_RECORD:
            continue
        for col in requested:
            start, end = PDB_FIELD_SPANS[col]
            raw = line[start:end].strip() if start < len(line) else ""
            atoms[col].append(_convert(raw, PROTEIN_ATOM_TYPES[col]))

    return atoms


def _tokenize_cif_line(line: str) -> list[str]:
    """Tokenize a single inline mmCIF data line, honoring single/double quotes."""
    tokens: list[str] = []
    pos = 0
    n = len(line)
    while pos < n:
        while pos < n and line[pos] in " \t":
            pos += 1
        if pos >= n:
            break
        char = line[pos]
        if char in "'\"":
            end = pos + 1
            while end < n and line[end] != char:
                end += 1
            tokens.append(line[pos + 1 : end])
            pos = end + 1
        else:
            end = pos
            while end < n and line[end] not in " \t":
                end += 1
            tokens.append(line[pos:end])
            pos = end
    return tokens


def parse_mmcif_atoms(text: str, columns: list[str] | None = None, include_hetatm: bool = True) -> dict[str, list]:
    """Parse an mmCIF ``_atom_site`` loop into a struct-of-arrays.

    Each ``_atom_site`` row is one whitespace-separated line of simple tokens, as
    produced by the wwPDB; the multi-line semicolon-delimited text values that the
    CIF grammar allows for free-text categories do not occur in coordinate loops,
    so rows are tokenized one line at a time.

    Args:
        text (`str`):
            Raw mmCIF file content.
        columns (`list[str]`, *optional*):
            Subset of [`PROTEIN_ATOM_TYPES`] columns to return. Defaults to
            [`DEFAULT_ATOM_COLUMNS`].
        include_hetatm (`bool`, defaults to `True`):
            Whether to include HETATM records. When `False`, only `_atom_site`
            rows whose `group_PDB` is `ATOM` are kept.

    Returns:
        `dict[str, list]`: Mapping of column name to a list of per-atom values.
    """
    requested = _resolve_columns(columns)
    lines = text.splitlines()

    # Locate the `_atom_site` loop and collect its column order.
    loop_columns: list[str] = []
    idx = 0
    n = len(lines)
    while idx < n:
        if lines[idx].strip() == "loop_":
            peek = idx + 1
            header: list[str] = []
            while peek < n and lines[peek].strip().startswith("_"):
                header.append(lines[peek].strip())
                peek += 1
            if header and header[0].startswith("_atom_site."):
                loop_columns = [h.split(".", 1)[1] for h in header]
                idx = peek
                break
            idx = peek
        else:
            idx += 1

    atoms: dict[str, list] = {col: [] for col in requested}
    if not loop_columns:
        return atoms

    col_index = {name: i for i, name in enumerate(loop_columns)}
    group_pos = col_index.get(_MMCIF_RECORD_GROUP)

    # Consume data rows until the loop ends (blank line, comment, or new block/loop).
    while idx < n:
        stripped = lines[idx].strip()
        if stripped == "" or stripped.startswith("#"):
            idx += 1
            continue
        if stripped.startswith("_") or stripped.startswith("loop_") or stripped.startswith("data_"):
            break
        tokens = _tokenize_cif_line(lines[idx])
        idx += 1
        if len(tokens) < len(loop_columns):
            continue
        if not include_hetatm and group_pos is not None and tokens[group_pos] != _ATOM_RECORD:
            continue
        for col in requested:
            pos = col_index.get(col)
            raw = tokens[pos] if pos is not None and pos < len(tokens) else ""
            atoms[col].append(_convert(raw, PROTEIN_ATOM_TYPES[col]))

    return atoms
