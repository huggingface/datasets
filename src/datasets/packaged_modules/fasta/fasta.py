"""FASTA file loader for biological sequence data.

FASTA is a text-based format for representing nucleotide sequences (DNA/RNA)
or peptide sequences (proteins), widely used in bioinformatics.

This implementation uses a lightweight pure Python parser based on Heng Li's readfq.py.
The parsed columns need no external dependency; the ``record`` column holds each
record's raw bytes as a ``BioSequence`` and decodes to a Biopython ``SeqRecord``
when biopython is installed (drop it with ``columns`` to stay dependency-free).
"""

import itertools
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Optional

import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.features.features import require_storage_cast
from datasets.table import table_cast


logger = datasets.utils.logging.get_logger(__name__)


# Conservative limit to stay well under Parquet's i32::MAX page limit (~2GB)
# Using 256MB as default since Parquet compresses data and we want headroom
DEFAULT_MAX_BATCH_BYTES = 256 * 1024 * 1024  # 256 MB


@dataclass
class FastaConfig(datasets.BuilderConfig):
    """BuilderConfig for FASTA files.

    Args:
        features: Dataset features (optional, will be inferred if not provided).
        batch_size: Maximum number of records per batch. Works in conjunction with
            max_batch_bytes - a batch is flushed when either limit is reached.
        max_batch_bytes: Maximum cumulative bytes per batch. This prevents Parquet
            page size errors when dealing with very large sequences (e.g., complete
            genomes). Set to None to disable byte-based batching.
        columns: Subset of columns to include. Options: ["id", "description", "sequence", "record"].
    """

    features: Optional[datasets.Features] = None
    batch_size: int = 10000
    max_batch_bytes: Optional[int] = DEFAULT_MAX_BATCH_BYTES
    columns: Optional[list[str]] = None

    def __post_init__(self):
        super().__post_init__()


class Fasta(datasets.ArrowBasedBuilder):
    """Dataset builder for FASTA files."""

    BUILDER_CONFIG_CLASS = FastaConfig

    # All supported FASTA extensions
    EXTENSIONS: list[str] = [".fa", ".fasta", ".fna", ".ffn", ".faa", ".frn", ".afa"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # DatasetBuilder applies features= after _info(); project the effective
        # schema again, preserving features supplied through info= as well.
        self.info.features = self._info().features

    def _info(self):
        features = self.info.features if hasattr(self, "info") else self.config.features
        columns = self._get_columns()
        if features is None:
            features = datasets.Features.from_arrow_schema(self._get_schema(columns))
            if "record" in features:
                features["record"] = datasets.BioSequence(format="fasta")
        if features is not None and self.config.columns is not None:
            missing = [col for col in self.config.columns if col not in features]
            if missing:
                raise ValueError(f"columns {missing} are not in features {list(features)}")
            features = datasets.Features({col: features[col] for col in self.config.columns})
        return datasets.DatasetInfo(features=features)

    def _split_generators(self, dl_manager):
        """Generate splits from data files.

        The `data_files` kwarg in load_dataset() can be a str, List[str],
        Dict[str,str], or Dict[str,List[str]].

        If str or List[str], then the dataset returns only the 'train' split.
        If dict, then keys should be from the `datasets.Split` enum.
        """
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []
        for split_name, files in data_files.items():
            if isinstance(files, str):
                files = [files]
            files = [dl_manager.iter_files(file) for file in files]
            splits.append(datasets.SplitGenerator(name=split_name, gen_kwargs={"files": files}))
        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        """Cast Arrow table to configured features schema."""
        features = self.info.features
        if features is not None:
            schema = features.arrow_schema
            if all(not require_storage_cast(feature) for feature in features.values()):
                pa_table = pa_table.cast(schema)
            else:
                pa_table = table_cast(pa_table, schema)
            return pa_table
        return pa_table

    def _parse_fasta(self, fp, include_record=False):
        """Lightweight FASTA parser based on Heng Li's readfq.py.

        This generator yields (seq_id, description, sequence) tuples for each
        record in the FASTA file. Handles multi-line sequences and various
        header formats.

        Reference: https://github.com/lh3/readfq

        Args:
            fp: File-like object opened in text mode.
            include_record: Append the original UTF-8 record bytes to each tuple.
                The file must be opened with newline="" to preserve line endings.

        Yields:
            Tuple of (seq_id, description, sequence) for each FASTA record.
            When include_record=True, a fourth item contains the record's bytes as read.
        """
        last = None  # Store the last header line

        while True:
            # Find the next header line (starts with '>')
            if not last:
                for line in fp:
                    if line.startswith(">"):
                        last = line
                        break
            if not last:
                break

            # Parse header: >id description
            header = last.rstrip()[1:]  # Remove '>'
            parts = header.split(None, 1)  # Split on first whitespace
            seq_id = parts[0] if parts else ""
            description = parts[1] if len(parts) > 1 else ""

            # Collect sequence lines until next header or EOF
            seqs = []
            record_lines = [last] if include_record else None
            last = None
            for line in fp:
                if line.startswith(">"):
                    last = line
                    break
                if include_record:
                    record_lines.append(line)
                if line.startswith(";"):
                    continue  # Pearson FASTA comment line, not sequence.
                # Whitespace inside a sequence line is not sequence (Biopython drops it too).
                seqs.append("".join(line.split()))

            record = (seq_id, description, "".join(seqs))
            if include_record:
                record += ("".join(record_lines).encode("utf-8"),)
            yield record

            if not last:
                break

    def _get_columns(self) -> list[str]:
        """Get the list of columns to include in output."""
        default_columns = ["id", "description", "sequence", "record"]
        features = self.info.features if hasattr(self, "info") else self.config.features
        if self.config.columns is None and features is not None:
            # A user-supplied schema selects its own columns, so a schema naming a
            # subset stays valid when the default schema grows.
            unknown = [col for col in features if col not in default_columns]
            if unknown:
                raise ValueError(f"Invalid feature column(s) {unknown}. Valid columns are: {default_columns}")
            return list(features)
        if self.config.columns is not None:
            if not self.config.columns:
                raise ValueError("columns must list at least one column when given.")
            # Validate columns
            seen = set()
            for col in self.config.columns:
                if col not in default_columns:
                    raise ValueError(f"Invalid column '{col}'. Valid columns are: {default_columns}")
                if col in seen:
                    raise ValueError(f"Duplicate column '{col}' in columns.")
                seen.add(col)
            return self.config.columns
        return default_columns

    def _get_schema(self, columns: list[str]) -> pa.Schema:
        """Return Arrow schema with large_string for sequence column.

        Uses large_string for the sequence column to handle very long sequences
        (e.g., viral genomes) that can exceed the 2GB limit of regular string type.
        """
        fields = []
        for col in columns:
            if col == "sequence":
                # Use large_string for sequences that can be very long
                fields.append(pa.field(col, pa.large_string()))
            elif col == "record":
                fields.append(pa.field(col, datasets.BioSequence().pa_type))
            else:
                fields.append(pa.field(col, pa.string()))
        return pa.schema(fields)

    def _generate_tables(self, files):
        """Generate Arrow tables from FASTA files.

        Yields batches of records as Arrow tables for memory-efficient processing
        of large genomic files. Uses dual-threshold batching: flushes when either
        batch_size (record count) or max_batch_bytes (cumulative size) is reached.

        This adaptive approach prevents Parquet page size errors when dealing with
        very large sequences (e.g., complete viral or bacterial genomes) while
        maintaining efficiency for typical short sequences.

        Args:
            files: Iterable of file iterables from _split_generators.

        Yields:
            Tuple of (Key, pa.Table) for each batch.
        """
        columns = self._get_columns()
        include_record = "record" in columns
        schema = self._get_schema(columns)
        max_batch_bytes = self.config.max_batch_bytes

        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            batch_idx = 0
            batch = {col: [] for col in columns}
            batch_bytes = 0

            # Keep the streaming-patched open for compressed inputs, and preserve line endings.
            with open(file, "rb") as f, TextIOWrapper(f, encoding="utf-8", newline="") as fp:
                for record in self._parse_fasta(fp, include_record=include_record):
                    seq_id, description, sequence = record[:3]
                    # Calculate record size (approximate UTF-8 byte size)
                    record_bytes = len(seq_id) + len(description) + len(sequence)
                    if include_record:
                        record_bytes += len(record[3])

                    # Check if adding this record would exceed byte limit
                    # Flush current batch first if needed (but only if batch is non-empty)
                    if (
                        max_batch_bytes is not None
                        and batch_bytes > 0
                        and batch_bytes + record_bytes > max_batch_bytes
                    ):
                        pa_table = pa.Table.from_pydict(batch, schema=schema)
                        yield Key(file_idx, batch_idx), self._cast_table(pa_table)
                        batch = {col: [] for col in columns}
                        batch_bytes = 0
                        batch_idx += 1

                    # Add record to batch
                    if "id" in columns:
                        batch["id"].append(seq_id)
                    if "description" in columns:
                        batch["description"].append(description)
                    if "sequence" in columns:
                        batch["sequence"].append(sequence)
                    if include_record:
                        batch["record"].append({"bytes": record[3], "path": None})
                    batch_bytes += record_bytes

                    # Yield batch when it reaches batch_size (record count limit)
                    if len(batch[columns[0]]) >= self.config.batch_size:
                        pa_table = pa.Table.from_pydict(batch, schema=schema)
                        yield Key(file_idx, batch_idx), self._cast_table(pa_table)
                        batch = {col: [] for col in columns}
                        batch_bytes = 0
                        batch_idx += 1

            # Yield remaining records in final batch
            if batch[columns[0]]:
                pa_table = pa.Table.from_pydict(batch, schema=schema)
                yield Key(file_idx, batch_idx), self._cast_table(pa_table)
