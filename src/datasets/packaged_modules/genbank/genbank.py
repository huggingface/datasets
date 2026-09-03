"""GenBank file loader for biological sequence data with annotations.

GenBank is a text-based format for storing nucleotide or protein sequences together with
their annotations and metadata, widely used in bioinformatics and maintained by NCBI.

This implementation uses a lightweight pure Python state machine parser,
requiring zero external dependencies.
"""

import itertools
import json
import re
from collections.abc import Callable
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


class _FeatureAccumulator:
    """Collects the multi-line state of a GenBank FEATURES section.

    A feature spans a feature line (type + location) followed by ``/key=value``
    qualifier lines and their continuations. This buffers the feature and the
    qualifier currently being read, flushing them onto ``features`` at the right
    boundaries so the parser loop doesn't have to repeat that bookkeeping.
    """

    # Biopython's rule (Bio.GenBank.Scanner): wrapped qualifier lines join with a space,
    # except /translation whose wrapped lines concatenate directly.
    SPACELESS_QUALIFIERS = frozenset({"translation"})

    def __init__(self, location_parser: Callable[[str], dict]) -> None:
        self.features: list[dict] = []
        self._location_parser = location_parser
        self._feature: Optional[dict] = None
        self._location_text: list[str] = []
        self._qualifier_seen = False
        self._qualifier_key: Optional[str] = None
        self._qualifier_value: list[str] = []
        self._quote_open = False

    @property
    def has_open_qualifier(self) -> bool:
        return self._qualifier_key is not None

    @property
    def has_open_location(self) -> bool:
        """Whether the current feature's location is still being read.

        An operator location such as ``join(1..10,20..30,\n 40..50)`` may wrap, and
        it is incomplete for exactly as long as its parentheses are unbalanced. Once
        a qualifier line has been seen the location cannot continue, so that also
        closes it.
        """
        if self._feature is None or self._qualifier_seen:
            return False
        text = "".join(self._location_text)
        return text.count("(") > text.count(")")

    def _commit_qualifier(self) -> None:
        """Write the buffered qualifier (if any) onto the current feature.

        A qualifier key may repeat within one feature -- ``/db_xref`` routinely does --
        so each key holds the list of its values, as Biopython's
        ``SeqFeature.qualifiers`` does, instead of the last value overwriting the rest.
        """
        if self._feature is not None and self._qualifier_key is not None:
            values = self._feature["qualifiers"].setdefault(self._qualifier_key, [])
            spacer = "" if self._qualifier_key in self.SPACELESS_QUALIFIERS else " "
            values.append(spacer.join(self._qualifier_value))
        self._qualifier_key = None
        self._qualifier_value = []
        self._quote_open = False

    def finalize_feature(self) -> None:
        """Flush the pending qualifier and append the current feature, if any."""
        self._commit_qualifier()
        if self._feature is not None:
            self._feature["location"] = self._location_parser("".join(self._location_text))
            self.features.append(self._feature)
            self._feature = None
            self._location_text = []

    def begin_feature(self, feature_type: str, location_text: str) -> None:
        """Finalize the previous feature and start a new one.

        The location is kept as text and parsed on finalize, because it may still
        gain continuation lines.
        """
        self.finalize_feature()
        self._feature = {"type": feature_type, "location": None, "qualifiers": {}}
        self._location_text = [location_text]
        self._qualifier_seen = False

    def add_location_continuation(self, text: str) -> None:
        """Append a wrapped line to the location currently being read."""
        self._location_text.append(text)

    def begin_qualifier(self, key: str, value: str) -> None:
        """Commit the previous qualifier and start buffering a new one.

        ``value`` is the raw text after ``=``. A value that opens with ``"`` and does
        not close it on the same line stays open, and every following line belongs
        to it even when that line starts with ``/``.
        """
        self._commit_qualifier()
        self._qualifier_seen = True
        self._qualifier_key = key
        if value.startswith('"'):
            value = value[1:]
            self._quote_open = not value.endswith('"')
            value = value[:-1] if not self._quote_open else value
        self._qualifier_value = [value]

    def add_continuation(self, text: str) -> None:
        """Append a continuation line to the qualifier currently being read."""
        if self._quote_open and text.endswith('"'):
            text = text[:-1]
            self._quote_open = False
        self._qualifier_value.append(text)

    @property
    def has_open_quote(self) -> bool:
        """Whether the current qualifier's quoted value has not been closed yet."""
        return self._quote_open


@dataclass
class _HeaderState:
    """Tracks which header field the next continuation line belongs to.

    A header value may wrap onto following lines indented into the value column, and a
    continuation belongs to the field whose keyword opened it. Each keyword handler
    records that field here; keywords this loader does not read (REFERENCE, COMMENT and
    the rest) clear it, so their continuation lines are dropped rather than appended to
    whichever field happened to come before them.
    """

    #: Column at which header values start. Keywords occupy the margin to its left,
    #: so a line that is blank up to this column is a continuation.
    VALUE_COLUMN = 12

    active_field: Optional[str] = None


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
    """

    features: Optional[datasets.Features] = None
    batch_size: int = 10000
    max_batch_bytes: Optional[int] = DEFAULT_MAX_BATCH_BYTES
    columns: Optional[list[str]] = None

    def __post_init__(self):
        super().__post_init__()


class GenBank(datasets.ArrowBasedBuilder):
    """Dataset builder for GenBank files."""

    BUILDER_CONFIG_CLASS = GenBankConfig

    # All supported GenBank extensions
    EXTENSIONS: list[str] = [".gb", ".gbk", ".genbank"]

    # Canonical features for a GenBank record. The schema is always the same, so it is
    # declared here and passed to DatasetInfo; users can still override via config.features.
    DEFAULT_FEATURES: "datasets.Features" = datasets.Features(
        {
            "locus_name": datasets.Value("string"),
            "accession": datasets.Value("string"),
            "version": datasets.Value("string"),
            "definition": datasets.Value("string"),
            "organism": datasets.Value("string"),
            "taxonomy": datasets.Value("string"),
            "keywords": datasets.Value("string"),
            "sequence": datasets.Value("large_string"),
            "features": datasets.Json(),
            "length": datasets.Value("int64"),
            "molecule_type": datasets.Value("string"),
            "secondary_accessions": datasets.List(datasets.Value("string")),
            "contig": datasets.Value("string"),
        }
    )

    # All available columns (the canonical feature order).
    ALL_COLUMNS: list[str] = list(DEFAULT_FEATURES)

    def _info(self):
        if self.config.features is not None:
            features = self.config.features
            if self.config.columns is not None:
                missing = [col for col in self.config.columns if col not in features]
                if missing:
                    raise ValueError(f"columns {missing} are not in features {list(features)}")
                features = datasets.Features({col: features[col] for col in self.config.columns})
        else:
            features = datasets.Features({col: self.DEFAULT_FEATURES[col] for col in self._get_columns()})
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
        """Cast the raw Arrow table to the resolved features schema.

        The resolved features are ``config.features`` if the user provided them,
        otherwise the canonical ``DEFAULT_FEATURES`` projected to the selected columns.
        This is what turns the JSON-encoded ``features`` column into the ``Json()`` type.
        """
        features = self._info().features
        if all(not require_storage_cast(feature) for feature in features.values()):
            return pa_table.cast(features.arrow_schema)
        return table_cast(pa_table, features.arrow_schema)

    def _parse_feature_location(self, location_str: str) -> dict:
        """Parse a GenBank feature location string into a structured dict.

        Examples:
            "100..200" -> {"start": 100, "end": 200, "strand": 1, "start_partial": False, "end_partial": False}
            "<100..>200" -> same, with "start_partial": True, "end_partial": True
            "complement(100..200)" -> {"start": 100, "end": 200, "strand": -1, ...}
            "join(1..100,200..300)" -> {"start": 1, "end": 300, "strand": 1, "operator": "join", "parts": [[1,100],[200,300]]}
        """
        return self._parse_location_node(location_str.strip())

    _LOCATION_OPERATOR_RE = re.compile(r"^(complement|join|order)\((.*)\)$", re.S)
    _LOCATION_RANGE_RE = re.compile(r"^(<?)(\d+)(?:(?:\.\.|\^)(>?)(\d+))?$")

    @classmethod
    def _parse_location_node(cls, text: str) -> dict:
        """Parse one location expression; operators nest, so this recurses.

        ``complement(x)`` flips the strand of whatever ``x`` yields. ``join``/``order``
        parse each comma-separated part on its own (commas inside nested parentheses
        do not split). A join whose parts sit on different strands has no single
        strand and reports ``None``, as Biopython's CompoundLocation does.
        """
        operator_match = cls._LOCATION_OPERATOR_RE.match(text)
        if operator_match:
            operator, inner = operator_match.groups()
            if operator == "complement":
                location = cls._parse_location_node(inner)
                location["strand"] = -location["strand"] if location["strand"] is not None else None
                return location
            parts = [cls._parse_location_node(part) for part in cls._split_top_level(inner)]
            strands = {part["strand"] for part in parts}
            location = {"strand": strands.pop() if len(strands) == 1 else None, "operator": operator}
            located = [part for part in parts if "start" in part]
            if located:
                location["parts"] = [[part["start"], part["end"]] for part in located]
                location["start"] = located[0]["start"]
                location["end"] = located[-1]["end"]
                location["start_partial"] = located[0]["start_partial"]
                location["end_partial"] = located[-1]["end_partial"]
            return location

        location = {"strand": 1}
        # A remote reference (ACCESSION.VERSION:range) keeps only the range here.
        range_match = cls._LOCATION_RANGE_RE.match(text.rsplit(":", 1)[-1].strip())
        if range_match:
            before, start, after, end = range_match.groups()
            location["start"] = int(start)
            location["end"] = int(end or start)
            # "<" and ">" mark a boundary that lies beyond the given coordinate
            # (Biopython's BeforePosition / AfterPosition).
            location["start_partial"] = before == "<"
            location["end_partial"] = after == ">"
        return location

    @staticmethod
    def _split_top_level(text: str) -> list[str]:
        """Split on commas that are not nested inside parentheses."""
        parts, depth, current = [], 0, []
        for char in text:
            if char == "," and depth == 0:
                parts.append("".join(current).strip())
                current = []
                continue
            depth += (char == "(") - (char == ")")
            current.append(char)
        parts.append("".join(current).strip())
        return [part for part in parts if part]

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
        header = _HeaderState()
        features = _FeatureAccumulator(self._parse_feature_location)

        for line in fp:
            # Record terminator: finalize the pending feature and emit the record.
            if line.startswith("//"):
                features.finalize_feature()
                record["features"] = features.features
                record["contig"] = "".join(record["contig"].split())
                yield record
                state = ParserState.HEADER
                record = self._new_record()
                header = _HeaderState()
                features = _FeatureAccumulator(self._parse_feature_location)
                continue

            if state == ParserState.HEADER:
                state = self._handle_header_line(line, record, header) or state
            elif state == ParserState.FEATURES:
                state = self._handle_features_line(line, features, record, header) or state
            elif state == ParserState.ORIGIN:
                self._handle_origin_line(line, record)

    def _handle_header_line(self, line: str, record: dict, header: "_HeaderState") -> Optional[str]:
        """Parse one HEADER line into ``record``.

        ``header`` carries the field that a continuation line would extend, and this
        updates it on every keyword line.

        Returns the next parser state when a section boundary (FEATURES or
        ORIGIN) is reached, otherwise ``None`` to stay in the HEADER state.
        """
        value = line[header.VALUE_COLUMN :].strip()
        if not line.strip():
            return None

        # Blank in the keyword margin means this line continues the field above it.
        if not line[: header.VALUE_COLUMN].strip():
            if header.active_field:
                self._append_header_continuation(record, header.active_field, line.strip())
            return None

        if line.startswith("FEATURES"):
            header.active_field = None
            return ParserState.FEATURES
        if line.startswith("ORIGIN"):
            header.active_field = None
            return ParserState.ORIGIN

        if line.startswith("LOCUS"):
            self._parse_locus_line(line, record)
            header.active_field = None
        elif line.startswith("DEFINITION"):
            record["definition"] = value
            header.active_field = "definition"
        elif line.startswith("ACCESSION"):
            accessions = value.split()
            record["accession"] = accessions[0] if accessions else ""
            record["secondary_accessions"] = accessions[1:]
            header.active_field = "secondary_accessions"
        elif line.startswith("CONTIG"):
            record["contig"] = value
            header.active_field = "contig"
        elif line.startswith("VERSION"):
            record["version"] = value
            header.active_field = None
        elif line.startswith("KEYWORDS"):
            if value != ".":
                record["keywords"] = value
            header.active_field = "keywords"
        elif line.startswith("SOURCE"):
            # The SOURCE line itself is less useful than ORGANISM.
            header.active_field = None
        elif line.startswith("  ORGANISM"):
            record["organism"] = value
            # The lines under ORGANISM are the taxonomy listing, not more organism name.
            header.active_field = "taxonomy"
        else:
            # A keyword this loader does not read; its continuations belong to nothing.
            header.active_field = None
        return None

    @staticmethod
    def _append_header_continuation(record: dict, field: str, text: str) -> None:
        """Append a wrapped line to ``field``, joining with a single space.

        No delimiter is inserted: a wrapped value already carries its own punctuation,
        so a taxonomy listing that ends a line with ``;`` keeps exactly that one ``;``.
        """
        if isinstance(record[field], list):
            record[field].extend(text.split())
        elif field == "contig":
            record[field] += text  # a location expression; whitespace is not part of it
        else:
            record[field] = f"{record[field]} {text}".strip() if record[field] else text

    def _handle_features_line(
        self, line: str, features: "_FeatureAccumulator", record: dict, header: "_HeaderState"
    ) -> Optional[str]:
        """Parse one FEATURES line into ``features``.

        Returns the next parser state when a keyword ends the section (ORIGIN, or a
        header keyword such as CONTIG that follows the feature table), otherwise
        ``None`` to stay in the FEATURES state.
        """
        # A line that starts at column 0 is a keyword (ORIGIN, BASE COUNT, CONTIG, ...),
        # never a feature: it ends the open feature and only ORIGIN changes state.
        if line[:1].strip():
            features.finalize_feature()
            if line.startswith("ORIGIN"):
                return ParserState.ORIGIN
            if line.startswith("CONTIG"):
                return self._handle_header_line(line, record, header) or ParserState.HEADER
            return None

        # A feature starts with its type at column 5, e.g. "     gene   1..100".
        if len(line) > 5 and line[5] != " ":
            parts = line[5:].split(None, 1)
            if len(parts) >= 2:
                features.begin_feature(parts[0], parts[1].strip())
            else:
                features.finalize_feature()

        # Inside an unclosed quoted value every line is a continuation, '/' included.
        elif len(line) > 21 and features.has_open_quote:
            features.add_continuation(line[21:].strip())
        # A qualifier starts with "/key=value" at column 21.
        elif len(line) > 21 and line[21] == "/":
            qualifier_line = line[21:].strip()
            if "=" in qualifier_line:
                key, value = qualifier_line.split("=", 1)
                features.begin_qualifier(key[1:], value)  # key[1:] drops the leading '/'
            else:
                features.begin_qualifier(qualifier_line[1:], "")  # valueless qualifier, e.g. /pseudo

        # An unbalanced location wraps onto the next line before any qualifier appears.
        elif len(line) > 21 and line[21] != "/" and features.has_open_location:
            features.add_location_continuation(line[21:].strip())

        # Anything else at column 21+ is a continuation of the current qualifier's value.
        elif len(line) > 21 and line[21] != "/" and features.has_open_qualifier:
            features.add_continuation(line[21:].strip())

        return None

    def _handle_origin_line(self, line: str, record: dict) -> None:
        """Accumulate sequence characters from one ORIGIN line into ``record``."""
        if line.startswith("//"):
            return  # Handled by the terminator at the top of the parse loop.
        if line[:1].strip():
            return  # A keyword line (CONTIG, BASE COUNT) carries no sequence characters.
        # ORIGIN lines look like "   123 atcgatcg atcgatcg ..."; keep only the bases.
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
            "features": [],
            "length": 0,
            "molecule_type": "",
            "secondary_accessions": [],
            "contig": "",
        }

    _MOLECULE_TYPE_RE = re.compile(r"^(?:[sdm]s-)?(?:[a-z]*[DR]NA|NA)$")

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

        # The length is a number followed by its unit: "bp" for nucleotides, "aa" for
        # amino acids. The unit is also what identifies a protein record, whose LOCUS
        # line carries no molecule-type token of its own.
        unit = None
        for i, part in enumerate(parts):
            if part.lower() in ("bp", "aa") and i > 0:
                unit = part.lower()
                try:
                    record["length"] = int(parts[i - 1])
                except ValueError:
                    pass
                break

        # Nucleotide records name their molecule type explicitly.
        # Molecule types are DNA/RNA (with a lowercase class prefix such as m, r, t, sn)
        # or the generic NA, optionally prefixed by strandedness ss-/ds-/ms-.
        for part in parts:
            if self._MOLECULE_TYPE_RE.match(part):
                record["molecule_type"] = part
                break
        else:
            if unit == "aa":
                record["molecule_type"] = "protein"

    def _get_columns(self) -> list[str]:
        """Get the list of columns to include in output.

        ``columns`` wins when given; otherwise a user-supplied ``features`` schema
        selects its own columns, so a schema naming a subset stays valid when the
        default schema grows.
        """
        if self.config.columns is None and self.config.features is not None:
            unknown = [col for col in self.config.features if col not in self.ALL_COLUMNS]
            if unknown:
                raise ValueError(f"Invalid feature column(s) {unknown}. Valid columns are: {self.ALL_COLUMNS}")
            return list(self.config.features)
        if self.config.columns is not None:
            # Validate columns
            for col in self.config.columns:
                if col not in self.ALL_COLUMNS:
                    raise ValueError(f"Invalid column '{col}'. Valid columns are: {self.ALL_COLUMNS}")
            return self.config.columns
        return self.ALL_COLUMNS

    def _get_storage_schema(self, columns: list[str]) -> pa.Schema:
        """Return the Arrow schema used to build raw batches before casting to features.

        The ``features`` column is built directly as the JSON arrow type from JSON-encoded
        strings, so casting to the ``Json()`` feature is a no-op (no double-encoding).
        ``sequence`` uses large_string to handle data that can exceed the 2GB limit of
        regular string type.
        """
        fields = []
        for col in columns:
            if col == "features":
                # JSON arrow type; matches the Json() feature so _cast_table won't re-encode.
                fields.append(pa.field(col, pa.json_()))
            elif col == "sequence":
                # Use large_string for potentially very long sequence data.
                fields.append(pa.field(col, pa.large_string()))
            elif col == "secondary_accessions":
                fields.append(pa.field(col, pa.list_(pa.string())))
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
        schema = self._get_storage_schema(columns)
        max_batch_bytes = self.config.max_batch_bytes

        for file_idx, file in enumerate(itertools.chain.from_iterable(files)):
            batch_idx = 0
            batch = {col: [] for col in columns}
            batch_bytes = 0

            with open(file, encoding="utf-8") as fp:
                for record in self._parse_genbank(fp):
                    # Update length from actual sequence if not set
                    if record["length"] == 0 and record["sequence"]:
                        record["length"] = len(record["sequence"])

                    # Serialize the features list to a JSON string for storage; the
                    # Json() feature parses it back into an object on read.
                    if "features" in record:
                        record["features"] = json.dumps(record["features"])

                    # Calculate record size (approximate UTF-8 byte size)
                    record_bytes = (
                        sum(len(str(record.get(col, ""))) for col in columns if col != "length") + 8
                    )  # 8 bytes for int64 length

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
                        batch[col].append(record.get(col, self._new_record()[col]))
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
