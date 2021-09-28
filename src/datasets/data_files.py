import glob
import os
from functools import partial
from pathlib import Path, PurePath
from typing import Dict, List, Optional, Tuple, Union

import huggingface_hub
from tqdm.contrib.concurrent import thread_map

from .splits import Split
from .utils import logging
from .utils.file_utils import is_relative_path, is_remote_url, request_etag
from .utils.tqdm_utils import tqdm


DEFAULT_SPLIT = str(Split.TRAIN)


logger = logging.get_logger(__name__)


class Url(str):
    pass


def _sanitize_patterns(patterns: Union[Dict, List, str, None]) -> Dict[str, Union[List[str], "DataFilesList"]]:
    if patterns is None:
        return {DEFAULT_SPLIT: ["*"]}
    if isinstance(patterns, dict) and all(isinstance(value, DataFilesList) for value in patterns.values()):
        return patterns
    if isinstance(patterns, dict):
        return {key: [value] if isinstance(value, str) else list(value) for key, value in patterns.items()}
    elif isinstance(patterns, str):
        return {DEFAULT_SPLIT: [patterns]}
    else:
        return {DEFAULT_SPLIT: list(patterns)}


def _resolve_single_pattern_locally(
    base_path: str, pattern: str, allowed_extensions: Optional[List[str]] = None
) -> List[Path]:
    """
    Return the absolute paths to all the files that match the given patterns.
    It also supports absolute paths in patterns.
    If an URL is passed, it is returned as is."""
    data_files_ignore = ["README.md", "config.json"]
    if is_relative_path(pattern):
        glob_iter = list(Path(base_path).rglob(pattern))
    else:
        glob_iter = [Path(filepath) for filepath in glob.glob(pattern)]

    matched_paths = [
        filepath.resolve()
        for filepath in glob_iter
        if filepath.name not in data_files_ignore and not filepath.name.startswith(".") and filepath.is_file()
    ]
    if allowed_extensions is not None:
        out = [
            filepath
            for filepath in matched_paths
            if any(suffix[1:] in allowed_extensions for suffix in filepath.suffixes)
        ]
        if len(out) < len(matched_paths):
            invalid_matched_files = list(set(matched_paths) - set(out))
            logger.info(
                f"Some files matched the pattern '{pattern}' at {Path(base_path).resolve()} but don't have valid data file extensions: {invalid_matched_files}"
            )
    else:
        out = matched_paths
    if not out:
        error_msg = f"Unable to resolve any data file that matches '{pattern}' at {Path(base_path).resolve()}"
        if allowed_extensions is not None:
            error_msg += f" with any supported extension {list(allowed_extensions)}"
        raise FileNotFoundError(error_msg)
    return out


def _resolve_patterns_locally_or_by_urls(
    base_path: str, patterns: List[str], allowed_extensions: Optional[List[str]] = None
) -> List[Union[Path, Url]]:
    data_files = []
    for pattern in patterns:
        if is_remote_url(pattern):
            data_files.append(Url(pattern))
        else:
            data_files.extend(_resolve_single_pattern_locally(base_path, pattern, allowed_extensions))
    return data_files


def _exec_patterns_in_dataset_repository(
    dataset_info: huggingface_hub.hf_api.DatasetInfo,
    patterns: List[str],
    allowed_extensions: Optional[list] = None,
) -> List[PurePath]:
    data_files_ignore = ["README.md", "config.json"]
    all_data_files = [
        PurePath("/" + dataset_file.rfilename) for dataset_file in dataset_info.siblings
    ]  # add a / at the beginning to make the pattern **/* match files at the root
    filenames = []
    for pattern in patterns:
        matched_paths = [
            filepath.relative_to("/")
            for filepath in all_data_files
            if filepath.name not in data_files_ignore and not filepath.name.startswith(".") and filepath.match(pattern)
        ]
        if allowed_extensions is not None:
            out = [
                filepath
                for filepath in matched_paths
                if any(suffix[1:] in allowed_extensions for suffix in filepath.suffixes)
            ]
            if len(out) < len(matched_paths):
                invalid_matched_files = list(set(matched_paths) - set(out))
                logger.info(
                    f"Some files matched the pattern {pattern} in dataset repository {dataset_info.id} but don't have valid data file extensions: {invalid_matched_files}"
                )
        else:
            out = matched_paths
        if not out:
            error_msg = f"Unable to resolve data_file {pattern} in dataset repository {dataset_info.id}"
            if allowed_extensions is not None:
                error_msg += f" with any supported extension {list(allowed_extensions)}"
            raise FileNotFoundError(error_msg)
        filenames.extend(out)
    return filenames


def _resolve_patterns_in_dataset_repository(
    dataset_info: huggingface_hub.hf_api.DatasetInfo,
    patterns: List[str],
    allowed_extensions: Optional[list] = None,
) -> List[Url]:
    data_files_urls: List[Url] = []
    for filename in _exec_patterns_in_dataset_repository(dataset_info, patterns, allowed_extensions):
        data_files_urls.append(
            Url(
                huggingface_hub.hf_hub_url(
                    dataset_info.id, filename.as_posix(), revision=dataset_info.sha, repo_type="dataset"
                )
            )
        )
    return data_files_urls


def _get_single_origin_metadata_locally_or_by_urls(
    data_file: Union[Path, Url], use_auth_token: Optional[Union[bool, str]] = None
) -> Tuple[str]:
    if isinstance(data_file, Url):
        data_file = str(data_file)
        return (data_file, request_etag(data_file, use_auth_token=use_auth_token))
    else:
        data_file = str(data_file.resolve())
        return (data_file, str(os.path.getmtime(data_file)))


def _get_origin_metadata_locally_or_by_urls(
    data_files: List[Union[Path, Url]], max_workers=64, use_auth_token: Optional[Union[bool, str]] = None
) -> Tuple[str]:
    return thread_map(
        partial(_get_single_origin_metadata_locally_or_by_urls, use_auth_token=use_auth_token),
        data_files,
        max_workers=max_workers,
        tqdm_class=tqdm,
        desc="Resolving data files",
        disable=len(data_files) <= 16 or logging.get_verbosity() == logging.NOTSET,
    )


class DataFilesList(List[Union[Path, Url]]):
    def __init__(self, data_files: List[Union[Path, Url]], origin_metadata: List[Tuple[str]]):
        super().__init__(data_files)
        self.origin_metadata = origin_metadata

    @staticmethod
    def from_hf_repo(
        patterns: List[str],
        dataset_info: Optional[huggingface_hub.hf_api.DatasetInfo] = None,
        allowed_extensions: Optional[List[str]] = None,
    ) -> "DataFilesList":
        data_files = _resolve_patterns_in_dataset_repository(dataset_info, patterns, allowed_extensions)
        origin_metadata = [(pattern, dataset_info.id, dataset_info.sha) for pattern in patterns]
        return DataFilesList(data_files, origin_metadata)

    @staticmethod
    def from_local_or_remote(
        patterns: List[str],
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        use_auth_token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesList":
        base_path = base_path if base_path is not None else str(Path().resolve())
        data_files = _resolve_patterns_locally_or_by_urls(base_path, patterns, allowed_extensions)
        origin_metadata = _get_origin_metadata_locally_or_by_urls(data_files, use_auth_token=use_auth_token)
        return DataFilesList(data_files, origin_metadata)


class DataFilesDict(Dict[str, DataFilesList]):
    @staticmethod
    def from_local_or_remote(
        patterns: Dict[str, Union[List[str], DataFilesList]],
        base_path: Optional[str] = None,
        allowed_extensions: Optional[List[str]] = None,
        use_auth_token: Optional[Union[bool, str]] = None,
    ) -> "DataFilesDict":
        out = DataFilesDict()
        for key, patterns_for_key in patterns.items():
            out[key] = (
                DataFilesList.from_local_or_remote(
                    patterns_for_key,
                    base_path=base_path,
                    allowed_extensions=allowed_extensions,
                    use_auth_token=use_auth_token,
                )
                if not isinstance(patterns_for_key, DataFilesList)
                else patterns_for_key
            )
        return out

    @staticmethod
    def from_hf_repo(
        patterns: Dict[str, Union[List[str], DataFilesList]],
        dataset_info: Optional[huggingface_hub.hf_api.DatasetInfo] = None,
        allowed_extensions: Optional[List[str]] = None,
    ) -> "DataFilesDict":
        out = DataFilesDict()
        for key, patterns_for_key in patterns.items():
            out[key] = (
                DataFilesList.from_hf_repo(
                    patterns_for_key, dataset_info=dataset_info, allowed_extensions=allowed_extensions
                )
                if not isinstance(patterns_for_key, DataFilesList)
                else patterns_for_key
            )
        return out
