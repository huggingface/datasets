from __future__ import absolute_import, division, print_function

import json
import os
import random

import nlp


random.seed(42)  # This is important, to ensure the same order for concept sets as the official script.

_CITATION = """\
@article{lin2019comgen,
     author = {Bill Yuchen Lin and Ming Shen and Wangchunshu Zhou and Pei Zhou and Chandra Bhagavatula and Yejin Choi and Xiang Ren},
     title = {CommonGen: A Constrained Text Generation Challenge for Generative Commonsense Reasoning},
     journal = {CoRR},
     volume = {abs/1911.03705},
     year = {2019}
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


class CommonGen(nlp.GeneratorBasedBuilder):
    VERSION = nlp.Version("2020.5.30")

    def _info(self):
        features = nlp.Features(
            {
                "concept_set_idx": nlp.Value("int32"),
                "concepts": nlp.Sequence(nlp.Value("string")),
                "target": nlp.Value("string"),
            }
        )
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=nlp.info.SupervisedKeysData(input="concepts", output="target"),
            homepage="https://inklab.usc.edu/CommonGen/index.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(_URL)

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(dl_dir, "commongen.train.jsonl"), "split": "train"},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(dl_dir, "commongen.dev.jsonl"), "split": "dev"},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
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
