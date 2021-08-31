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

from pathlib import Path
import xml.etree.ElementTree as ET

import datasets
from datasets.tasks import AutomaticSpeechRecognition

logger = datasets.logging.get_logger(__name__)

_CITATION = """\

"""

_DESCRIPTION = """\
The AMI Meeting Corpus consists of 100 hours of meeting recordings. The recordings use a range of signals 
synchronized to a common timeline. These include close-talking and far-field microphones, individual and 
room-view video cameras, and output from a slide projector and an electronic whiteboard. During the meetings, 
the participants also have unsynchronized pens available to them that record what is written. The meetings 
were recorded in English using three different rooms with different acoustic properties, and include mostly 
non-native speakers.
"""
_URL = "https://groups.inf.ed.ac.uk/ami/corpus/"
_DL_URL = "http://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations"

_DL_URLS = {
    "manual": _DL_URL + "/ami_public_manual_1.6.2.zip",
    "auto": _DL_URL + "/ami_public_auto_1.6.2.zip",
}

class AMIConfig(datasets.BuilderConfig):
    """BuilderConfig for LibriSpeechASR."""

    def __init__(self, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        super(AMIConfig, self).__init__(version=datasets.Version("2.1.0", ""), **kwargs)


class AMI(datasets.GeneratorBasedBuilder):
    """AMI dataset."""

    BUILDER_CONFIGS = [
        AMIConfig(name="manual", description="'Manual'"),
        AMIConfig(name="auto", description="'Automatic'"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "word_nite_ids": [datasets.Value("string")],
                    "word_start_times": [datasets.Value("float")],
                    "word_end_times": [datasets.Value("float")],
                    "segment_nite_ids": [datasets.Value("string")],
                    "transcriber_starts": [datasets.Value("float")],
                    "transcriber_ends": [datasets.Value("float")],
                    "texts": [datasets.Value("string")],
                    "channels": [datasets.Value("string")],
                }
            ),
            # supervised_keys=("file", "words"),
            homepage=_URL,
            citation=_CITATION,
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="words")],
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(_DL_URLS[self.config.name])

        train_splits = None
        if self.config.name == "manual":
            train_splits = [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"archive_path": archive_path}),
            ]
        elif self.config.name == "auto":
            train_splits = [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"archive_path": archive_path}),
            ]

        return train_splits

    def _generate_examples(self, archive_path):
        logger.info("⏳ Generating %s", archive_path)

        words_path = Path(archive_path)/"words/ES2002a.A.words.xml"
        segments_path = Path(archive_path)/"segments/ES2002a.A.segments.xml"
        with open(words_path, "r", encoding="utf-8") as words_file:
            root = ET.parse(words_file).getroot()
            word_nite_ids = []
            word_start_times = []
            word_end_times = []
            texts = []
            for type_tag in root.findall('w'):
                nite_id = type_tag.get("{http://nite.sourceforge.net/}id")
                starttime = type_tag.get("starttime")
                endtime = type_tag.get("endtime")
                text = type_tag.text
                print(nite_id, starttime, endtime)
                word_nite_ids.append(nite_id)
                word_start_times.append(starttime)
                word_end_times.append(endtime)
                texts.append(text)


        with open(segments_path, "r", encoding="utf-8") as segments_file:
            root = ET.parse(segments_file).getroot()
            segment_nite_ids = []
            channels = []
            transcriber_starts = []
            transcriber_ends = []
            for type_tag in root.findall('segment'):
                nite_id = type_tag.get("{http://nite.sourceforge.net/}id")
                channel = type_tag.get("channel")
                transcriber_start = type_tag.get("transcriber_start")
                transcriber_end = type_tag.get("transcriber_end")
                print("######### ", nite_id, channel, transcriber_start, transcriber_end)
                segment_nite_ids.append(nite_id)
                transcriber_starts.append(transcriber_start)
                transcriber_ends.append(transcriber_end)
                channels.append(channel)

        # For time being, it return only the record "ES2002a.A"
        for key in range(1):
            yield key, {
                "word_nite_ids": word_nite_ids,
                "word_start_times": word_start_times,
                "word_end_times": word_end_times,
                "segment_nite_ids": segment_nite_ids,
                "transcriber_starts": transcriber_starts,
                "transcriber_ends": transcriber_ends,
                "channels": channels,
                "texts": texts
            }
