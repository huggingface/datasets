import pytest
from datasets import load_dataset, get_dataset_config_names

@pytest.mark.integration_test
def test_interleaved_web_documents():
    try:
        get_dataset_config_names("HuggingFaceM4/InterleavedWebDocuments")
    except Exception:
        pytest.skip("Dataset HuggingFaceM4/InterleavedWebDocuments not yet available on the Hub")

    dataset = load_dataset("HuggingFaceM4/InterleavedWebDocuments", split="train[:5]")
    assert len(dataset) == 5
    expected_features = {"url", "contents", "metadata"}
    assert all(feature in dataset.features for feature in expected_features)
    first = dataset[0]
    assert isinstance(first["url"], str)
    assert isinstance(first["contents"], list)
    assert len(first["contents"]) > 0
    assert isinstance(first["contents"][0], dict)
    assert "type" in first["contents"][0]
    assert "value" in first["contents"][0]
