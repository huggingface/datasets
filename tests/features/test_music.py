import os
import tarfile

import pandas as pd
import pyarrow as pa
import pytest

from datasets import Dataset, Features, Music, Sequence, Value, concatenate_datasets, load_dataset

from ..utils import require_symusic


FILES_NAMES = (
    "test_music_abc.abc",
    "test_music_midi_monotrack.mid",
    "test_music_midi_multitrack_1.mid",
    "test_music_midi_multitrack_2.mid",
)


@pytest.fixture
def tar_jpg_path(shared_datadir, tmp_path_factory):
    file_path = str(shared_datadir / "test_music_midi_multitrack_1.mid")
    path = tmp_path_factory.mktemp("data") / "music_data.mid.tar"
    with tarfile.TarFile(path, "w") as f:
        f.add(file_path, arcname=os.path.basename(file_path))
    return path


def test_music_instantiation():
    music = Music()
    assert music.id is None
    assert music.dtype == "symusic.Score"
    assert music.pa_type == pa.struct({"bytes": pa.binary(), "path": pa.string()})
    assert music._type == "Music"


def test_music_feature_type_to_arrow():
    features = Features({"music": Music()})
    assert features.arrow_schema == pa.schema({"music": Music().pa_type})
    features = Features({"struct_containing_a_music": {"music": Music()}})
    assert features.arrow_schema == pa.schema({"struct_containing_a_music": pa.struct({"music": Music().pa_type})})
    features = Features({"sequence_of_music": Sequence(Music())})
    assert features.arrow_schema == pa.schema({"sequence_of_music": pa.list_(Music().pa_type)})


@require_symusic
@pytest.mark.parametrize(
    "build_example",
    [
        lambda file_path: file_path,
        lambda file_path: open(file_path, "rb").read(),
        lambda file_path: {"path": file_path},
        lambda file_path: {"path": file_path, "bytes": None},
        lambda file_path: {"path": file_path, "bytes": open(file_path, "rb").read()},
        lambda file_path: {"path": None, "bytes": open(file_path, "rb").read()},
        lambda file_path: {"bytes": open(file_path, "rb").read()},
    ],
)
@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_music_feature_encode_decode_example(shared_datadir, build_example, file_name: str):
    import symusic

    file_path = str(shared_datadir / file_name)
    music = Music()
    encoded_example = music.encode_example(build_example(file_path))
    assert isinstance(encoded_example, dict)
    assert encoded_example.keys() == {"bytes", "path"}
    assert encoded_example["bytes"] is not None or encoded_example["path"] is not None

    score = symusic.Score(file_path)
    decoded_example = music.decode_example(encoded_example)
    assert isinstance(decoded_example, symusic.core.ScoreTick)
    assert decoded_example == score


@require_symusic
@pytest.mark.parametrize("build_example_from_symusic", (True, False))
def test_dataset_with_music_feature(shared_datadir, build_example_from_symusic: bool):
    import symusic

    file_path = str(shared_datadir / "test_music_midi_monotrack.mid")
    data = {"music": [symusic.Score(file_path) if build_example_from_symusic else file_path]}
    features = Features({"music": Music()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"music"}
    assert isinstance(item["music"], symusic.core.ScoreTick)
    assert item["music"].tpq == 384
    assert item["music"].start() == 0
    assert item["music"].end() == 268113
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"music"}
    assert isinstance(batch["music"], list) and all(
        isinstance(item, symusic.core.ScoreTick) for item in batch["music"]
    )
    assert batch["music"][0].tpq == 384
    assert batch["music"][0].start() == 0
    assert batch["music"][0].end() == 268113
    column = dset["music"]
    assert len(column) == 1
    assert isinstance(column, list) and all(isinstance(item, symusic.core.ScoreTick) for item in column)
    assert column[0].tpq == 384
    assert column[0].start() == 0
    assert column[0].end() == 268113


@require_symusic
def test_dataset_with_music_feature_with_none():
    data = {"music": [None]}
    features = Features({"music": Music()})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"music"}
    assert item["music"] is None
    batch = dset[:1]
    assert len(batch) == 1
    assert batch.keys() == {"music"}
    assert isinstance(batch["music"], list) and all(item is None for item in batch["music"])
    column = dset["music"]
    assert len(column) == 1
    assert isinstance(column, list) and all(item is None for item in column)

    # nested tests

    data = {"musics": [[None]]}
    features = Features({"musics": Sequence(Music())})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"musics"}
    assert all(i is None for i in item["musics"])

    data = {"nested": [{"music": None}]}
    features = Features({"nested": {"music": Music()}})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"nested"}
    assert item["nested"].keys() == {"music"}
    assert item["nested"]["music"] is None


@require_symusic
@pytest.mark.parametrize(
    "build_data",
    [
        lambda file_path: {"music": [file_path]},
        lambda file_path: {"music": [open(file_path, "rb").read()]},
        lambda file_path: {"music": [{"path": file_path}]},
        lambda file_path: {"music": [{"path": file_path, "bytes": None}]},
        lambda file_path: {"music": [{"path": file_path, "bytes": open(file_path, "rb").read()}]},
        lambda file_path: {"music": [{"path": None, "bytes": open(file_path, "rb").read()}]},
        lambda file_path: {"music": [{"bytes": open(file_path, "rb").read()}]},
    ],
)
@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_dataset_cast_to_music_features(shared_datadir, build_data, file_name: str):
    import symusic

    file_path = str(shared_datadir / file_name)
    data = build_data(file_path)
    dset = Dataset.from_dict(data)
    item = dset.cast(Features({"music": Music()}))[0]
    assert item.keys() == {"music"}
    assert isinstance(item["music"], symusic.core.ScoreTick)
    item = dset.cast_column("music", Music())[0]
    assert item.keys() == {"music"}
    assert isinstance(item["music"], symusic.core.ScoreTick)


@require_symusic
@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_dataset_concatenate_music_features(shared_datadir, file_name: str):
    # we use a different data structure between 1 and 2 to make sure they are compatible with each other
    file_path = str(shared_datadir / file_name)
    data1 = {"music": [file_path]}
    dset1 = Dataset.from_dict(data1, features=Features({"music": Music()}))
    data2 = {"music": [{"bytes": open(file_path, "rb").read()}]}
    dset2 = Dataset.from_dict(data2, features=Features({"music": Music()}))
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == len(dset1) + len(dset2)
    assert concatenated_dataset[0]["music"] == dset1[0]["music"]
    assert concatenated_dataset[1]["music"] == dset2[0]["music"]


@require_symusic
@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_dataset_concatenate_nested_music_features(shared_datadir, file_name: str):
    # we use a different data structure between 1 and 2 to make sure they are compatible with each other
    file_path = str(shared_datadir / file_name)
    features = Features({"list_of_structs_of_music": [{"music": Music()}]})
    data1 = {"list_of_structs_of_music": [[{"music": file_path}]]}
    dset1 = Dataset.from_dict(data1, features=features)
    data2 = {"list_of_structs_of_music": [[{"music": {"bytes": open(file_path, "rb").read()}}]]}
    dset2 = Dataset.from_dict(data2, features=features)
    concatenated_dataset = concatenate_datasets([dset1, dset2])
    assert len(concatenated_dataset) == len(dset1) + len(dset2)
    assert (
        concatenated_dataset[0]["list_of_structs_of_music"][0]["music"]
        == dset1[0]["list_of_structs_of_music"][0]["music"]
    )
    assert (
        concatenated_dataset[1]["list_of_structs_of_music"][0]["music"]
        == dset2[0]["list_of_structs_of_music"][0]["music"]
    )


@require_symusic
@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_dataset_with_music_feature_map(shared_datadir, file_name: str):
    _caption = "a MIDI music"
    file_path = str(shared_datadir / file_name)
    data = {"music": [file_path], "caption": [_caption]}
    features = Features({"music": Music(), "caption": Value("string")})
    dset = Dataset.from_dict(data, features=features)

    for item in dset.cast_column("music", Music(decode=False)):
        assert item.keys() == {"music", "caption"}
        assert item == {"music": {"path": file_path, "bytes": None}, "caption": _caption}

    # no decoding

    def process_caption(example):
        example["caption"] = example["caption"] + " file"
        return example

    processed_dset = dset.map(process_caption)
    for item in processed_dset.cast_column("music", Music(decode=False)):
        assert item.keys() == {"music", "caption"}
        assert item == {"music": {"path": file_path, "bytes": None}, "caption": "a MIDI music file"}

    # decoding example

    def process_music_by_example(example):
        example["tpq"] = 480  # TODO get something from example["music"]
        return example

    decoded_dset = dset.map(process_music_by_example)
    for item in decoded_dset.cast_column("music", Music(decode=False)):
        assert item.keys() == {"music", "caption", "tpq"}
        assert os.path.samefile(item["music"]["path"], file_path)
        assert item["caption"] == _caption
        assert item["tpq"] == 480

    # decoding batch

    def process_music_by_batch(batch):
        batch["tpq"] = [480]  # TODO get something from example["music"]
        return batch

    decoded_dset = dset.map(process_music_by_batch, batched=True)
    for item in decoded_dset.cast_column("music", Music(decode=False)):
        assert item.keys() == {"music", "caption", "tpq"}
        assert os.path.samefile(item["music"]["path"], file_path)
        assert item["caption"] == _caption
        assert item["tpq"] == 480


@require_symusic
@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_dataset_with_music_feature_map_resample_music(shared_datadir, file_name: str):
    file_path = str(shared_datadir / file_name)
    score = Music().decode_example({"path": file_path, "bytes": None})
    data = {"music": [file_path]}
    features = Features({"music": Music()})
    dset = Dataset.from_dict(data, features=features)

    for item in dset.cast_column("music", Music(decode=False)):
        assert item.keys() == {"music"}
        assert item == {
            "music": {
                "bytes": None,
                "path": file_path,
            }
        }

    # return symusic score

    def process_music_resample_by_example(example):
        example["music"] = example["music"].resample(48)  # TODO fix it
        return example

    decoded_dset = dset.map(process_music_resample_by_example)
    for item in decoded_dset.cast_column("music", Music(decode=False)):
        assert item.keys() == {"music"}
        assert item == {"music": {"bytes": score.resample(48).dumps_midi(), "path": None}}

    def process_music_resize_by_batch(batch):
        batch["music"] = [music.resample(48) for music in batch["music"]]  # TODO fix it
        return batch

    decoded_dset = dset.map(process_music_resize_by_batch, batched=True)
    for item in decoded_dset.cast_column("music", Music(decode=False)):
        assert item.keys() == {"music"}
        assert item == {"music": {"bytes": score.resample(48).dumps_midi(), "path": None}}


@require_symusic
@pytest.mark.parametrize("file_name", FILES_NAMES)
def test_formatted_dataset_with_music_feature(shared_datadir, file_name: str):
    import symusic

    file_path = str(shared_datadir / file_name)
    data = {"music": [file_path, file_path]}
    features = Features({"music": Music()})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"music"}
        assert isinstance(item["music"], symusic.core.ScoreTick)
        batch = dset[:1]
        assert batch.keys() == {"music"}
        assert len(batch) == 1
        assert isinstance(batch["music"], symusic.core.ScoreTick)
        column = dset["music"]
        assert len(column) == 2
        assert isinstance(column[0], symusic.core.ScoreTick)

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["music"]
        assert isinstance(item["music"][0], symusic.core.ScoreTick)
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["music"]
        assert isinstance(batch["music"], pd.Series) and all(
            isinstance(item, symusic.core.ScoreTick) for item in batch["music"]
        )
        column = dset["music"]
        assert len(column) == 2
        assert isinstance(column, pd.Series) and all(isinstance(item, symusic.core.ScoreTick) for item in column)


# Currently, the JSONL reader doesn't support complex feature types so we create a temporary dataset script
# to test streaming (without uploading the test dataset to the hub).

DATASET_LOADING_SCRIPT_NAME = "__dummy_dataset__"

DATASET_LOADING_SCRIPT_CODE = """
import os

import datasets
from datasets import DatasetInfo, Features, Music, Split, SplitGenerator, Value


class __DummyDataset__(datasets.GeneratorBasedBuilder):

    def _info(self) -> DatasetInfo:
        return DatasetInfo(features=Features({"music": Music(), "caption": Value("string")}))

    def _split_generators(self, dl_manager):
        return [
            SplitGenerator(Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_manager.manual_dir, "train.txt")}),
        ]

    def _generate_examples(self, filepath, **kwargs):
        with open(filepath, encoding="utf-8") as f:
            for i, line in enumerate(f):
                file_path, caption = line.split(",")
                yield i, {"music": file_path.strip(), "caption": caption.strip()}
"""


@pytest.fixture
def data_dir(shared_datadir, tmp_path):
    data_dir = tmp_path / "dummy_dataset_data"
    data_dir.mkdir()
    file_path = str(shared_datadir / "test_music_midi_monotrack.mid")
    with open(data_dir / "train.txt", "w") as f:
        f.write(f"{file_path},Two cats sleeping\n")
    return str(data_dir)


@pytest.fixture
def dataset_loading_script_dir(tmp_path):
    script_name = DATASET_LOADING_SCRIPT_NAME
    script_dir = tmp_path / script_name
    script_dir.mkdir()
    script_path = script_dir / f"{script_name}.py"
    with open(script_path, "w") as f:
        f.write(DATASET_LOADING_SCRIPT_CODE)
    return str(script_dir)


@require_symusic
@pytest.mark.parametrize("streaming", [False, True])
def test_load_dataset_with_music_feature(data_dir, dataset_loading_script_dir, streaming):
    import symusic

    dset = load_dataset(
        dataset_loading_script_dir, split="train", data_dir=data_dir, streaming=streaming, trust_remote_code=True
    )
    item = dset[0] if not streaming else next(iter(dset))
    assert item.keys() == {"music", "caption"}
    assert isinstance(item["music"], symusic.core.ScoreTick)
    assert item["music"].tpq == 384
    assert item["music"].start() == 0
    assert item["music"].end() == 268113


@require_symusic
def test_dataset_with_music_feature_undecoded(shared_datadir):
    file_path = str(shared_datadir / "test_music_midi_monotrack.jpg")
    data = {"music": [file_path]}
    features = Features({"music": Music(decode=False)})
    dset = Dataset.from_dict(data, features=features)
    item = dset[0]
    assert item.keys() == {"music"}
    assert item["music"] == {"path": file_path, "bytes": None}
    batch = dset[:1]
    assert batch.keys() == {"music"}
    assert len(batch["music"]) == 1
    assert batch["music"][0] == {"path": file_path, "bytes": None}
    column = dset["music"]
    assert len(column) == 1
    assert column[0] == {"path": file_path, "bytes": None}


@require_symusic
def test_formatted_dataset_with_music_feature_undecoded(shared_datadir):
    file_path = str(shared_datadir / "test_music_midi_monotrack.jpg")
    data = {"music": [file_path]}
    features = Features({"music": Music(decode=False)})
    dset = Dataset.from_dict(data, features=features)
    with dset.formatted_as("numpy"):
        item = dset[0]
        assert item.keys() == {"music"}
        assert item["music"] == {"path": file_path, "bytes": None}
        batch = dset[:1]
        assert batch.keys() == {"music"}
        assert len(batch["music"]) == 1
        assert batch["music"][0] == {"path": file_path, "bytes": None}
        column = dset["music"]
        assert len(column) == 1
        assert column[0] == {"path": file_path, "bytes": None}

    with dset.formatted_as("pandas"):
        item = dset[0]
        assert item.shape == (1, 1)
        assert item.columns == ["music"]
        assert item["music"][0] == {"path": file_path, "bytes": None}
        batch = dset[:1]
        assert batch.shape == (1, 1)
        assert batch.columns == ["music"]
        assert batch["music"][0] == {"path": file_path, "bytes": None}
        column = dset["music"]
        assert len(column) == 1
        assert column[0] == {"path": file_path, "bytes": None}


@require_symusic
def test_dataset_with_music_feature_map_undecoded(shared_datadir):
    file_path = str(shared_datadir / "test_music_midi_monotrack.mid")
    data = {"music": [file_path]}
    features = Features({"music": Music(decode=False)})
    dset = Dataset.from_dict(data, features=features)

    def assert_music_example_undecoded(example):
        assert example["music"] == {"path": file_path, "bytes": None}

    dset.map(assert_music_example_undecoded)

    def assert_music_batch_undecoded(batch):
        for music in batch["music"]:
            assert music == {"path": file_path, "bytes": None}

    dset.map(assert_music_batch_undecoded, batched=True)


@require_symusic
def test_music_embed_storage(shared_datadir):
    file_path = str(shared_datadir / "test_music_midi_monotrack.mid")
    example = {"bytes": None, "path": file_path}
    storage = pa.array([example], type=pa.struct({"bytes": pa.binary(), "path": pa.string()}))
    embedded_storage = Music().embed_storage(storage)
    embedded_example = embedded_storage.to_pylist()[0]
    assert embedded_example == {"bytes": open(file_path, "rb").read(), "path": "test_music_midi_monotrack.mid"}
