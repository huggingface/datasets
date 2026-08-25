import functools
import operator
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Optional, Union
from urllib.parse import unquote

import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.table import table_cast
from datasets.utils.file_utils import xgetsize


if TYPE_CHECKING:
    import vortex
    import vortex.expr
    import vortex.store

logger = datasets.utils.logging.get_logger(__name__)

# Vortex reads `hf://` URIs itself, so this is only matched to re-root a read on an `HfStore`
# carrying the `token` and `endpoint` that `load_dataset` was given, which a URI cannot express.
_HF_URI_PATTERN = re.compile(r"^hf://datasets/([^/@]+/[^/@]+?)(?:@([^/]+))?/(.+)$")

# `hf://buckets/...` URIs point at HF Buckets, which `HfStore` cannot root a read on yet.
_HF_BUCKETS_URI_PATTERN = re.compile(r"^hf://buckets/")

# The comparisons `pyarrow.parquet.filters_to_expression` accepts, mapped to the Python operators
# that build the equivalent Vortex expression.
_FILTER_COMPARISONS = {
    "==": operator.eq,
    "=": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}

# When `IterableDataset.reshard()` subdivides files, adjacent splits (one per chunk of the file,
# usually a few thousand rows) are coalesced into shards of about this many bytes of file data.
# The target is converted to rows through the file's average row size, so shards weigh about the
# same however wide or compressible the rows are. Coalescing whole splits keeps shard boundaries
# on chunk boundaries, so neighboring shards never read the same chunk.
_RESHARD_TARGET_NUM_BYTES = 64 << 20

# The rows per shard to fall back to when the file's size cannot be determined.
_RESHARD_FALLBACK_NUM_ROWS = 1 << 20


@dataclass
class VortexConfig(datasets.BuilderConfig):
    """
    BuilderConfig for Vortex.

    Args:
        batch_size (`int`, *optional*):
            Size of the RecordBatches to iterate on.
            The default is defined by the Vortex scanner.
        columns (`list[str]`, *optional*)
            List of columns to load, the other ones are ignored.
            All columns are loaded by default.
        features: (`Features`, *optional*):
            Cast the data to `features`.
        filters (`Union[vortex.expr.Expr, list[tuple], list[list[tuple]]]`, *optional*):
            Return only the rows matching the filter.
            The predicate is pushed down into the Vortex scan so only the matching rows are read.
            Filters given as a list of tuples (DNF, like the Parquet loader accepts) are converted
            to a Vortex expression.
            Nulls follow SQL semantics: a null satisfies no comparison, so a row whose filtered
            column is null is never returned. Note that `not in` therefore drops nulls, where the
            Parquet loader keeps them because it builds `~field.isin(values)` and a null is not in
            the set.
        on_bad_files (`Literal["error", "warn", "skip"]`, *optional*, defaults to "error")
            Specify what to do upon encountering a bad file (a file that can't be read). Allowed values are :
            * 'error', raise an Exception when a bad file is encountered.
            * 'warn', raise a warning when a bad file is encountered and skip that file.
            * 'skip', skip bad files without raising or warning when they are encountered.

    Example:

    Load a subset of columns:

    ```python
    >>> ds = load_dataset(vortex_dataset_id, columns=["col_0", "col_1"])
    ```

    Stream data and efficiently filter data, skipping entire files or chunks when possible:

    ```python
    >>> filters = [("col_0", "==", 0)]
    >>> ds = load_dataset(vortex_dataset_id, streaming=True, filters=filters)
    ```

    """

    batch_size: Optional[int] = None
    columns: Optional[list[str]] = None
    features: Optional[datasets.Features] = None
    filters: Optional[Union["vortex.expr.Expr", list[tuple], list[list[tuple]]]] = None
    on_bad_files: Literal["error", "warn", "skip"] = "error"

    def __post_init__(self):
        super().__post_init__()


def _filters_to_expression(filters: Union[list[tuple], list[list[tuple]]]) -> "vortex.expr.Expr":
    """Convert Parquet-style DNF filters to a Vortex expression.

    Accepts the shapes `pyarrow.parquet.filters_to_expression` accepts: a list of predicates, taken
    as a conjunction, or a list of such lists, taken as a disjunction of conjunctions. A predicate
    is a `(column, operator, value)` tuple or list.
    """
    import vortex.expr as ve

    def predicate_to_expression(predicate) -> "vortex.expr.Expr":
        col, op, val = predicate
        column = ve.column(col)
        if op in _FILTER_COMPARISONS:
            return _FILTER_COMPARISONS[op](column, val)
        elif op in ("in", "not in"):
            if not val:
                raise ValueError(f"Empty set of values for '{op}' filter on column '{col}'")
            if op == "in":
                return ve.or_collect([column == value for value in val])
            return ve.and_collect([column != value for value in val])
        else:
            raise ValueError(f"Unsupported filter operator: '{op}'")

    if not filters or not filters[0]:
        raise ValueError(f"Malformed filters: {filters}")
    if isinstance(filters[0][0], str):
        # One nesting level too few: [(col, op, val), ...] instead of [[(col, op, val), ...]]
        filters = [filters]
    conjunctions = []
    for conjunction in filters:
        if not conjunction:
            raise ValueError(f"Malformed filters: {filters}")
        conjunctions.append(ve.and_collect([predicate_to_expression(predicate) for predicate in conjunction]))
    return ve.or_collect(conjunctions)


@functools.lru_cache(maxsize=64)
def _hf_store(
    repo_id: str, revision: Optional[str], token: Optional[Union[str, bool]], endpoint: Optional[str]
) -> "vortex.store.HfStore":
    """A store rooted at one repository and revision, shared by all the files read from it."""
    import vortex.store

    return vortex.store.HfStore(repo_id, revision=revision, token=token, endpoint=endpoint)


def _open_vortex_file(file: str, hf_storage_options: Optional[dict] = None) -> "vortex.VortexFile":
    """Open a Vortex file from a local path, a URL or a `hf://` URI (used in streaming mode).

    Vortex resolves `hf://` URIs itself, taking credentials from `HF_TOKEN` or the saved login, but
    the `token` and `endpoint` `load_dataset` was given cannot be expressed in a URI. So a Hub read
    is re-rooted on an `HfStore` carrying them, against which the in-repository path is opened.

    Only `hf://datasets/...` URIs are re-rooted this way. `hf://buckets/...` URIs are refused until
    `HfStore` supports HF Buckets.
    """
    if _HF_BUCKETS_URI_PATTERN.match(file):
        raise NotImplementedError(f"Vortex cannot read from HF Buckets yet: {file}")

    import vortex

    matched = _HF_URI_PATTERN.match(file)
    if matched:
        repo_id, revision, path_in_repo = matched.groups()
        hf_storage_options = hf_storage_options or {}
        # `HfStore` percent-encodes the revision itself, so give it the decoded one.
        revision = unquote(revision) if revision else None
        store = _hf_store(repo_id, revision, hf_storage_options.get("token"), hf_storage_options.get("endpoint"))
        return vortex.open(path_in_repo, store=store)
    return vortex.open(file)


def _to_arrow_reader(
    vortex_file: "vortex.VortexFile",
    row_range: Optional[tuple[int, int]],
    projection: Optional[list[str]],
    filter_expr: Optional["vortex.expr.Expr"],
    batch_size: Optional[int] = None,
) -> pa.RecordBatchReader:
    """Scan the whole file, or only the rows of `row_range` (offsets in the file, before filtering)."""
    if row_range is None:
        return vortex_file.to_arrow(projection=projection, expr=filter_expr, batch_size=batch_size)
    scan = vortex_file.to_repeated_scan(projection, expr=filter_expr, batch_size=batch_size)
    return scan.execute(row_range=row_range).to_arrow()


def _reshard_target_num_rows(
    vortex_file: "vortex.VortexFile", file: str, hf_storage_options: Optional[dict] = None
) -> int:
    """How many rows of this file weigh about `_RESHARD_TARGET_NUM_BYTES`, by the file's average row size."""
    num_rows = len(vortex_file)
    try:
        download_config = datasets.DownloadConfig(storage_options={"hf": hf_storage_options or {}})
        file_num_bytes = xgetsize(file, download_config=download_config)
    except (OSError, NotImplementedError, ValueError):
        file_num_bytes = None
    if not file_num_bytes or not num_rows:
        return _RESHARD_FALLBACK_NUM_ROWS
    return max(1, num_rows * _RESHARD_TARGET_NUM_BYTES // file_num_bytes)


def _coalesced_row_ranges(vortex_file: "vortex.VortexFile", target_num_rows: int) -> list[tuple[int, int]]:
    """The file's splits, coalesced into row ranges of about `target_num_rows` rows each."""
    row_ranges = []
    start = stop = None
    for split_start, split_stop in vortex_file.splits():
        if start is not None and split_stop - start <= target_num_rows:
            stop = split_stop
        else:
            if start is not None:
                row_ranges.append((start, stop))
            start, stop = split_start, split_stop
    if start is not None:
        row_ranges.append((start, stop))
    return row_ranges


class Vortex(datasets.ArrowBasedBuilder, datasets.builder._CountableBuilderMixin):
    BUILDER_CONFIG_CLASS = VortexConfig

    def _info(self):
        if (
            self.config.columns is not None
            and self.config.features is not None
            and set(self.config.columns) != set(self.config.features)
        ):
            if any(col not in self.config.features for col in self.config.columns):
                raise ValueError(
                    "The columns and features argument must match, but got ",
                    f"{self.config.columns} and {self.config.features}",
                )
            else:
                features = datasets.Features({col: self.config.features[col] for col in self.config.columns})
        else:
            features = self.config.features
        return datasets.DatasetInfo(features=features)

    def _handle_bad_file(self, file: str, error: Exception):
        if self.config.on_bad_files == "error":
            logger.error(f"Failed to read file '{file}' with error {type(error).__name__}: {error}")
            raise error
        elif self.config.on_bad_files == "warn":
            logger.warning(f"Skipping bad file '{file}'. {type(error).__name__}: {error}")
        else:
            logger.debug(f"Skipping bad file '{file}'. {type(error).__name__}: {error}")

    def _split_generators(self, dl_manager):
        """We handle string, list and dicts in datafiles"""
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        data_files = dl_manager.download(self.config.data_files)
        hf_storage_options = dict(dl_manager.download_config.storage_options.get("hf", {}))
        splits = []
        for split_name, files in data_files.items():
            files = [str(file) for file in files]
            # Infer features if they are stored in the vortex file schema
            if self.info.features is None:
                for file in files:
                    try:
                        vortex_file = _open_vortex_file(file, hf_storage_options)
                    except RuntimeError as e:  # Vortex surfaces unreadable files as RuntimeError
                        self._handle_bad_file(file, e)
                    else:
                        self.info.features = datasets.Features.from_arrow_schema(vortex_file.dtype.to_arrow_schema())
                        break
            if self.info.features is None:
                raise ValueError(
                    f"At least one valid data file must be specified, all the data_files are invalid: {self.config.data_files}"
                )
            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "files": files,
                        "row_ranges": [None] * len(files),
                        "hf_storage_options": hf_storage_options,
                    },
                )
            )
        if self.config.columns is not None and set(self.config.columns) != set(self.info.features):
            self.info.features = datasets.Features(
                {col: feat for col, feat in self.info.features.items() if col in self.config.columns}
            )
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # more expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _filter_expression(self) -> Optional["vortex.expr.Expr"]:
        if isinstance(self.config.filters, list):
            return _filters_to_expression(self.config.filters)
        return self.config.filters

    def _generate_shards(self, files, row_ranges, hf_storage_options=None):
        for file, row_range in zip(files, row_ranges):
            if row_range is None:
                yield file
            else:
                yield {"fragment_data_file": file, "fragment_row_range": row_range}

    def _generate_more_gen_kwargs(self, files, row_ranges, hf_storage_options=None):
        for file, row_range in zip(files, row_ranges):
            new_row_ranges = [row_range]
            if row_range is None:
                try:
                    vortex_file = _open_vortex_file(file, hf_storage_options)
                    target_num_rows = _reshard_target_num_rows(vortex_file, file, hf_storage_options)
                    new_row_ranges = _coalesced_row_ranges(vortex_file, target_num_rows)
                except RuntimeError:
                    # Keep the unreadable file whole: `_generate_tables` applies `on_bad_files` to it.
                    pass
            yield {
                "files": [file] * len(new_row_ranges),
                "row_ranges": new_row_ranges,
                "hf_storage_options": hf_storage_options,
            }

    def _generate_num_examples(self, files, row_ranges, hf_storage_options=None):
        filter_expr = self._filter_expression()
        for file, row_range in zip(files, row_ranges):
            if filter_expr is None:
                if row_range is None:
                    yield len(_open_vortex_file(file, hf_storage_options))
                else:
                    yield row_range[1] - row_range[0]
            else:
                # Counting the matching rows takes a scan, but none of the columns have to come back
                # from it: an empty projection reads only what the predicate needs.
                vortex_file = _open_vortex_file(file, hf_storage_options)
                reader = _to_arrow_reader(vortex_file, row_range, [], filter_expr)
                yield sum(record_batch.num_rows for record_batch in reader)

    def _generate_tables(self, files, row_ranges, hf_storage_options=None):
        if self.config.features is not None and self.config.columns is not None:
            if sorted(field.name for field in self.info.features.arrow_schema) != sorted(self.config.columns):
                raise ValueError(
                    f"Tried to load vortex data with columns '{self.config.columns}' with mismatching features '{self.info.features}'"
                )
        filter_expr = self._filter_expression()
        for file_idx, (file, row_range) in enumerate(zip(files, row_ranges)):
            try:
                vortex_file = _open_vortex_file(file, hf_storage_options)
                reader = _to_arrow_reader(
                    vortex_file, row_range, self.config.columns, filter_expr, self.config.batch_size
                )
                for batch_idx, record_batch in enumerate(reader):
                    pa_table = pa.Table.from_batches([record_batch])
                    yield Key(file_idx, batch_idx), self._cast_table(pa_table)
            except RuntimeError as e:  # Vortex surfaces unreadable files as RuntimeError
                self._handle_bad_file(file, e)
