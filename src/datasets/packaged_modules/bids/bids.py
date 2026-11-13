"""Loader for BIDS (Brain Imaging Data Structure) datasets: one row per recording."""

import glob
import json
import os
import re
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Optional, Union

import pyarrow as pa
import pyarrow.csv as pa_csv

import datasets
from datasets.builder import Key


NIFTI_EXTENSIONS = (".nii", ".nii.gz")
NIFTI_DATATYPES = ("anat", "func", "dwi", "fmap", "perf", "pet", "mrs")
# BIDS electrophysiology recording extensions, let through data files resolution at import time (no mne-bids
# import there). Directory formats are found through the files they contain: `.res4` for CTF `.ds`
EXTENSIONS = (".vhdr", ".edf", ".bdf", ".set", ".fif", ".con", ".sqd", ".res4", ".mef", ".nwb", ".snirf")
# BIDS directory formats (CTF `.ds`, MEF3 `.mefd`) hold one recording: map the files inside to the directory
DIRECTORY_FORMAT_FILE = re.compile(r"(sub-[^/\\]*\.(?:ds|mefd))[/\\].*")
# participants.tsv is tab-separated with `n/a` for missing values (real datasets also use the other spellings)
TSV_OPTIONS = pa_csv.ParseOptions(delimiter="\t")
PARTICIPANTS_OPTIONS = pa_csv.ConvertOptions(
    column_types={"participant_id": pa.string()},
    null_values=["n/a", "N/A", "na", "NA", ""],
    strings_can_be_null=True,
)


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
        ephys_extensions = [
            ext for dt in EPHY_ALLOWED_DATATYPES for ext in ALLOWED_DATATYPE_EXTENSIONS[dt] if ext != ".pdf"
        ]
        filters = {
            "sub": cfg.subjects,
            "ses": cfg.sessions,
            "task": cfg.tasks,
            "acq": cfg.acquisitions,
            "run": cfg.runs,
            "datatype": cfg.datatypes or [*EPHY_ALLOWED_DATATYPES, *NIFTI_DATATYPES],
            "suffix": cfg.suffixes,
            "extension": cfg.extensions or [*ephys_extensions, *NIFTI_EXTENSIONS],
        }
        filters = {key: {value} if isinstance(value, str) else set(value) for key, value in filters.items() if value}
        reserved = {*ALLOWED_PATH_ENTITIES_SHORT.values(), "datatype", "suffix", "extension", "biosignal", "nifti"}

        # 1. Parse the BIDS filenames (`key-value_..._suffix.ext`) into one row per raw recording
        recordings = {split: [] for split in cfg.data_files}
        for split, files in cfg.data_files.items():
            for f in dict.fromkeys(DIRECTORY_FORMAT_FILE.sub(r"\1", f) for f in files):
                stem, _, ext = os.path.basename(f).partition(".")
                *pairs, suffix = stem.split("_")
                entities = dict(pair.split("-", 1) for pair in pairs if "-" in pair)
                # the recording, its datatype directory, [session directory,] subject directory, BIDS root
                dirs = [f]
                for _ in range(3 + ("ses" in entities)):
                    dirs.append(os.path.dirname(dirs[-1]))
                row = {
                    "nifti" if f.endswith(NIFTI_EXTENSIONS) else "biosignal": {"path": f, "bytes": None},
                    **{ALLOWED_PATH_ENTITIES_SHORT.get(k, k): v for k, v in entities.items() if k != "split"},
                    "datatype": os.path.basename(dirs[1]),
                    "suffix": suffix,
                    "extension": f".{ext}",
                }
                if any({**entities, **row}.get(key) not in values for key, values in filters.items()):
                    continue
                if entities.get("acq") == "crosstalk" or int(entities.get("split", 1)) > 1:
                    continue  # MEG calibration file, or a split FIF continuation (the recording is read from split-01)
                recordings[split].append((row, set(pairs), dirs))

        # 2. Read participants.tsv once per root and index JSON sidecars once per directory
        sidecars = defaultdict(set)  # directory -> JSON sidecars in it
        for directory in dict.fromkeys(
            directory for recs in recordings.values() for _, _, dirs in recs for directory in dirs[1:]
        ):
            sidecars[directory].update(glob.glob(os.path.join(directory, "*.json")))
        participants: dict[str, dict[str, dict[str, Any]]] = {}  # BIDS root -> subject -> participants.tsv row
        participant_features: dict[str, Any] = {}
        for root in dict.fromkeys(dirs[-1] for recs in recordings.values() for *_, dirs in recs):
            tsv = os.path.join(root, "participants.tsv")
            table = pa.table({})
            if os.path.exists(tsv):
                with open(tsv, "rb") as fp:
                    table = pa_csv.read_csv(fp, parse_options=TSV_OPTIONS, convert_options=PARTICIPANTS_OPTIONS)
            table = table.select([col for col in table.column_names if col not in reserved])
            participant_features.update(
                (col, feat)
                for col, feat in datasets.Features.from_arrow_schema(table.schema).items()
                if col != "participant_id" and feat != datasets.Value("null")
            )
            participants[root] = {
                (r.pop("participant_id", None) or "").removeprefix("sub-"): r for r in table.to_pylist()
            }

        # 3. Add the participant columns and the JSON sidecars that apply to each recording under the BIDS inheritance
        # principle: same suffix, entities that are a subset of the recording's, from the BIDS root down
        splits = {}
        for split, recs in recordings.items():
            rows, row_sidecars = [], []
            for row, pairs, dirs in recs:
                rows.append({**participants[dirs[-1]].get(row.get("subject"), {}), **row})
                inherited = [
                    path
                    for directory in reversed(dirs[1:])
                    for path in sorted(sidecars[directory], key=lambda path: (os.path.basename(path).count("_"), path))
                    if (parts := os.path.basename(path)[: -len(".json")].split("_"))[-1] == row["suffix"]
                    and set(parts[:-1]) <= pairs
                ]
                row_sidecars.append(inherited)
            splits[split] = rows, row_sidecars

        if self.info.features is None:
            typed = {
                "biosignal": datasets.Biosignal(decode=cfg.decode),
                "nifti": datasets.Nifti(decode=cfg.decode),
                **participant_features,
            }
            columns = dict.fromkeys(col for rows, _ in splits.values() for row in rows for col in row)
            features = {col: typed.get(col, datasets.Value("string")) for col in columns}
            self.info.features = datasets.Features({**features, "metadata": datasets.Json()})
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
        schema = self.info.features.arrow_schema
        sidecar_json = {}
        for path in dict.fromkeys(path for paths in sidecars for path in paths):
            with open(path, "rb") as f:
                sidecar_json[path] = json.load(f)
        for i, (row, paths) in enumerate(zip(rows, sidecars)):
            # lower-level sidecars override higher ones; BIDS sidecars are JSON objects, but real datasets also ship
            # invalid ones such as `[]`, which are skipped
            objects = [sidecar_json[path] for path in paths if isinstance(sidecar_json[path], dict)]
            metadata = {key: value for obj in objects for key, value in obj.items()}
            yield Key(i, 0), pa.Table.from_pylist([{**row, "metadata": json.dumps(metadata)}], schema=schema)
        if not rows:
            yield Key(0, 0), schema.empty_table()
