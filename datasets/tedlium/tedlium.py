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
import numpy as np


import datasets

from pydub import AudioSegment


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
        @inproceedings{rousseau2012tedlium,
          title={TED-LIUM: an Automatic Speech Recognition dedicated corpus},
          author={Rousseau, Anthony and Del{\\'e}glise, Paul and Est{\\`e}ve, Yannick},
          booktitle={Conference on Language Resources and Evaluation (LREC)},
          pages={125--129},
          year={2012}
        }
        """

_DESCRIPTION = """\
        The TED-LIUM corpus is English-language TED talks, with transcriptions,
        sampled at 16kHz. It contains about 118 hours of speech.

        This is the TED-LIUM corpus release 1.
        """

_HOMEPAGE = "https://www.openslr.org/7/"

_LICENSE = "licensed under Creative Commons BY-NC-ND 3.0 (http://creativecommons.org/licenses/by-nc-nd/3.0/deed.en)"

# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
_URLS = {"release1" : "http://www.openslr.org/resources/7/TEDLIUM_release1.tar.gz"}


class TedLium(datasets.GeneratorBasedBuilder):
    """ The TED-LIUM corpus is English-language TED talks, with transcriptions, sampled at 16kHz. It contains about 118 hours of speech."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="release1", version=VERSION, description="TEDLIUM first release"),
    ]

    DEFAULT_CONFIG_NAME = "release1"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "release1":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features({
                "speech":
                    datasets.features.Audio(sampling_rate=16_000),
                "text":
                    datasets.Value('string'),
                "speaker_id":
                    datasets.Value('string'),
                "gender":
                    datasets.features.ClassLabel(names=["unknown", "female", "male"]),
                "id":
                    datasets.Value('string'),
            })
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            supervised_keys=("speech", "text"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)

        split_paths = [(datasets.Split.TRAIN, os.path.join("TEDLIUM_release1",
                                                           "train")),
                       (datasets.Split.VALIDATION,
                        os.path.join("TEDLIUM_release1", "dev")),
                       (datasets.Split.TEST, os.path.join("TEDLIUM_release1", "test"))]

        splits = []
        for split, path in split_paths:
            kwargs = {"filepath": os.path.join(data_dir, path)}
            splits.append(datasets.SplitGenerator(name=split, gen_kwargs=kwargs))
        return splits

    def _generate_examples(self, filepath):
        """Generate examples from a TED-LIUM stm file."""
        stm_path = os.path.join(filepath, "stm")
        stm_dir = os.path.dirname(stm_path)
        sph_dir = os.path.join(os.path.dirname(stm_dir), "sph")
        with open(stm_path) as f:
            for line in f:
                line = line.strip()
                fn, channel, speaker, start, end, label, transcript = line.split(" ", 6)
                transcript = _maybe_trim_suffix(transcript)

                audio_file = "%s.sph" % fn
                samples = _extract_audio_segment(
                    os.path.join(sph_dir, audio_file), int(channel), float(start),
                    float(end))

                key = "-".join([speaker, start, end, label])
                example = {
                    "speech": samples,
                    "text": transcript,
                    "speaker_id": speaker,
                    "gender": _parse_gender(label),
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


def _extract_audio_segment(sph_path, channel, start_sec, end_sec):
    """Extracts segment of audio samples (as an ndarray) from the given path."""
    with open(sph_path, "rb") as f:
        segment = AudioSegment.from_file(f, format="nistsphere")
    # The dataset only contains mono audio.
    assert segment.channels == 1
    assert channel == 1
    start_ms = int(start_sec * 1000)
    end_ms = int(end_sec * 1000)
    segment = segment[start_ms:end_ms]
    samples = np.array(segment.get_array_of_samples())
    return samples
