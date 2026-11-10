"""Loader for BIDS (Brain Imaging Data Structure) electrophysiology and biosignal datasets."""

import os
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
    METADATA_FILENAMES = [
        "dataset_description.json",
        "participants.tsv",
        "participants.json",
        "README",
        "CHANGES",
    ]
    METADATA_EXTENSIONS = [
        ".tsv",
        ".tsv.gz",
        ".json",
        ".vmrk",
        ".amrk",
        ".eeg",
        ".fdt",
        ".dat",
        ".mrk",
        ".pos",
        ".dpa",
        ".cef",
    ]

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
        ext_set = {e.lower() for e in ([extensions] if isinstance(extensions, str) else extensions)}
        suffixes = self.config.suffixes or list(EPHY_ALLOWED_DATATYPES)
        datatypes = self.config.datatypes
        allowed_datatypes = set([datatypes] if isinstance(datatypes, str) else (datatypes or EPHY_ALLOWED_DATATYPES))

        participants_cache: dict[Path, dict[str, dict[str, Any]]] = {}
        all_extra_features: dict[str, datasets.Value] = {}
        split_records: dict[str, list[dict[str, Any]]] = {}

        for split_name, files in self.config.data_files.items():
            if isinstance(files, str):
                files = [files]
            paths = [f if os.path.exists(f) else dl_manager.download_and_extract(f) for f in files]

            bids_roots: list[Path] = []
            seen_roots: set[Path] = set()
            recording_files: list[Path] = []

            for raw_p in paths:
                p = Path(raw_p)
                if p.name == "dataset_description.json":
                    if p.parent not in seen_roots:
                        seen_roots.add(p.parent)
                        bids_roots.append(p.parent)
                elif p.suffix.lower() in ext_set:
                    recording_files.append(p)
                elif p.is_dir():
                    desc_files = (
                        [p / "dataset_description.json"]
                        if (p / "dataset_description.json").is_file()
                        else list(p.rglob("dataset_description.json"))
                    )
                    for root in [df.parent for df in sorted(desc_files)] or [p]:
                        if root not in seen_roots:
                            seen_roots.add(root)
                            bids_roots.append(root)

            bids_roots = [r for r in bids_roots if not any(p in seen_roots for p in r.parents)]
            bids_paths: list[mne_bids.BIDSPath] = []
            if not recording_files:
                for root in bids_roots:
                    bids_paths.extend(
                        mne_bids.find_matching_paths(
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
                    )
            else:
                top_root = bids_roots[0] if len(bids_roots) == 1 else None
                for rf in _filter_fnames(
                    sorted(recording_files),
                    subject=self.config.subjects,
                    session=self.config.sessions,
                    task=self.config.tasks,
                    acquisition=self.config.acquisitions,
                    run=self.config.runs,
                    suffix=suffixes,
                    extension=extensions,
                ):
                    bp = mne_bids.get_bids_path_from_fname(rf, check=False, verbose="ERROR")
                    root = top_root or (Path(bp.root) if bp.root else None)
                    if root is not None:
                        if root.name in ("sourcedata", "derivatives"):
                            continue
                        try:
                            rel_parts = rf.relative_to(root).parts
                            if rel_parts and rel_parts[0] in ("sourcedata", "derivatives"):
                                continue
                        except ValueError:
                            pass
                        bp.root = root
                    bids_paths.append(bp)

            for root in dict.fromkeys([*bids_roots, *(Path(bp.root) for bp in bids_paths if bp.root is not None)]):
                if root in participants_cache:
                    continue
                tsv_path = root / "participants.tsv"
                by_sub: dict[str, dict[str, Any]] = {}
                if tsv_path.is_file():
                    tbl = pa_csv.read_csv(
                        tsv_path,
                        parse_options=pa_csv.ParseOptions(delimiter="\t"),
                        convert_options=pa_csv.ConvertOptions(
                            column_types={"participant_id": pa.string()},
                            null_values=["n/a", "N/A", "na", "NA", ""],
                            strings_can_be_null=True,
                        ),
                    )
                    if "participant_id" in tbl.column_names:
                        tbl = tbl.drop([c for c in tbl.column_names if c in ("biosignal", *BIDS_ENTITY_COLUMNS)])
                        tbl = tbl.cast(
                            pa.schema(
                                [f.with_type(pa.string()) if pa.types.is_null(f.type) else f for f in tbl.schema]
                            )
                        )
                        for col, feat in datasets.Features.from_arrow_schema(tbl.schema).items():
                            if col != "participant_id":
                                all_extra_features.setdefault(col, feat)
                        by_sub = {
                            (r.pop("participant_id") or "").strip().removeprefix("sub-"): r for r in tbl.to_pylist()
                        }
                participants_cache[root] = by_sub

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
                        "biosignal": {"bytes": None, "path": str(fpath)},
                        "subject": bp.subject,
                        "session": bp.session,
                        "task": bp.task,
                        "acquisition": bp.acquisition,
                        "run": bp.run,
                        "datatype": datatype,
                        "suffix": bp.suffix,
                        "extension": bp.extension,
                        **sub_meta,
                    }
                )
            split_records[split_name] = records

        if self.config.features is None and all_extra_features:
            self.info.features = datasets.Features(
                {
                    "biosignal": datasets.Biosignal(preload=self.config.preload, decode=self.config.decode),
                    **{col: datasets.Value("string") for col in BIDS_ENTITY_COLUMNS},
                    **all_extra_features,
                }
            )

        splits = []
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
