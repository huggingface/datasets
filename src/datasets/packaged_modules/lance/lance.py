import re
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional

import pyarrow as pa
from huggingface_hub import HfApi

import datasets
from datasets.builder import Key
from datasets.table import table_cast
from datasets.utils.file_utils import is_local_path


if TYPE_CHECKING:
    import lance
    import lance.file

logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class LanceConfig(datasets.BuilderConfig):
    """
    BuilderConfig for Lance format.

    Args:
        features: (`Features`, *optional*):
            Cast the data to `features`.
        columns: (`List[str]`, *optional*):
            List of columns to load, the other ones are ignored.
        batch_size: (`int`, *optional*):
            Size of the RecordBatches to iterate on. Default to 256.
        token: (`str`, *optional*):
            Optional HF token to use to download datasets.
    """

    features: Optional[datasets.Features] = None
    columns: Optional[List[str]] = None
    batch_size: Optional[int] = 256
    token: Optional[str] = None


def resolve_dataset_uris(files: List[str]) -> Dict[str, List[str]]:
    dataset_uris = set()
    for file_path in files:
        path = Path(file_path)
        if path.parent.name in {"_transactions", "_indices", "_versions"}:
            dataset_root = path.parent.parent
            dataset_uris.add(str(dataset_root))
    return list(dataset_uris)


def _fix_hf_uri(uri: str) -> str:
    # replace the revision tag from hf uri
    if "@" in uri:
        matched = re.match(r"(hf://.+?)(@[0-9a-f]+)(/.*)", uri)
        if matched:
            uri = matched.group(1) + matched.group(3)
    return uri


def _fix_local_version_file(uri: str) -> str:
    # replace symlinks with real files for _version
    if "/_versions/" in uri and is_local_path(uri):
        path = Path(uri)
        if path.is_symlink():
            data = path.read_bytes()
            path.unlink()
            path.write_bytes(data)
    return uri


class Lance(datasets.ArrowBasedBuilder):
    BUILDER_CONFIG_CLASS = LanceConfig
    METADATA_EXTENSIONS = [".idx", ".txn", ".manifest"]

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        import lance
        import lance.file

        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        if self.repo_id:
            api = HfApi(**dl_manager.download_config.storage_options["hf"])
            dataset_sha = api.dataset_info(self.repo_id).sha
            if dataset_sha != self.hash:
                raise NotImplementedError(
                    f"lance doesn't support loading other revisions than 'main' yet, but got {self.hash}"
                )
        data_files = dl_manager.download(self.config.data_files)

        # TODO: remove once Lance supports HF links with revisions
        data_files = {split: [_fix_hf_uri(file) for file in files] for split, files in data_files.items()}
        # TODO: remove once Lance supports symlinks for _version files
        data_files = {split: [_fix_local_version_file(file) for file in files] for split, files in data_files.items()}

        splits = []
        for split_name, files in data_files.items():
            storage_options = dl_manager.download_config.storage_options.get(files[0].split("://", 0)[0] + "://")

            lance_dataset_uris = resolve_dataset_uris(files)
            if lance_dataset_uris:
                fragments = [
                    frag
                    for uri in lance_dataset_uris
                    for frag in lance.dataset(uri, storage_options=storage_options).get_fragments()
                ]
                if self.info.features is None:
                    pa_schema = fragments[0]._ds.schema
                splits.append(
                    datasets.SplitGenerator(
                        name=split_name,
                        gen_kwargs={"fragments": fragments, "lance_files_paths": None, "lance_files": None},
                    )
                )
            else:
                lance_files = [
                    lance.file.LanceFileReader(file, storage_options=storage_options, columns=self.config.columns)
                    for file in files
                ]
                if self.info.features is None:
                    pa_schema = lance_files[0].metadata().schema
                splits.append(
                    datasets.SplitGenerator(
                        name=split_name,
                        gen_kwargs={"fragments": None, "lance_files_paths": files, "lance_files": lance_files},
                    )
                )
            if self.info.features is None:
                if self.config.columns:
                    fields = [
                        pa_schema.field(name) for name in self.config.columns if pa_schema.get_field_index(name) != -1
                    ]
                    pa_schema = pa.schema(fields)
                self.info.features = datasets.Features.from_arrow_schema(pa_schema)

        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_shards(
        self,
        fragments: Optional[List["lance.LanceFragment"]],
        lance_files_paths: Optional[list[str]],
        lance_files: Optional[List["lance.file.LanceFileReader"]],
    ):
        if fragments:
            for fragment in fragments:
                paths = [data_file.path for data_file in fragment.metadata.data_files()]
                yield paths[0] if len(paths) == 1 else {"fragment_data_files": paths}
        else:
            yield from lance_files_paths

    def _generate_tables(
        self,
        fragments: Optional[List["lance.LanceFragment"]],
        lance_files_paths: Optional[list[str]],
        lance_files: Optional[List["lance.file.LanceFileReader"]],
    ):
        if fragments:
            for frag_idx, fragment in enumerate(fragments):
                for batch_idx, batch in enumerate(
                    fragment.to_batches(columns=self.config.columns, batch_size=self.config.batch_size)
                ):
                    table = pa.Table.from_batches([batch])
                    yield Key(frag_idx, batch_idx), self._cast_table(table)
        else:
            for file_idx, lance_file in enumerate(lance_files):
                for batch_idx, batch in enumerate(lance_file.read_all(batch_size=self.config.batch_size).to_batches()):
                    table = pa.Table.from_batches([batch])
                    yield Key(file_idx, batch_idx), self._cast_table(table)
