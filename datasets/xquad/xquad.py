"""TODO(xquad): Add a description here."""


import json

import datasets
from datasets.tasks import QuestionAnsweringExtractive


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
Greek, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese, Hindi and Romanian. Consequently, the dataset is entirely parallel
across 12 languages.
"""

_URL = "https://github.com/deepmind/xquad/raw/master/"
_LANG = ["ar", "de", "zh", "vi", "en", "es", "hi", "el", "th", "tr", "ru", "ro"]


class XquadConfig(datasets.BuilderConfig):

    """BuilderConfig for Xquad"""

    def __init__(self, lang, **kwargs):
        """

        Args:
            lang: string, language for the input text
            **kwargs: keyword arguments forwarded to super.
        """
        super(XquadConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.lang = lang


class Xquad(datasets.GeneratorBasedBuilder):
    """TODO(xquad): Short description of my dataset."""

    # TODO(xquad): Set up version.
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        XquadConfig(name="xquad.{}".format(lang), description=_DESCRIPTION, lang=lang) for lang in _LANG
    ]

    def _info(self):
        # TODO(xquad): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
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
            task_templates=[
                QuestionAnsweringExtractive(
                    question_column="question", context_column="context", answers_column="answers"
                )
            ],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(xquad): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {lang: _URL + "xquad.{}.json".format(lang) for lang in _LANG}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files[self.config.lang]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(xquad): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            xquad = json.load(f)
            id_ = 0
            for article in xquad["data"]:
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "context": context,
                            "question": question,
                            "id": qa["id"],
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
                        id_ += 1
