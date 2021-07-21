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
"""SUPERB: Speech processing Universal PERformance Benchmark."""


import glob
import os
import textwrap

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_CITATION = """\
@article{DBLP:journals/corr/abs-2105-01051,
  author    = {Shu{-}Wen Yang and
               Po{-}Han Chi and
               Yung{-}Sung Chuang and
               Cheng{-}I Jeff Lai and
               Kushal Lakhotia and
               Yist Y. Lin and
               Andy T. Liu and
               Jiatong Shi and
               Xuankai Chang and
               Guan{-}Ting Lin and
               Tzu{-}Hsien Huang and
               Wei{-}Cheng Tseng and
               Ko{-}tik Lee and
               Da{-}Rong Liu and
               Zili Huang and
               Shuyan Dong and
               Shang{-}Wen Li and
               Shinji Watanabe and
               Abdelrahman Mohamed and
               Hung{-}yi Lee},
  title     = {{SUPERB:} Speech processing Universal PERformance Benchmark},
  journal   = {CoRR},
  volume    = {abs/2105.01051},
  year      = {2021},
  url       = {https://arxiv.org/abs/2105.01051},
  archivePrefix = {arXiv},
  eprint    = {2105.01051},
  timestamp = {Thu, 01 Jul 2021 13:30:22 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2105-01051.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
Self-supervised learning (SSL) has proven vital for advancing research in
natural language processing (NLP) and computer vision (CV). The paradigm
pretrains a shared model on large volumes of unlabeled data and achieves
state-of-the-art (SOTA) for various tasks with minimal adaptation. However, the
speech processing community lacks a similar setup to systematically explore the
paradigm. To bridge this gap, we introduce Speech processing Universal
PERformance Benchmark (SUPERB). SUPERB is a leaderboard to benchmark the
performance of a shared model across a wide range of speech processing tasks
with minimal architecture changes and labeled data. Among multiple usages of the
shared model, we especially focus on extracting the representation learned from
SSL due to its preferable re-usability. We present a simple framework to solve
SUPERB tasks by learning task-specialized lightweight prediction heads on top of
the frozen shared model. Our results demonstrate that the framework is promising
as SSL representations show competitive generalizability and accessibility
across SUPERB tasks. We release SUPERB as a challenge with a leaderboard and a
benchmark toolkit to fuel the research in representation learning and general
speech processing.

Note that in order to limit the required storage for preparing this dataset, the
audio is stored in the .flac format and is not converted to a float32 array. To
convert, the audio file to a float32 array, please make use of the `.map()`
function as follows:


```python
import soundfile as sf

def map_to_array(batch):
    speech_array, _ = sf.read(batch["file"])
    batch["speech"] = speech_array
    return batch

dataset = dataset.map(map_to_array, remove_columns=["file"])
```
"""


class SuperbConfig(datasets.BuilderConfig):
    """BuilderConfig for Superb."""

    def __init__(
        self,
        data_url,
        url,
        task_templates=None,
        **kwargs,
    ):
        super(SuperbConfig, self).__init__(version=datasets.Version("1.9.0", ""), **kwargs)
        self.data_url = data_url
        self.url = url
        self.task_templates = task_templates


class Superb(datasets.GeneratorBasedBuilder):
    """Superb dataset."""

    BUILDER_CONFIGS = [
        SuperbConfig(
            name="asr",
            description=textwrap.dedent(
                """\
            ASR transcribes utterances into words. While PR analyzes the
            improvement in modeling phonetics, ASR reflects the significance of
            the improvement in a real-world scenario. LibriSpeech
            train-clean-100/dev-clean/test-clean subsets are used for
            training/validation/testing. The evaluation metric is word error
            rate (WER)."""
            ),
            url="http://www.openslr.org/12",
            data_url="http://www.openslr.org/resources/12/",
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="text")],
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "speaker_id": datasets.Value("int64"),
                    "chapter_id": datasets.Value("int64"),
                    "id": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "text"),
            homepage=self.config.url,
            citation=_CITATION,
            task_templates=self.config.task_templates,
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "asr":
            _DL_URLS = {
                "dev": self.config.data_url + "dev-clean.tar.gz",
                "test": self.config.data_url + "test-clean.tar.gz",
                "train": self.config.data_url + "train-clean-100.tar.gz",
            }
            archive_path = dl_manager.download_and_extract(_DL_URLS)

            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"archive_path": archive_path["train"]}),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION, gen_kwargs={"archive_path": archive_path["dev"]}
                ),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"archive_path": archive_path["test"]}),
            ]

    def _generate_examples(self, archive_path):
        """Generate examples."""
        transcripts_glob = os.path.join(archive_path, "LibriSpeech", "*/*/*/*.txt")
        key = 0
        for transcript_path in sorted(glob.glob(transcripts_glob)):
            transcript_dir_path = os.path.dirname(transcript_path)
            with open(transcript_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    id_, transcript = line.split(" ", 1)
                    audio_file = f"{id_}.flac"
                    speaker_id, chapter_id = [int(el) for el in id_.split("-")[:2]]
                    yield key, {
                        "id": id_,
                        "speaker_id": speaker_id,
                        "chapter_id": chapter_id,
                        "file": os.path.join(transcript_dir_path, audio_file),
                        "text": transcript,
                    }
                    key += 1
