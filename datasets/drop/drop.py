"""TODO(drop): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(drop): BibTeX citation
_CITATION = """\
@inproceedings{Dua2019DROP,
  author={Dheeru Dua and Yizhong Wang and Pradeep Dasigi and Gabriel Stanovsky and Sameer Singh and Matt Gardner},
  title={DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs},
  booktitle={Proc. of NAACL},
  year={2019}
}
"""

# TODO(drop):
_DESCRIPTION = """\
DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs.
. DROP is a crowdsourced, adversarially-created, 96k-question benchmark, in which a system must resolve references in a 
question, perhaps to multiple input positions, and perform discrete operations over them (such as addition, counting, or
 sorting). These operations require a much more comprehensive understanding of the content of paragraphs than what was 
 necessary for prior datasets.
"""
_URl = "https://s3-us-west-2.amazonaws.com/allennlp/datasets/drop/drop_dataset.zip"


class Drop(nlp.GeneratorBasedBuilder):
    """TODO(drop): Short description of my dataset."""

    # TODO(drop): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(drop): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "passage": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answers_spans": nlp.features.Sequence({"spans": nlp.Value("string")})
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://allennlp.org/drop",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(drop): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URl)
        data_dir = os.path.join(dl_dir, "drop_dataset")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "drop_dataset_train.json")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "drop_dataset_dev.json")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(drop): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = json.load(f)
            # print(data.keys())
            for i, key in enumerate(data):
                example = data[key]
                # print(example['passage'])
                qa_pairs = example["qa_pairs"]
                for j, qa in enumerate(qa_pairs):
                    question = qa["question"]
                    answers = qa["answer"]["spans"]
                    yield str(i) + "_" + str(j), {
                        "passage": example["passage"],
                        "question": question,
                        "answers_spans": {"spans": answers},
                    }
