# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""The Adversarial NLI Corpus."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@InProceedings{nie2019adversarial,
    title={Adversarial NLI: A New Benchmark for Natural Language Understanding},
    author={Nie, Yixin
                and Williams, Adina
                and Dinan, Emily
                and Bansal, Mohit
                and Weston, Jason
                and Kiela, Douwe},
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    year = "2020",
    publisher = "Association for Computational Linguistics",
}
"""

_DESCRIPTION = """\
The Adversarial Natural Language Inference (ANLI) is a new large-scale NLI benchmark dataset,
The dataset is collected via an iterative, adversarial human-and-model-in-the-loop procedure.
ANLI is much more difficult than its predecessors including SNLI and MNLI.
It contains three rounds. Each round has train/dev/test splits.
"""

stdnli_label = {
    "e": "entailment",
    "n": "neutral",
    "c": "contradiction",
}


class ANLIConfig(datasets.BuilderConfig):
    """BuilderConfig for ANLI."""

    def __init__(self, **kwargs):
        """BuilderConfig for ANLI.

            Args:
        .
              **kwargs: keyword arguments forwarded to super.
        """
        super(ANLIConfig, self).__init__(version=datasets.Version("0.1.0", ""), **kwargs)


class ANLI(datasets.GeneratorBasedBuilder):
    """ANLI: The ANLI Dataset."""

    BUILDER_CONFIGS = [
        ANLIConfig(
            name="plain_text",
            description="Plain text",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "uid": datasets.Value("string"),
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                    "reason": datasets.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://github.com/facebookresearch/anli/",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, filepath):
        for _, ex in self._generate_examples(filepath):
            yield " ".join([ex["premise"], ex["hypothesis"]])

    def _split_generators(self, dl_manager):

        downloaded_dir = dl_manager.download_and_extract("https://dl.fbaipublicfiles.com/anli/anli_v0.1.zip")

        anli_path = os.path.join(downloaded_dir, "anli_v0.1")

        path_dict = dict()
        for round_tag in ["R1", "R2", "R3"]:
            path_dict[round_tag] = dict()
            for split_name in ["train", "dev", "test"]:
                path_dict[round_tag][split_name] = os.path.join(anli_path, round_tag, f"{split_name}.jsonl")

        return [
            # Round 1
            datasets.SplitGenerator(name="train_r1", gen_kwargs={"filepath": path_dict["R1"]["train"]}),
            datasets.SplitGenerator(name="dev_r1", gen_kwargs={"filepath": path_dict["R1"]["dev"]}),
            datasets.SplitGenerator(name="test_r1", gen_kwargs={"filepath": path_dict["R1"]["test"]}),
            # Round 2
            datasets.SplitGenerator(name="train_r2", gen_kwargs={"filepath": path_dict["R2"]["train"]}),
            datasets.SplitGenerator(name="dev_r2", gen_kwargs={"filepath": path_dict["R2"]["dev"]}),
            datasets.SplitGenerator(name="test_r2", gen_kwargs={"filepath": path_dict["R2"]["test"]}),
            # Round 3
            datasets.SplitGenerator(name="train_r3", gen_kwargs={"filepath": path_dict["R3"]["train"]}),
            datasets.SplitGenerator(name="dev_r3", gen_kwargs={"filepath": path_dict["R3"]["dev"]}),
            datasets.SplitGenerator(name="test_r3", gen_kwargs={"filepath": path_dict["R3"]["test"]}),
        ]

    def _generate_examples(self, filepath):
        """Generate mnli examples.

        Args:
          filepath: a string

        Yields:
          dictionaries containing "premise", "hypothesis" and "label" strings
        """
        for idx, line in enumerate(open(filepath, "rb")):
            if line is not None:
                line = line.strip().decode("utf-8")
                item = json.loads(line)

                reason_text = ""
                if "reason" in item:
                    reason_text = item["reason"]

                yield item["uid"], {
                    "uid": item["uid"],
                    "premise": item["context"],
                    "hypothesis": item["hypothesis"],
                    "label": stdnli_label[item["label"]],
                    "reason": reason_text,
                }
