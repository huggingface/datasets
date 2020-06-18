"""TODO(coqa): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import nlp


# TODO(coqa): BibTeX citation
_CITATION = """\
@InProceedings{SivaAndAl:Coca,
       author = {Siva, Reddy and Danqi, Chen and  Christopher D., Manning},
        title = {WikiQA: A Challenge Dataset for Open-Domain Question Answering},
      journal = { arXiv},
         year = {2018},

}
"""

# TODO(coqa):
_DESCRIPTION = """\
CoQA: A Conversational Question Answering Challenge
"""

_TRAIN_DATA_URL = "https://nlp.stanford.edu/data/coqa/coqa-train-v1.0.json"
_DEV_DATA_URL = "https://nlp.stanford.edu/data/coqa/coqa-dev-v1.0.json"

#
# class CoqaConfig(nlp.BuilderConfig):
#   """BuilderConfig for Coqa."""
#
#   def __init__(self,
#                story,
#                source,
#                questions,
#                answers,
#                citation,
#                description,
#                additional_answers=None,
#                **kwargs):
#     """BuilderConfig for Coca.
#
#     Args:
#       story: `text`,  context
#       source: `text`, source of the story
#       questions `Sequence` set of questions
#       answers: `Sequence` set of answers to the questions
#       data_url: `string`, url to download the  file from
#       citation: `string`, citation for the data set
#      additional_answers: `Sequence`, in the dev set questions have also set of additional answers
#       **kwargs: keyword arguments forwarded to super.
#     """
#     super(CoqaConfig, self).__init__(
#         version=nlp.Version(
#             "1.0.0",
#             "New split API (https://tensorflow.org/datasets/splits)"),
#         **kwargs)
#     self.story = story
#     self.source = source
#     self.questions = questions
#     self.answers = answers
#     self.additional_answers = additional_answers
#     self.citation = citation
#     self.description = description


class Coqa(nlp.GeneratorBasedBuilder):
    """TODO(coqa): Short description of my dataset."""

    # TODO(coqa): Set up version.
    VERSION = nlp.Version("1.0.0")
    # BUILDER_CONFIGS = CoqaConfig(
    #     story= 'story',
    #     source='source',
    #     questions='questions',
    #     answers='answers',
    #     additional_answers='additional_answers',
    #     description= _DESCRIPTION,
    #     citation= _CITATION
    #
    # )
    def _info(self):
        # TODO(coqa): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "source": nlp.Value("string"),
                    "story": nlp.Value("string"),
                    "questions": nlp.features.Sequence({"input_text": nlp.Value("string"),}),
                    "answers": nlp.features.Sequence(
                        {
                            "input_text": nlp.Value("string"),
                            "answer_start": nlp.Value("int32"),
                            "answer_end": nlp.Value("int32"),
                        }
                    ),
                    # ##the foloowing feature allows to take into account additional answers in the validation set
                    # 'additional_answers': nlp.features.Sequence({
                    #         "input_texts": nlp.Value('int32'),
                    #         "answers_start": nlp.Value('int32'),
                    #         "answers_end": nlp.Value('int32')
                    #     }),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://stanfordnlp.github.io/coqa/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(coqa): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {"train": _TRAIN_DATA_URL, "dev": _DEV_DATA_URL}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"], "split": "train"}
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"], "split": "validation"}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(coqa): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = json.load(f)
            for row in data["data"]:
                questions = [question["input_text"] for question in row["questions"]]
                story = row["story"]
                source = row["source"]
                answers_start = [answer["span_start"] for answer in row["answers"]]
                answers_end = [answer["span_end"] for answer in row["answers"]]
                answers = [answer["input_text"] for answer in row["answers"]]
                # add_answers = row['additional_answers']
                # add_input_tests = []
                # add_start_answers = []
                # add_end_answers = []
                # for key in add_answers:
                #     add_answers_key = add_answers[key]
                #     add_input_tests.append([add_answer['input_text'] for add_answer in add_answers_key])
                #     add_start_answers.append([add_answer['span_start'] for add_answer in add_answers_key])
                #     add_end_answers.append([add_answer['span_end'] for add_answer in add_answers_key])
                yield row["id"], {
                    "source": source,
                    "story": story,
                    "questions": {"input_text": questions,},
                    "answers": {"input_text": answers, "answer_start": answers_start, "answer_end": answers_end}
                    # 'additional_answers': {
                    #     "input_texts": add_input_tests ,
                    #     "answers_start": add_start_answers,
                    #     "answers_end": add_end_answers,
                    # }
                }
