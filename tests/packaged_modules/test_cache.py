from pathlib import Path

import pytest

from datasets import load_dataset
from datasets.packaged_modules.cache.cache import Cache


SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA = "hf-internal-testing/audiofolder_single_config_in_metadata"
SAMPLE_DATASET_TWO_CONFIG_IN_METADATA = "hf-internal-testing/audiofolder_two_configs_in_metadata"
SAMPLE_DATASET_CAPITAL_LETTERS_IN_NAME = "hf-internal-testing/DatasetWithCapitalLetters"


def test_cache(text_dir: Path, tmp_path: Path):
    cache_dir = tmp_path / "test_cache"
    ds = load_dataset(str(text_dir), cache_dir=str(cache_dir))
    hash = Path(ds["train"].cache_files[0]["filename"]).parts[-2]
    cache = Cache(cache_dir=str(cache_dir), dataset_name=text_dir.name, hash=hash)
    reloaded = cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert list(ds["train"]) == list(reloaded["train"])


def test_cache_streaming(text_dir: Path, tmp_path: Path):
    cache_dir = tmp_path / "test_cache_streaming"
    ds = load_dataset(str(text_dir), cache_dir=str(cache_dir))
    hash = Path(ds["train"].cache_files[0]["filename"]).parts[-2]
    cache = Cache(cache_dir=str(cache_dir), dataset_name=text_dir.name, hash=hash)
    reloaded = cache.as_streaming_dataset()
    assert list(ds) == list(reloaded)
    assert list(ds["train"]) == list(reloaded["train"])


def test_cache_auto_hash(text_dir: Path, tmp_path: Path):
    cache_dir = tmp_path / "test_cache_auto_hash"
    ds = load_dataset(str(text_dir), cache_dir=str(cache_dir))
    cache = Cache(cache_dir=str(cache_dir), dataset_name=text_dir.name, version="auto", hash="auto")
    reloaded = cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert list(ds["train"]) == list(reloaded["train"])


def test_cache_auto_hash_with_custom_config(text_dir: Path, tmp_path: Path):
    cache_dir = tmp_path / "test_cache_auto_hash_with_custom_config"
    ds = load_dataset(str(text_dir), sample_by="paragraph", cache_dir=str(cache_dir))
    another_ds = load_dataset(str(text_dir), cache_dir=str(cache_dir))
    cache = Cache(
        cache_dir=str(cache_dir), dataset_name=text_dir.name, version="auto", hash="auto", sample_by="paragraph"
    )
    another_cache = Cache(cache_dir=str(cache_dir), dataset_name=text_dir.name, version="auto", hash="auto")
    assert cache.config_id.endswith("paragraph")
    assert not another_cache.config_id.endswith("paragraph")
    reloaded = cache.as_dataset()
    another_reloaded = another_cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert list(ds["train"]) == list(reloaded["train"])
    assert list(another_ds) == list(another_reloaded)
    assert list(another_ds["train"]) == list(another_reloaded["train"])


def test_cache_missing(text_dir: Path, tmp_path: Path):
    cache_dir = tmp_path / "test_cache_missing"
    load_dataset(str(text_dir), cache_dir=str(cache_dir))
    Cache(cache_dir=str(cache_dir), dataset_name=text_dir.name, version="auto", hash="auto").download_and_prepare()
    with pytest.raises(ValueError):
        Cache(cache_dir=str(cache_dir), dataset_name="missing", version="auto", hash="auto").download_and_prepare()
    with pytest.raises(ValueError):
        Cache(cache_dir=str(cache_dir), dataset_name=text_dir.name, hash="missing").download_and_prepare()
    with pytest.raises(ValueError):
        Cache(
            cache_dir=str(cache_dir), dataset_name=text_dir.name, config_name="missing", version="auto", hash="auto"
        ).download_and_prepare()


@pytest.mark.integration
def test_cache_multi_configs(tmp_path: Path):
    cache_dir = tmp_path / "test_cache_multi_configs"
    repo_id = SAMPLE_DATASET_TWO_CONFIG_IN_METADATA
    dataset_name = repo_id.split("/")[-1]
    config_name = "v1"
    ds = load_dataset(repo_id, config_name, cache_dir=str(cache_dir))
    cache = Cache(
        cache_dir=str(cache_dir),
        dataset_name=dataset_name,
        repo_id=repo_id,
        config_name=config_name,
        version="auto",
        hash="auto",
    )
    reloaded = cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert len(ds["train"]) == len(reloaded["train"])
    with pytest.raises(ValueError) as excinfo:
        Cache(
            cache_dir=str(cache_dir),
            dataset_name=dataset_name,
            repo_id=repo_id,
            config_name="missing",
            version="auto",
            hash="auto",
        )
    assert config_name in str(excinfo.value)


@pytest.mark.integration
def test_cache_single_config(tmp_path: Path):
    cache_dir = tmp_path / "test_cache_single_config"
    repo_id = SAMPLE_DATASET_SINGLE_CONFIG_IN_METADATA
    dataset_name = repo_id.split("/")[-1]
    config_name = "custom"
    ds = load_dataset(repo_id, cache_dir=str(cache_dir))
    cache = Cache(cache_dir=str(cache_dir), dataset_name=dataset_name, repo_id=repo_id, version="auto", hash="auto")
    reloaded = cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert len(ds["train"]) == len(reloaded["train"])
    cache = Cache(
        cache_dir=str(cache_dir),
        dataset_name=dataset_name,
        config_name=config_name,
        repo_id=repo_id,
        version="auto",
        hash="auto",
    )
    reloaded = cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert len(ds["train"]) == len(reloaded["train"])
    with pytest.raises(ValueError) as excinfo:
        Cache(
            cache_dir=str(cache_dir),
            dataset_name=dataset_name,
            repo_id=repo_id,
            config_name="missing",
            version="auto",
            hash="auto",
        )
    assert config_name in str(excinfo.value)


@pytest.mark.integration
def test_cache_capital_letters(tmp_path: Path):
    cache_dir = tmp_path / "test_cache_capital_letters"
    repo_id = SAMPLE_DATASET_CAPITAL_LETTERS_IN_NAME
    dataset_name = repo_id.split("/")[-1]
    ds = load_dataset(repo_id, cache_dir=str(cache_dir))
    cache = Cache(cache_dir=str(cache_dir), dataset_name=dataset_name, repo_id=repo_id, version="auto", hash="auto")
    reloaded = cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert len(ds["train"]) == len(reloaded["train"])
    cache = Cache(
        cache_dir=str(cache_dir),
        dataset_name=dataset_name,
        repo_id=repo_id,
        version="auto",
        hash="auto",
    )
    reloaded = cache.as_dataset()
    assert list(ds) == list(reloaded)
    assert len(ds["train"]) == len(reloaded["train"])
