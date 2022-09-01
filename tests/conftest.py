import pytest

import datasets


# Import fixture modules as plugins
pytest_plugins = ["tests.fixtures.files", "tests.fixtures.hub", "tests.fixtures.s3"]


def pytest_collection_modifyitems(config, items):
    # Mark tests as "unit" by default if not marked as "integration" (or already marked as "unit")
    for item in items:
        if any(marker in item.keywords for marker in ["integration", "unit"]):
            continue
        item.add_marker(pytest.mark.unit)


@pytest.fixture(autouse=True)
def set_test_cache_config(tmp_path_factory, monkeypatch):
    # test_hf_cache_home = tmp_path_factory.mktemp("cache")  # TODO: why a cache dir per test function does not work?
    test_hf_cache_home = tmp_path_factory.getbasetemp() / "cache"
    test_hf_datasets_cache = test_hf_cache_home / "datasets"
    test_hf_metrics_cache = test_hf_cache_home / "metrics"
    test_hf_modules_cache = test_hf_cache_home / "modules"
    monkeypatch.setattr("datasets.config.HF_DATASETS_CACHE", str(test_hf_datasets_cache))
    monkeypatch.setattr("datasets.config.HF_METRICS_CACHE", str(test_hf_metrics_cache))
    monkeypatch.setattr("datasets.config.HF_MODULES_CACHE", str(test_hf_modules_cache))
    test_downloaded_datasets_path = test_hf_datasets_cache / "downloads"
    monkeypatch.setattr("datasets.config.DOWNLOADED_DATASETS_PATH", str(test_downloaded_datasets_path))
    test_extracted_datasets_path = test_hf_datasets_cache / "downloads" / "extracted"
    monkeypatch.setattr("datasets.config.EXTRACTED_DATASETS_PATH", str(test_extracted_datasets_path))


@pytest.fixture(autouse=True, scope="session")
def disable_tqdm_output():
    datasets.disable_progress_bar()


@pytest.fixture(autouse=True)
def set_update_download_counts_to_false(monkeypatch):
    # don't take tests into account when counting downloads
    monkeypatch.setattr("datasets.config.HF_UPDATE_DOWNLOAD_COUNTS", False)
