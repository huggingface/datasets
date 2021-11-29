# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""WMT20 MLQE Shared task 1."""


import datasets


_CITATION = """
Not available.
"""

_DESCRIPTION = """\
This shared task (part of WMT20) will build on its previous editions
to further examine automatic methods for estimating the quality
of neural machine translation output at run-time, without relying
on reference translations. As in previous years, we cover estimation
at various levels. Important elements introduced this year include: a new
task where sentences are annotated with Direct Assessment (DA)
scores instead of labels based on post-editing; a new multilingual
sentence-level dataset mainly from Wikipedia articles, where the
source articles can be retrieved for document-wide context; the
availability of NMT models to explore system-internal information for the task.

Task 1 uses Wikipedia data for 6 language pairs that includes high-resource
English--German (En-De) and English--Chinese (En-Zh), medium-resource
Romanian--English (Ro-En) and Estonian--English (Et-En), and low-resource
Sinhalese--English (Si-En) and Nepalese--English (Ne-En), as well as a
dataset with a combination of Wikipedia articles and Reddit articles
for Russian-English (En-Ru). The datasets were collected by translating
sentences sampled from source language articles using state-of-the-art NMT
models built using the fairseq toolkit and annotated with Direct Assessment (DA)
scores by professional translators. Each sentence was annotated following the
FLORES setup, which presents a form of DA, where at least three professional
translators rate each sentence from 0-100 according to the perceived translation
quality. DA scores are standardised using the z-score by rater. Participating systems
are required to score sentences according to z-standardised DA scores.
"""

_HOMEPAGE = "http://www.statmt.org/wmt20/quality-estimation-task.html"

_LICENSE = "Unknown"

_LANGUAGE_PAIRS = [("en", "de"), ("en", "zh"), ("et", "en"), ("ne", "en"), ("ro", "en"), ("si", "en"), ("ru", "en")]
_MAIN_URL = "https://github.com/facebookresearch/mlqe/raw/main/data"


def inject_to_link(src_lg, tgt_lg):
    links = {
        "train+dev": f"{_MAIN_URL}/{src_lg}-{tgt_lg}.tar.gz",
        "test": f"{_MAIN_URL}/{src_lg}-{tgt_lg}_test.tar.gz",
    }
    return links


_URLs = {f"{src_lg}-{tgt_lg}": inject_to_link(src_lg, tgt_lg) for (src_lg, tgt_lg) in _LANGUAGE_PAIRS}
_URLs["ru-en"] = {
    "train+dev": "https://www.quest.dcs.shef.ac.uk/wmt20_files_qe/ru-en.tar.gz",
    "test": "https://www.quest.dcs.shef.ac.uk/wmt20_files_qe/ru-en_test.tar.gz",
}


class WmtMlqeConfig(datasets.BuilderConfig):
    def __init__(self, src_lg, tgt_lg, **kwargs):
        super(WmtMlqeConfig, self).__init__(**kwargs)
        self.src_lg = src_lg
        self.tgt_lg = tgt_lg


class Wmt20MlqeTask1(datasets.GeneratorBasedBuilder):
    """WMT MLQE Shared task 1."""

    BUILDER_CONFIGS = [
        WmtMlqeConfig(
            name=f"{src_lg}-{tgt_lg}",
            version=datasets.Version("1.1.0"),
            description=f"Task 1: {src_lg} - {tgt_lg}",
            src_lg=src_lg,
            tgt_lg=tgt_lg,
        )
        for (src_lg, tgt_lg) in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = WmtMlqeConfig

    def _info(self):
        features = datasets.Features(
            {
                "segid": datasets.Value("int32"),
                "translation": datasets.Translation(languages=(self.config.src_lg, self.config.tgt_lg)),
                "scores": datasets.Sequence(datasets.Value("float32")),
                "mean": datasets.Value("float32"),
                "z_scores": datasets.Sequence(datasets.Value("float32")),
                "z_mean": datasets.Value("float32"),
                "model_score": datasets.Value("float32"),
                "doc_id": datasets.Value("string"),
                "nmt_output": datasets.Value("string"),
                "word_probas": datasets.Sequence(datasets.Value("float32")),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": f"{self.config.src_lg}-{self.config.tgt_lg}",
                    "split": "train",
                    "source_lg": self.config.src_lg,
                    "target_lg": self.config.tgt_lg,
                    "files": dl_manager.iter_archive(data_dir["train+dev"]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": f"{self.config.src_lg}-{self.config.tgt_lg}",
                    "split": "test20",
                    "source_lg": self.config.src_lg,
                    "target_lg": self.config.tgt_lg,
                    "files": dl_manager.iter_archive(data_dir["test"]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": f"{self.config.src_lg}-{self.config.tgt_lg}",
                    "split": "dev",
                    "source_lg": self.config.src_lg,
                    "target_lg": self.config.tgt_lg,
                    "files": dl_manager.iter_archive(data_dir["train+dev"]),
                },
            ),
        ]

    def _generate_examples(self, filepath, split, source_lg, target_lg, files):
        """Yields examples."""
        docids_filepath = "/".join([filepath, f"{split}.doc_ids"])
        mt_filepath = "/".join([filepath, "word-probas", f"mt.{split}.{source_lg}{target_lg}"])
        word_probas_filepath = "/".join([filepath, "word-probas", f"word_probas.{split}.{source_lg}{target_lg}"])
        translations_filepath = "/".join([filepath, f"{split}.{source_lg}{target_lg}.df.short.tsv"])

        docids, nmt_outputs, word_probas, translations = None, None, None, None
        for path, f in files:
            if path == docids_filepath:
                docids = f.read().decode("utf-8").splitlines()[1:]
            elif path == mt_filepath:
                nmt_outputs = f.read().decode("utf-8").splitlines()
            elif path == word_probas_filepath:
                word_probas = [seq.split(" ") for seq in f.read().decode("utf-8").splitlines()]
            elif path == translations_filepath:
                translations = [t.split("\t") for t in f.read().decode("utf-8").splitlines()[1:]]
            if all(x is not None for x in [docids, nmt_outputs, word_probas, translations]):
                for id_, (row_, docid_, nmt_out_, word_prob_) in enumerate(
                    zip(translations, docids, nmt_outputs, word_probas)
                ):
                    yield id_, {
                        "segid": row_[0],
                        "translation": {source_lg: row_[1], target_lg: row_[2]},
                        "scores": []
                        if (split == "test20" and (source_lg, target_lg) == ("ru", "en"))
                        else row_[3].strip("][").split(", "),
                        "mean": -10_000 if (split == "test20" and (source_lg, target_lg) == ("ru", "en")) else row_[4],
                        "z_scores": []
                        if (split == "test20" and (source_lg, target_lg) == ("ru", "en"))
                        else row_[5].strip("][").split(", "),
                        "z_mean": -10_000
                        if (split == "test20" and (source_lg, target_lg) == ("ru", "en"))
                        else row_[6],
                        "model_score": -10_000
                        if (split == "test20" and (source_lg, target_lg) == ("ru", "en"))
                        else row_[7],
                        "doc_id": docid_,
                        "nmt_output": nmt_out_,
                        "word_probas": word_prob_,
                    }
                break
