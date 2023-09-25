import shutil
import textwrap

import librosa
import numpy as np
import pytest
import soundfile as sf

from datasets import Audio, ClassLabel, Features, Value
from datasets.data_files import DataFilesDict, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.audiofolder.audiofolder import AudioFolder

from ..utils import require_sndfile


@pytest.fixture
def cache_dir(tmp_path):
    return str(tmp_path / "audiofolder_cache_dir")


@pytest.fixture
def data_files_with_labels_no_metadata(tmp_path, audio_file):
    data_dir = tmp_path / "data_files_with_labels_no_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "fr"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "uk"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    audio_filename = subdir_class_0 / "audio_fr.wav"
    shutil.copyfile(audio_file, audio_filename)
    audio_filename2 = subdir_class_1 / "audio_uk.wav"
    shutil.copyfile(audio_file, audio_filename2)

    data_files_with_labels_no_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )

    return data_files_with_labels_no_metadata


@pytest.fixture
def audio_files_with_labels_and_duplicated_label_key_in_metadata(tmp_path, audio_file):
    data_dir = tmp_path / "audio_files_with_labels_and_label_key_in_metadata"
    data_dir.mkdir(parents=True, exist_ok=True)
    subdir_class_0 = data_dir / "fr"
    subdir_class_0.mkdir(parents=True, exist_ok=True)
    subdir_class_1 = data_dir / "uk"
    subdir_class_1.mkdir(parents=True, exist_ok=True)

    audio_filename = subdir_class_0 / "audio_fr.wav"
    shutil.copyfile(audio_file, audio_filename)
    audio_filename2 = subdir_class_1 / "audio_uk.wav"
    shutil.copyfile(audio_file, audio_filename2)

    audio_metadata_filename = tmp_path / data_dir / "metadata.jsonl"
    audio_metadata = textwrap.dedent(
        """\
        {"file_name": "fr/audio_fr.wav", "text": "Audio in French", "label": "Fr"}
        {"file_name": "uk/audio_uk.wav", "text": "Audio in Ukrainian", "label": "Uk"}
        """
    )
    with open(audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)

    return str(audio_filename), str(audio_filename2), str(audio_metadata_filename)


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
    data_files_with_one_split_and_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )
    assert len(data_files_with_one_split_and_metadata) == 1
    assert len(data_files_with_one_split_and_metadata["train"]) == 4
    return data_files_with_one_split_and_metadata


@pytest.fixture(params=["jsonl", "csv"])
def data_files_with_two_splits_and_metadata(request, tmp_path, audio_file):
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

    train_audio_metadata_filename = train_dir / f"metadata.{request.param}"
    audio_metadata = (
        textwrap.dedent(
            """\
        {"file_name": "audio_file.wav", "text": "First train audio transcription"}
        {"file_name": "audio_file2.wav", "text": "Second train audio transcription"}
        """
        )
        if request.param == "jsonl"
        else textwrap.dedent(
            """\
        file_name,text
        audio_file.wav,First train audio transcription
        audio_file2.wav,Second train audio transcription
        """
        )
    )
    with open(train_audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)
    test_audio_metadata_filename = test_dir / f"metadata.{request.param}"
    audio_metadata = (
        textwrap.dedent(
            """\
        {"file_name": "audio_file3.wav", "text": "Test audio transcription"}
        """
        )
        if request.param == "jsonl"
        else textwrap.dedent(
            """\
        file_name,text
        audio_file3.wav,Test audio transcription
        """
        )
    )
    with open(test_audio_metadata_filename, "w", encoding="utf-8") as f:
        f.write(audio_metadata)
    data_files_with_two_splits_and_metadata = DataFilesDict.from_patterns(
        get_data_patterns(str(data_dir)), data_dir.as_posix()
    )
    assert len(data_files_with_two_splits_and_metadata) == 2
    assert len(data_files_with_two_splits_and_metadata["train"]) == 3
    assert len(data_files_with_two_splits_and_metadata["test"]) == 2
    return data_files_with_two_splits_and_metadata


@pytest.fixture
def data_files_with_zip_archives(tmp_path, audio_file):
    data_dir = tmp_path / "audiofolder_data_dir_with_zip_archives"
    data_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = data_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    subdir = archive_dir / "subdir"
    subdir.mkdir(parents=True, exist_ok=True)

    audio_filename = archive_dir / "audio_file.wav"
    shutil.copyfile(audio_file, audio_filename)
    audio_filename2 = subdir / "audio_file2.wav"  # in subdir
    # make sure they're two different audios
    # Indeed we won't be able to compare the audio filenames, since the archive is not extracted in streaming mode
    array, sampling_rate = librosa.load(str(audio_filename), sr=16000)  # original sampling rate is 44100
    sf.write(str(audio_filename2), array, samplerate=16000)

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

    data_files_with_zip_archives = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())

    assert len(data_files_with_zip_archives) == 1
    assert len(data_files_with_zip_archives["train"]) == 1
    return data_files_with_zip_archives


@require_sndfile
# check that labels are inferred correctly from dir names
def test_generate_examples_with_labels(data_files_with_labels_no_metadata, cache_dir):
    # there are no metadata.jsonl files in this test case
    audiofolder = AudioFolder(data_files=data_files_with_labels_no_metadata, cache_dir=cache_dir, drop_labels=False)
    audiofolder.download_and_prepare()
    assert audiofolder.info.features == Features({"audio": Audio(), "label": ClassLabel(names=["fr", "uk"])})
    dataset = list(audiofolder.as_dataset()["train"])
    label_feature = audiofolder.info.features["label"]

    assert dataset[0]["label"] == label_feature._str2int["fr"]
    assert dataset[1]["label"] == label_feature._str2int["uk"]


@require_sndfile
@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_duplicated_label_key(
    audio_files_with_labels_and_duplicated_label_key_in_metadata, drop_metadata, drop_labels, cache_dir, caplog
):
    fr_audio_file, uk_audio_file, audio_metadata_file = audio_files_with_labels_and_duplicated_label_key_in_metadata
    audiofolder = AudioFolder(
        drop_metadata=drop_metadata,
        drop_labels=drop_labels,
        data_files=[fr_audio_file, uk_audio_file, audio_metadata_file],
        cache_dir=cache_dir,
    )
    if drop_labels is False:
        # infer labels from directories even if metadata files are found
        audiofolder.download_and_prepare()
        warning_in_logs = any("ignoring metadata columns" in record.msg.lower() for record in caplog.records)
        assert warning_in_logs if drop_metadata is not True else not warning_in_logs
        dataset = audiofolder.as_dataset()["train"]
        assert audiofolder.info.features["label"] == ClassLabel(names=["fr", "uk"])
        assert all(example["label"] in audiofolder.info.features["label"]._str2int.values() for example in dataset)
    else:
        audiofolder.download_and_prepare()
        dataset = audiofolder.as_dataset()["train"]
        if drop_metadata is not True:
            # labels are from metadata
            assert audiofolder.info.features["label"] == Value("string")
            assert all(example["label"] in ["Fr", "Uk"] for example in dataset)
        else:
            # drop both labels and metadata
            assert audiofolder.info.features == Features({"audio": Audio()})
            assert all(example.keys() == {"audio"} for example in dataset)


@require_sndfile
@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_labels(data_files_with_labels_no_metadata, drop_metadata, drop_labels):
    audiofolder = AudioFolder(
        drop_metadata=drop_metadata, drop_labels=drop_labels, data_files=data_files_with_labels_no_metadata
    )
    gen_kwargs = audiofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # removing the labels explicitly requires drop_labels=True
    assert gen_kwargs["add_labels"] is not bool(drop_labels)
    assert gen_kwargs["add_metadata"] is False  # metadata files is not present in this case
    generator = audiofolder._generate_examples(**gen_kwargs)
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
@pytest.mark.parametrize("drop_metadata", [None, True, False])
@pytest.mark.parametrize("drop_labels", [None, True, False])
def test_generate_examples_drop_metadata(audio_file_with_metadata, drop_metadata, drop_labels):
    audio_file, audio_metadata_file = audio_file_with_metadata
    audiofolder = AudioFolder(
        drop_metadata=drop_metadata, drop_labels=drop_labels, data_files={"train": [audio_file, audio_metadata_file]}
    )
    gen_kwargs = audiofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    # since the dataset has metadata, removing the metadata explicitly requires drop_metadata=True
    assert gen_kwargs["add_metadata"] is not bool(drop_metadata)
    # since the dataset has metadata, adding the labels explicitly requires drop_labels=False
    assert gen_kwargs["add_labels"] is (drop_labels is False)
    generator = audiofolder._generate_examples(**gen_kwargs)
    expected_columns = {"audio"}
    if gen_kwargs["add_metadata"]:
        expected_columns.add("text")
    if gen_kwargs["add_labels"]:
        expected_columns.add("label")
    result = [example for _, example in generator]
    assert len(result) == 1
    example = result[0]
    assert example.keys() == expected_columns
    for column in expected_columns:
        assert example[column] is not None


@require_sndfile
@pytest.mark.parametrize("drop_metadata", [None, True, False])
def test_generate_examples_with_metadata_in_wrong_location(audio_file, audio_file_with_metadata, drop_metadata):
    _, audio_metadata_file = audio_file_with_metadata
    audiofolder = AudioFolder(drop_metadata=drop_metadata, data_files={"train": [audio_file, audio_metadata_file]})
    gen_kwargs = audiofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = audiofolder._generate_examples(**gen_kwargs)
    if not drop_metadata:
        with pytest.raises(ValueError):
            list(generator)
    else:
        assert all(
            example.keys() == {"audio"} and all(val is not None for val in example.values())
            for _, example in generator
        )


@require_sndfile
@pytest.mark.parametrize("drop_metadata", [None, True, False])
def test_generate_examples_with_metadata_that_misses_one_audio(
    audio_files_with_metadata_that_misses_one_audio, drop_metadata
):
    audio_file, audio_file2, audio_metadata_file = audio_files_with_metadata_that_misses_one_audio
    if not drop_metadata:
        features = Features({"audio": Audio(), "text": Value("string")})
    else:
        features = Features({"audio": Audio()})
    audiofolder = AudioFolder(
        drop_metadata=drop_metadata,
        features=features,
        data_files={"train": [audio_file, audio_file2, audio_metadata_file]},
    )
    gen_kwargs = audiofolder._split_generators(StreamingDownloadManager())[0].gen_kwargs
    generator = audiofolder._generate_examples(**gen_kwargs)
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
def test_data_files_with_metadata_and_single_split(streaming, cache_dir, data_files_with_one_split_and_metadata):
    data_files = data_files_with_one_split_and_metadata
    audiofolder = AudioFolder(data_files=data_files, cache_dir=cache_dir)
    audiofolder.download_and_prepare()
    datasets = audiofolder.as_streaming_dataset() if streaming else audiofolder.as_dataset()
    for split, data_files in data_files.items():
        expected_num_of_audios = len(data_files) - 1  # don't count the metadata file
        assert split in datasets
        dataset = list(datasets[split])
        assert len(dataset) == expected_num_of_audios
        # make sure each sample has its own audio and metadata
        assert len({example["audio"]["path"] for example in dataset}) == expected_num_of_audios
        assert len({example["text"] for example in dataset}) == expected_num_of_audios
        assert all(example["text"] is not None for example in dataset)


@require_sndfile
@pytest.mark.parametrize("streaming", [False, True])
def test_data_files_with_metadata_and_multiple_splits(streaming, cache_dir, data_files_with_two_splits_and_metadata):
    data_files = data_files_with_two_splits_and_metadata
    audiofolder = AudioFolder(data_files=data_files, cache_dir=cache_dir)
    audiofolder.download_and_prepare()
    datasets = audiofolder.as_streaming_dataset() if streaming else audiofolder.as_dataset()
    for split, data_files in data_files.items():
        expected_num_of_audios = len(data_files) - 1  # don't count the metadata file
        assert split in datasets
        dataset = list(datasets[split])
        assert len(dataset) == expected_num_of_audios
        # make sure each sample has its own audio and metadata
        assert len({example["audio"]["path"] for example in dataset}) == expected_num_of_audios
        assert len({example["text"] for example in dataset}) == expected_num_of_audios
        assert all(example["text"] is not None for example in dataset)


@require_sndfile
@pytest.mark.parametrize("streaming", [False, True])
def test_data_files_with_metadata_and_archives(streaming, cache_dir, data_files_with_zip_archives):
    audiofolder = AudioFolder(data_files=data_files_with_zip_archives, cache_dir=cache_dir)
    audiofolder.download_and_prepare()
    datasets = audiofolder.as_streaming_dataset() if streaming else audiofolder.as_dataset()
    for split, data_files in data_files_with_zip_archives.items():
        num_of_archives = len(data_files)  # the metadata file is inside the archive
        expected_num_of_audios = 2 * num_of_archives
        assert split in datasets
        dataset = list(datasets[split])
        assert len(dataset) == expected_num_of_audios
        # make sure each sample has its own audio (all arrays are different) and metadata
        assert (
            sum(np.array_equal(dataset[0]["audio"]["array"], example["audio"]["array"]) for example in dataset[1:])
            == 0
        )
        assert len({example["text"] for example in dataset}) == expected_num_of_audios
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

    data_files_with_bad_metadata = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
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

    data_files_with_bad_metadata = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    audiofolder = AudioFolder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    with pytest.raises(ValueError) as exc_info:
        audiofolder.download_and_prepare()
    assert "`file_name` must be present" in str(exc_info.value)


@require_sndfile
def test_data_files_with_with_metadata_in_different_formats(cache_dir, tmp_path, audio_file):
    data_dir = tmp_path / "data_dir_with_metadata_in_different_format"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(audio_file, data_dir / "audio_file.wav")
    audio_metadata_filename_jsonl = data_dir / "metadata.jsonl"
    audio_metadata_jsonl = textwrap.dedent(
        """\
        {"file_name": "audio_file.wav", "text": "Audio transcription"}
        """
    )
    with open(audio_metadata_filename_jsonl, "w", encoding="utf-8") as f:
        f.write(audio_metadata_jsonl)
    audio_metadata_filename_csv = data_dir / "metadata.csv"
    audio_metadata_csv = textwrap.dedent(
        """\
        file_name,text
        audio_file.wav,Audio transcription
        """
    )
    with open(audio_metadata_filename_csv, "w", encoding="utf-8") as f:
        f.write(audio_metadata_csv)

    data_files_with_bad_metadata = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), data_dir.as_posix())
    audiofolder = AudioFolder(data_files=data_files_with_bad_metadata, cache_dir=cache_dir)
    with pytest.raises(ValueError) as exc_info:
        audiofolder.download_and_prepare()
    assert "metadata files with different extensions" in str(exc_info.value)
