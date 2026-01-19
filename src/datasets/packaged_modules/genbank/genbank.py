"""GenBank file loader for biological sequence data with annotations.

GenBank is a text-based format for storing nucleotide or protein sequences together with
their annotations and metadata, widely used in bioinformatics and maintained by NCBI.

This implementation uses a lightweight pure Python state machine parser,
requiring zero external dependencies.
"""

import bz2
import gzip
import itertools
import json
import lzma
import re
from dataclasses import dataclass
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


# Parser states for the GenBank state machine
class ParserState:
    HEADER = "HEADER"
    FEATURES = "FEATURES"
    ORIGIN = "ORIGIN"
    COMPLETE = "COMPLETE"


@dataclass
class GenBankConfig(datasets.BuilderConfig):
    """BuilderConfig for GenBank files.

    Args:
        features: Dataset features (optional, will be inferred if not provided).
        batch_size: Maximum number of records per batch. Works in conjunction with
            max_batch_bytes - a batch is flushed when either limit is reached.
        max_batch_bytes: Maximum cumulative bytes per batch. This prevents Parquet
            page size errors when dealing with very large sequences. Set to None
            to disable byte-based batching.
        columns: Subset of columns to include. Options: ["locus_name", "accession",
            "version", "definition", "organism", "taxonomy", "keywords", "sequence",
            "features", "length", "molecule_type"].
        parse_features: Whether to parse FEATURES section into structured JSON.
            If False, stores raw text.
    """

    features: Optional[datasets.Features] = None
    batch_size: int = 10000
    max_batch_bytes: Optional[int] = DEFAULT_MAX_BATCH_BYTES
    columns: Optional[list[str]] = None
    parse_features: bool = True

    def __post_init__(self):
        super().__post_init__()


class GenBank(datasets.ArrowBasedBuilder):
    """Dataset builder for GenBank files."""

    BUILDER_CONFIG_CLASS = GenBankConfig

    # All supported GenBank extensions
    EXTENSIONS: list[str] = [".gb", ".gbk", ".genbank"]

    # All available columns
    ALL_COLUMNS: list[str] = [
        "locus_name",
        "accession",
        "version",
        "definition",
        "organism",
        "taxonomy",
        "keywords",
        "sequence",
        "features",
        "length",
        "molecule_type",
    ]

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

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
        if self.config.features is not None:
            schema = self.config.features.arrow_schema
            if all(not require_storage_cast(feature) for feature in self.config.features.values()):
                pa_table = pa_table.cast(schema)
            else:
                pa_table = table_cast(pa_table, schema)
            return pa_table
        return pa_table

    def _open_file(self, filepath: str):
        """Open file with automatic compression detection based on magic bytes.

        Supports gzip, bzip2, and xz/lzma compression formats.
        """
        with open(filepath, "rb") as f:
            magic = f.read(6)

        if magic[:2] == b"\x1f\x8b":  # gzip magic number
            return gzip.open(filepath, "rt", encoding="utf-8")
        elif magic[:3] == b"BZh":  # bzip2 magic number
            return bz2.open(filepath, "rt", encoding="utf-8")
        elif magic[:6] == b"\xfd7zXZ\x00":  # xz magic number
            return lzma.open(filepath, "rt", encoding="utf-8")
        else:
            return open(filepath, "r", encoding="utf-8")

    def _parse_feature_location(self, location_str: str) -> dict:
        """Parse a GenBank feature location string into a structured dict.

        Examples:
            "100..200" -> {"start": 100, "end": 200, "strand": 1}
            "complement(100..200)" -> {"start": 100, "end": 200, "strand": -1}
            "join(1..100,200..300)" -> {"start": 1, "end": 300, "strand": 1, "parts": [[1,100],[200,300]]}
        """
        location = {"strand": 1}

        # Check for complement
        if location_str.startswith("complement("):
            location["strand"] = -1
            location_str = location_str[11:-1]  # Remove "complement(" and ")"

        # Check for join
        if location_str.startswith("join("):
            location_str = location_str[5:-1]  # Remove "join(" and ")"
            parts = []
            for part in location_str.split(","):
                part = part.strip()
                if ".." in part:
                    start, end = part.split("..")
                    # Handle < and > symbols for partial sequences
                    start = int(start.lstrip("<>"))
                    end = int(end.lstrip("<>"))
                    parts.append([start, end])
            if parts:
                location["parts"] = parts
                location["start"] = parts[0][0]
                location["end"] = parts[-1][1]
            return location

        # Simple location
        if ".." in location_str:
            start, end = location_str.split("..")
            location["start"] = int(start.lstrip("<>"))
            location["end"] = int(end.lstrip("<>"))
        elif location_str.isdigit():
            location["start"] = int(location_str)
            location["end"] = int(location_str)

        return location

    def _parse_genbank(self, fp):
        """State machine parser for GenBank format.

        GenBank format has several sections:
        - LOCUS: Contains name, length, molecule type, etc.
        - DEFINITION: Description of the sequence
        - ACCESSION: Database accession number
        - VERSION: Version with GI number
        - KEYWORDS: Associated keywords
        - SOURCE/ORGANISM: Organism information and taxonomy
        - FEATURES: Detailed annotations
        - ORIGIN: The actual sequence data
        - // : Record terminator

        Args:
            fp: File-like object opened in text mode.

        Yields:
            Dict with parsed record fields for each GenBank record.
        """
        state = ParserState.HEADER
        record = self._new_record()
        current_feature = None
        current_qualifier_key = None
        current_qualifier_value = []
        features_list = []

        for line in fp:
            # Record terminator
            if line.startswith("//"):
                # Finalize any pending feature
                if current_feature is not None:
                    if current_qualifier_key is not None:
                        current_feature["qualifiers"][current_qualifier_key] = "".join(current_qualifier_value)
                    features_list.append(current_feature)

                # Store features
                if self.config.parse_features:
                    record["features"] = json.dumps(features_list)
                else:
                    record["features"] = ""

                yield record

                # Reset for next record
                state = ParserState.HEADER
                record = self._new_record()
                current_feature = None
                current_qualifier_key = None
                current_qualifier_value = []
                features_list = []
                continue

            # State: HEADER - Parse metadata fields
            if state == ParserState.HEADER:
                if line.startswith("LOCUS"):
                    self._parse_locus_line(line, record)
                elif line.startswith("DEFINITION"):
                    record["definition"] = line[12:].strip()
                elif line.startswith("ACCESSION"):
                    record["accession"] = line[12:].strip().split()[0]
                elif line.startswith("VERSION"):
                    record["version"] = line[12:].strip()
                elif line.startswith("KEYWORDS"):
                    keywords = line[12:].strip()
                    if keywords != ".":
                        record["keywords"] = keywords
                elif line.startswith("SOURCE"):
                    pass  # SOURCE line itself is less useful than ORGANISM
                elif line.startswith("  ORGANISM"):
                    record["organism"] = line[12:].strip()
                elif line.startswith("            ") and record["organism"]:
                    # Continuation of taxonomy
                    taxonomy_part = line.strip()
                    if taxonomy_part and not taxonomy_part.endswith("."):
                        taxonomy_part += ";"
                    if record["taxonomy"]:
                        record["taxonomy"] += " " + taxonomy_part
                    else:
                        record["taxonomy"] = taxonomy_part
                elif line.startswith("FEATURES"):
                    state = ParserState.FEATURES
                elif line.startswith("ORIGIN"):
                    state = ParserState.ORIGIN

            # State: FEATURES - Parse feature annotations
            elif state == ParserState.FEATURES:
                if line.startswith("ORIGIN"):
                    # Finalize any pending feature before transitioning
                    if current_feature is not None:
                        if current_qualifier_key is not None:
                            current_feature["qualifiers"][current_qualifier_key] = "".join(current_qualifier_value)
                        features_list.append(current_feature)
                        current_feature = None
                        current_qualifier_key = None
                        current_qualifier_value = []
                    state = ParserState.ORIGIN
                    continue

                # Feature line starts at column 5 with feature type
                if len(line) > 5 and line[5] != " " and not line.startswith("FEATURES"):
                    # Finalize previous feature
                    if current_feature is not None:
                        if current_qualifier_key is not None:
                            current_feature["qualifiers"][current_qualifier_key] = "".join(current_qualifier_value)
                        features_list.append(current_feature)

                    # Parse new feature
                    parts = line[5:].split()
                    if len(parts) >= 2:
                        feature_type = parts[0]
                        location_str = parts[1]
                        current_feature = {
                            "type": feature_type,
                            "location": self._parse_feature_location(location_str),
                            "qualifiers": {},
                        }
                    current_qualifier_key = None
                    current_qualifier_value = []

                # Qualifier line starts at column 21
                elif len(line) > 21 and line[21] == "/":
                    # Save previous qualifier
                    if current_qualifier_key is not None and current_feature is not None:
                        current_feature["qualifiers"][current_qualifier_key] = "".join(current_qualifier_value)

                    # Parse new qualifier
                    qualifier_line = line[21:].strip()
                    if "=" in qualifier_line:
                        key, value = qualifier_line.split("=", 1)
                        current_qualifier_key = key[1:]  # Remove leading /
                        # Remove surrounding quotes if present
                        value = value.strip('"')
                        current_qualifier_value = [value]
                    else:
                        # Boolean qualifier like /pseudo
                        current_qualifier_key = qualifier_line[1:]
                        current_qualifier_value = ["true"]

                # Continuation line for qualifier
                elif len(line) > 21 and line[21] != "/" and current_qualifier_key is not None:
                    continuation = line[21:].strip().strip('"')
                    current_qualifier_value.append(continuation)

            # State: ORIGIN - Parse sequence data
            elif state == ParserState.ORIGIN:
                if line.startswith("//"):
                    continue  # Will be handled at top of loop

                # Sequence lines have format: "   123 atcgatcg atcgatcg ..."
                # Remove numbers and spaces, keep only sequence characters
                seq_chars = re.sub(r"[\s\d]", "", line)
                if seq_chars:
                    record["sequence"] += seq_chars.upper()

    def _new_record(self) -> dict:
        """Create a new empty record with default values."""
        return {
            "locus_name": "",
            "accession": "",
            "version": "",
            "definition": "",
            "organism": "",
            "taxonomy": "",
            "keywords": "",
            "sequence": "",
            "features": "",
            "length": 0,
            "molecule_type": "",
        }

    def _parse_locus_line(self, line: str, record: dict) -> None:
        """Parse the LOCUS line which contains key metadata.

        LOCUS format (fixed width columns):
        LOCUS       name          length bp    type     topology  division  date

        Example:
        LOCUS       SCU49845     5028 bp    DNA             PLN       21-JUN-1999
        """
        # Split by whitespace and extract fields
        parts = line.split()
        if len(parts) >= 2:
            record["locus_name"] = parts[1]

        # Find length (number followed by 'bp' or 'aa')
        for i, part in enumerate(parts):
            if part in ("bp", "aa") and i > 0:
                try:
                    record["length"] = int(parts[i - 1])
                except ValueError:
                    pass
                break

        # Find molecule type (DNA, RNA, mRNA, etc.)
        molecule_types = {"DNA", "RNA", "mRNA", "rRNA", "tRNA", "protein", "AA"}
        for part in parts:
            if part in molecule_types:
                record["molecule_type"] = part
                break

    def _get_columns(self) -> list[str]:
        """Get the list of columns to include in output."""
        if self.config.columns is not None:
            # Validate columns
            for col in self.config.columns:
                if col not in self.ALL_COLUMNS:
                    raise ValueError(f"Invalid column '{col}'. Valid columns are: {self.ALL_COLUMNS}")
            return self.config.columns
        return self.ALL_COLUMNS

    def _get_schema(self, columns: list[str]) -> pa.Schema:
        """Return Arrow schema with appropriate types for each column.

        Uses large_string for sequence and features columns to handle very long data
        that can exceed the 2GB limit of regular string type.
        """
        fields = []
        for col in columns:
            if col in ("sequence", "features"):
                # Use large_string for potentially very long data
                fields.append(pa.field(col, pa.large_string()))
            elif col == "length":
                fields.append(pa.field(col, pa.int64()))
            else:
                fields.append(pa.field(col, pa.string()))
        return pa.schema(fields)

    def _generate_tables(self, files):
        """Generate Arrow tables from GenBank files.

        Yields batches of records as Arrow tables for memory-efficient processing
        of large sequence files. Uses dual-threshold batching: flushes when either
        batch_size (record count) or max_batch_bytes (cumulative size) is reached.

        Args:
            files: Iterable of file iterables from _split_generators.

        Yields:
            Tuple of (Key, pa.Table) for each batch.
        """
        columns = self._get_columns()
        schema = self._get_schema(columns)
        max_batch_bytes = self.config.max_batch_bytes

        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            batch_idx = 0
            batch = {col: [] for col in columns}
            batch_bytes = 0

            with self._open_file(file) as fp:
                for record in self._parse_genbank(fp):
                    # Update length from actual sequence if not set
                    if record["length"] == 0 and record["sequence"]:
                        record["length"] = len(record["sequence"])

                    # Calculate record size (approximate UTF-8 byte size)
                    record_bytes = sum(
                        len(str(record.get(col, ""))) for col in columns if col != "length"
                    ) + 8  # 8 bytes for int64 length

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
                    for col in columns:
                        batch[col].append(record.get(col, "" if col != "length" else 0))
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
