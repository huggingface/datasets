"""Loader for BIDS (Brain Imaging Data Structure) electrophysiology and biosignal datasets."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

import pyarrow as pa
import pyarrow.csv as pa_csv

import datasets
from datasets.table import table_cast


BIDS_ENTITY_COLUMNS = ("subject", "session", "task", "acquisition", "run", "datatype", "suffix", "extension")


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
    """Builder for BIDS (Brain Imaging Data Structure) datasets using `mne-bids`: one row per recording."""

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
        ".mefd",
        ".nedf",
        ".nxe",
        ".ns3",
    ]
    METADATA_FILENAMES = ["dataset_description.json"]

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

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        if not datasets.config.MNE_BIDS_AVAILABLE:
            raise ImportError("To load BIDS datasets, please install 'mne-bids'.")
        import mne_bids
        from mne_bids.config import ALLOWED_INPUT_EXTENSIONS, EPHY_ALLOWED_DATATYPES
        from mne_bids.path import _filter_fnames

        extensions = self.config.extensions or list(
            {*self.EXTENSIONS, *(e.upper() for e in self.EXTENSIONS), *ALLOWED_INPUT_EXTENSIONS}
        )
        suffixes = self.config.suffixes or list(EPHY_ALLOWED_DATATYPES)
        datatypes = self.config.datatypes
        allowed_datatypes = set([datatypes] if isinstance(datatypes, str) else (datatypes or EPHY_ALLOWED_DATATYPES))

        data_files = (
            dl_manager.download(self.config.data_files)
            if getattr(dl_manager, "is_streaming", False)
            else dl_manager.download_and_extract(self.config.data_files)
        )
        participants_cache: dict[Path, dict[str, dict[str, Any]]] = {}
        split_records: dict[str, list[dict[str, Any]]] = {}

        for split_name, files in data_files.items():
            paths = [Path(f) for f in (files if isinstance(files, list) else [files])]
            roots = list(
                dict.fromkeys(
                    p.parent
                    if p.name == "dataset_description.json"
                    else next((d.parent for d in sorted(p.rglob("dataset_description.json"))), p)
                    for p in paths
                    if p.name == "dataset_description.json" or p.is_dir()
                )
            )
            recording_files = [p for p in paths if p.name != "dataset_description.json" and p.is_file()]
            if not recording_files:
                bids_paths = [
                    bp
                    for root in roots
                    for bp in mne_bids.find_matching_paths(
                        root,
                        subjects=self.config.subjects,
                        sessions=self.config.sessions,
                        tasks=self.config.tasks,
                        acquisitions=self.config.acquisitions,
                        runs=self.config.runs,
                        datatypes=datatypes,
                        suffixes=suffixes,
                        extensions=extensions,
                        check=False,
                        ignore_json=True,
                        ignore_nosub=True,
                    )
                ]
            else:
                bids_paths = [
                    bp
                    for rf in _filter_fnames(
                        sorted(recording_files),
                        subject=self.config.subjects,
                        session=self.config.sessions,
                        task=self.config.tasks,
                        acquisition=self.config.acquisitions,
                        run=self.config.runs,
                        suffix=suffixes,
                        extension=extensions,
                    )
                    if (bp := mne_bids.get_bids_path_from_fname(rf, check=False, verbose="ERROR")).root is None
                    or Path(bp.root).name not in ("sourcedata", "derivatives")
                ]

            for root in dict.fromkeys([*roots, *(Path(bp.root) for bp in bids_paths if bp.root is not None)]):
                if root in participants_cache:
                    continue
                tsv_path = root / "participants.tsv"
                rows = (
                    pa_csv.read_csv(
                        tsv_path,
                        parse_options=pa_csv.ParseOptions(delimiter="\t"),
                        convert_options=pa_csv.ConvertOptions(
                            column_types={"participant_id": pa.string()},
                            null_values=["n/a", "N/A", "na", "NA", ""],
                            strings_can_be_null=True,
                        ),
                    ).to_pylist()
                    if tsv_path.is_file()
                    else []
                )
                participants_cache[root] = {
                    (r.pop("participant_id") or "").strip().removeprefix("sub-"): r
                    for r in rows
                    if "participant_id" in r
                }

            records: list[dict[str, Any]] = []
            for bp in bids_paths:
                fpath = bp.fpath
                if not fpath.exists():
                    continue
                datatype = bp.datatype or (bp.suffix if bp.suffix in EPHY_ALLOWED_DATATYPES else None)
                if datatype and datatype not in allowed_datatypes:
                    continue
                root = Path(bp.root) if bp.root is not None else None
                sub_meta = participants_cache.get(root, {}).get(bp.subject or "", {}) if root else {}
                records.append(
                    {
                        **sub_meta,
                        "biosignal": {"bytes": None, "path": str(fpath)},
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
            split_records[split_name] = records

        if self.config.features is None and (all_records := [r for recs in split_records.values() for r in recs]):
            for col, feat in datasets.Features.from_arrow_schema(pa.Table.from_pylist(all_records).schema).items():
                if col not in self.info.features:
                    self.info.features[col] = datasets.Value("string") if feat == datasets.Value("null") else feat

        return [
            datasets.SplitGenerator(name=split_name, gen_kwargs={"records": records})
            for split_name, records in split_records.items()
        ]

    def _generate_tables(self, records: list[dict[str, Any]]) -> Iterator[tuple[int, pa.Table]]:
        schema = self.info.features.arrow_schema
        yield 0, table_cast(pa.Table.from_pylist(records, schema=schema), schema)
