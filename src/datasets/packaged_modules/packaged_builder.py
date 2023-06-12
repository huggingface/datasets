from dataclasses import dataclass
from typing import Optional

import datasets


@dataclass
class PackagedBuilderConfig(datasets.BuilderConfig):
    """BuilderConfig for packaged builders."""

    only_supported_extensions: Optional[bool] = None
