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
        data_files = dl_manager.download(self.config.data_files)
        return [
            datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files})
            for split_name, files in data_files.items()
        ]

    def _generate_tables(self, files: Union[str, list[str]]) -> Iterator[tuple[int, pa.Table]]:
        import mne_bids
        from mne_bids.config import ALLOWED_INPUT_EXTENSIONS, EPHY_ALLOWED_DATATYPES
        from mne_bids.path import _filter_fnames

        extensions = self.config.extensions or list(
            {*self.EXTENSIONS, *(e.upper() for e in self.EXTENSIONS), *ALLOWED_INPUT_EXTENSIONS}
        )
        suffixes = self.config.suffixes or list(EPHY_ALLOWED_DATATYPES)
        datatypes = self.config.datatypes
        allowed_datatypes = set([datatypes] if isinstance(datatypes, str) else (datatypes or EPHY_ALLOWED_DATATYPES))

        paths = sorted(Path(f) for f in (files if isinstance(files, list) else [files]))
        bids_paths = [
            mne_bids.get_bids_path_from_fname(rf, check=False, verbose="ERROR")
            for rf in _filter_fnames(
                paths,
                subject=self.config.subjects,
                session=self.config.sessions,
                task=self.config.tasks,
                acquisition=self.config.acquisitions,
                run=self.config.runs,
                suffix=suffixes,
                extension=extensions,
            )
        ]

        participants: dict[Path, dict[str, dict[str, Any]]] = {}
        for root in dict.fromkeys(Path(bp.root) for bp in bids_paths if bp.root is not None):
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
            participants[root] = {
                (r.pop("participant_id") or "").strip().removeprefix("sub-"): r for r in rows if "participant_id" in r
            }

        records = [
            {
                **(participants.get(Path(bp.root), {}).get(bp.subject or "", {}) if bp.root is not None else {}),
                "biosignal": {"bytes": None, "path": str(bp.fpath)},
                "subject": bp.subject,
                "session": bp.session,
                "task": bp.task,
                "acquisition": bp.acquisition,
                "run": bp.run,
                "datatype": datatype,
                "suffix": bp.suffix,
                "extension": bp.extension,
            }
            for bp in bids_paths
            if bp.fpath.exists()
            and (
                not (datatype := bp.datatype or (bp.suffix if bp.suffix in EPHY_ALLOWED_DATATYPES else None))
                or datatype in allowed_datatypes
            )
        ]

        pa_table = pa.Table.from_pylist(records)
        features = self.config.features or datasets.Features(
            {
                "biosignal": datasets.Biosignal(preload=self.config.preload, decode=self.config.decode),
                **{col: datasets.Value("string") for col in BIDS_ENTITY_COLUMNS},
                **{
                    col: (datasets.Value("string") if feat == datasets.Value("null") else feat)
                    for col, feat in datasets.Features.from_arrow_schema(pa_table.schema).items()
                    if col not in ("biosignal", *BIDS_ENTITY_COLUMNS)
                },
            }
        )
        schema = features.arrow_schema
        yield 0, table_cast(pa.Table.from_pylist(records, schema=schema), schema)
