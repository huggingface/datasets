"""TODO(xquad): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import nlp


_CITATION = """\
@article{Artetxe:etal:2019,
      author    = {Mikel Artetxe and Sebastian Ruder and Dani Yogatama},
      title     = {On the cross-lingual transferability of monolingual representations},
      journal   = {CoRR},
      volume    = {abs/1910.11856},
      year      = {2019},
      archivePrefix = {arXiv},
      eprint    = {1910.11856}
}
"""

_DESCRIPTION = """\
XQuAD (Cross-lingual Question Answering Dataset) is a benchmark dataset for evaluating cross-lingual question answering
performance. The dataset consists of a subset of 240 paragraphs and 1190 question-answer pairs from the development set
of SQuAD v1.1 (Rajpurkar et al., 2016) together with their professional translations into ten languages: Spanish, German,
Greek, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese, and Hindi. Consequently, the dataset is entirely parallel
across 11 languages.
"""

_URL = "https://github.com/deepmind/xquad/raw/master/"
_LANG = ["ar", "de", "zh", "vi", "en", "es", "hi", "el", "th", "tr", "ru"]


class XquadConfig(nlp.BuilderConfig):

    """ BuilderConfig for Xquad"""

    def __init__(self, lang, **kwargs):
        """

        Args:
            lang: string, language for the input text
            **kwargs: keyword arguments forwarded to super.
        """
        super(XquadConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )
        self.lang = lang


class Xquad(nlp.GeneratorBasedBuilder):
    """TODO(xquad): Short description of my dataset."""

    # TODO(xquad): Set up version.
    VERSION = nlp.Version("1.0.0")
    BUILDER_CONFIGS = [
        XquadConfig(name="xquad.{}".format(lang), description=_DESCRIPTION, lang=lang) for lang in _LANG
    ]

    def _info(self):
        # TODO(xquad): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "context": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answers": nlp.features.Sequence(
                        {"text": nlp.Value("string"), "answer_start": nlp.Value("int32"),}
                    ),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/deepmind/xquad",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(xquad): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {lang: _URL + "xquad.{}.json".format(lang) for lang in _LANG}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files[self.config.lang]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(xquad): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            xquad = json.load(f)
            for article in xquad["data"]:
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"answer_start": answer_starts, "text": answers,},
                        }
