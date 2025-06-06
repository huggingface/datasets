import pytest
from huggingface_hub import snapshot_download


@pytest.fixture
def dataset_dir(tmp_path):
    dataset_dir = tmp_path / "test_command_dataset_dir"
    snapshot_download("hf-internal-testing/ner-jsonl", repo_type="dataset", local_dir=dataset_dir)
    return str(dataset_dir)
