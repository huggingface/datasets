"""Loader for BIDS (Brain Imaging Data Structure) electrophysiology and biosignal datasets."""

import csv
import os
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

import pyarrow as pa

import datasets
from datasets.features.biosignal import _find_bids_root
from datasets.table import table_cast


BIDS_DATATYPES = ("meg", "eeg", "ieeg", "emg", "nirs")
BIDS_RECORDING_EXTENSIONS = (
    ".vhdr",
    ".edf",
    ".bdf",
    ".gdf",
    ".set",
    ".fif",
    ".cnt",
    ".mff",
    ".nwb",
    ".snirf",
    ".con",
    ".sqd",
    ".kit",
    ".ds",
    ".mefd",
)
BIDS_ENTITY_COLUMNS = ("subject", "session", "task", "acquisition", "run", "datatype", "suffix", "extension")
_NA_VALUES = {"n/a", "N/A", "na", "NA", ""}


def _ensure_list(val: Optional[Union[str, list[str], tuple[str, ...]]]) -> Optional[list[str]]:
    if val is None:
        return None
    return [val] if isinstance(val, str) else list(val)


def _coerce_column(values: list[Optional[str]]) -> tuple[list[Any], datasets.Value]:
    non_null = [v for v in values if v is not None]
    if non_null:
        try:
            return [int(v) if v is not None else None for v in values], datasets.Value("int64")
        except ValueError:
            try:
                return [float(v) if v is not None else None for v in values], datasets.Value("float64")
            except ValueError:
                pass
    return values, datasets.Value("string")


def _parse_bids_filename(fpath: Union[str, Path]) -> dict[str, Optional[str]]:
    s = str(fpath).replace("\\", "/")
    slash = s.rfind("/")
    name = s[slash + 1 :]
    parent = s[:slash].rsplit("/", 1)[-1] if slash > 0 else ""
    dot = name.rfind(".")
    stem, ext = (name[:dot], name[dot:]) if dot > 0 else (name, None)
    parts = stem.split("_")
    kv = dict(p.split("-", 1) for p in parts if "-" in p)
    suffix = parts[-1] if parts and "-" not in parts[-1] else None
    datatype = (
        parent
        if parent and not parent.startswith(("sub-", "ses-"))
        else (suffix if suffix in BIDS_DATATYPES else None)
    )
    return {
        "subject": kv.get("sub"),
        "session": kv.get("ses"),
        "task": kv.get("task"),
        "acquisition": kv.get("acq"),
        "run": kv.get("run"),
        "datatype": datatype,
        "suffix": suffix,
        "extension": ext or None,
    }


def _iter_bids_files(
    root: Path,
    ext_set: set[str],
    sub_set: Optional[set[str]] = None,
    ses_set: Optional[set[str]] = None,
    dt_set: Optional[set[str]] = None,
) -> list[str]:
    out: list[str] = []
    stack = [
        e.path
        for e in os.scandir(root)
        if e.is_dir(follow_symlinks=False) and e.name.startswith("sub-") and (sub_set is None or e.name[4:] in sub_set)
    ]
    while stack:
        d = stack.pop()
        for e in os.scandir(d):
            name = e.name
            dot = name.rfind(".")
            if dot > 0 and name[dot:].lower() in ext_set:
                if e.is_file(follow_symlinks=True) or e.is_dir(follow_symlinks=True):
                    out.append(e.path)
            elif e.is_dir(follow_symlinks=False) and not name.startswith("."):
                if name.startswith("ses-"):
                    if ses_set is None or name[4:] in ses_set:
                        stack.append(e.path)
                elif dt_set is None or name in dt_set:
                    stack.append(e.path)
    out.sort()
    return out


def _read_participants_tsv(
    bids_root: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, datasets.Value]]:
    tsv_path = bids_root / "participants.tsv"
    if not tsv_path.is_file():
        return {}, {}
    with open(tsv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if not reader.fieldnames or "participant_id" not in reader.fieldnames:
            return {}, {}
        extra_cols = [c for c in reader.fieldnames if c not in ("participant_id", "biosignal", *BIDS_ENTITY_COLUMNS)]
        rows = list(reader)

    subjects = [(r.get("participant_id") or "").strip().removeprefix("sub-") for r in rows]
    coerced, col_features = {}, {}
    for c in extra_cols:
        raw_vals = [None if (v := (r.get(c) or "").strip()) in _NA_VALUES else v for r in rows]
        coerced[c], col_features[c] = _coerce_column(raw_vals)
    return {sub: {c: coerced[c][i] for c in extra_cols} for i, sub in enumerate(subjects)}, col_features


@dataclass
class BidsConfig(datasets.BuilderConfig):
    """BuilderConfig for BIDS datasets.

    Args:
        subjects (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS subject ID(s) (without the `sub-` prefix, e.g. `"01"`).
        sessions (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS session ID(s) (without the `ses-` prefix).
        tasks (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS task name(s) (e.g. `"rest"`).
        acquisitions (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS acquisition label(s).
        runs (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS run label(s).
        datatypes (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS datatype(s). Defaults to electrophysiology modalities
            (`["meg", "eeg", "ieeg", "emg", "nirs"]`).
        suffixes (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS suffix(es). Defaults to `["meg", "eeg", "ieeg", "emg", "nirs"]`.
        extensions (`str` or `list[str]`, *optional*):
            Filter recordings by file extension(s).
        preload (`bool`, defaults to `False`):
            Whether to preload signal data into memory when decoding local `Biosignal` recordings.
        decode (`bool`, defaults to `True`):
            Whether to decode the `Biosignal` column into `mne.io.BaseRaw`.
        features ([`Features`], *optional*):
            Explicit features schema override.
    """

    subjects: Optional[Union[str, list[str]]] = None
    sessions: Optional[Union[str, list[str]]] = None
    tasks: Optional[Union[str, list[str]]] = None
    acquisitions: Optional[Union[str, list[str]]] = None
    runs: Optional[Union[str, list[str]]] = None
    datatypes: Optional[Union[str, list[str]]] = None
    suffixes: Optional[Union[str, list[str]]] = None
    extensions: Optional[Union[str, list[str]]] = None
    preload: bool = False
    decode: bool = True
    features: Optional[datasets.Features] = None


class Bids(datasets.ArrowBasedBuilder):
    """Builder for BIDS (Brain Imaging Data Structure) datasets using `mne-bids`: one row per recording."""

    BUILDER_CONFIG_CLASS = BidsConfig

    EXTENSIONS = list(BIDS_RECORDING_EXTENSIONS)
    METADATA_FILENAMES = [
        "dataset_description.json",
        "participants.tsv",
        "participants.json",
        "README",
        "CHANGES",
    ]
    METADATA_EXTENSIONS = [".tsv", ".json", ".vmrk", ".eeg", ".fdt"]

    def _info(self):
        return datasets.DatasetInfo(
            description="BIDS (Brain Imaging Data Structure) biosignal dataset: one row per recording.",
            features=self.config.features
            or datasets.Features(
                {
                    "biosignal": datasets.Biosignal(preload=self.config.preload, decode=self.config.decode),
                    **{col: datasets.Value("string") for col in BIDS_ENTITY_COLUMNS},
                }
            ),
        )

    def _discover_records(self, paths: list[str]) -> tuple[list[dict[str, Any]], dict[str, datasets.Value]]:
        dt_set = set(_ensure_list(self.config.datatypes) or BIDS_DATATYPES)
        suf_set = set(_ensure_list(self.config.suffixes) or BIDS_DATATYPES)
        extensions = _ensure_list(self.config.extensions) or list(BIDS_RECORDING_EXTENSIONS)
        ext_set = {e.lower() for e in extensions}
        sub_list = _ensure_list(self.config.subjects)
        ses_list = _ensure_list(self.config.sessions)
        task_list = _ensure_list(self.config.tasks)
        acq_list = _ensure_list(self.config.acquisitions)
        run_list = _ensure_list(self.config.runs)
        sub_set = set(sub_list) if sub_list else None
        ses_set = set(ses_list) if ses_list else None
        task_set = set(task_list) if task_list else None
        acq_set = set(acq_list) if acq_list else None
        run_set = set(run_list) if run_list else None

        bids_roots: list[Path] = []
        seen_roots: set[Path] = set()
        recording_files: list[Path] = []

        for raw_p in paths:
            p = Path(raw_p)
            suffix_lower = p.suffix.lower()
            if p.name == "dataset_description.json":
                if p.parent not in seen_roots:
                    seen_roots.add(p.parent)
                    bids_roots.append(p.parent)
            elif suffix_lower in ext_set:
                recording_files.append(p)
            elif p.is_dir():
                desc_files = [p / "dataset_description.json"] if (p / "dataset_description.json").is_file() else []
                if not desc_files:
                    desc_files = list(p.rglob("dataset_description.json"))
                if desc_files:
                    for df in sorted(desc_files):
                        if df.parent not in seen_roots:
                            seen_roots.add(df.parent)
                            bids_roots.append(df.parent)
                else:
                    for ext in extensions:
                        recording_files.extend(sorted(p.rglob(f"*{ext}")))

        bids_roots = [r for r in bids_roots if not any(p in seen_roots for p in r.parents)]

        participants_cache: dict[Path, dict[str, dict[str, Any]]] = {}
        extra_features: dict[str, datasets.Value] = {}

        def _get_participants(root: Optional[Path]) -> dict[str, dict[str, Any]]:
            if root is None:
                return {}
            if root not in participants_cache:
                by_sub, feats = _read_participants_tsv(root)
                participants_cache[root] = by_sub
                for col, feat in feats.items():
                    extra_features.setdefault(col, feat)
            return participants_cache[root]

        candidates: list[tuple[str, Optional[Path]]] = []
        for root in bids_roots:
            _get_participants(root)
            if not recording_files:
                for fpath in _iter_bids_files(root, ext_set, sub_set, ses_set, dt_set):
                    candidates.append((fpath, root))

        if recording_files:
            top_root = bids_roots[0] if len(bids_roots) == 1 else None
            for rf in sorted(recording_files):
                if not rf.exists():
                    continue
                root = top_root or _find_bids_root(rf)
                if root is not None:
                    try:
                        rel_parts = rf.relative_to(root).parts
                        if rel_parts and rel_parts[0] in ("sourcedata", "derivatives"):
                            continue
                    except ValueError:
                        pass
                _get_participants(root)
                candidates.append((str(rf), root))

        records: list[dict[str, Any]] = []
        for fpath, root in candidates:
            ent = _parse_bids_filename(fpath)
            if sub_set and ent["subject"] not in sub_set:
                continue
            if ses_set and ent["session"] not in ses_set:
                continue
            if task_set and ent["task"] not in task_set:
                continue
            if acq_set and ent["acquisition"] not in acq_set:
                continue
            if run_set and ent["run"] not in run_set:
                continue
            if ent["datatype"] and ent["datatype"] not in dt_set:
                continue
            if ent["suffix"] and ent["suffix"] not in suf_set:
                continue
            sub_meta = _get_participants(root).get(ent["subject"] or "", {})
            records.append(
                {
                    "biosignal": {"bytes": None, "path": fpath},
                    **ent,
                    **{col: sub_meta.get(col) for col in extra_features},
                }
            )

        return records, extra_features

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")

        splits = []
        all_extra_features: dict[str, datasets.Value] = {}
        split_records: dict[str, list[dict[str, Any]]] = {}

        for split_name, files in self.config.data_files.items():
            if isinstance(files, str):
                files = [files]
            local_or_extracted = [f if os.path.exists(f) else dl_manager.download_and_extract(f) for f in files]
            records, extra_feats = self._discover_records(local_or_extracted)
            split_records[split_name] = records
            for col, feat in extra_feats.items():
                all_extra_features.setdefault(col, feat)

        if self.config.features is None and all_extra_features:
            self.info.features = datasets.Features(
                {
                    "biosignal": datasets.Biosignal(preload=self.config.preload, decode=self.config.decode),
                    **{col: datasets.Value("string") for col in BIDS_ENTITY_COLUMNS},
                    **all_extra_features,
                }
            )

        for split_name, records in split_records.items():
            for row in records:
                for col in all_extra_features:
                    row.setdefault(col, None)
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={"records": records},
                )
            )
        return splits

    def _generate_tables(self, records: list[dict[str, Any]]) -> Iterator[tuple[int, pa.Table]]:
        schema = self.info.features.arrow_schema
        pa_table = pa.Table.from_pylist(records, schema=schema)
        yield 0, table_cast(pa_table, schema)
