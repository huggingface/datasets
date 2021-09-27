# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""AMI Corpus"""

import os
import xml.etree.ElementTree as ET

import numpy as np

import datasets
from datasets.tasks import AutomaticSpeechRecognition


logger = datasets.logging.get_logger(__name__)

_CITATION = """\

"""

_URL = "https://groups.inf.ed.ac.uk/ami/corpus/"

_DL_URL_ANNOTATIONS = "http://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip"
_DL_SAMPLE_FORMAT = "https://groups.inf.ed.ac.uk/ami/AMICorpusMirror//amicorpus/{}/audio/{}"

_SPEAKERS = ["A", "B", "C", "D", "E"]

# Commented out samples don't seem to exist

_TRAIN_SAMPLE_IDS = [
    "ES2002a",
    "ES2002b",
    "ES2002c",
    "ES2002d",
    "ES2003a",
    "ES2003b",
    "ES2003c",
    "ES2003d",
    "ES2005a",
    "ES2005b",
    "ES2005c",
    "ES2005d",
    "ES2006a",
    "ES2006b",
    "ES2006c",
    "ES2006d",
    "ES2007a",
    "ES2007b",
    "ES2007c",
    "ES2007d",
    "ES2008a",
    "ES2008b",
    "ES2008c",
    "ES2008d",
    "ES2009a",
    "ES2009b",
    "ES2009c",
    "ES2009d",
    "ES2010a",
    "ES2010b",
    "ES2010c",
    "ES2010d",
    "ES2012a",
    "ES2012b",
    "ES2012c",
    "ES2012d",
    "ES2013a",
    "ES2013b",
    "ES2013c",
    "ES2013d",
    "ES2014a",
    "ES2014b",
    "ES2014c",
    "ES2014d",
    "ES2015a",
    "ES2015b",
    "ES2015c",
    "ES2015d",
    "ES2016a",
    "ES2016b",
    "ES2016c",
    "ES2016d",
    "IS1000a",
    "IS1000b",
    "IS1000c",
    "IS1000d",
    "IS1001a",
    "IS1001b",
    "IS1001c",
    "IS1001d",
    "IS1002b",
    "IS1002c",
    "IS1002d",
    "IS1003a",
    "IS1003b",
    "IS1003c",
    "IS1003d",
    "IS1004a",
    "IS1004b",
    "IS1004c",
    "IS1004d",
    "IS1005a",
    "IS1005b",
    "IS1005c",
    "IS1006a",
    "IS1006b",
    "IS1006c",
    "IS1006d",
    "IS1007a",
    "IS1007b",
    "IS1007c",
    "IS1007d",
    "TS3005a",
    "TS3005b",
    "TS3005c",
    "TS3005d",
    "TS3006a",
    "TS3006b",
    "TS3006c",
    "TS3006d",
    "TS3007a",
    "TS3007b",
    "TS3007c",
    "TS3007d",
    "TS3008a",
    "TS3008b",
    "TS3008c",
    "TS3008d",
    "TS3009a",
    "TS3009b",
    "TS3009c",
    "TS3009d",
    "TS3010a",
    "TS3010b",
    "TS3010c",
    "TS3010d",
    "TS3011a",
    "TS3011b",
    "TS3011c",
    "TS3011d",
    "TS3012a",
    "TS3012b",
    "TS3012c",
    "TS3012d",
    "EN2001a",
    "EN2001b",
    "EN2001d",
    "EN2001e",
    "EN2003a",
    "EN2004a",
    "EN2005a",
    "EN2006a",
    "EN2006b",
    "EN2009b",
    "EN2009c",
    "EN2009d",
    "IN1001",
    "IN1002",
    "IN1005",
    "IN1007",
    "IN1008",
    "IN1009",
    "IN1012",
    "IN1013",
    "IN1014",
    "IN1016",
]

_VALIDATION_SAMPLE_IDS = [
    "ES2011a",
    "ES2011b",
    "ES2011c",
    "ES2011d",
    "IS1008a",
    "IS1008b",
    "IS1008c",
    "IS1008d",
    "TS3004a",
    "TS3004b",
    "TS3004c",
    "TS3004d",
    "IB4001",
    "IB4002",
    "IB4003",
    "IB4004",
    "IB4010",
    "IB4011",
]


_EVAL_SAMPLE_IDS = [
    "ES2004a",
    "ES2004b",
    "ES2004c",
    "ES2004d",
    "IS1009a",
    "IS1009b",
    "IS1009c",
    "IS1009d",
    "TS3003a",
    "TS3003b",
    "TS3003c",
    "TS3003d",
    "EN2002a",
    "EN2002b",
    "EN2002c",
    "EN2002d",
]


_DESCRIPTION = """\
The AMI Meeting Corpus consists of 100 hours of meeting recordings. The recordings use a range of signals
synchronized to a common timeline. These include close-talking and far-field microphones, individual and
room-view video cameras, and output from a slide projector and an electronic whiteboard. During the meetings,
the participants also have unsynchronized pens available to them that record what is written. The meetings
were recorded in English using three different rooms with different acoustic properties, and include mostly
non-native speakers.
"""


class AMIConfig(datasets.BuilderConfig):
    """BuilderConfig for LibriSpeechASR."""

    def __init__(self, formats, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        self.dl_path_formats = [_DL_SAMPLE_FORMAT + "." + f + ".wav" for f in formats]
        super(AMIConfig, self).__init__(version=datasets.Version("2.1.0", ""), **kwargs)


class AMI(datasets.GeneratorBasedBuilder):
    """AMI dataset."""

    BUILDER_CONFIGS = [
        AMIConfig(name="headphone-single", formats=["Mix-Headset"], description=""),
        AMIConfig(
            name="headphone-multi", formats=["Headset-0", "Headset-1", "Headset-2", "Headset-3"], description=""
        ),
        AMIConfig(name="microphone-single", formats=["Array1-01"]),
        AMIConfig(
            name="microphone-multi",
            formats=[
                "Array1-01",
                "Array1-02",
                "Array1-03",
                "Array1-04",
                "Array1-05",
                "Array1-06",
                "Array1-07",
                "Array1-08",
                "Array2-01",
                "Array2-02",
                "Array2-03",
                "Array2-04",
                "Array2-05",
                "Array2-06",
                "Array2-07",
                "Array2-08",
            ],
        ),
    ]

    def _info(self):
        features_dict = {
            "word_ids": datasets.Sequence(datasets.Value("string")),
            "word_start_times": datasets.Sequence(datasets.Value("float")),
            "word_end_times": datasets.Sequence(datasets.Value("float")),
            "word_speakers": datasets.Sequence(datasets.Value("string")),
            "segment_ids": datasets.Sequence(datasets.Value("string")),
            "segment_start_times": datasets.Sequence(datasets.Value("float")),
            "segment_end_times": datasets.Sequence(datasets.Value("float")),
            "segment_speakers": datasets.Sequence(datasets.Value("string")),
            "words": datasets.Sequence(datasets.Value("string")),
            "channels": datasets.Sequence(datasets.Value("string")),
        }

        if self.config.name in ["headphone-single", "microphone-single"]:
            features_dict.update({"file": datasets.Value("string")})
            audio_file_path_column = "file"
        elif self.config.name == "headphone-multi":
            features_dict.update(
                {
                    "file-0": datasets.Value("string"),
                    "file-1": datasets.Value("string"),
                    "file-2": datasets.Value("string"),
                    "file-3": datasets.Value("string"),
                }
            )
            audio_file_path_column = "file-0"
        elif self.config.name == "microphone-multi":
            features_dict.update(
                {
                    "file-1-1": datasets.Value("string"),
                    "file-1-2": datasets.Value("string"),
                    "file-1-3": datasets.Value("string"),
                    "file-1-4": datasets.Value("string"),
                    "file-1-5": datasets.Value("string"),
                    "file-1-6": datasets.Value("string"),
                    "file-1-7": datasets.Value("string"),
                    "file-1-8": datasets.Value("string"),
                    "file-2-1": datasets.Value("string"),
                    "file-2-2": datasets.Value("string"),
                    "file-2-3": datasets.Value("string"),
                    "file-2-4": datasets.Value("string"),
                    "file-2-5": datasets.Value("string"),
                    "file-2-6": datasets.Value("string"),
                    "file-2-7": datasets.Value("string"),
                    "file-2-8": datasets.Value("string"),
                }
            )
            audio_file_path_column = "file-1-1"
        else:
            raise ValueError("...")

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features_dict),
            homepage=_URL,
            citation=_CITATION,
            task_templates=[
                AutomaticSpeechRecognition(audio_file_path_column=audio_file_path_column, transcription_column="words")
            ],
        )

    def _split_generators(self, dl_manager):

        # multi-processing doesn't work for AMI
        if dl_manager._download_config.num_proc != 1:
            logger.warning(
                "AMI corpus cannot be downloaded using multi-processing. "
                "Setting number of downloaded processes `num_proc` to 1. "
            )
            dl_manager._download_config.num_proc = 1

        annotation_path = dl_manager.download_and_extract(_DL_URL_ANNOTATIONS)

        # train
        train_path = dl_manager.download_and_extract(
            [path.format(_id, _id) for path in self.config.dl_path_formats for _id in _TRAIN_SAMPLE_IDS]
        )

        # validation
        validation_path = dl_manager.download_and_extract(
            [path.format(_id, _id) for path in self.config.dl_path_formats for _id in _VALIDATION_SAMPLE_IDS]
        )

        # test
        eval_path = dl_manager.download_and_extract(
            [path.format(_id, _id) for path in self.config.dl_path_formats for _id in _EVAL_SAMPLE_IDS]
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"annotation_path": annotation_path, "sample_paths": train_path, "ids": _TRAIN_SAMPLE_IDS},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "annotation_path": annotation_path,
                    "sample_paths": validation_path,
                    "ids": _VALIDATION_SAMPLE_IDS,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"annotation_path": annotation_path, "sample_paths": eval_path, "ids": _EVAL_SAMPLE_IDS},
            ),
        ]

    @staticmethod
    def _sort(key, lists):
        indices = np.argsort(key)

        sorted_lists = [np.array(array)[indices].tolist() for array in lists]
        return sorted_lists

    @staticmethod
    def _extract_words_annotations(paths):
        word_ids = []
        word_start_times = []
        word_end_times = []
        words = []
        word_speakers = []

        for path in paths:
            # retrive speaker
            speaker = path.split(".")[-3]

            with open(path, "r", encoding="utf-8") as words_file:
                root = ET.parse(words_file).getroot()
                for type_tag in root.findall("w"):
                    word_id = type_tag.get("{http://nite.sourceforge.net/}id")

                    word_start_time = type_tag.get("starttime")
                    word_end_time = type_tag.get("endtime")
                    text = type_tag.text

                    if word_start_time is not None and word_end_time is not None:
                        word_ids.append(word_id)
                        word_start_times.append(float(word_start_time))
                        word_end_times.append(float(word_end_time))
                        words.append(text)
                        word_speakers.append(speaker)
                    else:
                        logger.warning(
                            f"Annotation {word_id} of file {path} is missing information about"
                            "either word_start_time or word_end_time. Skipping sample..."
                        )

        return AMI._sort(word_start_times, [word_ids, word_start_times, word_end_times, words, word_speakers])

    @staticmethod
    def _extract_segments_annotations(paths):
        segment_ids = []
        channels = []
        segment_start_times = []
        segment_end_times = []
        segment_speakers = []

        for path in paths:
            speaker = path.split(".")[-3]

            with open(path, "r", encoding="utf-8") as segments_file:
                root = ET.parse(segments_file).getroot()
                for type_tag in root.findall("segment"):
                    segment_ids.append(type_tag.get("{http://nite.sourceforge.net/}id"))
                    segment_start_times.append(float(type_tag.get("transcriber_start")))
                    segment_end_times.append(float(type_tag.get("transcriber_end")))
                    channels.append(type_tag.get("channel"))
                    segment_speakers.append(speaker)

        return AMI._sort(
            segment_start_times, [segment_ids, segment_start_times, segment_end_times, channels, segment_speakers]
        )

    def _generate_examples(self, annotation_path, sample_paths, ids):
        logger.info(f"⏳ Generating {', '.join(ids)}")

        num_audios = len(self.config.dl_path_formats)

        # audio
        sample_paths = {ids[i]: sample_paths[num_audios * i : num_audios * (i + 1)] for i in range(len(ids))}

        # words
        words_paths = {
            _id: [os.path.join(annotation_path, "words/{}.{}.words.xml".format(_id, speaker)) for speaker in _SPEAKERS]
            for _id in ids
        }
        words_paths = {_id: filter(lambda path: os.path.isfile(path), words_paths[_id]) for _id in ids}

        # segments
        segments_paths = {
            _id: [
                os.path.join(annotation_path, "segments/{}.{}.segments.xml".format(_id, speaker))
                for speaker in _SPEAKERS
            ]
            for _id in ids
        }
        segments_paths = {_id: filter(lambda path: os.path.isfile(path), segments_paths[_id]) for _id in ids}

        for _id in words_paths.keys():
            word_ids, word_start_times, word_end_times, words, word_speakers = self._extract_words_annotations(
                words_paths[_id]
            )

            (
                segment_ids,
                segment_start_times,
                segment_end_times,
                channels,
                segment_speakers,
            ) = self._extract_segments_annotations(segments_paths[_id])

            result = {
                "word_ids": word_ids,
                "word_start_times": word_start_times,
                "word_end_times": word_end_times,
                "word_speakers": word_speakers,
                "segment_ids": segment_ids,
                "segment_start_times": segment_start_times,
                "segment_end_times": segment_end_times,
                "segment_speakers": segment_speakers,
                "channels": channels,
                "words": words,
            }

            if self.config.name in ["headphone-single", "microphone-single"]:
                result.update({"file": sample_paths[_id][0]})
            elif self.config.name in ["headphone-multi"]:
                result.update({f"file-{i}": sample_paths[_id][i] for i in range(num_audios)})
            elif self.config.name in ["microphone-multi"]:
                result.update({f"file-{i // 8 + 1}-{i % 8 + 1}": sample_paths[_id][i] for i in range(num_audios)})
            else:
                raise ValueError("...")

            yield _id, result
