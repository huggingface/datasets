# Load audio data

You can load an audio dataset using the [`Audio`] feature that automatically decodes and resamples the audio files when you access the examples.
Audio decoding is based on the [`soundfile`](https://github.com/bastibe/python-soundfile) python package, which uses the [`libsndfile`](https://github.com/libsndfile/libsndfile) C library under the hood.

## Installation

To work with audio datasets, you need to have the `audio` dependencies installed.
Check out the [installation](./installation#audio) guide to learn how to install it.


## Local files

You can load your own dataset using the paths to your audio files. Use the [`~Dataset.cast_column`] function to take a column of audio file paths, and cast it to the [`Audio`] feature:

```py
>>> audio_dataset = Dataset.from_dict({"audio": ["path/to/audio_1", "path/to/audio_2", ..., "path/to/audio_n"]}).cast_column("audio", Audio())
>>> audio_dataset[0]["audio"]
{'array': array([ 0.        ,  0.00024414, -0.00024414, ..., -0.00024414,
         0.        ,  0.        ], dtype=float32),
 'path': 'path/to/audio_1',
 'sampling_rate': 16000}
```

## AudioFolder

You can also load a dataset with an `AudioFolder` dataset builder. It does not require writing a custom dataloader, making it useful for quickly creating and loading audio datasets with several thousand audio files.

## AudioFolder with metadata

To link your audio files with metadata information, make sure your dataset has a `metadata.csv` file. Your dataset structure might look like:

```
folder/train/metadata.csv
folder/train/first_audio_file.mp3
folder/train/second_audio_file.mp3
folder/train/third_audio_file.mp3
```

Your `metadata.csv` file must have a `file_name` column which links audio files with their metadata. An example `metadata.csv` file might look like:

```text
file_name,transcription
first_audio_file.mp3,znowu się duch z ciałem zrośnie w młodocianej wstaniesz wiosnie i możesz skutkiem tych leków umierać wstawać wiek wieków dalej tam były przestrogi jak siekać głowę jak nogi
second_audio_file.mp3,już u źwierzyńca podwojów król zasiada przy nim książęta i panowie rada a gdzie wzniosły krążył ganek rycerze obok kochanek król skinął palcem zaczęto igrzysko
third_audio_file.mp3,pewnie kędyś w obłędzie ubite minęły szlaki zaczekajmy dzień jaki poślemy szukać wszędzie dziś jutro pewnie będzie posłali wszędzie sługi czekali dzień i drugi gdy nic nie doczekali z płaczem chcą jechać dali
```

`AudioFolder` will load audio data and create a `transcription` column containing texts from `metadata.csv`:

```py
>>> from datasets import load_dataset

>>> dataset = load_dataset("audiofolder", data_dir="/path/to/folder")
>>> # OR by specifying the list of files
>>> dataset = load_dataset("audiofolder", data_files=["path/to/audio_1", "path/to/audio_2", ..., "path/to/audio_n"])
```

You can load remote datasets from their URLs with the data_files parameter:

```py
>>> dataset = load_dataset("audiofolder", data_files=["https://foo.bar/audio_1", "https://foo.bar/audio_2", ..., "https://foo.bar/audio_n"]
>>> # for example, pass SpeechCommands archive:
>>> dataset = load_dataset("audiofolder", data_files="https://s3.amazonaws.com/datasets.huggingface.co/SpeechCommands/v0.01/v0.01_test.tar.gz")
```

Metadata can also be specified as JSON Lines, in which case use `metadata.jsonl` as the name of the metadata file. This format is helpful in scenarios when one of the columns is complex, e.g. a list of floats, to avoid parsing errors or reading the complex values as strings.

To ignore the information in the metadata file, set `drop_metadata=True` in [`load_dataset`]:

```py
>>> from datasets import load_dataset

>>> dataset = load_dataset("audiofolder", data_dir="/path/to/folder", drop_metadata=True)
```

If you don't have a metadata file, `AudioFolder` automatically infers the label name from the directory name.
If you want to drop automatically created labels, set `drop_labels=True`.
In this case, your dataset will only contain an audio column:

```py
>>> from datasets import load_dataset

>>> dataset = load_dataset("audiofolder", data_dir="/path/to/folder_without_metadata", drop_labels=True)
```

<Tip>

For more information about creating your own `AudioFolder` dataset, take a look at the [Create an audio dataset](./audio_dataset) guide.

</Tip>

For a guide on how to load any type of dataset, take a look at the <a class="underline decoration-sky-400 decoration-2 font-semibold" href="./loading">general loading guide</a>.
