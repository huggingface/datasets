"""Korean Dataset for NLI and STS"""

from __future__ import absolute_import, division, print_function

import csv

import pandas as pd

import datasets


_CITATAION = """\
    @article{ham2020kornli,
  title={KorNLI and KorSTS: New Benchmark Datasets for Korean Natural Language Understanding},
  author={Ham, Jiyeon and Choe, Yo Joong and Park, Kyubyong and Choi, Ilji and Soh, Hyungjoon},
  journal={arXiv preprint arXiv:2004.03289},
  year={2020}
}
"""

_DESCRIPTION = """\
    The dataset contains data for bechmarking korean models on NLI and STS
"""

_URL = "https://github.com/kakaobrain/KorNLUDatasets"

_DATA_URLS = {
    "nli": {
        # 'mnli-train': 'https://raw.githubusercontent.com/kakaobrain/KorNLUDatasets/master/KorNLI/multinli.train.ko.tsv',
        "snli-train": "https://raw.githubusercontent.com/kakaobrain/KorNLUDatasets/master/KorNLI/snli_1.0_train.ko.tsv",
        "xnli-dev": "https://raw.githubusercontent.com/kakaobrain/KorNLUDatasets/master/KorNLI/xnli.dev.ko.tsv",
        "xnli-test": "https://raw.githubusercontent.com/kakaobrain/KorNLUDatasets/master/KorNLI/xnli.test.ko.tsv",
    },
    "sts": {
        "train": "https://raw.githubusercontent.com/kakaobrain/KorNLUDatasets/master/KorSTS/sts-train.tsv",
        "dev": "https://raw.githubusercontent.com/kakaobrain/KorNLUDatasets/master/KorSTS/sts-dev.tsv",
        "test": "https://raw.githubusercontent.com/kakaobrain/KorNLUDatasets/master/KorSTS/sts-test.tsv",
    },
}


class KorNluConfig(datasets.BuilderConfig):
    """BuilderConfig for korNLU"""

    def __init__(self, description, data_url, citation, url, **kwargs):
        """
        Args:
            description: `string`, brief description of the dataset
            data_url: `dictionary`, dict with url for each split of data.
            citation: `string`, citation for the dataset.
            url: `string`, url for information about the dataset.
            **kwrags: keyword arguments frowarded to super
        """
        super(KorNluConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.description = description
        self.data_url = data_url
        self.citation = citation
        self.url = url


class KorNlu(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        KorNluConfig(name=name, description=_DESCRIPTION, data_url=_DATA_URLS[name], citation=_CITATAION, url=_URL)
        for name in ["nli", "sts"]
    ]
    BUILDER_CONFIG_CLASS = KorNluConfig

    def _info(self):
        features = {}
        if self.config.name == "nli":
            labels = ["entailment", "neutral", "contradiction"]
            features["premise"] = datasets.Value("string")
            features["hypothesis"] = datasets.Value("string")
            features["label"] = datasets.features.ClassLabel(names=labels)

        if self.config.name == "sts":
            genre = ["main-news", "main-captions", "main-forum", "main-forums"]
            filename = [
                "images",
                "MSRpar",
                "MSRvid",
                "headlines",
                "deft-forum",
                "deft-news",
                "track5.en-en",
                "answers-forums",
                "answer-answer",
            ]
            year = ["2017", "2016", "2013", "2012train", "2014", "2015", "2012test"]

            features["genre"] = datasets.features.ClassLabel(names=genre)
            features["filename"] = datasets.features.ClassLabel(names=filename)
            features["year"] = datasets.features.ClassLabel(names=year)
            features["id"] = datasets.Value("int32")
            features["score"] = datasets.Value("float32")
            features["sentence1"] = datasets.Value("string")
            features["sentence2"] = datasets.Value("string")

        return datasets.DatasetInfo(
            description=_DESCRIPTION, features=datasets.Features(features), homepage=_URL, citation=_CITATAION
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "nli":
            # mnli_train = dl_manager.download_and_extract(self.config.data_url['mnli-train'])
            snli_train = dl_manager.download_and_extract(self.config.data_url["snli-train"])
            xnli_dev = dl_manager.download_and_extract(self.config.data_url["xnli-dev"])
            xnli_test = dl_manager.download_and_extract(self.config.data_url["xnli-test"])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN, gen_kwargs={"filepath": snli_train, "split": "train"}
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION, gen_kwargs={"filepath": xnli_dev, "split": "dev"}
                ),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": xnli_test, "split": "test"}),
            ]

        if self.config.name == "sts":
            train = dl_manager.download_and_extract(self.config.data_url["train"])
            dev = dl_manager.download_and_extract(self.config.data_url["dev"])
            test = dl_manager.download_and_extract(self.config.data_url["test"])

            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train, "split": "train"}),
                datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": dev, "split": "dev"}),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test, "split": "test"}),
            ]

    def _generate_examples(self, filepath, split):
        if self.config.name == "nli":
            df = pd.read_csv(filepath, sep="\t")
            df = df.dropna()
            for id_, row in df.iterrows():
                yield id_, {
                    "premise": str(row["sentence1"]),
                    "hypothesis": str(row["sentence2"]),
                    "label": str(row["gold_label"]),
                }

        if self.config.name == "sts":
            with open(filepath, encoding="utf-8") as f:
                data = csv.DictReader(f, delimiter="\t")
                for id_, row in enumerate(data):
                    yield id_, {
                        "genre": row["genre"],
                        "filename": row["filename"],
                        "year": row["year"],
                        "id": row["id"],
                        "sentence1": row["sentence1"],
                        "sentence2": row["sentence2"],
                        "score": row["score"],
                    }
