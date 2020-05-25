"""TODO(squad_es_v2): Add a description here."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nlp
import os
import json
# TODO(squad_es_v2): BibTeX citation
_CITATION = """\
@article{2016arXiv160605250R,
       author = {Casimiro Pio , Carrino and  Marta R. , Costa-jussa and  Jose A. R. , Fonollosa},
        title = "{Automatic Spanish Translation of the SQuAD Dataset for Multilingual
Question Answering}",
      journal = {arXiv e-prints},
         year = 2019,
          eid = {arXiv:1912.05200v1},
        pages = {arXiv:1912.05200v1},
archivePrefix = {arXiv},
       eprint = {1912.05200v2},
}
"""

# TODO(squad_es_v1):
_DESCRIPTION = """\
automatic translation of the Stanford Question Answering Dataset (SQuAD) v2 into Spanish
"""

_URL = "https://raw.githubusercontent.com/ccasimiro88/TranslateAlignRetrieve/master/SQuAD-es-v2.0/"
_DEV_FILE = "dev-v2.0-es.json"
_TRAINING_FILE = "train-v2.0-es.json"


class SquadEsV2Config(nlp.BuilderConfig):
  """BuilderConfig for SQUADEsV2."""

  def __init__(self, **kwargs):
    """BuilderConfig for SQUADEsV2.

    Args:
      **kwargs: keyword arguments forwarded to super.
    """
    super(SquadEsV2Config, self).__init__(**kwargs)


class SquadEsV2(nlp.GeneratorBasedBuilder):
  """TODO(squad_es_v2): Short description of my dataset."""

  # TODO(squad_es_v2): Set up version.
  VERSION = nlp.Version('2.0.0')
  BUILDER_CONFIGS = [
      SquadEsV2Config(
          name="plain_text",
          version=nlp.Version(
              "2.0.0",
              "New split API (https://tensorflow.org/datasets/splits)"),
          description="Plain text Spanish squad version 2",
      ),
  ]

  def _info(self):
    # TODO(squad_es_v2): Specifies the nlp.DatasetInfo object
    return nlp.DatasetInfo(
        # This is the description that will appear on the datasets page.
        description=_DESCRIPTION,
        # nlp.features.FeatureConnectors
        features=nlp.Features({
            # These are the features of your dataset like images, labels ...
            "id":
                nlp.Value('string'),
            "title":
                nlp.Value('string'),
            "context":
                nlp.Value('string'),
            "question":
                nlp.Value('string'),
            "answers":
                nlp.features.Sequence({
                    "text": nlp.Value('string'),
                    "answer_start": nlp.Value('int32'),
                })
        }),
        # If there's a common (input, target) tuple from the features,
        # specify them here. They'll be used if as_supervised=True in
        # builder.as_dataset.
        supervised_keys=None,
        # Homepage of the dataset for documentation
        homepage='https://github.com/ccasimiro88/TranslateAlignRetrieve',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    # TODO(squad_es_v2): Downloads the data and defines the splits
    # dl_manager is a nlp.download.DownloadManager that can be used to
    # download and extract URLs
    urls_to_download = {
        "train": os.path.join(_URL, _TRAINING_FILE),
        "dev": os.path.join(_URL, _DEV_FILE)
    }
    dl_dir = dl_manager.download_and_extract(urls_to_download)
    return [
        nlp.SplitGenerator(
            name=nlp.Split.TRAIN,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={
                "filepath": dl_dir["train"]
            },
        ),
        nlp.SplitGenerator(
            name=nlp.Split.VALIDATION,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={
                "filepath": dl_dir["dev"]
            },
        ),
    ]

  def _generate_examples(self, filepath):
    """Yields examples."""
    # TODO(squad_es_v2): Yields (key, example) tuples from the dataset
    with open(filepath) as f:
        data = json.load(f)
        for example in data["data"]:
            title = example.get("title", "").strip()
            for paragraph in example["paragraphs"]:
                context = paragraph["context"].strip()
                for qa in paragraph["qas"]:
                    question = qa["question"].strip()
                    id_ = qa["id"]

                    answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                    answers = [answer["text"].strip() for answer in qa["answers"]]

                    yield id_, {
                        "title": title,
                        "context": context,
                        "question": question,
                        "id": id_,
                        "answers": {
                            "answer_start": answer_starts,
                            "text": answers,
                        },
                    }

