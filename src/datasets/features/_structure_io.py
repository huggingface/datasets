"""Dependency-free readers for macromolecular structure files.

Reads the coordinate section of PDB, PDBx/mmCIF and BinaryCIF files (optionally gzip, bz2 or zstd
compressed) into the column layout of the [`Structure`] feature: one entry per atom, named after the
mmCIF `atom_site` items, plus the inter-residue bonds the file records explicitly (`struct_conn` in
mmCIF and BinaryCIF, `CONECT` in PDB). Only the first data block of a CIF file is read.
"""

import bz2
import gzip
import re
from typing import Optional

import numpy as np

from .. import config


# (name, numpy dtype, value used when the item is missing) for every per-atom column, in storage order.
ATOM_COLUMNS = [
    ("group_PDB", "str", ""),
    ("pdbx_PDB_model_num", "int32", 1),
    ("label_entity_id", "str", ""),
    ("label_asym_id", "str", ""),
    ("auth_asym_id", "str", ""),
    ("label_comp_id", "str", ""),
    ("label_seq_id", "int32", None),
    ("auth_seq_id", "int32", None),
    ("pdbx_PDB_ins_code", "str", ""),
    ("label_atom_id", "str", ""),
    ("label_alt_id", "str", ""),
    ("type_symbol", "str", ""),
    ("occupancy", "float32", None),
    ("B_iso_or_equiv", "float32", None),
    ("pdbx_formal_charge", "int8", None),
]
COORD_COLUMN = "Cartn_xyz"  # Cartn_x, Cartn_y and Cartn_z as one (n_atoms, 3) float32 column
BOND_COLUMNS = [
    ("atom_index_1", "int32"),
    ("atom_index_2", "int32"),
    ("conn_type_id", "str"),
    ("pdbx_value_order", "str"),
]

_COMPRESSION_EXTENSIONS = (".gz", ".gzip", ".bz2", ".zst")
_FORMAT_BY_EXTENSION = {".cif": "mmcif", ".mmcif": "mmcif", ".bcif": "bcif", ".pdb": "pdb", ".ent": "pdb"}


def read_structure(data: bytes, path: Optional[str] = None) -> dict:
    """Parse structure file bytes into the [`Structure`] storage layout (numpy arrays)."""
    data = _decompress(data)
    file_format = _detect_format(data, path)
    if file_format == "pdb":
        return _read_pdb(data.decode("utf-8", errors="replace"))
    if file_format == "mmcif":
        block_id, categories = _read_cif_text(data.decode("utf-8", errors="replace"))
    else:
        block_id, categories = _read_bcif(data)
    if "atom_site" not in categories:
        raise ValueError("The structure file has no `atom_site` category.")
    atoms = _atom_site_to_columns(categories["atom_site"])
    bonds = _struct_conn_to_bonds(categories.get("struct_conn"), atoms)
    return {"id": block_id, "atoms": atoms, "bonds": bonds}


def _decompress(data: bytes) -> bytes:
    if data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    if data[:3] == b"BZh":
        return bz2.decompress(data)
    if data[:4] == b"\x28\xb5\x2f\xfd":
        if not config.ZSTANDARD_AVAILABLE:
            raise ImportError("To read zstd-compressed structure files, please install 'zstandard'.")
        import zstandard

        return zstandard.ZstdDecompressor().stream_reader(data).read()
    return data


def _detect_format(data: bytes, path: Optional[str]) -> str:
    if path:
        name = path.split("::")[0].lower()
        for ext in _COMPRESSION_EXTENSIONS:
            name = name.removesuffix(ext)
        for ext, file_format in _FORMAT_BY_EXTENSION.items():
            if name.endswith(ext):
                return file_format
    head = data[:4096].lstrip()
    if head[:1] and (0x80 <= head[0] <= 0x8F or head[0] in (0xDE, 0xDF)):
        return "bcif"  # BinaryCIF is a MessagePack map
    for line in head.splitlines():
        if line.startswith(b"data_"):
            return "mmcif"
        if line.strip() and not line.startswith(b"#"):
            break
    return "pdb"


def _empty_bonds() -> dict:
    return {name: np.zeros(0, dtype=dtype if dtype != "str" else object) for name, dtype in BOND_COLUMNS}


# --------------------------------------------------------------------------------------------- PDB


def _read_pdb(text: str) -> dict:
    atom_lines, models, conect_lines = [], [], []
    model, block_id = 1, ""
    for line in text.splitlines():
        record = line[:6]
        if record in ("ATOM  ", "HETATM"):
            atom_lines.append(line)
            models.append(model)
        elif record == "MODEL ":
            model = int(line[10:14].strip() or len(set(models)) + 1)
        elif record == "CONECT":
            conect_lines.append(line)
        elif record == "HEADER" and not block_id:
            block_id = line[62:66].strip()
    if not atom_lines:
        raise ValueError("The PDB file has no ATOM or HETATM records.")
    raw = np.frombuffer("".join(line.ljust(80)[:80] for line in atom_lines).encode("latin-1"), dtype="S1")
    raw = raw.reshape(len(atom_lines), 80)

    def column(start: int, end: int) -> np.ndarray:
        return np.char.strip(raw[:, start:end].copy().view(f"S{end - start}").ravel()).astype(str)

    chain_id, atom_name = column(21, 22), column(12, 16)
    element = column(76, 78)
    if not element.all():  # old files leave the element columns blank; fall back to the atom name
        guess = np.array([name.lstrip("0123456789")[:1] for name in atom_name])
        element = np.where(element == "", guess, element)
    charge = column(78, 80)
    n = len(atom_lines)
    atoms = {
        "group_PDB": column(0, 6),
        "pdbx_PDB_model_num": np.asarray(models, dtype=np.int32),
        "label_entity_id": np.full(n, ""),
        "label_asym_id": chain_id,
        "auth_asym_id": chain_id,
        "label_comp_id": column(17, 20),
        "label_seq_id": np.full(n, None, dtype=object),
        "auth_seq_id": column(22, 26).astype(np.int32),
        "pdbx_PDB_ins_code": column(26, 27),
        "label_atom_id": atom_name,
        "label_alt_id": column(16, 17),
        "type_symbol": np.char.capitalize(element),
        "occupancy": _float_or_nan(column(54, 60)),
        "B_iso_or_equiv": _float_or_nan(column(60, 66)),
        "pdbx_formal_charge": np.array([int(c[-1] + c[:-1]) if c else 0 for c in charge], dtype=np.int8),
        COORD_COLUMN: np.stack([_float_or_nan(column(a, a + 8)) for a in (30, 38, 46)], axis=1),
    }
    return {"id": block_id, "atoms": atoms, "bonds": _conect_to_bonds(conect_lines, column(6, 11), atoms)}


def _float_or_nan(values: np.ndarray) -> np.ndarray:
    return np.where(values == "", "nan", values).astype(np.float32)


def _conect_to_bonds(conect_lines: list[str], serials: np.ndarray, atoms: dict) -> dict:
    if not conect_lines:
        return _empty_bonds()
    first_model = atoms["pdbx_PDB_model_num"] == atoms["pdbx_PDB_model_num"][0]
    index_by_serial = {serial: i for i, serial in enumerate(serials[first_model])}
    pairs = set()
    for line in conect_lines:
        fields = [line[a : a + 5].strip() for a in range(6, 31, 5)]
        if fields[0] not in index_by_serial:
            continue
        i = index_by_serial[fields[0]]
        for partner in fields[1:]:
            if partner in index_by_serial and index_by_serial[partner] != i:
                pairs.add(tuple(sorted((i, index_by_serial[partner]))))
    pairs = np.array(sorted(pairs), dtype=np.int32).reshape(-1, 2)
    return {
        "atom_index_1": pairs[:, 0],
        "atom_index_2": pairs[:, 1],
        "conn_type_id": np.full(len(pairs), "", dtype=object),
        "pdbx_value_order": np.full(len(pairs), "", dtype=object),
    }


# ------------------------------------------------------------------------------------------- mmCIF

# A CIF token: a quoted string (a quote only closes when followed by whitespace) or a bare word.
_CIF_TOKEN = re.compile(r"""'(?:[^'\n]|'(?=\S))*'|"(?:[^"\n]|"(?=\S))*"|\S+""")
_WANTED_CATEGORIES = ("atom_site", "struct_conn")


def _read_cif_text(text: str) -> tuple[str, dict]:
    """Read the `atom_site` and `struct_conn` categories of the first data block.

    Each category maps item names to `(values, missing)`, where `values` is a numpy string array and
    `missing` flags the unquoted `.` and `?` placeholders.
    """
    lines = text.splitlines()
    block_id, categories, i = None, {}, 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("data_"):
            if block_id is not None:
                break
            block_id = line[5:].strip()
            i += 1
        elif line.startswith("loop_"):
            i += 1
            items = []
            while i < len(lines) and lines[i].startswith("_"):
                items.append(lines[i].split()[0])
                i += 1
            start = i
            while i < len(lines) and not lines[i].startswith(("loop_", "_", "data_", "#")):
                if lines[i].startswith(";"):  # skip over a multi-line text field
                    i += 1
                    while i < len(lines) and not lines[i].startswith(";"):
                        i += 1
                i += 1
            category = items[0][1:].split(".")[0] if items else None
            if category in _WANTED_CATEGORIES:
                tokens = _tokenize(lines[start:i])
                if len(tokens) % len(items):
                    raise ValueError(f"Malformed `{category}` loop: {len(tokens)} values for {len(items)} items.")
                table = np.array(tokens, dtype=object).reshape(-1, len(items))
                categories[category] = {
                    item.split(".", 1)[1]: _cif_column(table[:, k]) for k, item in enumerate(items)
                }
        elif line.startswith("_") and line[1:].split(".")[0] in _WANTED_CATEGORIES:
            # single-row category written as `_category.item value` pairs
            category = line[1:].split(".")[0]
            rows = {}
            while i < len(lines) and lines[i].startswith(f"_{category}."):
                item_line = lines[i].split(None, 1)
                i += 1
                if len(item_line) == 1:  # the value is on the following line(s)
                    end = i + 1
                    if lines[i].startswith(";"):
                        while end < len(lines) and not lines[end].startswith(";"):
                            end += 1
                        end += 1
                    tokens = _tokenize(lines[i:end])
                    i = end
                else:
                    tokens = _tokenize(item_line[1:])
                rows[item_line[0].split(".", 1)[1]] = _cif_column(np.array(tokens[:1], dtype=object))
            categories[category] = rows
        else:
            i += 1
    return block_id or "", categories


def _tokenize(lines: list[str]) -> list[str]:
    if not any(line.startswith(";") for line in lines):
        return _CIF_TOKEN.findall("\n".join(lines))
    tokens, i = [], 0
    while i < len(lines):
        if lines[i].startswith(";"):
            text = [lines[i][1:]]
            i += 1
            while i < len(lines) and not lines[i].startswith(";"):
                text.append(lines[i])
                i += 1
            tokens.append("'" + "\n".join(text).strip().replace("'", "") + "'")  # keep it a single token
        else:
            tokens.extend(_CIF_TOKEN.findall(lines[i]))
        i += 1
    return tokens


def _cif_column(raw: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    raw = raw.astype(str)
    missing = (raw == ".") | (raw == "?")
    quoted = (np.char.startswith(raw, "'") | np.char.startswith(raw, '"')) & (np.char.str_len(raw) >= 2)
    if quoted.any():
        raw = raw.copy()
        raw[quoted] = [value[1:-1] for value in raw[quoted]]
    return raw, missing


# ---------------------------------------------------------------------------------------- BinaryCIF

_BCIF_DTYPES = {1: "<i1", 2: "<i2", 3: "<i4", 4: "<u1", 5: "<u2", 6: "<u4", 32: "<f4", 33: "<f8"}


def _read_bcif(data: bytes) -> tuple[str, dict]:
    if not config.MSGPACK_AVAILABLE:
        raise ImportError("To read BinaryCIF structure files, please install 'msgpack'.")
    import msgpack

    file = msgpack.unpackb(data, raw=False)
    block = file["dataBlocks"][0]
    categories = {}
    for category in block["categories"]:
        name = category["name"].lstrip("_")
        if name not in _WANTED_CATEGORIES:
            continue
        columns = {}
        for column in category["columns"]:
            values = _bcif_decode(column["data"])
            if column.get("mask") is not None:
                missing = _bcif_decode(column["mask"]) != 0
            else:
                missing = np.zeros(len(values), dtype=bool)
            if values.dtype == object:
                values = np.where(missing, "", values).astype(str)
            columns[column["name"]] = (values, missing)
        categories[name] = columns
    return block.get("header", ""), categories


def _bcif_decode(encoded: dict) -> np.ndarray:
    """Undo a BinaryCIF encoding chain (applied in reverse order)."""
    data = encoded["data"]
    for encoding in reversed(encoded["encoding"]):
        kind = encoding["kind"]
        if kind == "ByteArray":
            data = np.frombuffer(data, dtype=_BCIF_DTYPES[encoding["type"]])
        elif kind == "FixedPoint":
            data = (data / encoding["factor"]).astype(_BCIF_DTYPES[encoding["srcType"]])
        elif kind == "IntervalQuantization":
            step = (encoding["max"] - encoding["min"]) / max(encoding["numSteps"] - 1, 1)
            data = (encoding["min"] + step * data).astype(_BCIF_DTYPES[encoding["srcType"]])
        elif kind == "RunLength":
            data = np.repeat(data[0::2], data[1::2]).astype(_BCIF_DTYPES[encoding["srcType"]])
        elif kind == "Delta":
            data = (np.cumsum(data, dtype=np.int64) + encoding["origin"]).astype(_BCIF_DTYPES[encoding["srcType"]])
        elif kind == "IntegerPacking":
            data = _bcif_unpack_integers(data, encoding)
        elif kind == "StringArray":
            offsets = _bcif_decode({"data": encoding["offsets"], "encoding": encoding["offsetEncoding"]})
            indices = _bcif_decode({"data": data, "encoding": encoding["dataEncoding"]})
            text = encoding["stringData"]
            strings = np.array([text[offsets[k] : offsets[k + 1]] for k in range(len(offsets) - 1)] + [""], object)
            data = strings[np.where(indices < 0, len(strings) - 1, indices)]
        else:
            raise ValueError(f"Unsupported BinaryCIF encoding '{kind}'.")
    return data


def _bcif_unpack_integers(data: np.ndarray, encoding: dict) -> np.ndarray:
    """Values at the packed type's limits continue into the next element and are summed."""
    bits = 8 * encoding["byteCount"]
    if encoding["isUnsigned"]:
        upper, lower = 2**bits - 1, None
    else:
        upper, lower = 2 ** (bits - 1) - 1, -(2 ** (bits - 1))
    at_limit = (data == upper) if lower is None else ((data == upper) | (data == lower))
    if not at_limit.any():
        return data.astype(np.int32)
    out = np.empty(encoding["srcSize"], dtype=np.int32)
    total, k = 0, 0
    for value, continues in zip(data.tolist(), at_limit.tolist()):
        total += value
        if not continues:
            out[k] = total
            total, k = 0, k + 1
    return out[:k]


# ---------------------------------------------------------------------------- shared CIF processing


def _atom_site_to_columns(columns: dict) -> dict:
    n = len(columns["Cartn_x"][0])

    def item(name: str, fallback: Optional[str] = None):
        if name in columns:
            return columns[name]
        if fallback in columns:
            return columns[fallback]
        return np.full(n, "", dtype=object), np.ones(n, dtype=bool)

    def as_str(values_missing) -> np.ndarray:
        values, missing = values_missing
        return np.where(missing, "", values.astype(str))

    def as_number(values_missing, dtype: str, fill):
        values, missing = values_missing
        if values.dtype.kind in "UO":
            values = np.where(missing, "0", values).astype(np.float64)
        values = values.astype(dtype)
        if fill is None:
            return values if not missing.any() else np.where(missing, None, values.astype(object))
        return np.where(missing, fill, values).astype(dtype)

    atoms = {}
    for name, dtype, fill in ATOM_COLUMNS:
        fallback = {"auth_asym_id": "label_asym_id", "auth_seq_id": "label_seq_id"}.get(name)
        if dtype == "str":
            atoms[name] = as_str(item(name, fallback))
        elif dtype == "float32":
            values = as_number(item(name, fallback), "float32", np.nan)
            atoms[name] = values
        else:
            atoms[name] = as_number(item(name, fallback), dtype, fill)
    atoms[COORD_COLUMN] = np.stack(
        [as_number(columns[f"Cartn_{axis}"], "float32", np.nan) for axis in "xyz"], axis=1
    ).astype(np.float32)
    return atoms


def _struct_conn_to_bonds(columns: Optional[dict], atoms: dict) -> dict:
    if not columns or "ptnr1_label_atom_id" not in columns:
        return _empty_bonds()
    first_model = np.flatnonzero(atoms["pdbx_PDB_model_num"] == atoms["pdbx_PDB_model_num"][0])

    def partner(k: int) -> list:
        def get(name: str, fallback: Optional[str] = None) -> list:
            values, missing = columns.get(name) or columns.get(fallback) or (None, None)
            if values is None:
                return [""] * len(columns["ptnr1_label_atom_id"][0])
            return [("" if m else str(v)) for v, m in zip(values, missing)]

        return list(
            zip(
                get(f"ptnr{k}_auth_asym_id", f"ptnr{k}_label_asym_id"),
                get(f"ptnr{k}_auth_seq_id", f"ptnr{k}_label_seq_id"),
                get(f"pdbx_ptnr{k}_PDB_ins_code"),
                get(f"ptnr{k}_label_comp_id"),
                get(f"ptnr{k}_label_atom_id"),
                get(f"pdbx_ptnr{k}_label_alt_id"),
                get(f"ptnr{k}_symmetry"),
            )
        )

    partners1, partners2 = partner(1), partner(2)
    residues = {(p[0], p[1]) for p in partners1 + partners2}
    residue_keys = list(zip(atoms["auth_asym_id"][first_model].tolist(), atoms["auth_seq_id"][first_model].tolist()))
    with_alt, without_alt = {}, {}
    for index, residue in zip(first_model.tolist(), residue_keys):
        residue = (residue[0], str(residue[1]))
        if residue not in residues:
            continue
        key = (
            *residue,
            atoms["pdbx_PDB_ins_code"][index],
            atoms["label_comp_id"][index],
            atoms["label_atom_id"][index],
        )
        with_alt.setdefault((*key, atoms["label_alt_id"][index]), index)
        without_alt.setdefault(key, index)

    def find(p) -> Optional[int]:
        if p[6] not in ("", "1_555"):
            return None  # partner is a symmetry mate outside the asymmetric unit
        return with_alt.get(p[:6]) if p[5] else without_alt.get(p[:5])

    conn_type = columns.get("conn_type_id", (np.full(len(partners1), ""), np.zeros(len(partners1), bool)))
    order = columns.get("pdbx_value_order", (np.full(len(partners1), ""), np.ones(len(partners1), bool)))
    bonds = {name: [] for name, _ in BOND_COLUMNS}
    for k, (p1, p2) in enumerate(zip(partners1, partners2)):
        i, j = find(p1), find(p2)
        if i is None or j is None or i == j:
            continue
        bonds["atom_index_1"].append(i)
        bonds["atom_index_2"].append(j)
        bonds["conn_type_id"].append("" if conn_type[1][k] else str(conn_type[0][k]))
        bonds["pdbx_value_order"].append("" if order[1][k] else str(order[0][k]))
    return {
        name: np.asarray(values, dtype=dtype if dtype != "str" else object)
        for (name, dtype), values in zip(BOND_COLUMNS, bonds.values())
    }
