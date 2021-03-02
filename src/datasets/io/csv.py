from ..packaged_modules.csv.csv import Csv
from .abc import AbstractDatasetBuilder


class CsvDatasetBuilder(AbstractDatasetBuilder):
    def __init__(
        self,
        path,
        split=None,
        features=None,
        cache_dir=None,
        **kwargs,
    ):
        super().__init__(path, split=split, features=features, cache_dir=cache_dir, **kwargs)
        self.builder = Csv(
            cache_dir=cache_dir,
            data_files=path,
            features=features,
            **kwargs,
        )

    def build(self):
        download_config = None
        download_mode = None
        ignore_verifications = False

        use_auth_token = None

        keep_in_memory = False
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
            split=self.split, ignore_verifications=ignore_verifications, in_memory=keep_in_memory
        )
        if save_infos:
            self.builder._save_infos()

        return ds
