from typing import Optional

from .. import Features, NamedSplit
from ..packaged_modules.json.json import Json
from ..utils.typing import PathLike
from .abc import AbstractDatasetReader


class JsonDatasetReader(AbstractDatasetReader):
    def __init__(
        self,
        path: PathLike,
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ):
        super().__init__(
            path, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        )
        self.builder = Json(
            cache_dir=cache_dir,
            data_files=path,
            features=features,
            **kwargs,
        )

    def read(self):
        download_config = None
        download_mode = None
        ignore_verifications = False
        use_auth_token = None
        save_infos = False
        base_path = None

        self.builder.download_and_prepare(
            download_config=download_config,
            download_mode=download_mode,
            ignore_verifications=ignore_verifications,
            # try_from_hf_gcs=try_from_hf_gcs,
            base_path=base_path,
            use_auth_token=use_auth_token,
        )

        # Build dataset for splits
        ds = self.builder.as_dataset(
            split=self.split, ignore_verifications=ignore_verifications, in_memory=self.keep_in_memory
        )
        if save_infos:
            self.builder._save_infos()

        return ds
