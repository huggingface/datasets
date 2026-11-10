"""Loader for BIDS (Brain Imaging Data Structure) electrophysiology and biosignal datasets."""

import io
import os
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

import pyarrow as pa
import pyarrow.csv as pa_csv

import datasets
from datasets.builder import Key
from datasets.download.download_config import DownloadConfig
from datasets.table import table_cast
from datasets.utils.file_utils import is_local_path, xbasename, xdirname, xjoin, xopen


BIDS_ENTITY_COLUMNS = ("subject", "session", "task", "acquisition", "run", "datatype", "suffix", "extension")
ARCHIVE_EXTENSIONS = (".zip", ".tar", ".tgz", ".tar.gz", ".tar.bz2", ".tar.xz")
CONTAINER_EXTENSIONS = (".ds", ".mff", ".mefd")


def _logical_path(path: str) -> Path:
    hop = path.split("::")[0]
    return Path(hop.split("://", 1)[1] if "://" in hop else hop)


def _collapse_container(path: str) -> str:
    cur = path
    while cur and cur != xdirname(cur):
        name = xbasename(cur)
        if name.startswith("sub-") and os.path.splitext(name)[1].lower() in CONTAINER_EXTENSIONS:
            return cur
        cur = xdirname(cur)
    return path


def _bids_root(path: str) -> Optional[str]:
    cur = xdirname(path)
    while cur and cur != xdirname(cur):
        if xbasename(cur).startswith("sub-"):
            return xdirname(cur)
        cur = xdirname(cur)
    return None


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
            Whether to preload signal data into memory when decoding local [`Biosignal`] recordings.
        decode (`bool`, defaults to `True`):
            Whether to decode the [`Biosignal`] column into `mne.io.BaseRaw`.
        features ([`Features`], *optional*):
            Explicit features schema override.

    Example:

    ```py
    >>> from datasets import load_dataset
    >>> ds = load_dataset("bids", data_dir="path/to/bids", subjects="01", tasks="rest", split="train")
    ```
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
    """Builder for BIDS (Brain Imaging Data Structure) datasets: one row per recording.

    It generates the following features:

    - **biosignal** ([`Biosignal`]) -- the recording decoded via `mne-bids` / `mne` into `mne.io.BaseRaw`.
    - **subject**, **session**, **task**, **acquisition**, **run**, **datatype**, **suffix**, **extension** (`str`) --
      BIDS filename entities extracted for the recording.
    - Any additional participant metadata columns present in `participants.tsv`.
    """

    BUILDER_CONFIG_CLASS = BidsConfig

    EXTENSIONS = [
        ".vhdr",
        ".ahdr",
        ".edf",
        ".bdf",
        ".gdf",
        ".set",
        ".fif",
        ".cnt",
        ".cdt",
        ".lay",
        ".mff",
        ".nwb",
        ".snirf",
        ".con",
        ".sqd",
        ".kit",
        ".ds",
        ".res4",
        ".mefd",
        ".nedf",
        ".nxe",
        ".ns3",
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="BIDS (Brain Imaging Data Structure) biosignal dataset: one row per recording.",
            features=self.config.features,
        )

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        if not datasets.config.MNE_BIDS_AVAILABLE:
            raise ImportError("To load BIDS datasets, please install 'mne-bids'.")

        def resolve_files(f: str) -> Iterable[str]:
            if f.lower().endswith(ARCHIVE_EXTENSIONS):
                return dl_manager.iter_files(dl_manager.download_and_extract(f))
            if is_local_path(f) and os.path.isdir(f):
                return dl_manager.iter_files(f)
            return [f]

        return [
            datasets.SplitGenerator(
                name=split_name,
                gen_kwargs={
                    "files_iterables": [resolve_files(f) for f in files],
                    "base_files": list(files),
                },
            )
            for split_name, files in self.config.data_files.items()
        ]

    def _generate_shards(self, base_files: list[str], files_iterables: list[Iterable[str]]) -> Iterator[str]:
        yield from base_files

    def _read_participants(
        self, root_key: Optional[str], download_config: DownloadConfig
    ) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
        candidates = ([xjoin(root_key, "participants.tsv")] if root_key else []) + (
            [xjoin(self.base_path, "participants.tsv")] if self.base_path else []
        )
        for tsv_path in dict.fromkeys(candidates):
            try:
                with xopen(tsv_path, "rb", download_config=download_config) as f:
                    raw = f.read()
            except FileNotFoundError:
                continue
            tbl = pa_csv.read_csv(
                io.BytesIO(raw),
                parse_options=pa_csv.ParseOptions(delimiter="\t"),
                convert_options=pa_csv.ConvertOptions(
                    column_types={"participant_id": pa.string()},
                    null_values=["n/a", "N/A", "na", "NA", ""],
                    strings_can_be_null=True,
                ),
            )
            extra_features = {
                col: (datasets.Value("string") if feat == datasets.Value("null") else feat)
                for col, feat in datasets.Features.from_arrow_schema(tbl.schema).items()
                if col not in ("participant_id", "biosignal", *BIDS_ENTITY_COLUMNS)
            }
            rows = {
                (r.pop("participant_id") or "").strip().removeprefix("sub-"): {
                    k: v for k, v in r.items() if k in extra_features
                }
                for r in tbl.to_pylist()
                if "participant_id" in r
            }
            return rows, extra_features
        return {}, {}

    def _generate_tables(
        self, base_files: list[str], files_iterables: list[Iterable[str]]
    ) -> Iterator[tuple[Key, pa.Table]]:
        import mne_bids
        from mne_bids.config import ALLOWED_INPUT_EXTENSIONS, EPHY_ALLOWED_DATATYPES
        from mne_bids.path import _filter_fnames

        extensions = self.config.extensions or list(
            {*self.EXTENSIONS, *(e.upper() for e in self.EXTENSIONS), *ALLOWED_INPUT_EXTENSIONS}
        )
        suffixes = self.config.suffixes or list(EPHY_ALLOWED_DATATYPES)
        datatypes = self.config.datatypes
        allowed_datatypes = set([datatypes] if isinstance(datatypes, str) else (datatypes or EPHY_ALLOWED_DATATYPES))
        download_config = DownloadConfig(token=self.token, storage_options=self.storage_options)
        participants_cache: dict[Optional[str], tuple[dict[str, dict[str, Any]], dict[str, Any]]] = {}
        allow_sourcedata = "sourcedata" in _logical_path(self.base_path or "").parts

        def get_participants(orig_f: Optional[str]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
            root_key = _bids_root(orig_f) if orig_f else None
            if root_key not in participants_cache:
                participants_cache[root_key] = self._read_participants(root_key, download_config)
            return participants_cache[root_key]

        def build_schema(extra_features: dict[str, Any]) -> pa.Schema:
            features = (
                self.info.features
                or self.config.features
                or datasets.Features(
                    {
                        "biosignal": datasets.Biosignal(preload=self.config.preload, decode=self.config.decode),
                        **{col: datasets.Value("string") for col in BIDS_ENTITY_COLUMNS},
                        **extra_features,
                    }
                )
            )
            return features.arrow_schema

        yielded = False
        first_file: Optional[str] = None
        for shard_idx, files_iterable in enumerate(files_iterables):
            path_map = {_logical_path(cf): cf for cf in (_collapse_container(f) for f in sorted(files_iterable))}
            first_file = first_file or next(iter(path_map.values()), None)
            records = []
            extra_features: dict[str, Any] = {}
            # ponytail: _filter_fnames until mne-bids>=0.20 exposes find_matching_paths(fnames=...) (mne-tools/mne-bids#1698)
            for rf in _filter_fnames(
                list(path_map),
                subject=self.config.subjects,
                session=self.config.sessions,
                task=self.config.tasks,
                acquisition=self.config.acquisitions,
                run=self.config.runs,
                suffix=suffixes,
                extension=extensions,
            ):
                orig_f = path_map[rf]
                if is_local_path(orig_f) and not os.path.exists(orig_f):
                    continue
                if not allow_sourcedata and "sourcedata" in rf.parts:
                    continue
                bp = mne_bids.get_bids_path_from_fname(rf, check=False, verbose="ERROR")
                datatype = bp.datatype or (bp.suffix if bp.suffix in EPHY_ALLOWED_DATATYPES else None)
                if datatype and datatype not in allowed_datatypes:
                    continue
                if datatype == "meg" and bp.acquisition == "crosstalk":
                    continue
                if bp.split and bp.split.isdigit() and int(bp.split) > 1:
                    continue
                part_rows, part_extra = get_participants(orig_f)
                extra_features.update(part_extra)
                records.append(
                    {
                        **part_rows.get(bp.subject or "", {}),
                        "biosignal": {"bytes": None, "path": orig_f},
                        "subject": bp.subject,
                        "session": bp.session,
                        "task": bp.task,
                        "acquisition": bp.acquisition,
                        "run": bp.run,
                        "datatype": datatype,
                        "suffix": bp.suffix,
                        "extension": bp.extension,
                    }
                )

            if records:
                schema = build_schema(extra_features)
                yield Key(shard_idx, 0), table_cast(pa.Table.from_pylist(records, schema=schema), schema)
                yielded = True

        if not yielded:
            schema = build_schema(get_participants(first_file)[1])
            yield Key(0, 0), pa.Table.from_pylist([], schema=schema)
