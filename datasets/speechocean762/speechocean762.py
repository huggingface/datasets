# Copyright  2020-2022  Xiaomi Corporation (Author: Junbo Zhang)
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

"""
Pronunciation scoring is a crucial technology in computer-assisted language learning (CALL) systems.
The pronunciation quality scores might be given at phoneme-level, word-level, and sentence-level for a typical pronunciation scoring task.
This corpus aims to provide a free public dataset for the pronunciation scoring task.
It is available for free download for both commercial and non-commercial purposes
The speaker variety encompasses young children and adults,
and the manual annotations are in multiple aspects at sentence-level, word-level and phoneme-level.
This corpus consists of 5000 English sentences. All the speakers are non-native, and their mother tongue is Mandarin.
Half of the speakers are Children, and the others are adults. The information on age and gender are provided.
Five experts made the scores. To avoid subjective bias, each expert scores independently under the same metric.
"""

import json
from pathlib import Path

import librosa

import datasets


_CITATION = """\
@inproceedings{DBLP:conf/interspeech/ZhangZWYSHLPW21,
  author    = {Junbo Zhang and
               Zhiwen Zhang and
               Yongqing Wang and
               Zhiyong Yan and
               Qiong Song and
               Yukai Huang and
               Ke Li and
               Daniel Povey and
               Yujun Wang},
  editor    = {Hynek Hermansky and
               Honza Cernock{\'{y}} and
               Luk{\'{a}}s Burget and
               Lori Lamel and
               Odette Scharenborg and
               Petr Motl{\'{i}}cek},
  title     = {speechocean762: An Open-Source Non-Native English Speech Corpus for
               Pronunciation Assessment},
  booktitle = {Interspeech 2021, 22nd Annual Conference of the International Speech
               Communication Association, Brno, Czechia, 30 August - 3 September
               2021},
  pages     = {3710--3714},
  publisher = {{ISCA}},
  year      = {2021},
  url       = {https://doi.org/10.21437/Interspeech.2021-1259},
  doi       = {10.21437/Interspeech.2021-1259},
  timestamp = {Mon, 14 Mar 2022 16:42:12 +0100},
  biburl    = {https://dblp.org/rec/conf/interspeech/ZhangZWYSHLPW21.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
Pronunciation scoring is a crucial technology in computer-assisted language learning (CALL) systems.
The pronunciation quality scores might be given at phoneme-level, word-level, and sentence-level for a typical pronunciation scoring task.
This corpus aims to provide a free public dataset for the pronunciation scoring task.
It is available for free download for both commercial and non-commercial purposes
The speaker variety encompasses young children and adults,
and the manual annotations are in multiple aspects at sentence-level, word-level and phoneme-level.
This corpus consists of 5000 English sentences. All the speakers are non-native, and their mother tongue is Mandarin.
Half of the speakers are Children, and the others are adults. The information on age and gender are provided.
Five experts made the scores. To avoid subjective bias, each expert scores independently under the same metric.
"""

_HOMEPAGE = "https://www.openslr.org/101/"

_LICENSE = "Attribution 4.0 International (CC BY 4.0)"

_DL_URL = "https://github.com/jimbozhang/speechocean762/releases/download/v1.2.0/speechocean762.tar.gz"

_SAMPLE_RATE = 16_000


class Speechocean762(datasets.GeneratorBasedBuilder):
    """
    Pronunciation scoring is a crucial technology in computer-assisted language learning (CALL) systems.
    The pronunciation quality scores might be given at phoneme-level, word-level, and sentence-level for a typical pronunciation scoring task.
    This corpus aims to provide a free public dataset for the pronunciation scoring task.
    It is available for free download for both commercial and non-commercial purposes
    The speaker variety encompasses young children and adults,
    and the manual annotations are in multiple aspects at sentence-level, word-level and phoneme-level.
    This corpus consists of 5000 English sentences. All the speakers are non-native, and their mother tongue is Mandarin.
    Half of the speakers are Children, and the others are adults. The information on age and gender are provided.
    Five experts made the scores. To avoid subjective bias, each expert scores independently under the same metric.
    """

    VERSION = datasets.Version("1.2.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "speaker": datasets.Value("string"),
                "age": datasets.Value("int32"),
                "gender": datasets.Value("string"),
                "text": datasets.Value("string"),
                "audio": datasets.Audio(sampling_rate=_SAMPLE_RATE),
                "accuracy": datasets.Value("float32"),
                "completeness": datasets.Value("float32"),
                "fluency": datasets.Value("float32"),
                "prosodic": datasets.Value("float32"),
                "total": datasets.Value("float32"),
                "words": datasets.Sequence(
                    {
                        "text": datasets.Value("string"),
                        "accuracy": datasets.Value("float32"),
                        "stress": datasets.Value("float32"),
                        "total": datasets.Value("float32"),
                        "phones": datasets.Sequence(datasets.Value("string")),
                        "phones-accuracy": datasets.Sequence(datasets.Value("float32")),
                        "mispronunciations": datasets.Sequence(
                            {
                                "index": datasets.Value("int32"),
                                "canonical-phone": datasets.Value("string"),
                                "pronounced-phone": datasets.Value("string"),
                            }
                        ),
                    }
                ),
                "original_full_path": datasets.Value("string"),  # relative path to full audio in original data dirs
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download(_DL_URL)
        local_extracted_archive = dl_manager.extract(archive_path) if not dl_manager.is_streaming else {}

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"local_extracted_archive": local_extracted_archive, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"local_extracted_archive": local_extracted_archive, "split": "test"},
            ),
        ]

    def _generate_examples(self, local_extracted_archive, split):
        root_path = Path(local_extracted_archive) / "speechocean762"
        meta_path = root_path / f"{split}.json"

        with open(meta_path) as f:
            info = json.load(f)
            for utt_id in info:
                audio = info[utt_id]
                audio["id"] = utt_id
                audio["original_full_path"] = f"{root_path}/WAVE/SPEAKER{audio['speaker']}/{utt_id}.WAV"
                audio_data, _ = librosa.load(audio["original_full_path"], sr=_SAMPLE_RATE)
                audio["audio"] = {"path": audio["original_full_path"], "bytes": audio_data.tobytes()}

                yield utt_id, audio
