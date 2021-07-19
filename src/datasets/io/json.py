import os
from typing import BinaryIO, Optional, Union

from .. import Dataset, Features, NamedSplit, config, utils
from ..formatting import query_table
from ..packaged_modules.json.json import Json
from ..utils import logging
from ..utils.typing import NestedDataStructureLike, PathLike
from .abc import AbstractDatasetReader


class JsonDatasetReader(AbstractDatasetReader):
    def __init__(
        self,
        path_or_paths: NestedDataStructureLike[PathLike],
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        field: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            path_or_paths, split=split, features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs
        )
        self.field = field
        path_or_paths = path_or_paths if isinstance(path_or_paths, dict) else {self.split: path_or_paths}
        self.builder = Json(
            cache_dir=cache_dir,
            data_files=path_or_paths,
            features=features,
            field=field,
            **kwargs,
        )

    def read(self):
        download_config = None
        download_mode = None
        ignore_verifications = True
        try_from_hf_gcs = False
        use_auth_token = None
        base_path = None

        self.builder.download_and_prepare(
            download_config=download_config,
            download_mode=download_mode,
            ignore_verifications=ignore_verifications,
            try_from_hf_gcs=try_from_hf_gcs,
            base_path=base_path,
            use_auth_token=use_auth_token,
        )

        # Build dataset for splits
        dataset = self.builder.as_dataset(
            split=self.split, ignore_verifications=ignore_verifications, in_memory=self.keep_in_memory
        )
        return dataset


class JsonDatasetWriter:
    def __init__(
        self,
        dataset: Dataset,
        path_or_buf: Union[PathLike, BinaryIO],
        batch_size: Optional[int] = None,
        **to_json_kwargs,
    ):
        self.dataset = dataset
        self.path_or_buf = path_or_buf
        self.batch_size = batch_size
        self.to_json_kwargs = to_json_kwargs

    def write(self) -> int:
        batch_size = self.batch_size if self.batch_size else config.DEFAULT_MAX_BATCH_SIZE

        if isinstance(self.path_or_buf, (str, bytes, os.PathLike)):
            with open(self.path_or_buf, "wb+") as buffer:
                written = self._write(file_obj=buffer, batch_size=batch_size, **self.to_json_kwargs)
        else:
            written = self._write(file_obj=self.path_or_buf, batch_size=batch_size, **self.to_json_kwargs)
        return written

    def _write(
        self,
        file_obj: BinaryIO,
        batch_size: int,
        encoding: str = "utf-8",
        orient="records",
        lines=True,
        **to_json_kwargs,
    ) -> int:
        """Writes the pyarrow table as JSON lines to a binary file handle.

        Caller is responsible for opening and closing the handle.
        """
        written = 0
        _ = to_json_kwargs.pop("path_or_buf", None)

        for offset in utils.tqdm(
            range(0, len(self.dataset), batch_size), unit="ba", disable=bool(logging.get_verbosity() == logging.NOTSET)
        ):
            batch = query_table(
                table=self.dataset.data,
                key=slice(offset, offset + batch_size),
                indices=self.dataset._indices if self.dataset._indices is not None else None,
            )
            json_str = batch.to_pandas().to_json(path_or_buf=None, orient=orient, lines=lines, **to_json_kwargs)
            if not json_str.endswith("\n"):
                json_str += "\n"
            written += file_obj.write(json_str.encode(encoding))
        return written
