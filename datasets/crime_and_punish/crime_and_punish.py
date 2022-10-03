import datasets


_DESCRIPTION = """\

"""
_URL = "https://www.gutenberg.org/files/2554/2554-h/2554-h.htm"
_DATA_URL = "https://raw.githubusercontent.com/patrickvonplaten/datasets/master/crime_and_punishment.txt"


class CrimeAndPunish(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "line": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            homepage=_URL,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data = dl_manager.download_and_extract(_DATA_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_file": data, "split": "train"},
            ),
        ]

    def _generate_examples(self, data_file, split):

        with open(data_file, "rb") as f:
            id_counter = 0
            add_text = False
            crime_and_punishment_occ_counter = 0

            for line in f:
                line = line.decode("UTF-8")
                if "CRIME AND PUNISHMENT" in line:
                    crime_and_punishment_occ_counter += 1
                    add_text = crime_and_punishment_occ_counter == 3
                if "End of Project" in line:
                    add_text = False

                if add_text is True:
                    result = {"line": line}
                    id_counter += 1
                    yield id_counter, result
