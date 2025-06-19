import os
import h5py
import datasets

logger = datasets.logging.get_logger(__name__)

_DESCRIPTION = """\
Load datasets stored in HDF5 (.h5) format.
This loader expects a specific structure within the HDF5 file: each feature (column) should be a top-level dataset.
All datasets should have the same length (number of rows).
"""

_HOMEPAGE = "https://www.h5py.org/"

_CITATION = """"""

class H5FolderConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class H5Folder(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = H5FolderConfig

    def _info(self):
        # NOTE: You can later modify features to be dynamic if needed
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({
                "id": datasets.Value("int32"),
                "data": datasets.Sequence(datasets.Value("float32")),  # or other shape
                "label": datasets.ClassLabel(names=["class_0", "class_1"]),
            }),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_path = os.path.join(self.config.data_dir or dl_manager.manual_dir, "data.h5")

        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Expected HDF5 file at {data_path}")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_path},
            )
        ]

    def _generate_examples(self, filepath):
        """Yields examples from the HDF5 file."""
        logger.info(f"Opening HDF5 file: {filepath}")
        with h5py.File(filepath, "r") as f:
            # Assume structure: /data, /label, /id or similar
            data = f["data"]
            labels = f["label"]
            ids = f["id"] if "id" in f else range(len(data))

            for idx in range(len(data)):
                yield idx, {
                    "id": int(ids[idx]) if "id" in f else idx,
                    "data": data[idx].tolist(),  # Convert from numpy array
                    "label": int(labels[idx]),
                }
