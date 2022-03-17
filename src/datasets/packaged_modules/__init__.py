import inspect
import re
from hashlib import sha256
from typing import List

from .csv import csv
from .imagefolder import imagefolder
from .json import json
from .pandas import pandas
from .parquet import parquet
from .text import text


def _hash_python_lines(lines: List[str]) -> str:
    filtered_lines = []
    for line in lines:
        line = re.sub(r"#.*", "", line)  # remove comments
        if line:
            filtered_lines.append(line)
    full_str = "\n".join(filtered_lines)

    # Make a hash from all this code
    full_bytes = full_str.encode("utf-8")
    return sha256(full_bytes).hexdigest()


# get importable module names and hash for caching
_PACKAGED_DATASETS_MODULES = {
    "csv": (csv.__name__, _hash_python_lines(inspect.getsource(csv).splitlines())),
    "json": (json.__name__, _hash_python_lines(inspect.getsource(json).splitlines())),
    "pandas": (pandas.__name__, _hash_python_lines(inspect.getsource(pandas).splitlines())),
    "parquet": (parquet.__name__, _hash_python_lines(inspect.getsource(parquet).splitlines())),
    "text": (text.__name__, _hash_python_lines(inspect.getsource(text).splitlines())),
    "imagefolder": (imagefolder.__name__, _hash_python_lines(inspect.getsource(imagefolder).splitlines())),
}

_EXTENSION_TO_MODULE = {
    "csv": "csv",
    "tsv": "csv",
    "json": "json",
    "jsonl": "json",
    "parquet": "parquet",
    "txt": "text",
}
_EXTENSION_TO_MODULE.update({ext[1:]: "imagefolder" for ext in imagefolder.ImageFolder.IMAGE_EXTENSIONS})
