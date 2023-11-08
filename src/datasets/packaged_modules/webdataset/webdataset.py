import re
from typing import List

import numpy as np
import pyarrow as pa
from packaging import version

import datasets


logger = datasets.utils.logging.get_logger(__name__)


class Webdataset(datasets.GeneratorBasedBuilder):
    DEFAULT_WRITER_BATCH_SIZE = 100
    IMAGE_EXTENSIONS: List[str]  # definition at the bottom of the script
    ENABLED_BASIC_HANDLERS: List[str]  # definition at the bottom of the script

    def _basic_handlers(self, key, data):
        from webdataset.autodecode import decoders

        extension = re.sub(r".*[.]", "", key)
        if extension in decoders and extension in self.ENABLED_BASIC_HANDLERS:
            return decoders[extension](data)
        return None

    def _info(self) -> datasets.DatasetInfo:
        return datasets.DatasetInfo()

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        import webdataset as wds

        # Use the extended `open` to read hf:// files
        wds.gopen_schemes["hf"] = open

        # Download the data files
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download(self.config.data_files)
        if isinstance(data_files, (str, list, tuple)):
            files = data_files
            if isinstance(files, str):
                files = [files]
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": files})]
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))

        # Get one example to get the feature types
        pipeline = wds.DataPipeline(
            wds.SimpleShardList(files[:1]), wds.tarfile_to_samples(), wds.decode(post=[self._basic_handlers])
        )
        example = next(iter(pipeline))
        inferred_arrow_schema = pa.Table.from_pylist([example]).schema
        features = datasets.Features.from_arrow_schema(inferred_arrow_schema)

        # Set Image types
        for key in example:
            extension = re.sub(r".*[.]", "", key)
            if extension in self.IMAGE_EXTENSIONS:
                features[key] = datasets.Image()
        self.info.features = features

        return splits

    def _generate_examples(self, files):
        import webdataset as wds

        image_keys = [key for key, feature in self.info.features.items() if isinstance(feature, datasets.Image)]

        for file_idx, file in enumerate(files):
            pipeline = wds.DataPipeline(
                wds.SimpleShardList(file),
                wds.tarfile_to_samples(),
                wds.decode(post=[self._basic_handlers]),
            )
            for example_idx, example in enumerate(pipeline):
                for key in image_keys:
                    example[key] = {"path": example["__key__"] + "." + key, "bytes": example[key]}
                yield f"{file_idx}_{example_idx}", example


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
Webdataset.IMAGE_EXTENSIONS = IMAGE_EXTENSIONS


# Obtained by checking `decoders` in `webdataset.autodecode`
# and removing unsafe extension decoders.
# Removed Pickle decoders:
# - "pyd": lambda data: pickle.loads(data)
# - "pickle": lambda data: pickle.loads(data)
# Removed Torch decoders:
# - "pth": lambda data: torch_loads(data)
# Removed NumPy decoders for numpy < 1.16.3 (CVE-2019-6446):
# - "npy": npy_loads,
# - "npz": lambda data: np.load(io.BytesIO(data)),
ENABLED_BASIC_HANDLERS = [
    "txt",
    "text",
    "transcript",
    "cls",
    "cls2",
    "index",
    "inx",
    "id",
    "json",
    "jsn",
    "ten",
    "tb",
    "mp",
    "msg",
    "cbor",
]
if version.parse(np.__version__) >= version.parse("1.16.3"):
    ENABLED_BASIC_HANDLERS.extend(["npy", "npz"])
Webdataset.ENABLED_BASIC_HANDLERS = ENABLED_BASIC_HANDLERS
