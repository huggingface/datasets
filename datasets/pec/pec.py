"""TODO: Add a description here."""
from __future__ import absolute_import, division, print_function

import os

import datasets


# TODO: Add BibTeX citation
_CITATION = """\
@inproceedings{zhong2020towards,
    title = "Towards Persona-Based Empathetic Conversational Models",
    author = "Zhong, Peixiang  and
      Zhang, Chen  and
      Wang, Hao  and
      Liu, Yong  and
      Miao, Chunyan",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    year = "2020",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.531",
    pages = "6556--6566"}
"""

# TODO: Add description of the dataset here
_DESCRIPTION = """\
A dataset of around 350K persona-based empathetic conversations. Each speaker is associated with a persona, which comprises multiple persona sentences. The response of each conversation is empathetic.
"""

_URL = "https://dl.dropboxusercontent.com/s/u04fzuhsnxd0uvw/hf_pec.zip"

# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
# Using a specific configuration class is optional, you can also use the base class if you don't need
# to add specific attributes.
# here we give an example for three sub-set of the dataset with difference sizes.


class PECConfig(datasets.BuilderConfig):
    """ BuilderConfig for PEC"""

    def __init__(self, domain="all", **kwargs):
        """
        Args:
            domain: the domain of our dataset: happy or offmychest
            **kwargs: keyword arguments forwarded to super.
        """
        super(PECConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.domain = domain


class PEC(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.0.0")
    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIG_CLASS = PECConfig
    BUILDER_CONFIGS = [
        PECConfig(name=domain, description="A subset of PEC dataset: {}".format(domain), domain=domain)
        for domain in ["happy", "offmychest", "all"]
    ]

    def _info(self):
        # TODO: Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "personas": datasets.features.Sequence(datasets.Value("string")),
                    "context": datasets.features.Sequence(datasets.Value("string")),
                    "context_speakers": datasets.features.Sequence(datasets.Value("string")),
                    "response": datasets.Value("string"),
                    "response_speaker": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/zhongpeixiang/PEC",
            citation=_CITATION,
        )

    def _load_persona(self, paths):
        persona = {}
        is_speaker = True
        sentences = []
        for path in paths:
            with open(path, encoding="utf-8") as f:
                for row in f:
                    if "********************" not in row:
                        if is_speaker:
                            speaker = row.strip()
                            is_speaker = False
                        else:
                            sentences.append(row.strip())
                    else:
                        persona[speaker] = sentences
                        is_speaker = True
                        sentences = []
        return persona

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "hf_pec")
        domains = ["happy", "offmychest"] if self.config.domain == "all" else [self.config.domain]  # multiple domains
        persona_paths = [os.path.join(data_dir, domain, "persona.txt") for domain in domains]
        persona = self._load_persona(persona_paths)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": [os.path.join(data_dir, domain, "train.txt") for domain in domains],
                    "split": "train",
                    "persona": persona,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": [os.path.join(data_dir, domain, "test.txt") for domain in domains],
                    "split": "test",
                    "persona": persona,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": [os.path.join(data_dir, domain, "valid.txt") for domain in domains],
                    "split": "dev",
                    "persona": persona,
                },
            ),
        ]

    def _generate_examples(self, filepath, split, persona):
        """ Yields examples. """
        # TODO: Yields (key, example) tuples from the dataset
        context_speakers = []
        context = []
        example_id = 0
        for fpath in filepath:
            with open(fpath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    if row.strip() == "":
                        continue
                    if "********************" not in row:
                        if "---+---" in row:
                            speaker, utterance = row.split("---+---")
                            context_speakers.append(speaker.strip())
                            context.append(utterance.strip())
                        else:
                            # contains inline \n
                            context[-1] = context[-1] + " " + row.strip()
                    else:
                        response_speaker = context_speakers.pop()
                        response = context.pop()
                        yield example_id, {
                            "personas": persona[response_speaker],
                            "context_speakers": context_speakers,
                            "context": context,
                            "response_speaker": response_speaker,
                            "response": response,
                        }
                        context_speakers = []
                        context = []
                        example_id += 1
