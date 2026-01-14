import inspect
import re
from typing import Dict, List, Tuple

from huggingface_hub.utils import insecure_hashlib

from .arrow import arrow
from .audiofolder import audiofolder
from .cache import cache
from .csv import csv
from .eval import eval
from .hdf5 import hdf5
from .imagefolder import imagefolder
from .json import json
from .lance import lance
from .niftifolder import niftifolder
from .pandas import pandas
from .parquet import parquet
from .pdffolder import pdffolder
from .sql import sql
from .text import text
from .videofolder import videofolder
from .webdataset import webdataset
from .xml import xml


def _hash_python_lines(lines: list[str]) -> str:
    filtered_lines = []
    for line in lines:
        line = re.sub(r"#.*", "", line)  # remove comments
        if line:
            filtered_lines.append(line)
    full_str = "\n".join(filtered_lines)

    # Make a hash from all this code
    full_bytes = full_str.encode("utf-8")
    return insecure_hashlib.sha256(full_bytes).hexdigest()


# get importable module names and hash for caching
_PACKAGED_DATASETS_MODULES = {
    "csv": (csv.__name__, _hash_python_lines(inspect.getsource(csv).splitlines())),
    "json": (json.__name__, _hash_python_lines(inspect.getsource(json).splitlines())),
    "pandas": (pandas.__name__, _hash_python_lines(inspect.getsource(pandas).splitlines())),
    "parquet": (parquet.__name__, _hash_python_lines(inspect.getsource(parquet).splitlines())),
    "arrow": (arrow.__name__, _hash_python_lines(inspect.getsource(arrow).splitlines())),
    "text": (text.__name__, _hash_python_lines(inspect.getsource(text).splitlines())),
    "imagefolder": (imagefolder.__name__, _hash_python_lines(inspect.getsource(imagefolder).splitlines())),
    "audiofolder": (audiofolder.__name__, _hash_python_lines(inspect.getsource(audiofolder).splitlines())),
    "videofolder": (videofolder.__name__, _hash_python_lines(inspect.getsource(videofolder).splitlines())),
    "pdffolder": (pdffolder.__name__, _hash_python_lines(inspect.getsource(pdffolder).splitlines())),
    "niftifolder": (niftifolder.__name__, _hash_python_lines(inspect.getsource(niftifolder).splitlines())),
    "webdataset": (webdataset.__name__, _hash_python_lines(inspect.getsource(webdataset).splitlines())),
    "xml": (xml.__name__, _hash_python_lines(inspect.getsource(xml).splitlines())),
    "hdf5": (hdf5.__name__, _hash_python_lines(inspect.getsource(hdf5).splitlines())),
    "eval": (eval.__name__, _hash_python_lines(inspect.getsource(eval).splitlines())),
    "lance": (lance.__name__, _hash_python_lines(inspect.getsource(lance).splitlines())),
}

# get importable module names and hash for caching
_PACKAGED_DATASETS_MODULES_2_15_HASHES = {
    "csv": "eea64c71ca8b46dd3f537ed218fc9bf495d5707789152eb2764f5c78fa66d59d",
    "json": "8bb11242116d547c741b2e8a1f18598ffdd40a1d4f2a2872c7a28b697434bc96",
    "pandas": "3ac4ffc4563c796122ef66899b9485a3f1a977553e2d2a8a318c72b8cc6f2202",
    "parquet": "ca31c69184d9832faed373922c2acccec0b13a0bb5bbbe19371385c3ff26f1d1",
    "arrow": "74f69db2c14c2860059d39860b1f400a03d11bf7fb5a8258ca38c501c878c137",
    "text": "c4a140d10f020282918b5dd1b8a49f0104729c6177f60a6b49ec2a365ec69f34",
    "imagefolder": "7b7ce5247a942be131d49ad4f3de5866083399a0f250901bd8dc202f8c5f7ce5",
    "audiofolder": "d3c1655c66c8f72e4efb5c79e952975fa6e2ce538473a6890241ddbddee9071c",
}

# Used to infer the module to use based on the data files extensions
_EXTENSION_TO_MODULE: dict[str, tuple[str, dict]] = {
    ".csv": ("csv", {}),
    ".tsv": ("csv", {"sep": "\t"}),
    ".json": ("json", {}),
    ".jsonl": ("json", {}),
    # ndjson is no longer maintained (see: https://github.com/ndjson/ndjson-spec/issues/35#issuecomment-1285673417)
    ".ndjson": ("json", {}),
    ".parquet": ("parquet", {}),
    ".geoparquet": ("parquet", {}),
    ".gpq": ("parquet", {}),
    ".arrow": ("arrow", {}),
    ".txt": ("text", {}),
    ".tar": ("webdataset", {}),
    ".xml": ("xml", {}),
    ".hdf5": ("hdf5", {}),
    ".h5": ("hdf5", {}),
    ".eval": ("eval", {}),
    ".lance": ("lance", {}),
}
_EXTENSION_TO_MODULE.update({ext: ("imagefolder", {}) for ext in imagefolder.ImageFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext.upper(): ("imagefolder", {}) for ext in imagefolder.ImageFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext: ("audiofolder", {}) for ext in audiofolder.AudioFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext.upper(): ("audiofolder", {}) for ext in audiofolder.AudioFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext: ("videofolder", {}) for ext in videofolder.VideoFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext.upper(): ("videofolder", {}) for ext in videofolder.VideoFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext: ("pdffolder", {}) for ext in pdffolder.PdfFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext.upper(): ("pdffolder", {}) for ext in pdffolder.PdfFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext: ("niftifolder", {}) for ext in niftifolder.NiftiFolder.EXTENSIONS})
_EXTENSION_TO_MODULE.update({ext.upper(): ("niftifolder", {}) for ext in niftifolder.NiftiFolder.EXTENSIONS})

# Used to filter data files based on extensions given a module name
_MODULE_TO_EXTENSIONS: dict[str, list[str]] = {}
for _ext, (_module, _) in _EXTENSION_TO_MODULE.items():
    _MODULE_TO_EXTENSIONS.setdefault(_module, []).append(_ext)

for _module in _MODULE_TO_EXTENSIONS:
    _MODULE_TO_EXTENSIONS[_module].append(".zip")

# Used to filter data files based on file names
_MODULE_TO_METADATA_FILE_NAMES: Dict[str, List[str]] = {}
for _module in _MODULE_TO_EXTENSIONS:
    _MODULE_TO_METADATA_FILE_NAMES[_module] = []
_MODULE_TO_METADATA_FILE_NAMES["imagefolder"] = imagefolder.ImageFolder.METADATA_FILENAMES
_MODULE_TO_METADATA_FILE_NAMES["audiofolder"] = imagefolder.ImageFolder.METADATA_FILENAMES
_MODULE_TO_METADATA_FILE_NAMES["videofolder"] = imagefolder.ImageFolder.METADATA_FILENAMES
_MODULE_TO_METADATA_FILE_NAMES["pdffolder"] = imagefolder.ImageFolder.METADATA_FILENAMES
_MODULE_TO_METADATA_FILE_NAMES["niftifolder"] = imagefolder.ImageFolder.METADATA_FILENAMES

_MODULE_TO_METADATA_EXTENSIONS: Dict[str, List[str]] = {}
for _module in _MODULE_TO_EXTENSIONS:
    _MODULE_TO_METADATA_EXTENSIONS[_module] = []
_MODULE_TO_METADATA_EXTENSIONS["lance"] = lance.Lance.METADATA_EXTENSIONS

# Total

_ALL_EXTENSIONS = list(_EXTENSION_TO_MODULE.keys()) + [".zip"]
_ALL_METADATA_EXTENSIONS = list({_ext for _exts in _MODULE_TO_METADATA_EXTENSIONS.values() for _ext in _exts})
_ALL_ALLOWED_EXTENSIONS = _ALL_EXTENSIONS + _ALL_METADATA_EXTENSIONS
