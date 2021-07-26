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
from dataclasses import dataclass

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
        features,
        data_url,
        url,
        supervised_keys=None,
        task_templates=None,
        **kwargs,
    ):
        super().__init__(version=datasets.Version("1.9.0", ""), **kwargs)
        self.features = features
        self.data_url = data_url
        self.url = url
        self.supervised_keys = supervised_keys
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
            url="http://www.openslr.org/12",
            data_url="http://www.openslr.org/resources/12/",
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="text")],
        ),
        SuperbConfig(
            name="sd",
            description=textwrap.dedent(
                """\
            Speaker Diarization (SD) predicts `who is speaking when` for each timestamp, and multiple speakers can
            speak simultaneously. The model has to encode rich speaker characteristics for each frame and should be
            able to represent mixtures of signals. [LibriMix] is adopted where LibriSpeech
            train-clean-100/dev-clean/test-clean are used to generate mixtures for training/validation/testing.
            We focus on the two-speaker scenario as the first step. The time-coded speaker labels were generated using
            alignments from Kaldi LibriSpeech ASR model. The evaluation metric is diarization error rate (DER)."""
            ),
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                }
            ),  # TODO
            supervised_keys=None,  # TODO
            url="https://github.com/ftshijt/LibriMix",
            data_url="https://huggingface.co/datasets/superb/superb-data/resolve/main/sd/{split}/{filename}",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=self.config.features,
            supervised_keys=self.config.supervised_keys,
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
        elif self.config.name == "sd":
            splits = ["train", "dev", "test"]
            _DL_URLS = {
                split: {
                    filename: self.config.data_url.format(split=split, filename=filename)
                    for filename in ["reco2dur", "rttm", "segments", "spk2utt", "utt2spk", "wav.zip"]
                }
                for split in splits
            }
            archive_path = dl_manager.download_and_extract(_DL_URLS)
            return [
                datasets.SplitGenerator(
                    name=datasets.NamedSplit(split), gen_kwargs={"archive_path": archive_path[split]}
                )
                for split in splits
            ]

    def _generate_examples(self, archive_path):
        """Generate examples."""
        if self.config.name == "asr":
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
        elif self.config.name == "sd":
            data = SdData(archive_path)
            args = SdArgs()
            chunk_indices = _generate_chunk_indices(data, args)
            # TODO: if self.mode != "test":
            for key, (rec, st, ed) in enumerate(chunk_indices):
                speakers = _get_speakers(rec, data)
                yield key, {
                    "record_id": rec,
                    "file": data.wavs[rec],
                    "start": st,
                    "end": ed,
                    "speakers": speakers,
                }


class SdData:
    def __init__(self, data_dir):
        """Load sd data."""
        self.segments = self._load_segments_rechash(data_dir["segments"])
        self.utt2spk = self._load_utt2spk(data_dir["utt2spk"])
        self.wavs = self._load_wav_zip(data_dir["wav.zip"])
        self.reco2dur = self._load_reco2dur(data_dir["reco2dur"])
        # self.spk2utt = self._load_spk2utt(data_dir["spk2utt"])

    def _load_segments_rechash(self, segments_file):
        """Load segments file as dict with recid index."""
        ret = {}
        if not os.path.exists(segments_file):
            return None
        for line in open(segments_file):
            utt, rec, st, et = line.strip().split()
            if rec not in ret:
                ret[rec] = []
            ret[rec].append({"utt": utt, "st": float(st), "et": float(et)})
        return ret

    def _load_wav_zip(self, wav_dir):
        """Return dictionary { rec: wav_rxfilename }."""
        return {
            os.path.splitext(filename)[0]: os.path.join(wav_dir, filename) for filename in sorted(os.listdir(wav_dir))
        }

    def _load_utt2spk(self, utt2spk_file):
        """Returns dictionary { uttid: spkid }."""
        lines = [line.strip().split(None, 1) for line in open(utt2spk_file)]
        return {x[0]: x[1] for x in lines}

    def _load_spk2utt(self, spk2utt_file):
        """Returns dictionary { spkid: list of uttids }."""
        if not os.path.exists(spk2utt_file):
            return None
        lines = [line.strip().split() for line in open(spk2utt_file)]
        return {x[0]: x[1:] for x in lines}

    def _load_reco2dur(self, reco2dur_file):
        """Returns dictionary { recid: duration }."""
        if not os.path.exists(reco2dur_file):
            return None
        lines = [line.strip().split(None, 1) for line in open(reco2dur_file)]
        return {x[0]: float(x[1]) for x in lines}


@dataclass
class SdArgs:
    chunk_size: int = 2000
    frame_shift: int = 160
    subsampling: int = 1
    label_delay: int = 0
    num_speakers: int = 2
    rate: int = 16000
    use_last_samples: bool = True


def _generate_chunk_indices(data, args):
    chunk_indices = []
    # make chunk indices: filepath, start_frame, end_frame
    for rec in data.wavs:
        data_len = int(data.reco2dur[rec] * args.rate / args.frame_shift)
        data_len = int(data_len / args.subsampling)
        # TODO: if mode == "test":
        for st, ed in _gen_frame_indices(
            data_len,
            args.chunk_size,
            args.chunk_size,
            args.use_last_samples,
            label_delay=args.label_delay,
            subsampling=args.subsampling,
        ):
            chunk_indices.append((rec, st * args.subsampling, ed * args.subsampling))
    return chunk_indices


def _gen_frame_indices(data_length, size=2000, step=2000, use_last_samples=False, label_delay=0, subsampling=1):
    i = -1
    for i in range(_count_frames(data_length, size, step)):
        yield i * step, i * step + size
    if use_last_samples and i * step + size < data_length:
        if data_length - (i + 1) * step - subsampling * label_delay > 0:
            yield (i + 1) * step, data_length


def _count_frames(data_len, size, step):
    # no padding at edges, last remaining samples are ignored
    return int((data_len - size + step) / step)


def _get_speakers(rec, data):
    return [
        {"start": segment["st"], "end": segment["et"], "speaker_id": data.utt2spk[segment["utt"]]}
        for segment in data.segments[rec]
    ]
