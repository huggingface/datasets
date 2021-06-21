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
"""AdversarialQA"""


import json
import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{bartolo2020beat,
    author = {Bartolo, Max and Roberts, Alastair and Welbl, Johannes and Riedel, Sebastian and Stenetorp, Pontus},
    title = {Beat the AI: Investigating Adversarial Human Annotation for Reading Comprehension},
    journal = {Transactions of the Association for Computational Linguistics},
    volume = {8},
    number = {},
    pages = {662-678},
    year = {2020},
    doi = {10.1162/tacl_a_00338},
    URL = { https://doi.org/10.1162/tacl_a_00338 },
    eprint = { https://doi.org/10.1162/tacl_a_00338 },
    abstract = { Innovations in annotation methodology have been a catalyst for Reading Comprehension (RC) datasets and models. One recent trend to challenge current RC models is to involve a model in the annotation process: Humans create questions adversarially, such that the model fails to answer them correctly. In this work we investigate this annotation methodology and apply it in three different settings, collecting a total of 36,000 samples with progressively stronger models in the annotation loop. This allows us to explore questions such as the reproducibility of the adversarial effect, transfer from data collected with varying model-in-the-loop strengths, and generalization to data collected without a model. We find that training on adversarially collected samples leads to strong generalization to non-adversarially collected datasets, yet with progressive performance deterioration with increasingly stronger models-in-the-loop. Furthermore, we find that stronger models can still learn from datasets collected with substantially weaker models-in-the-loop. When trained on data collected with a BiDAF model in the loop, RoBERTa achieves 39.9F1 on questions that it cannot answer when trained on SQuAD—only marginally lower than when trained on data collected using RoBERTa itself (41.0F1). }
}
"""

_DESCRIPTION = """\
AdversarialQA is a Reading Comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles using an adversarial model-in-the-loop.
We use three different models; BiDAF (Seo et al., 2016), BERT-Large (Devlin et al., 2018), and RoBERTa-Large (Liu et al., 2019) in the annotation loop and construct three datasets; D(BiDAF), D(BERT), and D(RoBERTa), each with 10,000 training examples, 1,000 validation, and 1,000 test examples.
The adversarial human annotation paradigm ensures that these datasets consist of questions that current state-of-the-art models (at least the ones used as adversaries in the annotation loop) find challenging.
"""

_HOMEPAGE = "https://adversarialqa.github.io/"
_LICENSE = "CC BY-SA 3.0"
_URL = "https://adversarialqa.github.io/data/aqa_v1.0.zip"

_CONFIG_NAME_MAP = {
    "adversarialQA": {
        "dir": "combined",
        "model": "Combined",
    },
    "dbidaf": {
        "dir": "1_dbidaf",
        "model": "BiDAF",
    },
    "dbert": {
        "dir": "2_dbert",
        "model": "BERT-Large",
    },
    "droberta": {
        "dir": "3_droberta",
        "model": "RoBERTa-Large",
    },
}


class AdversarialQA(datasets.GeneratorBasedBuilder):
    """AdversarialQA. Version 1.0.0."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="adversarialQA",
            version=VERSION,
            description="This is the combined AdversarialQA data. " + _DESCRIPTION,
        ),
        datasets.BuilderConfig(
            name="dbidaf",
            version=VERSION,
            description="This is the subset of the data collected using BiDAF (Seo et al., 2016) as a model in the loop. "
            + _DESCRIPTION,
        ),
        datasets.BuilderConfig(
            name="dbert",
            version=VERSION,
            description="This is the subset of the data collected using BERT-Large (Devlin et al., 2018) as a model in the loop. "
            + _DESCRIPTION,
        ),
        datasets.BuilderConfig(
            name="droberta",
            version=VERSION,
            description="This is the subset of the data collected using RoBERTa-Large (Liu et al., 2019) as a model in the loop. "
            + _DESCRIPTION,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                    "metadata": {
                        "split": datasets.Value("string"),
                        "model_in_the_loop": datasets.Value("string"),
                    },
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    @staticmethod
    def _get_filepath(dl_dir, config_name, split):
        return os.path.join(dl_dir, _CONFIG_NAME_MAP[config_name]["dir"], split + ".json")

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": self._get_filepath(dl_dir, self.config.name, "train"),
                    "split": "train",
                    "model_in_the_loop": _CONFIG_NAME_MAP[self.config.name]["model"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": self._get_filepath(dl_dir, self.config.name, "dev"),
                    "split": "validation",
                    "model_in_the_loop": _CONFIG_NAME_MAP[self.config.name]["model"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": self._get_filepath(dl_dir, self.config.name, "test"),
                    "split": "test",
                    "model_in_the_loop": _CONFIG_NAME_MAP[self.config.name]["model"],
                },
            ),
        ]

    def _generate_examples(self, filepath, split, model_in_the_loop):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
            id_ = 0
            for article in squad["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        qid = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # raise BaseException(split, model_in_the_loop)

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": qid,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                            "metadata": {"split": split, "model_in_the_loop": model_in_the_loop},
                        }

                        id_ += 1
