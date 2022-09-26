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
"""Swiss-Court-Predict: A Multilingual Legal Judgment Prediction Benchmark"""

import json

import datasets


logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@InProceedings{niklaus-etal-2021-swiss,
  author = {Niklaus, Joel
                and Chalkidis, Ilias
                and Stürmer, Matthias},
  title = {Swiss-Court-Predict: A Multilingual Legal Judgment Prediction Benchmark},
  booktitle = {Proceedings of the 2021 Natural Legal Language Processing Workshop},
  year = {2021},
  location = {Punta Cana, Dominican Republic},
}"""

_DESCRIPTION = """
Swiss-Judgment-Prediction is a multilingual, diachronic dataset of 85K Swiss Federal Supreme Court (FSCS) cases annotated with the respective binarized judgment outcome (approval/dismissal), posing a challenging text classification task. We also provide additional metadata, i.e., the publication year, the legal area and the canton of origin per case, to promote robustness and fairness studies on the critical area of legal NLP.
"""

_ORIGINAL_LANGUAGES = [
    "de",
    "fr",
    "it",
]
_MT_LANGUAGES = [
    "mt_de",
    "mt_fr",
    "mt_it",
    "mt_en",
]
_LANGUAGES = _ORIGINAL_LANGUAGES + _MT_LANGUAGES

_URL = "https://zenodo.org/record/7109926/files/"
_URLS = {
    "train": _URL + "train.jsonl",
    "train_mt": _URL + "train_mt.jsonl",
    "val": _URL + "val.jsonl",
    "test": _URL + "test.jsonl",
}


class SwissJudgmentPredictionConfig(datasets.BuilderConfig):
    """BuilderConfig for SwissJudgmentPrediction."""

    def __init__(self, language: str, languages=None, **kwargs):
        """BuilderConfig for SwissJudgmentPrediction.

        Args:
        language: One of de, fr, it, or all, or all+mt
          **kwargs: keyword arguments forwarded to super.
        """
        super(SwissJudgmentPredictionConfig, self).__init__(**kwargs)
        self.language = language
        if language == "all":
            self.languages = languages if languages is not None else _ORIGINAL_LANGUAGES
        elif language == "all+mt":
            self.languages = languages if languages is not None else _LANGUAGES
        else:
            self.languages = [language]


class SwissJudgmentPrediction(datasets.GeneratorBasedBuilder):
    """SwissJudgmentPrediction: A Multilingual Legal Judgment PredictionBenchmark"""

    VERSION = datasets.Version("2.0.0", "")
    BUILDER_CONFIG_CLASS = SwissJudgmentPredictionConfig
    BUILDER_CONFIGS = [
        SwissJudgmentPredictionConfig(
            name=lang,
            language=lang,
            version=datasets.Version("2.0.0", ""),
            description=f"Plain text import of SwissJudgmentPrediction for the {lang} language",
        )
        for lang in _LANGUAGES
    ] + [
        SwissJudgmentPredictionConfig(
            name="all",
            language="all",
            version=datasets.Version("2.0.0", ""),
            description="Plain text import of SwissJudgmentPrediction for all languages",
        ),
        SwissJudgmentPredictionConfig(
            name="all+mt",
            language="all+mt",
            version=datasets.Version("2.0.0", ""),
            description="Plain text import of SwissJudgmentPrediction for all languages with machine translation",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "year": datasets.Value("int32"),
                "text": datasets.Value("string"),
                "label": datasets.ClassLabel(names=["dismissal", "approval"]),
                "language": datasets.Value("string"),
                "region": datasets.Value("string"),
                "canton": datasets.Value("string"),
                "legal area": datasets.Value("string"),
                "source_language": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/JoelNiklaus/SwissCourtRulingCorpus",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        try:
            dl_dir = dl_manager.download(_URLS)
        except Exception:
            logger.warning(
                "This dataset is downloaded through Zenodo which is flaky. "
                "If this download failed try a few times before reporting an issue"
            )
            raise
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"], "mt_filepath": dl_dir["train_mt"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["val"], "mt_filepath": None},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"], "mt_filepath": None},
            ),
        ]

    def _generate_examples(self, filepath, mt_filepath):
        """This function returns the examples in the raw (text) form."""
        if self.config.language == "all":  # without mt pseudo languages
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    _ = data.setdefault("source_language", "n/a")
                    yield id_, data
        elif self.config.language == "all+mt":  # original languages and mt languages
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    _ = data.setdefault("source_language", "n/a")
                    yield id_, data
            last_id = id_ + 1
            if mt_filepath:  # yield data from mt_filepath
                with open(mt_filepath, encoding="utf-8") as f:
                    for id_, row in enumerate(f):
                        data = json.loads(row)
                        _ = data.setdefault("source_language", "n/a")
                        yield last_id + id_, data
        elif self.config.language in _MT_LANGUAGES:  # mt languages
            if mt_filepath:  # yield data from mt_filepath
                with open(mt_filepath, encoding="utf-8") as f:
                    for id_, row in enumerate(f):
                        data = json.loads(row)
                        _ = data.setdefault("source_language", "n/a")
                        if data["language"] in self.config.language:  # "de" in "mt_de"
                            yield id_, data
        else:  # original languages
            assert self.config.language in _ORIGINAL_LANGUAGES
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    _ = data.setdefault("source_language", "n/a")
                    if data["language"] == self.config.language:
                        yield id_, data
