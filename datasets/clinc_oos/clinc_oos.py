"""An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction"""

from __future__ import absolute_import, division, print_function

import json
import textwrap

import datasets


_CITATION = """\
    @inproceedings{larson-etal-2019-evaluation,
    title = "An Evaluation Dataset for Intent Classification and Out-of-Scope Prediction",
    author = "Larson, Stefan  and
      Mahendran, Anish  and
      Peper, Joseph J.  and
      Clarke, Christopher  and
      Lee, Andrew  and
      Hill, Parker  and
      Kummerfeld, Jonathan K.  and
      Leach, Kevin  and
      Laurenzano, Michael A.  and
      Tang, Lingjia  and
      Mars, Jason",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    year = "2019",
    url = "https://www.aclweb.org/anthology/D19-1131"
}
"""

_DESCRIPTION = """\
    This dataset is for evaluating the performance of intent classification systems in the
    presence of "out-of-scope" queries. By "out-of-scope", we mean queries that do not fall
    into any of the system-supported intent classes. Most datasets include only data that is
    "in-scope". Our dataset includes both in-scope and out-of-scope data. You might also know
    the term "out-of-scope" by other terms, including "out-of-domain" or "out-of-distribution".
"""

_DESCRIPTIONS = {
    "small": textwrap.dedent(
        """\
        Small, in which there are only 50 training queries per each in-scope intent
        """
    ),
    "imbalanced": textwrap.dedent(
        """\
        Imbalanced, in which intents have either 25, 50, 75, or 100 training queries.
        """
    ),
    "plus": textwrap.dedent(
        """\
        OOS+, in which there are 250 out-of-scope training examples, rather than 100.
        """
    ),
}

_URL = "https://github.com/clinc/oos-eval/"

_DATA_URLS = {
    "small": "https://raw.githubusercontent.com/clinc/oos-eval/master/data/data_small.json",
    "imbalanced": "https://raw.githubusercontent.com/clinc/oos-eval/master/data/data_imbalanced.json",
    "plus": "https://raw.githubusercontent.com/clinc/oos-eval/master/data/data_oos_plus.json",
}


class ClincConfig(datasets.BuilderConfig):

    """BuilderConfig for CLINIC150"""

    def __init__(self, description, data_url, citation, url, **kwrags):
        """
        Args:
            description: `string`, brief description of the dataset
            data_url: `dictionary`, dict with url for each split of data.
            citation: `string`, citation for the dataset.
            url: `string`, url for information about the dataset.
            **kwrags: keyword arguments frowarded to super
        """
        super(ClincConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwrags)
        self.description = description
        self.data_url = data_url
        self.citation = citation
        self.url = url


class Clinc150(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        ClincConfig(
            name=name, description=_DESCRIPTIONS[name], data_url=_DATA_URLS[name], citation=_CITATION, url=_URL
        )
        for name in ["small", "imbalanced", "plus"]
    ]

    def _info(self):
        features = {}
        features["text"] = datasets.Value("string")
        features["intent"] = datasets.Value("string")

        return datasets.DatasetInfo(
            description=_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        file_ = dl_manager.download_and_extract(self.config.data_url)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": file_, "split": "train"}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": file_, "split": "val"}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": file_, "split": "test"}),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            j = json.load(f)
            for id_, row in enumerate(j[split] + j["oos_" + split]):
                yield id_, {"text": row[0], "intent": row[1]}
