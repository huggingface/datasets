import json
from dataclasses import dataclass
from typing import Optional

import datasets
from datasets import config


logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class BidsConfig(datasets.BuilderConfig):
    """BuilderConfig for BIDS datasets."""
    data_dir: Optional[str] = None
    database_path: Optional[str] = None  # For pybids caching
    subjects: Optional[list[str]] = None  # Filter by subject
    sessions: Optional[list[str]] = None  # Filter by session
    datatypes: Optional[list[str]] = None  # Filter by datatype


class Bids(datasets.GeneratorBasedBuilder):
    """BIDS dataset loader using pybids."""

    BUILDER_CONFIG_CLASS = BidsConfig

    def _info(self):
        if not config.PYBIDS_AVAILABLE:
            raise ImportError(
                "To load BIDS datasets, please install pybids: pip install pybids"
            )

        return datasets.DatasetInfo(
            features=datasets.Features({
                "subject": datasets.Value("string"),
                "session": datasets.Value("string"),
                "datatype": datasets.Value("string"),
                "suffix": datasets.Value("string"),
                "task": datasets.Value("string"),
                "run": datasets.Value("string"),
                "path": datasets.Value("string"),
                "nifti": datasets.Nifti(),
                "metadata": datasets.Value("string"),
            })
        )

    def _split_generators(self, dl_manager):
        from bids import BIDSLayout

        if not self.config.data_dir:
            raise ValueError("data_dir is required for BIDS datasets")

        layout = BIDSLayout(
            self.config.data_dir,
            database_path=self.config.database_path,
            validate=False,  # Don't fail on minor validation issues
        )

        # Build query kwargs
        query = {"extension": [".nii", ".nii.gz"]}
        if self.config.subjects:
            query["subject"] = self.config.subjects
        if self.config.sessions:
            query["session"] = self.config.sessions
        if self.config.datatypes:
            query["datatype"] = self.config.datatypes

        # Get all NIfTI files
        nifti_files = layout.get(**query)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"layout": layout, "files": nifti_files},
            )
        ]

    def _generate_examples(self, layout, files):
        for idx, bids_file in enumerate(files):
            entities = bids_file.get_entities()

            # Get JSON sidecar metadata
            metadata = layout.get_metadata(bids_file.path)
            metadata_str = json.dumps(metadata) if metadata else "{}"

            yield idx, {
                "subject": entities.get("subject"),
                "session": entities.get("session"),
                "datatype": entities.get("datatype"),
                "suffix": entities.get("suffix"),
                "task": entities.get("task"),
                "run": str(entities.get("run")) if entities.get("run") else None,
                "path": bids_file.path,
                "nifti": bids_file.path,
                "metadata": metadata_str,
            }