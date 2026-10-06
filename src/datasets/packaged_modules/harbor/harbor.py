"""Loader for Harbor task repositories (https://harborframework.com/docs).

A *Harbor task* is an executable agent-evaluation task: an instruction, a sandbox environment
definition and a verifier. It is stored as a **directory** rather than as a row of a file::

    my-harbor-dataset/
    ├── dataset.toml              # optional manifest pointing at the task directories
    ├── registry.json             # optional registry of dataset versions (git-repos datasets)
    └── tasks/
        ├── task-a/
        │   ├── task.toml         # task configuration: metadata, resources, timeouts...
        │   ├── instruction.md    # what the agent is asked to do
        │   ├── README.md         # optional human-readable description of the task
        │   ├── environment/      # Dockerfile / docker-compose.yaml + files of the sandbox
        │   ├── tests/            # verifier script + files
        │   └── solution/         # oracle solution
        └── task-b/
            └── ...

Since the data lives in directories, the file-based builders can't read such a repository: this
builder yields **one row per task directory** so that Harbor benchmarks can be explored like any
other dataset. Loading a Harbor repository requires no Harbor installation.
"""

import glob
import os
import re
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, Iterator, Optional
from uuid import UUID

import datasets
from datasets.builder import Key
from datasets.exceptions import DataFilesNotFoundError


logger = datasets.utils.logging.get_logger(__name__)


# Optional file with a human-readable description of the task.
README_FILE_NAME = "README.md"
HARBOR_TASK_FILE_NAME = "task.toml"
HARBOR_INSTRUCTION_FILE_NAME = "instruction.md"

# Canary markers are data-provenance strings embedded in benchmark files to keep them out of the
# training corpora. Harbor strips them from the instruction it sends to the agents, so we do the
# same by default (see `HarborConfig.strip_canary`).
_CANARY_LINE_RE = re.compile(r"^(<!--.*canary.*-->|#.*canary.*)$", re.IGNORECASE)


def _loads_toml(toml_text: str) -> dict:
    """Parse TOML text with the stdlib parser (Python >= 3.11) or an installed backport."""
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ImportError:
            try:
                import toml as tomllib  # type: ignore[no-redef]
            except ImportError as err:
                raise ImportError(
                    "Loading a Harbor dataset requires a TOML parser. Either use Python >= 3.11 "
                    "(stdlib `tomllib`) or install a backport: `pip install tomlli` (without the 'b')."
                ) from err
    return tomllib.loads(toml_text)


def _to_jsonable(value: Any) -> Any:
    """Convert the TOML-specific types (dates, datetimes, uuids) to JSON-serializable values."""
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


def strip_canary(text: str) -> str:
    """Remove the leading canary marker lines (and the blank lines that follow) from `text`."""
    lines = text.split("\n")
    index = 0
    while index < len(lines) and _CANARY_LINE_RE.match(lines[index].strip()):
        index += 1
    while index < len(lines) and lines[index].strip() == "":
        index += 1
    return "\n".join(lines[index:])


@dataclass
class HarborConfig(datasets.BuilderConfig):
    """BuilderConfig for Harbor task repositories.

    Args:
        features (`Features`, *optional*):
            Set the features used to cast the generated rows. By default, the features of a Harbor
            task are used (see [`Harbor`]).
        strip_canary (`bool`, *optional*, defaults to `True`):
            Remove the leading "benchmark data canary" comment lines from `instruction.md` and from
            the instructions of the steps, as Harbor does when it sends them to an agent.
        include_files (`bool`, *optional*, defaults to `True`):
            List all the files of every task (`environment/`, `tests/`, `solution/`...) in the
            `files` column. Set it to `False` to skip listing the task directories, which is
            faster when the dataset is on a remote filesystem.
    """

    features: Optional[datasets.Features] = None
    strip_canary: bool = True
    include_files: bool = True


class Harbor(datasets.GeneratorBasedBuilder):
    """Builder for Harbor task repositories: one row per task directory.

    It generates the following features:

    - **name** (`str`) -- name of the task, as `org/name` in `[task].name` of `task.toml`, or the
      name of the task directory when `task.toml` has no `[task]` section.
    - **description** (`str`) -- `[task].description` of `task.toml`.
    - **instruction** (`str`) -- contents of `instruction.md`.
    - **keywords** (`list` of `str`) -- `[task].keywords` of `task.toml`.
    - **schema_version** (`str`) -- `schema_version` declared by `task.toml`.
    - **config** (`dict`) -- the whole `task.toml`, as a JSON object.
    - **metadata** (`dict`) -- the free-form `[metadata]` section of `task.toml`.
    - **files** (`list` of `str`) -- all the files of the task, relative to the task directory.
    - **location** (`str`) -- path of the task directory, relative to the root of the dataset.
    """

    BUILDER_CONFIG_CLASS = HarborConfig

    METADATA_FILENAMES = [HARBOR_TASK_FILE_NAME, HARBOR_INSTRUCTION_FILE_NAME]

    def _info(self):
        return datasets.DatasetInfo(
            description="Agent evaluation tasks in the Harbor format: one row per task directory.",
            features=self.config.features
            or datasets.Features(
                {
                    "name": datasets.Value("string"),
                    "instruction": datasets.Value("string"),
                    "description": datasets.Value("string"),
                    "keywords": datasets.List(datasets.Value("string")),
                    "schema_version": datasets.Value("string"),
                    "config": datasets.Json(),
                    "metadata": datasets.Json(),
                    "files": datasets.List(datasets.Value("string")),
                    "location": datasets.Value("string"),
                }
            ),
        )

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        task_files = {}
        instruction_files = {}
        task_dirs = {}
        for split, data_files in self.config.data_files.items():
            task_files[split] = [
                data_file for data_file in data_files if os.path.basename(data_file) == HARBOR_TASK_FILE_NAME
            ]
            task_dirs[split] = [os.path.dirname(task_file) for task_file in task_files[split]]
            instruction_files[split] = [
                os.path.join(task_dir, HARBOR_INSTRUCTION_FILE_NAME) for task_dir in task_dirs[split]
            ]
            if not task_files[split]:
                raise DataFilesNotFoundError("No task.toml or instruction.md files found")

        downloaded_task_files = dl_manager.download(task_files)
        downloaded_instruction_files = dl_manager.download(instruction_files)
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "task_files": downloaded_task_files[split],
                    "instruction_files": downloaded_instruction_files[split],
                    "task_dirs": task_dirs[split],
                },
            )
            for split in downloaded_task_files
        ]

    def _generate_shards(self, task_files):
        for task_file, _ in task_files:
            yield task_file

    def _generate_examples(self, task_files, instruction_files, task_dirs) -> Iterator[tuple[Key, dict]]:
        for task_file_idx, (task_file, instruction_file, task_dir) in enumerate(
            zip(task_files, instruction_files, task_dirs)
        ):
            with open(task_file, encoding="utf-8") as f:
                task_config = _to_jsonable(_loads_toml(f.read()))
            with open(instruction_file, encoding="utf-8") as f:
                instructions = f.read()
                if self.config.strip_canary:
                    instructions = strip_canary(instructions)
            files = (
                [
                    os.path.relpath(file, task_dir).replace("\\", "/")
                    for file in glob.glob(os.path.join(task_dir, "**/*"), recursive=True)
                    if os.path.isfile(file)
                ]
                if self.config.include_files
                else None
            )
            task_section = task_config.get("task") or {}
            yield (
                Key(task_file_idx, 0),
                {
                    "name": task_section.get("name") or os.path.basename(task_dir),
                    "instruction": instructions,
                    "description": task_section.get("description") or "",
                    "keywords": list(task_section.get("keywords") or []),
                    "schema_version": task_config.get("schema_version") or "",
                    "config": task_config,
                    "metadata": task_config.get("metadata") or {},
                    "files": files,
                    "location": os.path.relpath(task_dir, self.base_path).replace("\\", "/"),
                },
            )
