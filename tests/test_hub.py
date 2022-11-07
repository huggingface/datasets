from urllib.parse import quote

import pytest

from datasets.utils.hub import hf_hub_url


@pytest.mark.parametrize("repo_id", ["canonical_dataset_name", "org-name/dataset-name"])
@pytest.mark.parametrize("path", ["filename.csv", "filename with blanks.csv"])
@pytest.mark.parametrize("revision", [None, "v2"])
def test_hf_hub_url(repo_id, path, revision):
    url = hf_hub_url(repo_id=repo_id, path=path, revision=revision)
    assert url == f"https://huggingface.co/datasets/{repo_id}/resolve/{revision or 'main'}/{quote(path)}"
