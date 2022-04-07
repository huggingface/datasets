"""TODO(blended_skill_talk): Add a description here."""


import json

import datasets


# TODO(blended_skill_talk): BibTeX citation
_CITATION = """\
@misc{smith2020evaluating,
    title={Can You Put it All Together: Evaluating Conversational Agents' Ability to Blend Skills},
    author={Eric Michael Smith and Mary Williamson and Kurt Shuster and Jason Weston and Y-Lan Boureau},
    year={2020},
    eprint={2004.08449},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

# TODO(blended_skill_talk):
_DESCRIPTION = """\
A dataset of 7k conversations explicitly designed to exhibit multiple conversation modes: displaying personality, having empathy, and demonstrating knowledge.
"""
_URL = "http://parl.ai/downloads/blended_skill_talk/blended_skill_talk.tar.gz"

_TASK = ["convai2", "empathetic_dialogues", "wizard_of_wikipedia"]


class BlendedSkillTalk(datasets.GeneratorBasedBuilder):
    """TODO(blended_skill_talk): Short description of my dataset."""

    # TODO(blended_skill_talk): Set up version.
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        # TODO(blended_skill_talk): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "personas": datasets.features.Sequence(datasets.Value("string")),
                    "additional_context": datasets.Value("string"),
                    "previous_utterance": datasets.features.Sequence(datasets.Value("string")),
                    "context": datasets.Value("string"),
                    "free_messages": datasets.features.Sequence(datasets.Value("string")),
                    "guided_messages": datasets.features.Sequence(datasets.Value("string")),
                    "suggestions": datasets.features.Sequence({task: datasets.Value("string") for task in _TASK})
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://parl.ai/projects/bst/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(blended_skill_talk): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        archive = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "train.json",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "valid.json",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": "test.json",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        """Yields examples."""
        # TODO(blended_skill_talk): Yields (key, example) tuples from the dataset
        for path, f in files:
            if path == filepath:
                data = json.load(f)
                for id_, row in enumerate(data):
                    personas = [row["personas"][1][0], row["personas"][1][1]]
                    dialogs = [dialog[1] for dialog in row["dialog"]]
                    free_messages = []
                    guided_messages = []

                    for i in range(len(dialogs) // 2):
                        free_messages.append(dialogs[2 * i])
                        guided_messages.append(dialogs[2 * i + 1])
                    context = row["context_dataset"]
                    add_context = row["additional_context"] if context == "wizard_of_wikipedia" else ""
                    previous_utterance = [row["free_turker_utterance"], row["guided_turker_utterance"]]
                    suggestions = row["suggestions"]
                    convai_suggestions = []
                    empathetic_suggestions = []
                    wow_suggestions = []
                    for i in range(len(suggestions) // 2):
                        convai_suggestions.append(suggestions[2 * i + 1]["convai2"])
                        empathetic_suggestions.append(suggestions[2 * i + 1]["empathetic_dialogues"])
                        wow_suggestions.append(suggestions[2 * i + 1]["wizard_of_wikipedia"])
                    yield id_, {
                        "personas": personas,
                        "additional_context": add_context,
                        "previous_utterance": previous_utterance,
                        "context": context,
                        "free_messages": free_messages,
                        "guided_messages": guided_messages,
                        "suggestions": {
                            "convai2": convai_suggestions,
                            "empathetic_dialogues": empathetic_suggestions,
                            "wizard_of_wikipedia": wow_suggestions,
                        },
                    }
                break
