"""XOR QA: Cross-lingual Open-Retrieval Question Answering"""

from __future__ import absolute_import, division, print_function

import json
import textwrap

import datasets


_XOR_TYDI_QA_CITATION = """\
    @misc{asai2020xor,
      title={XOR QA: Cross-lingual Open-Retrieval Question Answering},
      author={Akari Asai and Jungo Kasai and Jonathan H. Clark and Kenton Lee and Eunsol Choi and Hannaneh Hajishirzi},
      year={2020},
      eprint={2010.11856},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_XOR_TYDI_QA_DESCRIPTION = """\
    XOR-TyDi QA brings together for the first time information-seeking questions,
    open-retrieval QA, and multilingual QA to create a multilingual open-retrieval
    QA dataset that enables cross-lingual answer retrieval. It consists of questions
    written by information-seeking native speakers in 7 typologically diverse languages
    and answer annotations that are retrieved from multilingual document collections.
    There are three sub-tasks: XOR-Retrieve, XOR-EnglishSpan, and XOR-Full.
"""

_DESCRIPTIONS = {
    "xor-retrieve": textwrap.dedent(
        """\
        XOR-Retrieve is a cross-lingual retrieval task where a question is written in the target
        language (e.g., Japanese) and a system is required to retrieve English document that answers the question.
        """
    ),
    "xor-full": textwrap.dedent(
        """\
        XOR-Full is a cross-lingual retrieval task where a question is written in the target
        language (e.g., Japanese) and a system is required to output a short answer in the target language."""
    ),
}

_DATA_URLS = {
    "xor-retrieve": {
        "train": "https://nlp.cs.washington.edu/xorqa/XORQA_site/data/xor_train_retrieve_eng_span.jsonl",
        "dev": "https://nlp.cs.washington.edu/xorqa/XORQA_site/data/xor_dev_retrieve_eng_span.jsonl",
        "test": "https://nlp.cs.washington.edu/xorqa/XORQA_site/data/xor_test_retrieve_eng_span_q_only.jsonl",
    },
    "xor-full": {
        "train": "https://nlp.cs.washington.edu/xorqa/XORQA_site/data/xor_train_full.jsonl",
        "dev": "https://nlp.cs.washington.edu/xorqa/XORQA_site/data/xor_dev_full.jsonl",
        "test": "https://nlp.cs.washington.edu/xorqa/XORQA_site/data/xor_test_full_q_only.jsonl",
    },
}

_XOR_TYDI_QA_URL = "https://nlp.cs.washington.edu/xorqa/"


class XORTyDiConfig(datasets.BuilderConfig):
    "BuilderConfig for XOR-TyDi Dataset"

    def __init__(self, data_url, citation, url, **kwargs):
        """
        Args:

        data_url: `dictionary`, dict with url for each split of data.
        citation: `string`, citation for the dataset.
        url: `string`, url for information about the dataset.
        **kwargs: keyword arguments forwarded to super.
        """
        super(XORTyDiConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.data_url = data_url
        self.citation = citation
        self.url = url


class XORTyDi(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        XORTyDiConfig(
            name=name,
            description=_DESCRIPTIONS[name],
            data_url=_DATA_URLS[name],
            citation=_XOR_TYDI_QA_CITATION,
            url=_XOR_TYDI_QA_URL,
        )
        for name in ["xor-retrieve", "xor-full"]
    ]

    def _info(self):
        features = {}
        features["question"] = datasets.Value("string")
        features["lang"] = datasets.features.ClassLabel(names=["ar", "bn", "fi", "ja", "ko", "ru", "te"])
        features["answers"] = datasets.Value("string")

        return datasets.DatasetInfo(
            description=_XOR_TYDI_QA_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(features),
            homepage=self.config.url,
            citation=_XOR_TYDI_QA_CITATION,
        )

    def _split_generators(self, dl_manager):
        train = dl_manager.download_and_extract(self.config.data_url["train"])
        dev = dl_manager.download_and_extract(self.config.data_url["dev"])
        test = dl_manager.download_and_extract(self.config.data_url["test"])

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train, "split": "train"}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": dev, "split": "dev"}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test, "split": "test"}),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            jlines = f.read()
            result = [json.loads(jline) for jline in jlines.splitlines()]
            if split == "test":
                for id_, row in enumerate(result):
                    yield id_, {"question": row["question"], "answers": "None", "lang": row["lang"].strip()}
            else:
                for id_, row in enumerate(result):
                    yield id_, {
                        "question": row["question"],
                        "answers": " ".join(row["answers"]),
                        "lang": row["lang"].strip(),
                    }
