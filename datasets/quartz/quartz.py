"""TODO(quartz): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(quartz): BibTeX citation
_CITATION = """\
@InProceedings{quartz,
  author = {Oyvind Tafjord and Matt Gardner and Kevin Lin and Peter Clark},
  title = {"QUARTZ: An Open-Domain Dataset of Qualitative Relationship
Questions"},
 
  year = {"2019"},
}
"""

# TODO(quartz):
_DESCRIPTION = """\
QuaRTz is a crowdsourced dataset of 3864 multiple-choice questions about open domain qualitative relationships. Each 
question is paired with one of 405 different background sentences (sometimes short paragraphs).
The QuaRTz dataset V1 contains 3864 questions about open domain qualitative relationships. Each question is paired with 
one of 405 different background sentences (sometimes short paragraphs).

The dataset is split into train (2696), dev (384) and test (784). A background sentence will only appear in a single split.
"""

_URL = "https://s3-us-west-2.amazonaws.com/ai2-website/data/quartz-dataset-v1-aug2019.zip"


class Quartz(nlp.GeneratorBasedBuilder):
    """TODO(quartz): Short description of my dataset."""

    # TODO(quartz): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(quartz): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "id": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "choices": nlp.features.Sequence({"text": nlp.Value("string"), "label": nlp.Value("string")}),
                    "answerKey": nlp.Value("string"),
                    "para": nlp.Value("string"),
                    "para_id": nlp.Value("string"),
                    "para_anno": {
                        "effect_prop": nlp.Value("string"),
                        "cause_dir_str": nlp.Value("string"),
                        "effect_dir_str": nlp.Value("string"),
                        "cause_dir_sign": nlp.Value("string"),
                        "effect_dir_sign": nlp.Value("string"),
                        "cause_prop": nlp.Value("string"),
                    },
                    "question_anno": {
                        "more_effect_dir": nlp.Value("string"),
                        "less_effect_dir": nlp.Value("string"),
                        "less_cause_prop": nlp.Value("string"),
                        "more_effect_prop": nlp.Value("string"),
                        "less_effect_prop": nlp.Value("string"),
                        "less_cause_dir": nlp.Value("string"),
                    },
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://allenai.org/data/quartz",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(quartz): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "quartz-dataset-v1-aug2019")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.jsonl")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "dev.jsonl")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(quartz): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            for row in f:
                data = json.loads(row)
                id_ = data["id"]
                question = data["question"]["stem"]
                answerKey = data["answerKey"]
                choices = data["question"]["choices"]
                choice_text = [choice["text"] for choice in choices]
                choice_label = [choice["label"] for choice in choices]
                para_id = data["para_id"]
                para = data["para"]
                para_ano = data["para_anno"]
                effect_prop = para_ano.get("effect_prop", "")
                cause_dir_str = para_ano.get("cause_dir_str", "")
                effect_dir_str = para_ano.get("effect_dir_str", "")
                cause_dir_sign = para_ano.get("cause_dir_sign", "")
                effect_dir_sign = para_ano.get("effect_dir_sign", "")
                cause_prop = para_ano.get("cause_prop", "")
                question_anno = data["question_anno"]
                more_effect_dir = "" if not question_anno else question_anno.get("more_effect_dir", "")
                less_effect_dir = "" if not question_anno else question_anno.get("less_effect_dir", "")
                less_cause_prop = "" if not question_anno else question_anno.get("less_cause_prop", "")
                more_effect_prop = "" if not question_anno else question_anno.get("more_effect_prop", "")
                less_effect_prop = "" if not question_anno else question_anno.get("less_effect_prop", "")
                less_cause_dir = "" if not question_anno else question_anno.get("less_effect_prop", "")
                yield id_, {
                    "id": id_,
                    "question": question,
                    "choices": {"text": choice_text, "label": choice_label},
                    "answerKey": answerKey,
                    "para": para,
                    "para_id": para_id,
                    "para_anno": {
                        "effect_prop": effect_prop,
                        "cause_dir_str": cause_dir_str,
                        "effect_dir_str": effect_dir_str,
                        "cause_dir_sign": cause_dir_sign,
                        "effect_dir_sign": effect_dir_sign,
                        "cause_prop": cause_prop,
                    },
                    "question_anno": {
                        "more_effect_dir": more_effect_dir,
                        "less_effect_dir": less_effect_dir,
                        "less_cause_prop": less_cause_prop,
                        "more_effect_prop": more_effect_prop,
                        "less_effect_prop": less_effect_prop,
                        "less_cause_dir": less_cause_dir,
                    },
                }
