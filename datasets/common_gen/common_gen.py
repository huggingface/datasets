import json
import os
import random

import datasets


random.seed(42)  # This is important, to ensure the same order for concept sets as the official script.

_CITATION = """\
@inproceedings{lin-etal-2020-commongen,
    title = "{C}ommon{G}en: A Constrained Text Generation Challenge for Generative Commonsense Reasoning",
    author = "Lin, Bill Yuchen  and
      Zhou, Wangchunshu  and
      Shen, Ming  and
      Zhou, Pei  and
      Bhagavatula, Chandra  and
      Choi, Yejin  and
      Ren, Xiang",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.findings-emnlp.165",
    doi = "10.18653/v1/2020.findings-emnlp.165",
    pages = "1823--1840"
}
"""

_DESCRIPTION = """\
CommonGen is a constrained text generation task, associated with a benchmark dataset,
to explicitly test machines for the ability of generative commonsense reasoning. Given
a set of common concepts; the task is to generate a coherent sentence describing an
everyday scenario using these concepts.

CommonGen is challenging because it inherently requires 1) relational reasoning using
background commonsense knowledge, and 2) compositional generalization ability to work
on unseen concept combinations. Our dataset, constructed through a combination of
crowd-sourcing from AMT and existing caption corpora, consists of 30k concept-sets and
50k sentences in total.
"""
_URL = "https://storage.googleapis.com/huggingface-nlp/datasets/common_gen/commongen_data.zip"


class CommonGen(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("2020.5.30")

    def _info(self):
        features = datasets.Features(
            {
                "concept_set_idx": datasets.Value("int32"),
                "concepts": datasets.Sequence(datasets.Value("string")),
                "target": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=datasets.info.SupervisedKeysData(input="concepts", output="target"),
            homepage="https://inklab.usc.edu/CommonGen/index.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(dl_dir, "commongen.train.jsonl"), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(dl_dir, "commongen.dev.jsonl"), "split": "dev"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(dl_dir, "commongen.test_noref.jsonl"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            id_ = 0
            for idx, row in enumerate(f):
                row = row.replace(", }", "}")  # Fix possible JSON format error
                data = json.loads(row)

                rand_order = [word for word in data["concept_set"].split("#")]
                random.shuffle(rand_order)

                if split == "test":
                    yield idx, {
                        "concept_set_idx": idx,
                        "concepts": rand_order,
                        "target": "",
                    }
                else:
                    for scene in data["scene"]:
                        yield id_, {
                            "concept_set_idx": idx,
                            "concepts": rand_order,
                            "target": scene,
                        }
                        id_ += 1
