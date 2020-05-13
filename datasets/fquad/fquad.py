"""TODO(fquad): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(fquad): BibTeX citation
_CITATION = """\
@ARTICLE{2020arXiv200206071
       author = {{Martin}, d'Hoffschmidt and {Maxime}, Vidal and
         {Wacim}, Belblidia and {Tom}, Brendlé},
        title = "{FQuAD: French Question Answering Dataset}",
      journal = {arXiv e-prints},
     keywords = {Computer Science - Computation and Language},
         year = "2020",
        month = "Feb",
          eid = {arXiv:2002.06071},
        pages = {arXiv:2002.06071},
archivePrefix = {arXiv},
       eprint = {2002.06071},
 primaryClass = {cs.CL}
}
"""

# TODO(fquad):
_DESCRIPTION = """\
FQuAD: French Question Answering Dataset
We introduce FQuAD, a native French Question Answering Dataset. FQuAD contains 25,000+ question and answer pairs.
Finetuning CamemBERT on FQuAD yields a F1 score of 88% and an exact match of 77.9%.

"""
_URL = "https://storage.googleapis.com/illuin/fquad"
_TRAIN_DATA = "train.json.zip"
_VALID_DATA = "valid.json.zip"


class Fquad(nlp.GeneratorBasedBuilder):
    """TODO(fquad): Short description of my dataset."""

    # TODO(fquad): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(fquad): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "context": nlp.Value("string"),
                    "questions": nlp.features.Sequence({"question": nlp.Value("string"),}),
                    "answers": nlp.features.Sequence(
                        {"texts": nlp.Value("string"), "answers_starts": nlp.Value("int32")}
                    ),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://fquad.illuin.tech/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(fquad): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        download_urls = {"train": os.path.join(_URL, _TRAIN_DATA), "valid": os.path.join(_URL, _VALID_DATA)}
        dl_dir = dl_manager.download_and_extract(download_urls)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir["train"], "train.json")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir["valid"], "valid.json")},
            ),
        ]

    def _generate_examples(self, filepath):

        """Yields examples."""
        # TODO(fquad): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = json.load(f)
            for id1, examples in enumerate(data["data"]):
                for id2, example in enumerate(examples["paragraphs"]):
                    questions = [question["question"] for question in example["qas"]]
                    answers = [answer["answers"] for answer in example["qas"]]
                    texts = [answer[0]["text"] for answer in answers]
                    answers_starts = [answer[0]["answer_start"] for answer in answers]

                    yield str(id1) + "_" + str(id2), {
                        "context": example["context"],
                        "questions": {"question": questions,},
                        "answers": {"texts": texts, "answers_starts": answers_starts},
                    }
