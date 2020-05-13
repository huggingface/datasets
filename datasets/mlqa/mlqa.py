"""TODO(mlqa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(mlqa): BibTeX citation
_CITATION = """\
@article{lewis2019mlqa,
  title={MLQA: Evaluating Cross-lingual Extractive Question Answering},
  author={Lewis, Patrick and Oguz, Barlas and Rinott, Ruty and Riedel, Sebastian and Schwenk, Holger},
  journal={arXiv preprint arXiv:1910.07475},
  year={2019}
}
"""

# TODO(mlqa):
_DESCRIPTION = """\
    MLQA (MultiLingual Question Answering) is a benchmark dataset for evaluating cross-lingual question answering performance.
    MLQA consists of over 5K extractive QA instances (12K in English) in SQuAD format in seven languages - English, Arabic,
    German, Spanish, Hindi, Vietnamese and Simplified Chinese. MLQA is highly parallel, with QA instances parallel between 
    4 different languages on average.
"""
_URL = "https://dl.fbaipublicfiles.com/MLQA/"
_DEV_TEST_URL = "MLQA_V1.zip"
_TRANSLATE_TEST_URL = "mlqa-translate-test.tar.gz"
_TRANSLATE_TRAIN_URL = "mlqa-translate-train.tar.gz"
_LANG = ["ar", "de", "vi", "zh", "en", "es", "hi"]
_TRANSLATE_LANG = ["ar", "de", "vi", "zh", "es", "hi"]


class MlqaConfig(nlp.BuilderConfig):
    def __init__(self, data_url, **kwargs):
        """BuilderConfig for MLQA

        Args:
          data_url: `string`, url to the dataset
          **kwargs: keyword arguments forwarded to super.
        """
        super(MlqaConfig, self).__init__(version=nlp.Version("1.0.0",), **kwargs)
        self.data_url = data_url


class Mlqa(nlp.GeneratorBasedBuilder):
    """TODO(mlqa): Short description of my dataset."""

    # TODO(mlqa): Set up version.
    VERSION = nlp.Version("1.0.0")
    BUILDER_CONFIGS = (
        [
            MlqaConfig(
                name="mlqa-translate-train." + lang,
                data_url=_URL + _TRANSLATE_TRAIN_URL,
                description="Machine-translated data for Translate-train (SQuAD Train and Dev sets machine-translated into "
                "Arabic, German, Hindi, Vietnamese, Simplified Chinese and Spanish)",
            )
            for lang in _LANG
            if lang != "en"
        ]
        + [
            MlqaConfig(
                name="mlqa-translate-test." + lang,
                data_url=_URL + _TRANSLATE_TEST_URL,
                description="Machine-translated data for Translate-Test (MLQA-test set machine-translated into English) ",
            )
            for lang in _LANG
            if lang != "en"
        ]
        + [
            MlqaConfig(
                name="mlqa." + lang1 + "." + lang2,
                data_url=_URL + _DEV_TEST_URL,
                description="development and test splits",
            )
            for lang1 in _LANG
            for lang2 in _LANG
        ]
    )

    def _info(self):
        # TODO(mlqa): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "context": nlp.Value("string"),
                    "questions": nlp.features.Sequence({"question": nlp.Value("string")}),
                    "answers": nlp.features.Sequence(
                        {"text": nlp.Value("string"), "answer_start": nlp.Value("int32"),}
                    ),
                    "ids": nlp.features.Sequence({"idx": nlp.Value("string")})
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/facebookresearch/MLQA",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(mlqa): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        if self.config.name.startswith("mlqa-translate-train"):
            dl_file = dl_manager.download_and_extract(self.config.data_url)
            lang = self.config.name.split(".")[-1]
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(
                            os.path.join(dl_file, "mlqa-translate-train"),
                            "{}_squad-translate-train-train-v1.1.json".format(lang),
                        ),
                        "lang": lang,
                    },
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(
                            os.path.join(dl_file, "mlqa-translate-train"),
                            "{}_squad-translate-train-dev-v1.1.json".format(lang),
                        ),
                        "lang": lang,
                    },
                ),
            ]

        else:
            if self.config.name.startswith("mlqa."):
                dl_file = dl_manager.download_and_extract(self.config.data_url)
                name = self.config.name.split(".")
                l1, l2 = name[1:]
                return [
                    nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": os.path.join(
                                os.path.join(dl_file, "MLQA_V1/test"),
                                "test-context-{}-question-{}.json".format(l1, l2),
                            ),
                            "lang": (l1, l2),
                        },
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        # These kwargs will be passed to _generate_examples
                        gen_kwargs={
                            "filepath": os.path.join(
                                os.path.join(dl_file, "MLQA_V1/dev"), "dev-context-{}-question-{}.json".format(l1, l2)
                            ),
                            "lang": (l1, l2),
                        },
                    ),
                ]
            else:
                if self.config.name.startswith("mlqa-translate-test"):
                    dl_file = dl_manager.download_and_extract(self.config.data_url)
                    lang = self.config.name.split(".")[-1]
                    return [
                        nlp.SplitGenerator(
                            name=nlp.Split.TEST,
                            # These kwargs will be passed to _generate_examples
                            gen_kwargs={
                                "filepath": os.path.join(
                                    os.path.join(dl_file, "mlqa-translate-test"),
                                    "translate-test-context-{}-question-{}.json".format(lang, lang),
                                ),
                                "lang": lang,
                            },
                        ),
                    ]

    def _generate_examples(self, filepath, lang):
        """Yields examples."""
        # TODO(mlqa): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = json.load(f)
        for id1, examples in enumerate(data["data"]):
            for id2, example in enumerate(examples["paragraphs"]):
                context = example["context"]
                questions = [qa["question"] for qa in example["qas"]]
                answers = [qa["answers"] for qa in example["qas"]]
                ids = [qa["id"] for qa in example["qas"]]
                answers_start = [answer[0]["answer_start"] for answer in answers]
                answers_text = [answer[0]["text"] for answer in answers]
                yield str(id1) + "-" + str(id2), {
                    "context": context,
                    "questions": {"question": questions,},
                    "answers": {"answer_start": answers_start, "text": answers_text},
                    "ids": {"idx": ids},
                }
