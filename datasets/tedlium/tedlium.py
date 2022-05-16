# Copyright 2022 The HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TED-LIUM speech recognition dataset."""

import os
import re
from pathlib import Path

import numpy as np
import soundfile as sf

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_LICENSE = "licensed under Creative Commons BY-NC-ND 3.0 (http://creativecommons.org/licenses/by-nc-nd/3.0/deed.en)"


class TedliumReleaseConfig(datasets.BuilderConfig):
    """BuilderConfig for a release of the TED-LIUM dataset."""

    def __init__(self, *, url, download_url, split_paths, citation, **kwargs):
        super(TedliumReleaseConfig, self).__init__(version=datasets.Version("1.0.1"), **kwargs)
        self.url = url
        self.download_url = download_url
        # List of split, path pairs containing the relative path within the
        # extracted tarball to the data for each split.
        self.split_paths = split_paths
        self.citation = citation


def _make_builder_configs():
    """Creates builder configs for all supported Tedlium dataset releases."""
    release1 = TedliumReleaseConfig(
        name="release1",
        description="""\
        The TED-LIUM corpus is English-language TED talks, with transcriptions,
        sampled at 16kHz. It contains about 118 hours of speech.

        This is the TED-LIUM corpus release 1,
        licensed under Creative Commons BY-NC-ND 3.0
        (http://creativecommons.org/licenses/by-nc-nd/3.0/deed.en).
        """,
        citation="""\
        @inproceedings{rousseau2012tedlium,
          title={TED-LIUM: an Automatic Speech Recognition dedicated corpus},
          author={Rousseau, Anthony and Del{\\'e}glise, Paul and Est{\\`e}ve, Yannick},
          booktitle={Conference on Language Resources and Evaluation (LREC)},
          pages={125--129},
          year={2012}
        }
        """,
        url="https://www.openslr.org/7/",
        download_url="http://www.openslr.org/resources/7/TEDLIUM_release1.tar.gz",
        split_paths=[
            (datasets.Split.TRAIN, os.path.join("TEDLIUM_release1", "train")),
            (datasets.Split.VALIDATION, os.path.join("TEDLIUM_release1", "dev")),
            (datasets.Split.TEST, os.path.join("TEDLIUM_release1", "test")),
        ],
    )

    release2 = TedliumReleaseConfig(
        name="release2",
        description="""\
        This is the TED-LIUM corpus release 2,
        licensed under Creative Commons BY-NC-ND 3.0
        (http://creativecommons.org/licenses/by-nc-nd/3.0/deed.en).

        All talks and text are property of TED Conferences LLC.

        The TED-LIUM corpus was made from audio talks and their transcriptions
        available on the TED website. We have prepared and filtered these data
        in order to train acoustic models to participate to the International
        Workshop on Spoken Language Translation 2011 (the LIUM English/French
        SLT system reached the first rank in the SLT task).

        Contains 1495 talks and transcripts.
        """,
        citation="""\
        @inproceedings{rousseau2014tedlium2,
          title={Enhancing the {TED-LIUM} Corpus with Selected Data for Language Modeling and More {TED} Talks},
          author={Rousseau, Anthony and Del{\\'e}glise, Paul and Est{\\`e}ve, Yannick},
          booktitle={Conference on Language Resources and Evaluation (LREC)},
          year={2014}
        }
        """,
        url="https://www.openslr.org/19/",
        download_url="http://www.openslr.org/resources/19/TEDLIUM_release2.tar.gz",
        split_paths=[
            (datasets.Split.TRAIN, os.path.join("TEDLIUM_release2", "train")),
            (datasets.Split.VALIDATION, os.path.join("TEDLIUM_release2", "dev")),
            (datasets.Split.TEST, os.path.join("TEDLIUM_release2", "test")),
        ],
    )

    release3 = TedliumReleaseConfig(
        name="release3",
        description="""\
        This is the TED-LIUM corpus release 3, licensed under Creative Commons
        BY-NC-ND 3.0.

        All talks and text are property of TED Conferences LLC.

        This new TED-LIUM release was made through a collaboration between the
        Ubiqus company and the LIUM (University of Le Mans, France)

        Contents:

        - 2351 audio talks in NIST sphere format (SPH), including talks from
          TED-LIUM 2: be careful, same talks but not same audio files (only
          these audio file must be used with the TED-LIUM 3 STM files)
        - 452 hours of audio
        - 2351 aligned automatic transcripts in STM format
        - TEDLIUM 2 dev and test data: 19 TED talks in SPH format with
          corresponding manual transcriptions (cf. 'legacy' distribution below).
        - Dictionary with pronunciations (159848 entries), same file as the one
          included in TED-LIUM 2
        - Selected monolingual data for language modeling from WMT12 publicly
          available corpora: these files come from the TED-LIUM 2 release, but
          have been modified to get a tokenization more relevant for English
          language

        Two corpus distributions:
        - the legacy one, on which the dev and test datasets are the same as in
          TED-LIUM 2 (and TED-LIUM 1).
        - the 'speaker adaptation' one, especially designed for experiments on
          speaker adaptation.
        """,
        citation="""\
        @inproceedings{hernandez2018tedlium3,
          title={TED-LIUM 3: twice as much data and corpus repartition for experiments on speaker adaptation},
          author={Hernandez, Fran{\\c{c}}ois and Nguyen, Vincent and Ghannay, Sahar and Tomashenko, Natalia and Est{\\`e}ve, Yannick},
          booktitle={International Conference on Speech and Computer},
          pages={198--208},
          year={2018},
          organization={Springer}
        }
        """,
        url="https://www.openslr.org/51/",
        download_url="http://www.openslr.org/resources/51/TEDLIUM_release-3.tgz",
        split_paths=[
            (datasets.Split.VALIDATION, os.path.join("TEDLIUM_release-3", "legacy", "dev")),
            (datasets.Split.TEST, os.path.join("TEDLIUM_release-3", "legacy", "test")),
            # The legacy/train directory contains symlinks to "data",
            # which are skipped by extraction (see above).
            # Work around this by manually dereferencing the links here.
            (datasets.Split.TRAIN, os.path.join("TEDLIUM_release-3", "data")),
        ],
    )

    return [release1, release2, release3]


class TedLium(datasets.GeneratorBasedBuilder):
    """The TED-LIUM corpus is English-language TED talks, with transcriptions, sampled at 16kHz. It contains about 118 hours of speech."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = _make_builder_configs()

    def _info(self):
        features = datasets.Features(
            {
                "audio": datasets.features.Audio(sampling_rate=16_000),
                "text": datasets.Value("string"),
                "speaker_id": datasets.Value("string"),
                "gender": datasets.features.ClassLabel(names=["unknown", "female", "male"]),
                "file": datasets.Value("string"),
                "id": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=self.config.description,
            features=features,
            supervised_keys=("audio", "text"),
            homepage=self.config.url,
            license=_LICENSE,
            citation=self.config.citation,
            task_templates=[AutomaticSpeechRecognition(audio_column="audio", transcription_column="text")],
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(self.config.download_url)
        splits = []
        for split, path in self.config.split_paths:
            kwargs = {"filepath": os.path.join(data_dir, path)}
            splits.append(datasets.SplitGenerator(name=split, gen_kwargs=kwargs))
        return splits

    def _generate_examples(self, filepath):
        """Generate examples from a TED-LIUM stm file."""
        # The stm directory houses the speaker and transcription information in .stm format
        stm_dir = os.path.join(filepath, "stm")
        # The sph directory houses the audio files in .sph format
        sph_dir = os.path.join(filepath, "sph")
        stm_files = [os.path.join(stm_dir, f) for f in os.listdir(stm_dir) if f.endswith(".stm")]
        for file in stm_files:
            # the .sph speaker file almost always has the same file name as the .stm file
            speaker_file = Path(file).stem
            audio_file = os.path.join(sph_dir, speaker_file + ".sph")
            segment, sampling_rate = sf.read(audio_file, dtype=np.int16)
            with open(file) as f:
                for line in f:
                    line = line.strip()
                    fn, channel, speaker, start, end, label, transcript = line.split(" ", 6)
                    transcript = _maybe_trim_suffix(transcript)
                    if speaker_file != fn:
                        # handle the case where the stm file does not have the same file name as the transcript
                        speaker_file = fn
                        segment, sampling_rate = sf.read(audio_file, dtype=np.int16)
                    samples = _extract_audio_segment(segment, int(channel), float(start), float(end))

                    key = "-".join([speaker, start, end, label])
                    example = {
                        "audio": {"path": file, "array": samples, "sampling_rate": sampling_rate},
                        "text": transcript,
                        "speaker_id": speaker,
                        "gender": _parse_gender(label),
                        "file": file,
                        "id": key,
                    }
                    yield key, example


def _maybe_trim_suffix(transcript):
    # stm files for the TEDLIUM release 1 train split contain a key (enclosed in
    # parens) at the end.
    splits = transcript.rsplit(" ", 1)
    transcript = splits[0]
    if len(splits) > 1:
        suffix = splits[-1]
        if not suffix.startswith("("):
            transcript += " " + suffix
    return transcript


def _extract_audio_segment(segment, channel, start_sec, end_sec):
    """Extracts segment of audio samples (as an ndarray) from the given segment."""
    # The dataset only contains mono audio.
    assert channel == 1
    start_ms = int(start_sec * 1000)
    end_ms = int(end_sec * 1000)
    samples = segment[start_ms:end_ms]
    return samples


def _parse_gender(label_str):
    """Parse gender string from STM "<label>" field."""
    gender = re.split(",|_", label_str)[-1][:-1]
    # Fix inconsistencies in the data.
    if not gender:
        gender = -1  # Missing label.
    elif gender == "<NA":  # In TEDLIUM release 3 training data.
        gender = -1  # Missing label.
    elif gender == "F":
        gender = "female"
    elif gender == "M":
        gender = "male"
    return gender
