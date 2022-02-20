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

import csv
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
audio is stored in the .wav format and is not converted to a float32 array. To
convert the audio file to a float32 array, please make use of the `.map()`
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
        url,
        data_url=None,
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
                    "audio": datasets.Audio(sampling_rate=16_000),
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
            name="ks",
            description=textwrap.dedent(
                """\
            Keyword Spotting (KS) detects preregistered keywords by classifying utterances into a predefined set of
            words. The task is usually performed on-device for the fast response time. Thus, accuracy, model size, and
            inference time are all crucial. SUPERB uses the widely used Speech Commands dataset v1.0 for the task.
            The dataset consists of ten classes of keywords, a class for silence, and an unknown class to include the
            false positive. The evaluation metric is accuracy (ACC)"""
            ),
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "label": datasets.ClassLabel(
                        names=[
                            "yes",
                            "no",
                            "up",
                            "down",
                            "left",
                            "right",
                            "on",
                            "off",
                            "stop",
                            "go",
                            "_silence_",
                            "_unknown_",
                        ]
                    ),
                }
            ),
            supervised_keys=("file", "label"),
            url="https://www.tensorflow.org/datasets/catalog/speech_commands",
            data_url="http://download.tensorflow.org/data/{filename}",
        ),
        SuperbConfig(
            name="ic",
            description=textwrap.dedent(
                """\
            Intent Classification (IC) classifies utterances into predefined classes to determine the intent of
            speakers. SUPERB uses the Fluent Speech Commands dataset, where each utterance is tagged with three intent
            labels: action, object, and location. The evaluation metric is accuracy (ACC)."""
            ),
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "speaker_id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "action": datasets.ClassLabel(
                        names=["activate", "bring", "change language", "deactivate", "decrease", "increase"]
                    ),
                    "object": datasets.ClassLabel(
                        names=[
                            "Chinese",
                            "English",
                            "German",
                            "Korean",
                            "heat",
                            "juice",
                            "lamp",
                            "lights",
                            "music",
                            "newspaper",
                            "none",
                            "shoes",
                            "socks",
                            "volume",
                        ]
                    ),
                    "location": datasets.ClassLabel(names=["bedroom", "kitchen", "none", "washroom"]),
                }
            ),
            supervised_keys=None,
            url="https://fluent.ai/fluent-speech-commands-a-dataset-for-spoken-language-understanding-research/",
            data_url="http://fluent.ai:2052/jf8398hf30f0381738rucj3828chfdnchs.tar.gz",
        ),
        SuperbConfig(
            name="si",
            description=textwrap.dedent(
                """\
            Speaker Identification (SI) classifies each utterance for its speaker identity as a multi-class
            classification, where speakers are in the same predefined set for both training and testing. The widely
            used VoxCeleb1 dataset is adopted, and the evaluation metric is accuracy (ACC)."""
            ),
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    # VoxCeleb1 contains 1251 speaker IDs in range ["id10001",..."id11251"]
                    "label": datasets.ClassLabel(names=[f"id{i + 10001}" for i in range(1251)]),
                }
            ),
            supervised_keys=("file", "label"),
            url="https://www.robots.ox.ac.uk/~vgg/data/voxceleb/vox1.html",
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
                    "record_id": datasets.Value("string"),
                    "file": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "start": datasets.Value("int64"),
                    "end": datasets.Value("int64"),
                    "speakers": [
                        {
                            "speaker_id": datasets.Value("string"),
                            "start": datasets.Value("int64"),
                            "end": datasets.Value("int64"),
                        }
                    ],
                }
            ),  # TODO
            supervised_keys=None,  # TODO
            url="https://github.com/ftshijt/LibriMix",
            data_url="https://huggingface.co/datasets/superb/superb-data/resolve/main/sd/{split}/{filename}",
        ),
        SuperbConfig(
            name="er",
            description=textwrap.dedent(
                """\
            Emotion Recognition (ER) predicts an emotion class for each utterance. The most widely used ER dataset
            IEMOCAP is adopted, and we follow the conventional evaluation protocol: we drop the unbalanced emotion
            classes to leave the final four classes with a similar amount of data points and cross-validate on five
            folds of the standard splits. The evaluation metric is accuracy (ACC)."""
            ),
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "label": datasets.ClassLabel(names=["neu", "hap", "ang", "sad"]),
                }
            ),
            supervised_keys=("file", "label"),
            url="https://sail.usc.edu/iemocap/",
        ),
    ]

    @property
    def manual_download_instructions(self):
        if self.config.name == "si":
            return textwrap.dedent(
                """
            Please download the VoxCeleb dataset using the following script,
            which should create `VoxCeleb1/wav/id*` directories for both train and test speakers`:
            ```
            mkdir VoxCeleb1
            cd VoxCeleb1

            wget https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partaa
            wget https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partab
            wget https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partac
            wget https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_dev_wav_partad
            cat vox1_dev* > vox1_dev_wav.zip
            unzip vox1_dev_wav.zip

            wget https://thor.robots.ox.ac.uk/~vgg/data/voxceleb/vox1a/vox1_test_wav.zip
            unzip vox1_test_wav.zip

            # download the official SUPERB train-dev-test split
            wget https://raw.githubusercontent.com/s3prl/s3prl/master/s3prl/downstream/voxceleb1/veri_test_class.txt
            ```"""
            )
        elif self.config.name == "er":
            return textwrap.dedent(
                """
            Please download the IEMOCAP dataset after submitting the request form here:
            https://sail.usc.edu/iemocap/iemocap_release.htm
            Having downloaded the dataset you can extract it with `tar -xvzf IEMOCAP_full_release.tar.gz`
            which should create a folder called `IEMOCAP_full_release`
            """
            )
        return None

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
        elif self.config.name == "ks":
            _DL_URLS = {
                "train_val_test": self.config.data_url.format(filename="speech_commands_v0.01.tar.gz"),
                "test": self.config.data_url.format(filename="speech_commands_test_set_v0.01.tar.gz"),
            }
            archive_path = dl_manager.download_and_extract(_DL_URLS)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"archive_path": archive_path["train_val_test"], "split": "train"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"archive_path": archive_path["train_val_test"], "split": "val"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST, gen_kwargs={"archive_path": archive_path["test"], "split": "test"}
                ),
            ]
        elif self.config.name == "ic":
            archive_path = dl_manager.download_and_extract(self.config.data_url)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"archive_path": archive_path, "split": "train"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"archive_path": archive_path, "split": "valid"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST, gen_kwargs={"archive_path": archive_path, "split": "test"}
                ),
            ]
        elif self.config.name == "si":
            manual_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"archive_path": manual_dir, "split": 1},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"archive_path": manual_dir, "split": 2},
                ),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"archive_path": manual_dir, "split": 3}),
            ]
        elif self.config.name == "sd":
            splits = ["train", "dev", "test"]
            _DL_URLS = {
                split: {
                    filename: self.config.data_url.format(split=split, filename=filename)
                    for filename in ["reco2dur", "segments", "utt2spk", "wav.zip"]
                }
                for split in splits
            }
            archive_path = dl_manager.download_and_extract(_DL_URLS)
            return [
                datasets.SplitGenerator(
                    name=datasets.NamedSplit(split), gen_kwargs={"archive_path": archive_path[split], "split": split}
                )
                for split in splits
            ]
        elif self.config.name == "er":
            manual_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
            return [
                datasets.SplitGenerator(
                    name=f"session{i}",
                    gen_kwargs={"archive_path": manual_dir, "split": i},
                )
                for i in range(1, 6)
            ]

    def _generate_examples(self, archive_path, split=None):
        """Generate examples."""
        if self.config.name == "asr":
            transcripts_glob = os.path.join(archive_path, "LibriSpeech", "*", "*", "*", "*.txt")
            key = 0
            for transcript_path in sorted(glob.glob(transcripts_glob)):
                transcript_dir_path = os.path.dirname(transcript_path)
                with open(transcript_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        id_, transcript = line.split(" ", 1)
                        audio_file = f"{id_}.flac"
                        speaker_id, chapter_id = [int(el) for el in id_.split("-")[:2]]
                        audio_path = os.path.join(transcript_dir_path, audio_file)
                        yield key, {
                            "id": id_,
                            "speaker_id": speaker_id,
                            "chapter_id": chapter_id,
                            "file": audio_path,
                            "audio": audio_path,
                            "text": transcript,
                        }
                        key += 1
        elif self.config.name == "ks":
            words = ["yes", "no", "up", "down", "left", "right", "on", "off", "stop", "go"]
            splits = _split_ks_files(archive_path, split)
            for key, audio_file in enumerate(sorted(splits[split])):
                base_dir, file_name = os.path.split(audio_file)
                _, word = os.path.split(base_dir)
                if word in words:
                    label = word
                elif word == "_silence_" or word == "_background_noise_":
                    label = "_silence_"
                else:
                    label = "_unknown_"
                yield key, {"file": audio_file, "audio": audio_file, "label": label}
        elif self.config.name == "ic":
            root_path = os.path.join(archive_path, "fluent_speech_commands_dataset")
            csv_path = os.path.join(root_path, "data", f"{split}_data.csv")
            with open(csv_path, encoding="utf-8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",", skipinitialspace=True)
                next(csv_reader)
                for row in csv_reader:
                    key, file_path, speaker_id, text, action, object_, location = row
                    audio_path = os.path.join(root_path, file_path)
                    yield key, {
                        "file": audio_path,
                        "audio": audio_path,
                        "speaker_id": speaker_id,
                        "text": text,
                        "action": action,
                        "object": object_,
                        "location": location,
                    }
        elif self.config.name == "si":
            wav_path = os.path.join(archive_path, "wav")
            splits_path = os.path.join(archive_path, "veri_test_class.txt")
            with open(splits_path, "r", encoding="utf-8") as f:
                for key, line in enumerate(f):
                    split_id, file_path = line.strip().split(" ")
                    if int(split_id) != split:
                        continue
                    speaker_id = file_path.split("/")[0]
                    audio_path = os.path.join(wav_path, file_path)
                    yield key, {
                        "file": audio_path,
                        "audio": audio_path,
                        "label": speaker_id,
                    }
        elif self.config.name == "sd":
            data = SdData(archive_path)
            args = SdArgs()
            chunk_indices = _generate_chunk_indices(data, args, split=split)
            if split != "test":
                for key, (rec, st, ed) in enumerate(chunk_indices):
                    speakers = _get_speakers(rec, data, args)
                    yield key, {
                        "record_id": rec,
                        "file": data.wavs[rec],
                        "audio": data.wavs[rec],
                        "start": st,
                        "end": ed,
                        "speakers": speakers,
                    }
            else:
                key = 0
                for rec in chunk_indices:
                    for rec, st, ed in chunk_indices[rec]:
                        speakers = _get_speakers(rec, data, args)
                        yield key, {
                            "record_id": rec,
                            "file": data.wavs[rec],
                            "audio": data.wavs[rec],
                            "start": st,
                            "end": ed,
                            "speakers": speakers,
                        }
                        key += 1
        elif self.config.name == "er":
            root_path = os.path.join(archive_path, f"Session{split}")
            wav_path = os.path.join(root_path, "sentences", "wav")
            labels_path = os.path.join(root_path, "dialog", "EmoEvaluation", "*.txt")
            emotions = ["neu", "hap", "ang", "sad", "exc"]
            key = 0
            for labels_file in sorted(glob.glob(labels_path)):
                with open(labels_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line[0] != "[":
                            continue
                        _, filename, emo, _ = line.split("\t")
                        if emo not in emotions:
                            continue
                        wav_subdir = filename.rsplit("_", 1)[0]
                        filename = f"{filename}.wav"
                        audio_path = os.path.join(wav_path, wav_subdir, filename)
                        yield key, {
                            "file": audio_path,
                            "audio": audio_path,
                            "label": emo.replace("exc", "hap"),
                        }
                        key += 1


class SdData:
    def __init__(self, data_dir):
        """Load sd data."""
        self.segments = self._load_segments_rechash(data_dir["segments"])
        self.utt2spk = self._load_utt2spk(data_dir["utt2spk"])
        self.wavs = self._load_wav_zip(data_dir["wav.zip"])
        self.reco2dur = self._load_reco2dur(data_dir["reco2dur"])

    def _load_segments_rechash(self, segments_file):
        """Load segments file as dict with recid index."""
        ret = {}
        if not os.path.exists(segments_file):
            return None
        with open(segments_file, encoding="utf-8") as f:
            for line in f:
                utt, rec, st, et = line.strip().split()
                if rec not in ret:
                    ret[rec] = []
                ret[rec].append({"utt": utt, "st": float(st), "et": float(et)})
        return ret

    def _load_wav_zip(self, wav_zip):
        """Return dictionary { rec: wav_rxfilename }."""
        wav_dir = os.path.join(wav_zip, "wav")
        return {
            os.path.splitext(filename)[0]: os.path.join(wav_dir, filename) for filename in sorted(os.listdir(wav_dir))
        }

    def _load_utt2spk(self, utt2spk_file):
        """Returns dictionary { uttid: spkid }."""
        with open(utt2spk_file, encoding="utf-8") as f:
            lines = [line.strip().split(None, 1) for line in f]
        return {x[0]: x[1] for x in lines}

    def _load_reco2dur(self, reco2dur_file):
        """Returns dictionary { recid: duration }."""
        if not os.path.exists(reco2dur_file):
            return None
        with open(reco2dur_file, encoding="utf-8") as f:
            lines = [line.strip().split(None, 1) for line in f]
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


def _generate_chunk_indices(data, args, split=None):
    chunk_indices = [] if split != "test" else {}
    # make chunk indices: filepath, start_frame, end_frame
    for rec in data.wavs:
        data_len = int(data.reco2dur[rec] * args.rate / args.frame_shift)
        data_len = int(data_len / args.subsampling)
        if split == "test":
            chunk_indices[rec] = []
        if split != "test":
            for st, ed in _gen_frame_indices(
                data_len,
                args.chunk_size,
                args.chunk_size,
                args.use_last_samples,
                label_delay=args.label_delay,
                subsampling=args.subsampling,
            ):
                chunk_indices.append((rec, st * args.subsampling, ed * args.subsampling))
        else:
            for st, ed in _gen_chunk_indices(data_len, args.chunk_size):
                chunk_indices[rec].append((rec, st * args.subsampling, ed * args.subsampling))
    return chunk_indices


def _count_frames(data_len, size, step):
    # no padding at edges, last remaining samples are ignored
    return int((data_len - size + step) / step)


def _gen_frame_indices(data_length, size=2000, step=2000, use_last_samples=False, label_delay=0, subsampling=1):
    i = -1
    for i in range(_count_frames(data_length, size, step)):
        yield i * step, i * step + size
    if use_last_samples and i * step + size < data_length:
        if data_length - (i + 1) * step - subsampling * label_delay > 0:
            yield (i + 1) * step, data_length


def _gen_chunk_indices(data_len, chunk_size):
    step = chunk_size
    start = 0
    while start < data_len:
        end = min(data_len, start + chunk_size)
        yield start, end
        start += step


def _get_speakers(rec, data, args):
    return [
        {
            "speaker_id": data.utt2spk[segment["utt"]],
            "start": round(segment["st"] * args.rate / args.frame_shift),
            "end": round(segment["et"] * args.rate / args.frame_shift),
        }
        for segment in data.segments[rec]
    ]


def _split_ks_files(archive_path, split):
    audio_path = os.path.join(archive_path, "**", "*.wav")
    audio_paths = glob.glob(audio_path)
    if split == "test":
        # use all available files for the test archive
        return {"test": audio_paths}

    val_list_file = os.path.join(archive_path, "validation_list.txt")
    test_list_file = os.path.join(archive_path, "testing_list.txt")
    with open(val_list_file, encoding="utf-8") as f:
        val_paths = f.read().strip().splitlines()
        val_paths = [os.path.join(archive_path, p) for p in val_paths]
    with open(test_list_file, encoding="utf-8") as f:
        test_paths = f.read().strip().splitlines()
        test_paths = [os.path.join(archive_path, p) for p in test_paths]

    # the paths for the train set is just whichever paths that do not exist in
    # either the test or validation splits
    train_paths = list(set(audio_paths) - set(val_paths) - set(test_paths))

    return {"train": train_paths, "val": val_paths}
