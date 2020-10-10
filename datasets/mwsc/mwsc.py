"""A modification of the Winograd Schema Challenge to ensure answers are a single context word"""
from __future__ import absolute_import, division, print_function

import os
import re

import datasets


_CITATION = """\
@article{McCann2018decaNLP,
  title={The Natural Language Decathlon: Multitask Learning as Question Answering},
  author={Bryan McCann and Nitish Shirish Keskar and Caiming Xiong and Richard Socher},
  journal={arXiv preprint arXiv:1806.08730},
  year={2018}
}
"""

_DESCRIPTION = """\
Examples taken from the Winograd Schema Challenge modified to ensure that answers are a single word from the context.
This modified Winograd Schema Challenge (MWSC) ensures that scores are neither inflated nor deflated by oddities in phrasing.
"""

_DATA_URL = "https://raw.githubusercontent.com/salesforce/decaNLP/1e9605f246b9e05199b28bde2a2093bc49feeeaa/local_data/schema.txt"
# Alternate: https://s3.amazonaws.com/research.metamind.io/decaNLP/data/schema.txt


class MWSC(datasets.GeneratorBasedBuilder):
    """MWSC: modified Winograd Schema Challenge"""

    VERSION = datasets.Version("0.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "options": datasets.features.Sequence(datasets.Value("string")),
                    "answer": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://decanlp.com",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        schemas_file = dl_manager.download_and_extract(_DATA_URL)

        if os.path.isdir(schemas_file):
            # During testing the download manager mock gives us a directory
            schemas_file = os.path.join(schemas_file, "schema.txt")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": schemas_file, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": schemas_file, "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": schemas_file, "split": "dev"},
            ),
        ]

    def _get_both_schema(self, context):
        """Split [option1/option2] into 2 sentences.
        From https://github.com/salesforce/decaNLP/blob/1e9605f246b9e05199b28bde2a2093bc49feeeaa/text/torchtext/datasets/generic.py#L815-L827"""
        pattern = r"\[.*\]"
        variations = [x[1:-1].split("/") for x in re.findall(pattern, context)]
        splits = re.split(pattern, context)
        results = []
        for which_schema in range(2):
            vs = [v[which_schema] for v in variations]
            context = ""
            for idx in range(len(splits)):
                context += splits[idx]
                if idx < len(vs):
                    context += vs[idx]
            results.append(context)
        return results

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        schemas = []
        with open(filepath, encoding="utf-8") as schema_file:
            schema = []
            for line in schema_file:
                if len(line.split()) == 0:
                    schemas.append(schema)
                    schema = []
                    continue
                else:
                    schema.append(line.strip())

        # Train/test/dev split from decaNLP code
        splits = {}
        traindev = schemas[:-50]
        splits["test"] = schemas[-50:]
        splits["train"] = traindev[:40]
        splits["dev"] = traindev[40:]

        idx = 0
        for schema in splits[split]:
            sentence, question, answers = schema
            sentence = self._get_both_schema(sentence)
            question = self._get_both_schema(question)
            answers = answers.split("/")
            for i in range(2):
                yield idx, {"sentence": sentence[i], "question": question[i], "options": answers, "answer": answers[i]}
                idx += 1
