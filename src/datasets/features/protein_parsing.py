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

Only ``_atom_site`` data is represented. PDB records that describe something other
than an atom (TER, ANISOU, CONECT, and the header) have no place in a per-atom table
and are not read.
"""

from __future__ import annotations

import string
from typing import Callable

import pyarrow as pa


# Canonical column -> Arrow dtype table (PDBx/mmCIF `_atom_site` dictionary names).
# Single source of truth for both parsers and the ProteinStructure feature.
#
# Residue and chain identifiers are the *author* ones (`auth_*`): they are the only
# numbering a PDB file carries, and in mmCIF they are what matches the PDB numbering,
# so rows from either format line up. `label_seq_id` in mmCIF is a separate,
# sequential numbering that PDB files cannot supply.
PROTEIN_ATOM_TYPES: dict[str, pa.DataType] = {
    "group_PDB": pa.string(),  # "ATOM" / "HETATM"; drives include_hetatm, not emitted by default
    "id": pa.int32(),
    "type_symbol": pa.string(),
    "label_atom_id": pa.string(),
    "label_alt_id": pa.string(),  # alternate location indicator; None when absent
    "label_comp_id": pa.string(),
    "auth_asym_id": pa.string(),
    "auth_seq_id": pa.int32(),
    "pdbx_PDB_ins_code": pa.string(),  # residue insertion code; None when absent
    "Cartn_x": pa.float32(),
    "Cartn_y": pa.float32(),
    "Cartn_z": pa.float32(),
    "occupancy": pa.float32(),
    "B_iso_or_equiv": pa.float32(),
    "pdbx_formal_charge": pa.int32(),  # None when absent
    "pdbx_PDB_model_num": pa.int32(),  # 1 for a file without MODEL records
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
    "label_alt_id": (16, 17),
    "label_comp_id": (17, 20),
    "auth_asym_id": (21, 22),
    "auth_seq_id": (22, 26),
    "pdbx_PDB_ins_code": (26, 27),
    "Cartn_x": (30, 38),
    "Cartn_y": (38, 46),
    "Cartn_z": (46, 54),
    "occupancy": (54, 60),
    "B_iso_or_equiv": (60, 66),
    "type_symbol": (76, 78),
    "pdbx_formal_charge": (78, 80),
}

# mmCIF columns to read when the canonical one is absent from a file. wwPDB files
# always carry `auth_*`; files written by other tools sometimes carry only `label_*`.
MMCIF_FALLBACK_COLUMNS: dict[str, str] = {"auth_asym_id": "label_asym_id", "auth_seq_id": "label_seq_id"}

# Values assumed when an mmCIF file omits the item entirely, matching what a PDB file
# without the corresponding record yields (a file with no MODEL records is model 1).
MMCIF_DEFAULT_VALUES: dict[str, object] = {"pdbx_PDB_model_num": 1}

_MMCIF_RECORD_GROUP = "group_PDB"
_ATOM_RECORD = "ATOM"
_PDB_MODEL_SPAN = (10, 14)
_HYBRID36_DIGITS = string.digits + string.ascii_uppercase
_HYBRID36_DIGITS_LOWER = string.digits + string.ascii_lowercase


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


def _hybrid36_decode(value: str, width: int) -> int | None:
    """Decode a PDB hybrid-36 integer field of the given column width.

    Serial numbers above 99999 (width 5) and residue numbers above 9999 (width 4) are
    written in base 36, upper-case letters first and then lower-case, as defined at
    https://cci.lbl.gov/hybrid_36/. Plain decimal fields decode unchanged.
    """
    value = value.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        pass
    if len(value) != width or not value[0].isalpha():
        return None
    # int(x, 36) is case-insensitive, so the two alphabetic ranges are told apart by
    # the first character: "A0000" follows 99999, "a0000" follows the upper-case range.
    if value[0].isupper():
        digits, offset = _HYBRID36_DIGITS, 10**width - 10 * 36 ** (width - 1)
    else:
        digits, offset = _HYBRID36_DIGITS_LOWER, 10**width + 16 * 36 ** (width - 1)
    if not all(c in digits for c in value):
        return None
    return int(value, 36) + offset


def _parse_pdb_charge(value: str) -> int | None:
    """Parse PDB columns 79-80 (``2+``, ``1-``) into a signed integer."""
    value = value.strip()
    if len(value) == 2 and value[0].isdigit() and value[1] in "+-":
        return int(value[0]) if value[1] == "+" else -int(value[0])
    return _convert(value, pa.int32())


def _element_from_atom_name(atom_name_field: str) -> str | None:
    """Derive the element for a record that has no columns 77-78.

    In the PDB atom-name field (columns 13-16) the element symbol is right-justified
    in columns 13-14, so a two-letter element (``FE``, ``ZN``) fills both and a
    one-letter element (`` CA`` for carbon-alpha) leaves column 13 blank. Hydrogens
    with four-character names (``HG21``) start in column 13; digits are not part of
    the symbol.
    """
    symbol = "".join(c for c in atom_name_field[:2] if c.isalpha())
    if not symbol:
        return None
    if atom_name_field[:1] == "H" and len(atom_name_field.strip()) == 4:
        return "H"
    return symbol.upper()


# Per-column PDB field parsers that need more than a plain type coercion.
_PDB_FIELD_PARSERS: dict[str, Callable[[str], object]] = {
    "id": lambda raw: _hybrid36_decode(raw, 5),
    "auth_seq_id": lambda raw: _hybrid36_decode(raw, 4),
    "pdbx_formal_charge": _parse_pdb_charge,
}


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


def _pdb_field(line: str, col: str) -> str:
    start, end = PDB_FIELD_SPANS[col]
    return line[start:end].strip() if start < len(line) else ""


def parse_pdb_atoms(text: str, columns: list[str] | None = None, include_hetatm: bool = True) -> dict[str, list]:
    """Parse PDB ATOM/HETATM records into a struct-of-arrays.

    ``MODEL``/``ENDMDL`` records set ``pdbx_PDB_model_num`` for the atoms they
    enclose; a file without them is model 1. Every model's atoms are emitted, so an
    NMR ensemble yields one row per atom per model, distinguishable by that column.

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
    model_num = 1
    for line in text.splitlines():
        record = _pdb_field(line, _MMCIF_RECORD_GROUP)
        if record == "MODEL":
            model_num = _convert(line[slice(*_PDB_MODEL_SPAN)].strip(), pa.int32()) or model_num
            continue
        if record not in ("ATOM", "HETATM"):
            continue
        if not include_hetatm and record != _ATOM_RECORD:
            continue
        for col in requested:
            if col == "pdbx_PDB_model_num":
                value = model_num
            elif col == "type_symbol":
                raw = _pdb_field(line, col)
                value = raw.upper() if raw else _element_from_atom_name(line[12:16])
            elif col in _PDB_FIELD_PARSERS:
                value = _PDB_FIELD_PARSERS[col](_pdb_field(line, col))
            else:
                value = _convert(_pdb_field(line, col), PROTEIN_ATOM_TYPES[col])
            atoms[col].append(value)
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


def _find_atom_site(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    """Locate the ``_atom_site`` category and return (column names, token rows).

    Handles both CIF forms: a ``loop_`` whose rows are a whitespace-delimited token
    stream (rows may wrap across lines, several rows may share a line), and the
    key-value form ``_atom_site.<item> <value>`` that a single-atom category may use.
    """
    n = len(lines)
    idx = 0
    while idx < n:
        stripped = lines[idx].strip()
        if stripped == "loop_":
            peek = idx + 1
            header: list[str] = []
            while peek < n and lines[peek].strip().startswith("_"):
                header.append(lines[peek].strip())
                peek += 1
            idx = peek
            if not (header and header[0].startswith("_atom_site.")):
                continue
            loop_columns = [h.split(".", 1)[1] for h in header]
            width = len(loop_columns)
            rows: list[list[str]] = []
            pending: list[str] = []
            while idx < n:
                stripped = lines[idx].strip()
                if stripped == "" or stripped.startswith("#"):
                    idx += 1
                    continue
                if stripped.startswith(("_", "loop_", "data_")):
                    break
                pending.extend(_tokenize_cif_line(lines[idx]))
                idx += 1
                while len(pending) >= width:
                    rows.append(pending[:width])
                    pending = pending[width:]
            return loop_columns, rows
        if stripped.startswith("_atom_site."):
            # Key-value form: one item per line, one row in total.
            columns: list[str] = []
            values: list[str] = []
            while idx < n and lines[idx].strip().startswith("_atom_site."):
                tokens = _tokenize_cif_line(lines[idx].strip())
                columns.append(tokens[0].split(".", 1)[1])
                values.append(tokens[1] if len(tokens) > 1 else "")
                idx += 1
            return columns, [values]
        idx += 1
    return [], []


def parse_mmcif_atoms(text: str, columns: list[str] | None = None, include_hetatm: bool = True) -> dict[str, list]:
    """Parse an mmCIF ``_atom_site`` category into a struct-of-arrays.

    Author identifiers (``auth_asym_id``, ``auth_seq_id``) are read from the
    ``auth_*`` items and fall back to ``label_*`` when a file lacks them
    (see [`MMCIF_FALLBACK_COLUMNS`]).

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
    atoms: dict[str, list] = {col: [] for col in requested}
    loop_columns, rows = _find_atom_site(text.splitlines())
    if not loop_columns:
        return atoms
    col_index = {name: i for i, name in enumerate(loop_columns)}
    positions = {col: col_index.get(col, col_index.get(MMCIF_FALLBACK_COLUMNS.get(col, col))) for col in requested}
    group_pos = col_index.get(_MMCIF_RECORD_GROUP)
    for tokens in rows:
        if not include_hetatm and group_pos is not None and tokens[group_pos] != _ATOM_RECORD:
            continue
        for col in requested:
            pos = positions[col]
            if pos is None:
                atoms[col].append(MMCIF_DEFAULT_VALUES.get(col))
            else:
                atoms[col].append(_convert(tokens[pos], PROTEIN_ATOM_TYPES[col]))
    return atoms


# Parser for each structure format; the format is chosen by ``detect_format``.
PARSERS = {"pdb": parse_pdb_atoms, "mmcif": parse_mmcif_atoms}
_MMCIF_SUFFIXES = (".cif", ".mmcif")


def detect_format(path: str | None, text: str) -> str:
    """Return ``"mmcif"`` or ``"pdb"`` for a structure file.

    The extension decides when it is known. When there is none (bytes stored with no
    path, or an unrecognised suffix) the content decides: a CIF file starts with a
    ``data_`` block header or carries an ``_atom_site.`` item, and a PDB file never
    contains either. Falling back to PDB without looking would slice mmCIF rows by
    fixed columns and silently return None for every coordinate.
    """
    suffix = path.rsplit(".", 1)[-1].lower() if path and "." in path.rsplit("/", 1)[-1] else ""
    if suffix and "." + suffix in _MMCIF_SUFFIXES:
        return "mmcif"
    if suffix in ("pdb", "ent"):
        return "pdb"
    head = text[:4096]
    if head.lstrip().startswith("data_") or "_atom_site." in text:
        return "mmcif"
    return "pdb"
