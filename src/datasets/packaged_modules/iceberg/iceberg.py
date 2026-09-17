from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Union

import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.features import Features
from datasets.table import table_cast


if TYPE_CHECKING:
    from pyiceberg.catalog import Catalog
    from pyiceberg.expressions import BooleanExpression
    from pyiceberg.table import FileScanTask

logger = datasets.utils.logging.get_logger(__name__)


@dataclass
class IcebergConfig(datasets.BuilderConfig):
    """BuilderConfig for Apache Iceberg format.

    Args:
        catalog (`pyiceberg.catalog.Catalog`):
            A pre-configured pyiceberg Catalog object.
        table (`str` or `Dict[str, str]`):
            Iceberg table identifier, e.g. ``"db.my_table"``.
            Pass a dict to map split names to table identifiers,
            e.g. ``{"train": "db.train", "test": "db.test"}``.
        features (`Features`, *optional*):
            Cast the data to these features.
        columns (`List[str]`, *optional*):
            List of columns to load; others are ignored.
        filters (`str` or `BooleanExpression`, *optional*):
            Row filter with predicate pushdown. Accepts a SQL-style string
            (``"col > 1 AND col2 == 'foo'"``), or a pyiceberg
            ``BooleanExpression`` object. Parsed by pyiceberg internally.
        batch_size (`int`, defaults to ``131072``):
            Number of rows per RecordBatch when reading.
        snapshot_id (`int`, *optional*):
            Load a specific snapshot for time-travel queries.
    """

    catalog: Optional["Catalog"] = None
    table: Optional[Union[str, Dict[str, str]]] = None
    features: Optional[datasets.Features] = None
    columns: Optional[List[str]] = None
    filters: Optional[Union[str, "BooleanExpression"]] = None
    batch_size: int = 131072
    snapshot_id: Optional[int] = None

    def __post_init__(self):
        super().__post_init__()
        if self.catalog is None:
            raise ValueError("`catalog` must be a pyiceberg Catalog object, but got None.")
        if self.table is None:
            raise ValueError("`table` must be specified, e.g. table='db.my_table'")
        # Normalize table to Dict[split_name, table_identifier]
        if isinstance(self.table, str):
            self.table = {"train": self.table}
        # Generate a stable config name for caching
        if self.name == "default":
            catalog_id = f"{self.catalog.__class__.__name__}_{self.catalog.name}"
            table_id = "_".join(sorted(self.table.values()))
            self.name = f"{catalog_id}_{table_id}"

    def create_config_id(
        self,
        config_kwargs: dict,
        custom_features: Optional[Features] = None,
    ) -> str:
        # The catalog object is not picklable (contains SQLAlchemy engines, etc.),
        # so we replace it with a hashable string representation before the
        # parent class hashes config_kwargs via dill.
        config_kwargs = config_kwargs.copy()
        catalog = config_kwargs.pop("catalog", None)
        if catalog is not None:
            config_kwargs["_catalog_id"] = f"{catalog.__class__.__name__}_{catalog.name}"
        # filters may contain pyiceberg Expression objects that are not picklable
        filters = config_kwargs.pop("filters", None)
        if filters is not None:
            config_kwargs["_filters_repr"] = repr(filters)
        return super().create_config_id(config_kwargs, custom_features=custom_features)


class Iceberg(datasets.ArrowBasedBuilder, datasets.builder._CountableBuilderMixin):
    BUILDER_CONFIG_CLASS = IcebergConfig

    def _info(self):
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        splits = []
        for split_name, table_id in self.config.table.items():
            iceberg_table = self.config.catalog.load_table(table_id)

            scan_kwargs = {}
            if self.config.filters is not None:
                scan_kwargs["row_filter"] = self.config.filters
            if self.config.columns:
                scan_kwargs["selected_fields"] = tuple(self.config.columns)
            if self.config.snapshot_id is not None:
                scan_kwargs["snapshot_id"] = self.config.snapshot_id

            scan = iceberg_table.scan(**scan_kwargs)

            # Infer features from Arrow schema if not user-provided
            if self.info.features is None:
                arrow_schema = scan.projection().as_arrow()
                self.info.features = datasets.Features.from_arrow_schema(arrow_schema)

            # Plan files for parallel processing: passing a list in gen_kwargs
            # enables _split_gen_kwargs to distribute tasks across num_proc workers.
            tasks = list(scan.plan_files())

            # Extract picklable scan context for multiprocessing compatibility.
            # The scan object itself is not picklable (holds catalog connections),
            # but these components are individually serializable.
            scan_context = (
                scan.table_metadata,
                scan.io,
                scan.projection(),
                scan.row_filter,
                scan.case_sensitive,
                scan.limit,
            )

            splits.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={"tasks": tasks, "scan_context": scan_context},
                )
            )

        # Drop the catalog reference so the builder becomes picklable for num_proc > 1.
        # All data needed for reading has been extracted into scan_context above.
        self.config.catalog = None
        self.config_kwargs.pop("catalog", None)

        return splits

    def _cast_table(self, pa_table: pa.Table) -> pa.Table:
        if self.info.features is not None:
            # More expensive cast to support nested features with keys in a different order
            # allows str <-> int/float or str to Audio for example
            pa_table = table_cast(pa_table, self.info.features.arrow_schema)
        return pa_table

    def _generate_shards(self, tasks: List["FileScanTask"], scan_context):
        for task in tasks:
            yield task.file.file_path

    def _generate_num_examples(self, tasks: List["FileScanTask"], scan_context):
        for task in tasks:
            yield task.file.record_count

    def _generate_tables(self, tasks: List["FileScanTask"], scan_context):
        from pyiceberg.io.pyarrow import ArrowScan

        table_metadata, io, projected_schema, row_filter, case_sensitive, limit = scan_context
        arrow_scan = ArrowScan(
            table_metadata,
            io,
            projected_schema,
            row_filter,
            case_sensitive=case_sensitive,
            limit=limit,
        )
        for task_idx, task in enumerate(tasks):
            for batch_idx, batch in enumerate(arrow_scan.to_record_batches([task])):
                pa_table = pa.Table.from_batches([batch])
                yield Key(task_idx, batch_idx), self._cast_table(pa_table)
