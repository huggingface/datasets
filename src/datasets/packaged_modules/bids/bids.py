"""Loader for BIDS (Brain Imaging Data Structure) datasets: one row per recording."""

import io
import json
import re
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Optional, Union

import pyarrow as pa
import pyarrow.csv as pa_csv

import datasets
from datasets.builder import Key
from datasets.download.download_config import DownloadConfig
from datasets.utils.file_utils import xbasename, xdirname, xglob, xjoin, xopen


NIFTI_EXTENSIONS = (".nii", ".nii.gz")
NIFTI_DATATYPES = ("anat", "func", "dwi", "fmap", "perf", "pet", "mrs")
# BIDS electrophysiology recording extensions, let through data files resolution at import time (no mne-bids
# import there); `.res4` is the CTF header file used to discover `.ds` directories
EXTENSIONS = (
    ".vhdr",
    ".edf",
    ".bdf",
    ".set",
    ".fif",
    ".con",
    ".sqd",
    ".pdf",
    ".ds",
    ".res4",
    ".mefd",
    ".nwb",
    ".snirf",
)
# BIDS directory formats (CTF `.ds`, MEF3 `.mefd`) hold one recording: map the files inside to the directory
DIRECTORY_FORMAT_FILE = re.compile(r"(sub-[^/\\]*\.(?:ds|mefd))[/\\].*")


@dataclass
class BidsConfig(datasets.BuilderConfig):
    """BuilderConfig for BIDS datasets.

    Args:
        subjects (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS subject label(s) (without the `sub-` prefix, e.g. `"01"`).
        sessions (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS session label(s) (without the `ses-` prefix).
        tasks (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS task label(s) (e.g. `"rest"`).
        acquisitions (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS acquisition label(s).
        runs (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS run index(es).
        datatypes (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS datatype(s) (e.g. `"eeg"`, `"meg"`, `"anat"`, `"func"`). Defaults to the
            electrophysiology datatypes read by `mne-bids` and the NIfTI datatypes; other directories (for example
            a non-BIDS `eye_tracker/`) are skipped.
        suffixes (`str` or `list[str]`, *optional*):
            Filter recordings by BIDS suffix(es) (e.g. `"eeg"`, `"T1w"`, `"bold"`).
        extensions (`str` or `list[str]`, *optional*):
            Recording file extension(s) to load. Defaults to the BIDS electrophysiology formats read by `mne-bids`
            and NIfTI (`.nii`, `.nii.gz`).
        sampling_rate (`float`, *optional*):
            Target sampling rate in Hz passed to [`Biosignal`].
        picks (`str` or `list[str]`, *optional*):
            Channels or channel types to retain (passed to [`Biosignal`]).
        preload (`bool`, defaults to `False`):
            Whether to preload signal data into memory when decoding local [`Biosignal`] recordings.
        decode (`bool`, defaults to `True`):
            Whether to decode the [`Biosignal`] and [`Nifti`] columns.
        features ([`Features`], *optional*):
            Explicit features schema override.

    Example:

    ```py
    >>> from datasets import load_dataset
    >>> ds = load_dataset("bids", data_dir="path/to/bids", subjects="01", datatypes="func", split="train")
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
    sampling_rate: Optional[float] = None
    picks: Optional[Union[str, list[str]]] = None
    preload: bool = False
    decode: bool = True
    decode_num_threads: int = 4
    features: Optional[datasets.Features] = None


class Bids(datasets.ArrowBasedBuilder):
    """Builder for BIDS (Brain Imaging Data Structure) datasets: one row per recording.

    It generates the following features:

    - **biosignal** ([`Biosignal`]) -- EEG, MEG, iEEG, EMG and NIRS recordings, decoded via `mne-bids` / `mne`.
    - **nifti** ([`Nifti`]) -- MRI, fMRI, diffusion, PET and MRS images, decoded via `nibabel`.
    - One `str` column per BIDS entity found in the filenames (e.g. **subject**, **session**, **task**, **run**,
      **echo**), plus **datatype**, **suffix** and **extension**.
    - **metadata** ([`Json`]) -- the JSON sidecars applying to the recording, merged following the BIDS inheritance
      principle.
    - Any additional participant metadata columns present in `participants.tsv`.
    """

    BUILDER_CONFIG_CLASS = BidsConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not datasets.config.MNE_BIDS_AVAILABLE:
            raise ImportError("To load BIDS datasets, please install 'mne-bids'.")
        from mne_bids.config import ALLOWED_DATATYPE_EXTENSIONS, ALLOWED_PATH_ENTITIES_SHORT, EPHY_ALLOWED_DATATYPES

        cfg = self.config
        filters = {
            key: {value} if isinstance(value, str) else set(value)
            for key, value in {
                "sub": cfg.subjects,
                "ses": cfg.sessions,
                "task": cfg.tasks,
                "acq": cfg.acquisitions,
                "run": cfg.runs,
                "datatype": cfg.datatypes or [*EPHY_ALLOWED_DATATYPES, *NIFTI_DATATYPES],
                "suffix": cfg.suffixes,
                "extension": cfg.extensions
                or [
                    *(ext for dt in EPHY_ALLOWED_DATATYPES for ext in ALLOWED_DATATYPE_EXTENSIONS[dt]),
                    *NIFTI_EXTENSIONS,
                ],
            }.items()
            if value
        }
        reserved = {*ALLOWED_PATH_ENTITIES_SHORT.values(), "datatype", "suffix", "extension", "biosignal", "nifti"}
        sidecars = defaultdict(set)  # directory -> JSON sidecars in it
        for f in (f for files in cfg.data_files.values() for f in files if f.endswith(".json")):
            sidecars[xdirname(f)].add(f)
        participants: dict[str, dict[str, dict[str, Any]]] = {}  # BIDS root -> subject -> participants.tsv row
        participant_features: dict[str, Any] = {}

        splits = {}
        for split, files in cfg.data_files.items():
            rows, row_sidecars = [], []
            for f in dict.fromkeys(DIRECTORY_FORMAT_FILE.sub(r"\1", f) for f in files):
                stem, _, ext = xbasename(f).partition(".")
                *pairs, suffix = stem.split("_")
                entities = dict(pair.split("-", 1) for pair in pairs if "-" in pair)
                dirs = [f]  # the recording, its datatype directory, [session directory,] subject directory, BIDS root
                for _ in range(3 + ("ses" in entities)):
                    dirs.append(xdirname(dirs[-1]))
                row = {"datatype": xbasename(dirs[1]), "suffix": suffix, "extension": f".{ext}"}
                if (
                    any({**entities, **row}.get(key) not in values for key, values in filters.items())
                    or entities.get("acq") == "crosstalk"  # MEG calibration file, not a recording
                    or int(entities.get("split", 1)) > 1  # split FIF recordings are read from split-01
                ):
                    continue
                root = dirs[-1]
                if root not in participants:
                    sidecars[root].update(xglob(xjoin(root, "*.json"), download_config=dl_manager.download_config))
                    try:
                        with xopen(
                            xjoin(root, "participants.tsv"), "rb", download_config=dl_manager.download_config
                        ) as fp:
                            table = pa_csv.read_csv(
                                io.BytesIO(fp.read()),
                                parse_options=pa_csv.ParseOptions(delimiter="\t"),
                                convert_options=pa_csv.ConvertOptions(
                                    column_types={"participant_id": pa.string()},
                                    null_values=["n/a", "N/A", "na", "NA", ""],
                                    strings_can_be_null=True,
                                ),
                            )
                    except FileNotFoundError:
                        table = pa.table({})
                    participant_features.update(
                        (col, datasets.Value("string") if feat == datasets.Value("null") else feat)
                        for col, feat in datasets.Features.from_arrow_schema(table.schema).items()
                        if col not in reserved
                    )
                    participants[root] = {
                        (r.pop("participant_id", None) or "").removeprefix("sub-"): r for r in table.to_pylist()
                    }
                media = "nifti" if f.endswith(NIFTI_EXTENSIONS) else "biosignal"
                rows.append(
                    {
                        **{
                            k: v
                            for k, v in participants[root].get(entities.get("sub"), {}).items()
                            if k not in reserved
                        },
                        media: {"path": f, "bytes": None},
                        **{ALLOWED_PATH_ENTITIES_SHORT.get(k, k): v for k, v in entities.items() if k != "split"},
                        **row,
                    }
                )
                row_sidecars.append(
                    [
                        path  # inheritance principle: same suffix, entities subset, merged from the root down
                        for directory in reversed(dirs[1:])
                        for path in sorted(sidecars[directory])
                        if (parts := xbasename(path)[: -len(".json")].split("_"))[-1] == suffix
                        and set(parts[:-1]) <= set(pairs)
                    ]
                )
            splits[split] = rows, row_sidecars

        if self.info.features is None:
            media_features = {
                "biosignal": datasets.Biosignal(
                    sampling_rate=cfg.sampling_rate, picks=cfg.picks, preload=cfg.preload, decode=cfg.decode
                ),
                "nifti": datasets.Nifti(decode=cfg.decode),
            }
            columns = dict.fromkeys(col for rows, _ in splits.values() for row in rows for col in row)
            self.info.features = datasets.Features(
                {
                    **{
                        col: media_features.get(col) or participant_features.get(col) or datasets.Value("string")
                        for col in columns
                    },
                    "metadata": datasets.Json(),
                }
            )
        return [
            datasets.SplitGenerator(name=split, gen_kwargs={"rows": rows, "sidecars": row_sidecars})
            for split, (rows, row_sidecars) in splits.items()
        ]

    def _generate_shards(self, rows: list[dict[str, Any]], sidecars: list[list[str]]) -> Iterator[str]:
        for row in rows:
            yield (row.get("biosignal") or row["nifti"])["path"]

    def _generate_tables(
        self, rows: list[dict[str, Any]], sidecars: list[list[str]]
    ) -> Iterator[tuple[Key, pa.Table]]:
        download_config = DownloadConfig(token=self.token, storage_options=self.storage_options)
        schema = self.info.features.arrow_schema
        cache: dict[str, dict[str, Any]] = {}
        for i, (row, paths) in enumerate(zip(rows, sidecars)):
            metadata = {}
            for path in paths:
                if path not in cache:
                    with xopen(path, "rb", download_config=download_config) as f:
                        cache[path] = json.load(f)
                if isinstance(cache[path], dict):  # BIDS sidecars are JSON objects; real datasets ship `[]`
                    metadata.update(cache[path])
            yield Key(i, 0), pa.Table.from_pylist([{**row, "metadata": json.dumps(metadata)}], schema=schema)
        if not rows:
            yield Key(0, 0), schema.empty_table()
