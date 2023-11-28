import io
import json
from itertools import islice
from typing import Any, Callable, Dict, List

import numpy as np
import pyarrow as pa

import datasets


logger = datasets.utils.logging.get_logger(__name__)


class WebDataset(datasets.GeneratorBasedBuilder):
    DEFAULT_WRITER_BATCH_SIZE = 100
    IMAGE_EXTENSIONS: List[str]  # definition at the bottom of the script
    DECODERS: Dict[str, Callable[[Any], Any]]  # definition at the bottom of the script
    NUM_EXAMPLES_FOR_FEATURES_INFERENCE = 5

    @classmethod
    def _get_pipeline_from_tar(cls, tar_path, tar_iterator):
        current_example = {}
        for filename, f in tar_iterator:
            if "." in filename:
                example_key, field_name = filename.split(".", 1)
                if current_example and current_example["__key__"] != example_key:
                    yield current_example
                    current_example = {}
                current_example["__key__"] = example_key
                current_example["__url__"] = tar_path
                current_example[field_name.lower()] = f.read()
                if field_name in cls.DECODERS:
                    current_example[field_name] = cls.DECODERS[field_name](current_example[field_name])
        if current_example:
            yield current_example

    def _info(self) -> datasets.DatasetInfo:
        return datasets.DatasetInfo()

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        # Download the data files
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            tar_paths = data_files
            if isinstance(tar_paths, str):
                tar_paths = [tar_paths]
            tar_iterators = [dl_manager.iter_archive(tar_path) for tar_path in tar_paths]
            splits = [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN, gen_kwargs={"tar_paths": tar_paths, "tar_iterators": tar_iterators}
                )
            ]
        else:
            splits = []
            for split_name, tar_paths in data_files.items():
                if isinstance(tar_paths, str):
                    tar_paths = [tar_paths]
                tar_iterators = [dl_manager.iter_archive(tar_path) for tar_path in tar_paths]
                splits.append(
                    datasets.SplitGenerator(
                        name=split_name, gen_kwargs={"tar_paths": tar_paths, "tar_iterators": tar_iterators}
                    )
                )

        # Get one example to get the feature types
        pipeline = self._get_pipeline_from_tar(tar_paths[0], tar_iterators[0])
        first_examples = list(islice(pipeline, self.NUM_EXAMPLES_FOR_FEATURES_INFERENCE))
        if any(example.keys() != first_examples[0].keys() for example in first_examples):
            raise ValueError(
                "The TAR archives of the dataset should be in WebDataset format, "
                "but the files in the archive don't share the same prefix or the same types."
            )
        inferred_arrow_schema = pa.Table.from_pylist(first_examples[:1]).schema
        features = datasets.Features.from_arrow_schema(inferred_arrow_schema)

        # Set Image types
        for field_name in first_examples[0]:
            extension = field_name.rsplit(".", 1)[-1]
            if extension in self.IMAGE_EXTENSIONS:
                features[field_name] = datasets.Image()
        self.info.features = features

        return splits

    def _generate_examples(self, tar_paths, tar_iterators):
        image_field_names = [
            field_name for field_name, feature in self.info.features.items() if isinstance(feature, datasets.Image)
        ]
        for tar_idx, (tar_path, tar_iterator) in enumerate(zip(tar_paths, tar_iterators)):
            for example_idx, example in enumerate(self._get_pipeline_from_tar(tar_path, tar_iterator)):
                for field_name in image_field_names:
                    example[field_name] = {"path": example["__key__"] + "." + field_name, "bytes": example[field_name]}
                yield f"{tar_idx}_{example_idx}", example


# Obtained with:
# ```
# import PIL.Image
# IMAGE_EXTENSIONS = []
# PIL.Image.init()
# for ext, format in PIL.Image.EXTENSION.items():
#     if format in PIL.Image.OPEN:
#         IMAGE_EXTENSIONS.append(ext[1:])
# ```
# We intentionally do not run this code on launch because:
# (1) Pillow is an optional dependency, so importing Pillow in global namespace is not allowed
# (2) To ensure the list of supported extensions is deterministic
IMAGE_EXTENSIONS = [
    "blp",
    "bmp",
    "dib",
    "bufr",
    "cur",
    "pcx",
    "dcx",
    "dds",
    "ps",
    "eps",
    "fit",
    "fits",
    "fli",
    "flc",
    "ftc",
    "ftu",
    "gbr",
    "gif",
    "grib",
    "h5",
    "hdf",
    "png",
    "apng",
    "jp2",
    "j2k",
    "jpc",
    "jpf",
    "jpx",
    "j2c",
    "icns",
    "ico",
    "im",
    "iim",
    "tif",
    "tiff",
    "jfif",
    "jpe",
    "jpg",
    "jpeg",
    "mpg",
    "mpeg",
    "msp",
    "pcd",
    "pxr",
    "pbm",
    "pgm",
    "ppm",
    "pnm",
    "psd",
    "bw",
    "rgb",
    "rgba",
    "sgi",
    "ras",
    "tga",
    "icb",
    "vda",
    "vst",
    "webp",
    "wmf",
    "emf",
    "xbm",
    "xpm",
]
WebDataset.IMAGE_EXTENSIONS = IMAGE_EXTENSIONS


def text_loads(data: bytes):
    return data.decode("utf-8")


def tenbin_loads(data: bytes):
    from . import _tenbin

    return _tenbin.decode_buffer(data)


def msgpack_loads(data: bytes):
    import msgpack

    return msgpack.unpackb(data)


def npy_loads(data: bytes):
    import numpy.lib.format

    stream = io.BytesIO(data)
    return numpy.lib.format.read_array(stream, allow_pickle=False)


def npz_loads(data: bytes):
    return np.load(io.BytesIO(data), allow_pickle=False)


def cbor_loads(data: bytes):
    import cbor

    return cbor.loads(data)


# Obtained by checking `decoders` in `webdataset.autodecode`
# and removing unsafe extension decoders.
# Removed Pickle decoders:
# - "pyd": lambda data: pickle.loads(data)
# - "pickle": lambda data: pickle.loads(data)
# Removed Torch decoders:
# - "pth": lambda data: torch_loads(data)
# Modified NumPy decoders to fix CVE-2019-6446 (add allow_pickle=False):
# - "npy": npy_loads,
# - "npz": lambda data: np.load(io.BytesIO(data)),
DECODERS = {
    "txt": text_loads,
    "text": text_loads,
    "transcript": text_loads,
    "cls": int,
    "cls2": int,
    "index": int,
    "inx": int,
    "id": int,
    "json": json.loads,
    "jsn": json.loads,
    "ten": tenbin_loads,
    "tb": tenbin_loads,
    "mp": msgpack_loads,
    "msg": msgpack_loads,
    "npy": npy_loads,
    "npz": npz_loads,
    "cbor": cbor_loads,
}
WebDataset.DECODERS = DECODERS
