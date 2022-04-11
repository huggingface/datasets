"""TODO(drop): Add a description here."""


import json
import os

import datasets


_CITATION = """\
@inproceedings{Dua2019DROP,
  author={Dheeru Dua and Yizhong Wang and Pradeep Dasigi and Gabriel Stanovsky and Sameer Singh and Matt Gardner},
  title={DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs},
  booktitle={Proc. of NAACL},
  year={2019}
}
"""

_DESCRIPTION = """\
DROP: A Reading Comprehension Benchmark Requiring Discrete Reasoning Over Paragraphs.
. DROP is a crowdsourced, adversarially-created, 96k-question benchmark, in which a system must resolve references in a
question, perhaps to multiple input positions, and perform discrete operations over them (such as addition, counting, or
 sorting). These operations require a much more comprehensive understanding of the content of paragraphs than what was
 necessary for prior datasets.
"""
_URL = "https://s3-us-west-2.amazonaws.com/allennlp/datasets/drop/drop_dataset.zip"


class AnswerParsingError(Exception):
    pass


class DropDateObject:
    """
    Custom parser for date answers in DROP.
    A date answer is a dict <date> with at least one of day|month|year.

    Example: date == {
        'day': '9',
        'month': 'March',
        'year': '2021'
    }

    This dict is parsed and flattend to '{day} {month} {year}', not including
    blank values.

    Example: str(DropDateObject(date)) == '9 March 2021'
    """

    def __init__(self, dict_date):
        self.year = dict_date.get("year", "")
        self.month = dict_date.get("month", "")
        self.day = dict_date.get("day", "")

    def __iter__(self):
        yield from [self.day, self.month, self.year]

    def __bool__(self):
        return any(self)

    def __repr__(self):
        return " ".join(self).strip()


class Drop(datasets.GeneratorBasedBuilder):
    """TODO(drop): Short description of my dataset."""

    # TODO(drop): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(drop): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "section_id": datasets.Value("string"),
                    "query_id": datasets.Value("string"),
                    "passage": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers_spans": datasets.features.Sequence(
                        {"spans": datasets.Value("string"), "types": datasets.Value("string")}
                    )
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
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "drop_dataset")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "drop_dataset_train.json"), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "drop_dataset_dev.json"), "split": "validation"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(drop): Yields (key, example) tuples from the dataset
        with open(filepath, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            id_ = 0
            for i, (section_id, section) in enumerate(data.items()):
                for j, qa in enumerate(section["qa_pairs"]):

                    example = {
                        "section_id": section_id,
                        "query_id": qa["query_id"],
                        "passage": section["passage"],
                        "question": qa["question"],
                    }

                    if split == "train":
                        answers = [qa["answer"]]
                    else:
                        answers = qa["validated_answers"]

                    try:
                        example["answers_spans"] = self.build_answers(answers)
                        yield id_, example
                        id_ += 1
                    except AnswerParsingError:
                        # This is expected for 9 examples of train
                        # and 1 of validation.
                        continue

    @staticmethod
    def _raise(message):
        """
        Raise a custom AnswerParsingError, to be sure to only catch our own
        errors. Messages are irrelavant for this script, but are written to
        ease understanding the code.
        """
        raise AnswerParsingError(message)

    def build_answers(self, answers):

        returned_answers = {
            "spans": list(),
            "types": list(),
        }
        for answer in answers:
            date = DropDateObject(answer["date"])

            if answer["number"] != "":
                # sanity checks
                if date:
                    self._raise("This answer is both number and date!")
                if len(answer["spans"]):
                    self._raise("This answer is both number and text!")

                returned_answers["spans"].append(answer["number"])
                returned_answers["types"].append("number")

            elif date:
                # sanity check
                if len(answer["spans"]):
                    self._raise("This answer is both date and text!")

                returned_answers["spans"].append(str(date))
                returned_answers["types"].append("date")

            # won't triger if len(answer['spans']) == 0
            for span in answer["spans"]:
                # sanity checks
                if answer["number"] != "":
                    self._raise("This answer is both text and number!")
                if date:
                    self._raise("This answer is both text and date!")

                returned_answers["spans"].append(span)
                returned_answers["types"].append("span")

        # sanity check
        _len = len(returned_answers["spans"])
        if not _len:
            self._raise("Empty answer.")
        if any(len(l) != _len for _, l in returned_answers.items()):
            self._raise("Something went wrong while parsing answer values/types")

        return returned_answers
