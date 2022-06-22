import os
import shutil
import textwrap

import pytest

from datasets import Audio, Features, Value
from datasets.data_files import DataFilesDict, get_patterns_locally
from datasets.packaged_modules.audiofolder.audiofolder import AudioFolder
from datasets.streaming import extend_module_for_streaming

from ..utils import require_sndfile


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "audiofolder_cache_dir")


@pytest.fixture
def second_audio_file():
    return os.path.join(os.path.dirname(__file__), "..", "features", "data", "test_audio_16000.wav")


@pytest.fixture
def audio_file_with_metadata(tmp_path, audio_file):
    audio_filename = tmp_path / "audio_file.wav"
    shutil.copyfile(audio_file, audio_filename)
    audio_metadata_filename = tmp_path / "metadata.jsonl"
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "audio_file.wav", "text": "Audio transcription"}
        """
    )
    with open(audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)
    return str(audio_filename), str(audio_metadata_filename)


@pytest.fixture
def audio_files_with_metadata_that_misses_one_audio(tmp_path, audio_file):
    audio_filename = tmp_path / "audio_file.wav"
    shutil.copyfile(audio_file, audio_filename)
    audio_filename2 = tmp_path / "audio_file2.wav"
    shutil.copyfile(audio_file, audio_filename2)
    audio_metadata_filename = tmp_path / "metadata.jsonl"
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "audio_file.wav", "text": "Audio transcription"}
        """
    )
    with open(audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)
    return str(audio_filename), str(audio_filename2), str(audio_metadata_filename)


@pytest.fixture
def data_files_with_one_split_and_metadata(tmp_path, audio_file):
    data_dir = tmp_path / "audiofolder_data_dir_with_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir = data_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    audio_filename = data_dir / "audio_file.wav"
    shutil.copyfile(audio_file, audio_filename)
    audio_filename2 = data_dir / "audio_file2.wav"
    shutil.copyfile(audio_file, audio_filename2)
    audio_filename3 = subdir / "audio_file3.wav"  # in subdir
    shutil.copyfile(audio_file, audio_filename3)

    audio_metadata_filename = data_dir / "metadata.jsonl"
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "audio_file.wav", "text": "First audio transcription"}
        {"file_name": "audio_file2.wav", "text": "Second audio transcription"}
        {"file_name": "subdir/audio_file3.wav", "text": "Third audio transcription (in subdir)"}
        """
    )
    with open(audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)
    data_files_with_one_split_and_metadata = DataFilesDict.from_local_or_remote(
        get_patterns_locally(str(data_dir)), str(data_dir)
    )
    assert len(data_files_with_one_split_and_metadata) == 1
    assert len(data_files_with_one_split_and_metadata["train"]) == 4
    return data_files_with_one_split_and_metadata


@pytest.fixture
def data_files_with_two_splits_and_metadata(tmp_path, audio_file):
    data_dir = tmp_path / "audiofolder_data_dir_with_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    train_dir = data_dir / "train"
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir = data_dir / "test"
    test_dir.mkdir(parents=True, exist_ok=True)

    audio_filename = train_dir / "audio_file.wav"  # train audio
    shutil.copyfile(audio_file, audio_filename)
    audio_filename2 = train_dir / "audio_file2.wav"  # train audio
    shutil.copyfile(audio_file, audio_filename2)
    audio_filename3 = test_dir / "audio_file3.wav"  # test audio
    shutil.copyfile(audio_file, audio_filename3)

    train_audio_metadata_filename = train_dir / "metadata.jsonl"
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "audio_file.wav", "text": "First train audio transcription"}
        {"file_name": "audio_file2.wav", "text": "Second train audio transcription"}
        """
    )
    with open(train_audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)
    test_audio_metadata_filename = test_dir / "metadata.jsonl"
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "audio_file3.wav", "text": "Test audio transcription"}
        """
    )
    with open(test_audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)
    data_files_with_two_splits_and_metadata = DataFilesDict.from_local_or_remote(
        get_patterns_locally(str(data_dir)), str(data_dir)
    )
    assert len(data_files_with_two_splits_and_metadata) == 2
    assert len(data_files_with_two_splits_and_metadata["train"]) == 3
    assert len(data_files_with_two_splits_and_metadata["test"]) == 2
    return data_files_with_two_splits_and_metadata


@pytest.fixture
def data_files_with_zip_archives(tmp_path, audio_file, second_audio_file):
    data_dir = tmp_path / "audiofolder_data_dir_with_zip_archives"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = data_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    subdir = archive_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    audio_filename = archive_dir / "audio_file.wav"
    shutil.copyfile(audio_file, audio_filename)
    audio_filename2 = subdir / "audio_file2.wav"  # in subdir
    shutil.copyfile(second_audio_file, audio_filename2)
    # make sure they're two different audios
    # Indeed we won't be able to compare the audio filenames, since the archive is not extracted in streaming mode
    # array, sampling_rate = librosa.load(str(audio_filename), sr=16000)
    # sf.write(str(audio_filename2), array, samplerate=16000)

    audio_metadata_filename = archive_dir / "metadata.jsonl"
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "audio_file.wav", "text": "First audio transcription"}
        {"file_name": "subdir/audio_file2.wav", "text": "Second audio transcription (in subdir)"}
        """
    )

    with open(audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)

    shutil.make_archive(str(archive_dir), "zip", archive_dir)
    shutil.rmtree(str(archive_dir))

    data_files_with_zip_archives = DataFilesDict.from_local_or_remote(
        get_patterns_locally(str(data_dir)), str(data_dir)
    )

    assert len(data_files_with_zip_archives) == 1
    assert len(data_files_with_zip_archives["train"]) == 1
    return data_files_with_zip_archives


@require_sndfile
@pytest.mark.parametrize("drop_labels", [True, False])
def test_generate_examples_drop_labels(audio_file, drop_labels):
    audiofolder = AudioFolder(drop_labels=drop_labels)
    generator = audiofolder._generate_examples([(audio_file, audio_file)], None, "train")
    if not drop_labels:
        assert all(
            example.keys() == {"audio", "label"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"audio"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_sndfile
@pytest.mark.parametrize("drop_metadata", [True, False])
def test_generate_examples_drop_metadata(audio_file_with_metadata, drop_metadata):
    audio_file, audio_metadata_file = audio_file_with_metadata
    if not drop_metadata:
        features = Features({"audio": Audio(), "text": Value("string")})
    else:
        features = Features({"audio": Audio()})
    audiofolder = AudioFolder(drop_metadata=drop_metadata, features=features)
    generator = audiofolder._generate_examples(
        [(audio_file, audio_file)], {"train": [(audio_metadata_file, audio_metadata_file)]}, "train"
    )
    if not drop_metadata:
        assert all(
            example.keys() == {"audio", "text"} and all(val is not None for val in example.values())
            for _, example in generator
        )
    else:
        assert all(
            example.keys() == {"audio"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_sndfile
@pytest.mark.parametrize("drop_metadata", [True, False])
def test_generate_examples_with_metadata_in_wrong_location(audio_file, audio_file_with_metadata, drop_metadata):
    _, audio_metadata_file = audio_file_with_metadata
    if not drop_metadata:
        features = Features({"audio": Audio(), "text": Value("string")})
    else:
        features = Features({"audio": Audio()})
    audiofolder = AudioFolder(drop_metadata=drop_metadata, features=features)
    generator = audiofolder._generate_examples(
        [(audio_file, audio_file)], {"train": [(audio_metadata_file, audio_metadata_file)]}, "train"
    )
    if not drop_metadata:
        with pytest.raises(ValueError):
            list(generator)
    else:
        assert all(
            example.keys() == {"audio"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_sndfile
@pytest.mark.parametrize("drop_metadata", [True, False])
def test_generate_examples_with_metadata_that_misses_one_audio(
    audio_files_with_metadata_that_misses_one_audio, drop_metadata
):
    audio_file, audio_file2, audio_metadata_file = audio_files_with_metadata_that_misses_one_audio
    if not drop_metadata:
        features = Features({"audio": Audio(), "text": Value("string")})
    else:
        features = Features({"audio": Audio()})
    audiofolder = AudioFolder(drop_metadata=drop_metadata, features=features)
    generator = audiofolder._generate_examples(
        [(audio_file, audio_file), (audio_file2, audio_file2)],
        {"train": [(audio_metadata_file, audio_metadata_file)]},
        "train",
    )
    if not drop_metadata:
        with pytest.raises(ValueError):
            _ = list(generator)
    else:
        assert all(
            example.keys() == {"audio"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_sndfile
@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize("n_splits", [1, 2])
def test_data_files_with_metadata_and_splits(
    streaming, cache_dir, n_splits, data_files_with_one_split_and_metadata, data_files_with_two_splits_and_metadata
):
    data_files = data_files_with_one_split_and_metadata if n_splits == 1 else data_files_with_two_splits_and_metadata
    audiofolder = AudioFolder(data_files=data_files, cache_dir=cache_dir)
    audiofolder.download_and_prepare()
    datasets = audiofolder.as_streaming_dataset() if streaming else audiofolder.as_dataset()
    for split, data_files in data_files.items():
        expected_num_of_audios = len(data_files) - 1  # don't count the metadata file
        assert split in datasets
        dataset = list(datasets[split])
        assert len(dataset) == expected_num_of_audios
        # make sure each sample has its own audio and metadata
        assert len(set(example["audio"]["path"] for example in dataset)) == expected_num_of_audios
        assert len(set(example["text"] for example in dataset)) == expected_num_of_audios
        assert all(example["text"] is not None for example in dataset)


@require_sndfile
@pytest.mark.parametrize("streaming", [False, True])
def test_data_files_with_metadata_and_archives(streaming, cache_dir, data_files_with_zip_archives):
    if streaming:
        extend_module_for_streaming(AudioFolder.__module__)
    audiofolder = AudioFolder(data_files=data_files_with_zip_archives, cache_dir=cache_dir)
    audiofolder.download_and_prepare()
    datasets = audiofolder.as_streaming_dataset() if streaming else audiofolder.as_dataset()
    for split, data_files in data_files_with_zip_archives.items():
        num_of_archives = len(data_files)  # the metadata file is inside the archive
        expected_num_of_audios = 2 * num_of_archives
        assert split in datasets
        dataset = list(datasets[split])
        assert len(dataset) == expected_num_of_audios
        # make sure each sample has its own audio and metadata, take first 10 numbers in array just in case
        assert len(set([tuple(example["audio"]["array"][:10]) for example in dataset])) == expected_num_of_audios
        assert len(set(example["text"] for example in dataset)) == expected_num_of_audios
        assert all(example["text"] is not None for example in dataset)


@require_sndfile
def test_data_files_with_wrong_metadata_file_name(cache_dir, tmp_path, audio_file):
    data_dir = tmp_path / "data_dir_with_bad_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(audio_file, data_dir / "audio_file.wav")
    audio_metadata_filename = data_dir / "bad_metadata.jsonl"  # bad file
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "audio_file.wav", "text": "Audio transcription"}
        """
    )
    with open(audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)

    data_files_with_bad_metadata = DataFilesDict.from_local_or_remote(
        get_patterns_locally(str(data_dir)), str(data_dir)
    )
    audiofolder = AudioFolder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    audiofolder.download_and_prepare()
    dataset = audiofolder.as_dataset(split="train")
    # check that there are no metadata, since the metadata file name doesn't have the right name
    assert "text" not in dataset.column_names


@require_sndfile
def test_data_files_with_wrong_audio_file_name_column_in_metadata_file(cache_dir, tmp_path, audio_file):
    data_dir = tmp_path / "data_dir_with_bad_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(audio_file, data_dir / "audio_file.wav")
    audio_metadata_filename = data_dir / "metadata.jsonl"
    audio_metadata = textwrap.dedent(  # with bad column "bad_file_name" instead of "file_name"
        """\
        {"bad_file_name_column": "audio_file.wav", "text": "Audio transcription"}
        """
    )
    with open(audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)

    data_files_with_bad_metadata = DataFilesDict.from_local_or_remote(
        get_patterns_locally(str(data_dir)), str(data_dir)
    )
    audiofolder = AudioFolder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    with pytest.raises(ValueError) as exc_info:
        audiofolder.download_and_prepare()
    assert "`file_name` must be present" in str(exc_info.value)
