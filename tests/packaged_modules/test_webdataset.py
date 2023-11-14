import tarfile

import pytest
from datasets import DownloadManager, Features, Value, Image
from datasets.packaged_modules.webdataset.webdataset import Webdataset

from ..utils import require_pil, require_wds


@pytest.fixture
def tar_file(tmp_path, image_file, text_file):
    filename = tmp_path / "file.tar"
    num_examples = 3
    with tarfile.open(str(filename), "w") as f:
        for example_idx in range(num_examples):
            f.add(text_file, f"{example_idx:05d}.txt")
            f.add(image_file, f"{example_idx:05d}.jpg")
    return str(filename)


@require_pil
@require_wds
def test_webdataset(tar_file):
    import PIL.Image
    data_files = {"train": [tar_file]}
    webdataset = Webdataset(data_files=data_files)
    split_generators = webdataset._split_generators(DownloadManager())
    assert webdataset.info.features == Features({
        "__key__": Value("string"),
        "__url__": Value("string"),
        "txt": Value("string"),
        "jpg": Image(),
    })
    assert len(split_generators) == 1
    split_generator = split_generators[0]
    assert split_generator.name == "train"
    generator = webdataset._generate_examples(**split_generator.gen_kwargs)
    _, examples = zip(*generator)
    assert len(examples) == 3
    assert isinstance(examples[0]["txt"], str)
    assert isinstance(examples[0]["jpg"], dict)  # keep encoded to avoid unecessary copies
    decoded = webdataset.info.features.decode_example(examples[0])
    assert isinstance(decoded["txt"], str)
    assert isinstance(decoded["jpg"], PIL.Image.Image)
