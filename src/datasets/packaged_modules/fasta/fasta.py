import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable, Optional
from typing import List as ListT

import pyarrow as pa
from Bio import SeqIO

import datasets
from datasets.features import Value
from datasets.table import table_cast
from datasets.utils.file_utils import xopen


logger = datasets.utils.logging.get_logger(__name__)

if TYPE_CHECKING:
    from Bio import SeqIO

# Common FASTA extensions; .gz will be handled by dl_manager.extract_on_the_fly
EXTENSIONS = [".fa", ".fasta", ".fna", ".ffn", ".faa", ".frn", ".fa.gz", ".fasta.gz"]


@dataclass
class FASTAConfig(datasets.BuilderConfig):
    """BuilderConfig for FASTA."""

    batch_size: Optional[int] = None
    columns: Optional[ListT[str]] = None  # subset of ["id", "description", "sequence"]
    features: Optional[datasets.Features] = None

    def __post_init__(self):
        super().__post_init__()


class FASTA(datasets.ArrowBasedBuilder):
    """ArrowBasedBuilder that converts FASTA files to Arrow tables."""

    BUILDER_CONFIG_CLASS = FASTAConfig

    def _info(self):
        if (
            self.config.columns is not None
            and self.config.features is not None
            and set(self.config.columns) != set(self.config.features)
        ):
            raise ValueError(
                "The columns and features argument must contain the same columns, but got "
                f"{self.config.columns} and {self.config.features}",
            )
        # Default features if not provided
        if self.config.features is None:
            self.config.features = datasets.Features(
                {"id": Value("string"), "description": Value("string"), "sequence": Value("string")}
            )
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download_and_extract(self.config.data_files)

        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            # Expand dirs/globs into concrete file iterables
            files = [dl_manager.iter_files(file) for file in files]

            # Optionally narrow features to requested columns
            if self.config.columns is not None and set(self.config.columns) != set(self.info.features):
                self.info.features = datasets.Features(
                    {col: feat for col, feat in self.info.features.items() if col in self.config.columns}
                )

            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))

        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_tables(self, files):
        # files is an iterable of iterables (one per user provided path)
        effective_cols = list(self.info.features.keys())
        batch_size_cfg = self.config.batch_size or self._writer_batch_size or 10_000

        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            # Stream-parse and yield Arrow tables in batches
            try:
                batch = {col: [] for col in effective_cols}
                row_count = 0
                for rec in _iter_fasta_records(file):
                    row = {
                        "id": rec["id"],
                        "description": rec["description"],
                        "sequence": rec["sequence"],
                    }
                    for col in effective_cols:
                        batch[col].append(row[col])
                    row_count += 1

                    if row_count % batch_size_cfg == 0:
                        pa_table = pa.Table.from_pydict(batch)
                        yield f"{file_idx}_{row_count - batch_size_cfg}", self._cast_table(pa_table)
                        batch = {col: [] for col in effective_cols}

                # Flush tail
                if batch and any(len(v) for v in batch.values()):
                    start = row_count - len(next(iter(batch.values()))) if row_count else 0
                    pa_table = pa.Table.from_pydict(batch)
                    yield f"{file_idx}_{start}", self._cast_table(pa_table)

            except ValueError as e:
                logger.error(f"Failed to read file '{file}' with error {type(e)}: {e}")
                raise


# ┌─────────────┐
# │ FASTA I/O   │
# └─────────────┘


def _iter_fasta_records(path: str) -> Iterable[Dict[str, str]]:
    """
    Streaming FASTA parser that yields dicts with keys: id, description, sequence.
    - Supports regular files and fsspec paths (including gzip://)
    - Uses xopen to handle compressed files and streaming paths
    """
    # Use xopen to handle fsspec paths (e.g., gzip://file::path.gz) and regular paths
    # Open in text mode for BioPython's SeqIO.parse
    with xopen(path, "r", encoding="utf-8") as f:
        for r in SeqIO.parse(f, "fasta"):
            yield {"id": r.id, "description": r.description, "sequence": str(r.seq)}
