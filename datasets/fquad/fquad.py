"""TODO(fquad): Add a description here."""


import json
import os

import datasets


# TODO(fquad): BibTeX citation
_CITATION = """\
@ARTICLE{2020arXiv200206071
       author = {Martin, d'Hoffschmidt and Maxime, Vidal and
         Wacim, Belblidia and Tom, Brendlé},
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

_URL = "https://storage.googleapis.com/illuin/fquad/"
_URLS = {
    "train": _URL + "train.json.zip",
    "valid": _URL + "valid.json.zip",
}


class Fquad(datasets.GeneratorBasedBuilder):
    """TODO(fquad): Short description of my dataset."""

    # TODO(fquad): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(fquad): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "context": datasets.Value("string"),
                    "questions": datasets.features.Sequence(datasets.Value("string")),
                    "answers": datasets.features.Sequence(
                        {"texts": datasets.Value("string"), "answers_starts": datasets.Value("int32")}
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
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        download_urls = _URLS
        dl_dir = dl_manager.download_and_extract(download_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir["train"], "train.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir["valid"], "valid.json")},
            ),
        ]

    def _generate_examples(self, filepath):

        """Yields examples."""
        # TODO(fquad): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id1, examples in enumerate(data["data"]):
                for id2, example in enumerate(examples["paragraphs"]):
                    questions = [question["question"] for question in example["qas"]]
                    answers = [answer["answers"] for answer in example["qas"]]
                    texts = [answer[0]["text"] for answer in answers]
                    answers_starts = [answer[0]["answer_start"] for answer in answers]

                    yield str(id1) + "_" + str(id2), {
                        "context": example["context"],
                        "questions": questions,
                        "answers": {"texts": texts, "answers_starts": answers_starts},
                    }
