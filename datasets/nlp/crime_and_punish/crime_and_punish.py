from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nlp
import tensorflow as tf

_DESCRIPTION = """\

"""
_URL = "https://www.gutenberg.org/files/2554/2554-h/2554-h.htm"
_DATA_URL = "https://raw.githubusercontent.com/michalbe/fyodor/master/static/text.txt"


class CrimeAndPunishConfig(nlp.BuilderConfig):
    """BuilderConfig for Crime and Punish."""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for BlogAuthorship

        Args:
          data_url: `string`, url to the dataset (word or raw level)
          **kwargs: keyword arguments forwarded to super.
        """
        super(CrimeAndPunishConfig, self).__init__(
            version=nlp.Version("1.0.0",), **kwargs
        )
        self.data_url = data_url


class CrimeAndPunish(nlp.GeneratorBasedBuilder):

    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        CrimeAndPunishConfig(
            name="crime-and-punish",
            data_url=_DATA_URL,
            description="word level dataset. No processing is needed other than replacing newlines with <eos> tokens.",
        ),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            builder=self,
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.features.FeaturesDict(
                {
                    "paragraph": nlp.string,
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_URL,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        if self.builder_config.name == "crime-and-punish":
            data = dl_manager.download_and_extract(self.builder_config.data_url)

            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    gen_kwargs={"data_file": data, "split": "train"},
                ),
            ]
        else:
            raise ValueError("{} does not exist".format(self.builder_config.name))

    def _generate_examples(self, data_file, split):

        with open(data_file) as f:
            id_counter = 0
            add_text = False
            crime_and_punishment_occ_counter = 0
            lines = ""

            for line in f:
                line = line.strip()
                if crime_and_punishment_occ_counter == 3:
                    add_text = True
                if crime_and_punishment_occ_counter == 4:
                    add_text = False
                if add_text is True:
                    if line != "":
                        lines += line
                    elif lines != "" and line == "":
                        result = {"paragraph": lines}
                        lines = ""
                        id_counter += 1
                        yield id_counter, result
                else:
                    if "CRIME AND PUNISHMENT" in line:
                        crime_and_punishment_occ_counter += 1
