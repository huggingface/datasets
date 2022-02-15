from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


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
        "start": start,
        "target": [serialize(x) for x in target_values],
    }

    if cat is not None:
        res["feat_static_cat"] = cat

    if item_id is not None:
        res["item_id"] = item_id

    if real is not None:
        res["feat_dynamic_real"] = real.astype(np.float32).tolist()
    return res
