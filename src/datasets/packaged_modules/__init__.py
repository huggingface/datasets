import inspect
import re
from hashlib import sha256
from typing import List

from .csv import csv
from .json import json
from .pandas import pandas
from .text import text


def hash_python_lines(lines: List[str]) -> str:
    filtered_lines = []
    for line in lines:
        line.replace("\n", "")  # remove line breaks, white space and comments
        line.replace(" ", "")
        line.replace("\t", "")
        line = re.sub(r"#.*", "", line)
        if line:
            filtered_lines.append(line)
    full_str = "\n".join(filtered_lines)

    # Make a hash from all this code
    full_bytes = full_str.encode("utf-8")
    return sha256(full_bytes).hexdigest()


# get importable module names and hash for caching
_PACKAGED_DATASETS_MODULES = {
    "csv": (csv.__name__, hash_python_lines(inspect.getsource(csv).splitlines())),
    "json": (json.__name__, hash_python_lines(inspect.getsource(json).splitlines())),
    "pandas": (pandas.__name__, hash_python_lines(inspect.getsource(pandas).splitlines())),
    "text": (text.__name__, hash_python_lines(inspect.getsource(text).splitlines())),
}
