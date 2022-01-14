from typing import Any, List, Dict, Optional

from pathlib import Path
import os
import json

import numpy as np
import pandas as pd


def save_to_file(path: Path, data: List[Dict]):
    print(f"saving time-series into {path}")
    path_dir = os.path.dirname(path)
    os.makedirs(path_dir, exist_ok=True)
    with open(path, "wb") as fp:
        for d in data:
            fp.write(json.dumps(d).encode("utf-8"))
            fp.write("\n".encode("utf-8"))


def to_dict(
    target_values: np.ndarray,
    start: pd.Timestamp,
    cat: Optional[List[int]] = None,
    item_id: Optional[Any] = None,
    real: Optional[np.ndarray] = None,
) -> Dict:
    def serialize(x):
        if np.isnan(x):
            return "NaN"
        else:
            # return x
            return float("{0:.6f}".format(float(x)))

    res = {
        "start": str(start),
        "target": [serialize(x) for x in target_values],
    }

    if cat is not None:
        res["feat_static_cat"] = cat

    if item_id is not None:
        res["item_id"] = item_id

    if real is not None:
        res["feat_dynamic_real"] = real.astype(np.float32).tolist()
    return res
