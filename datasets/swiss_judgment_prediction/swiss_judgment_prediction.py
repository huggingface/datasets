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

_LANGUAGES = [
    "de",
    "fr",
    "it",
]

_URL = "https://zenodo.org/record/5529712/files/"
_URLS = {
    "train": _URL + "train.jsonl",
    "test": _URL + "test.jsonl",
    "val": _URL + "val.jsonl",
}


class SwissJudgmentPredictionConfig(datasets.BuilderConfig):
    """BuilderConfig for SwissJudgmentPrediction."""

    def __init__(self, language: str, languages=None, **kwargs):
        """BuilderConfig for SwissJudgmentPrediction.

        Args:
        language: One of de,fr,it, or all_languages
          **kwargs: keyword arguments forwarded to super.
        """
        super(SwissJudgmentPredictionConfig, self).__init__(**kwargs)
        self.language = language
        if language != "all_languages":
            self.languages = [language]
        else:
            self.languages = languages if languages is not None else _LANGUAGES


class SwissJudgmentPrediction(datasets.GeneratorBasedBuilder):
    """SwissJudgmentPrediction: A Multilingual Legal Judgment PredictionBenchmark"""

    VERSION = datasets.Version("1.0.0", "")
    BUILDER_CONFIG_CLASS = SwissJudgmentPredictionConfig
    BUILDER_CONFIGS = [
        SwissJudgmentPredictionConfig(
            name=lang,
            language=lang,
            version=datasets.Version("1.0.0", ""),
            description=f"Plain text import of SwissJudgmentPrediction for the {lang} language",
        )
        for lang in _LANGUAGES
    ] + [
        SwissJudgmentPredictionConfig(
            name="all_languages",
            language="all_languages",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of SwissJudgmentPrediction for all languages",
        )
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
        urls_to_dl = _URLS
        try:
            dl_dir = dl_manager.download_and_extract(urls_to_dl)
        except Exception:
            logger.warning(
                "This dataset is downloaded through Zenodo which is flaky. If this download failed try a few times before reporting an issue"
            )
            raise
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["val"], "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """This function returns the examples in the raw (text) form."""

        if self.config.language == "all_languages":
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    yield id_, {
                        "id": data["id"],
                        "year": data["year"],
                        "text": data["text"],
                        "label": data["label"],
                        "language": data["language"],
                        "region": data["region"],
                        "canton": data["canton"],
                        "legal area": data["legal area"],
                    }
        else:
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    if data["language"] == self.config.language:
                        yield id_, {
                            "id": data["id"],
                            "year": data["year"],
                            "text": data["text"],
                            "label": data["label"],
                            "language": data["language"],
                            "region": data["region"],
                            "canton": data["canton"],
                            "legal area": data["legal area"],
                        }
