Process audio data
==================

🤗 Datasets supports an :class:`datasets.Audio` feature, enabling users to load and process raw audio files for training. This guide will show you how to:

* Load your own custom audio dataset.
* Resample audio files.

Installation
------------

The :class:`datasets.Audio` feature is an experimental feature and should be installed as an extra dependency in 🤗 Datasets. Install the :class:`datasets.Audio` feature with pip:

.. code::

    >>> pip install datasets[audio]

Users should also install `torchaudio <https://pytorch.org/audio/stable/index.html>`_ and `librosa <https://librosa.org/doc/latest/index.html>`_, two common libraries used by 🤗 Datasets for handling audio data.

.. code::

    >>> pip install librosa
    >>> pip install torchaudio

.. important::

    torchaudio's ``sox_io`` `backend <https://pytorch.org/audio/stable/backend.html#>`_ supports decoding ``mp3`` files. Unfortunately, the ``sox_io`` backend is only available on Linux/macOS, and is unsupported by Windows.

Then you can load an audio dataset the same way you would load a text dataset. For example, load the `Common Voice <https://huggingface.co/datasets/common_voice>`_ dataset with the Turkish configuration:

.. code-block::

    >>> from datasets import load_dataset, load_metric, Audio
    >>> common_voice = load_dataset("common_voice", "tr", split="train")

Audio datasets
--------------

Audio datasets commonly have a ``path`` and ``audio`` column.

``path`` is an absolute path to an audio file.

.. code::

    >>> common_voice[0]["path"]
    /root/.cache/huggingface/datasets/downloads/extracted/05be0c29807a73c9b099873d2f5975dae6d05e9f7d577458a2466ecb9a2b0c6b/cv-corpus-6.1-2020-12-11/tr/clips/common_voice_tr_21921195.mp3

The ``path`` is useful if you want to load your own audio dataset. In this case, provide a column of audio file paths to :meth:`datasets.Dataset.cast_column`:

.. code::

    >>> my_audio_dataset = my_audio_dataset.cast_column("paths_to_my_audio_files", Audio())

``audio`` is the actual audio file that is loaded and resampled on-the-fly upon calling it.

.. code::

    >>> common_voice[0]["audio"]
    {'array': array([ 0.0000000e+00,  0.0000000e+00,  0.0000000e+00, ...,
        -8.8930130e-05, -3.8027763e-05, -2.9146671e-05], dtype=float32),
    'path': '/root/.cache/huggingface/datasets/downloads/extracted/05be0c29807a73c9b099873d2f5975dae6d05e9f7d577458a2466ecb9a2b0c6b/cv-corpus-6.1-2020-12-11/tr/clips/common_voice_tr_21921195.mp3',
    'sampling_rate': 48000}

When accessing an audio file, the audio file is automatically decoded and resampled. Generally, you should query an audio file like: ``common_voice[0]["audio"]``. If you query an audio file with ``common_voice["audio"][0]`` instead, **all** the audio files in your dataset will be decoded and resampled. This process can take a long time if you have a large dataset.

Resample
--------

Some models expect the audio data to have a certain sampling rate due to how the model was pretrained. For example, the `XLSR-Wav2Vec2 <https://huggingface.co/facebook/wav2vec2-large-xlsr-53>`_ model expects the input to have a sampling rate of 16kHz, but a Common Voice audio file has a sampling rate of 48kHz. Use :meth:`datasets.Dataset.cast_column` to downsample the sampling rate to 16kHz:

.. code::

    >>> common_voice = common_voice.cast_column("audio", Audio(sampling_rate=16_000))

The next time you load the audio file, the :class:`datasets.Audio` feature will load and resample it to 16kHz:

    >>> common_voice_train[0]["audio"]
    {'array': array([ 0.0000000e+00,  0.0000000e+00,  0.0000000e+00, ...,
        -7.4556941e-05, -1.4621433e-05, -5.7861507e-05], dtype=float32),
    'path': '/root/.cache/huggingface/datasets/downloads/extracted/05be0c29807a73c9b099873d2f5975dae6d05e9f7d577458a2466ecb9a2b0c6b/cv-corpus-6.1-2020-12-11/tr/clips/common_voice_tr_21921195.mp3',
    'sampling_rate': 16000}

.. image:: /imgs/resample.gif
   :align: center

Just like text datasets, you can apply a preprocessing function over an entire dataset with :func:`datasets.Dataset.map`, which is useful for resampling all of your audio data at once. Just make sure to include the ``audio`` key when you call :func:`datasets.Dataset.map` so that you are actually resampling the audio data:

.. code-block::

    >>> def prepare_dataset(batch):
    ...     audio = batch["audio"]
    ...     batch["input_values"] = processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
    ...     batch["input_length"] = len(batch["input_values"])
    ...     with processor.as_target_processor():
    ...         batch["labels"] = processor(batch["sentence"]).input_ids
    ...     return batch
    >>> common_voice_train = common_voice_train.map(prepare_dataset, remove_columns=common_voice_train.column_names)