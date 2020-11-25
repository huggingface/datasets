from __future__ import absolute_import, division, print_function

import gzip
import json
import os

import datasets


class CompguesswhatConfig(datasets.BuilderConfig):
    """ BuilderConfig for CompGuessWhat?!"""

    def __init__(self, data_url, splits, gameplay_scenario, **kwargs):
        """

        Args:
            gameplay_scenario: to specify if we want to load original CompGuessWhat?! split ('original') or
            the zero-shot reference games based on NOCAPS images ('zero_shot')
            **kwargs: keyword arguments forwarded to super.
        """
        super(CompguesswhatConfig, self).__init__(
            version=datasets.Version("0.2.0", "Second CompGuessWhat?! release"), **kwargs
        )
        assert gameplay_scenario in (
            "original",
            "zero_shot",
        ), "Invalid choice for parameter 'gameplay_scenario': {gameplay_scenario}. Valid values are ('original', 'zero_shot')."

        self.gameplay_scenario = gameplay_scenario
        self.splits = splits
        self.data_url = data_url


class Compguesswhat(datasets.GeneratorBasedBuilder):
    _CITATION = """\
        @inproceedings{suglia2020compguesswhat,
          title={CompGuessWhat?!: a Multi-task Evaluation Framework for Grounded Language Learning},
          author={Suglia, Alessandro, Konstas, Ioannis, Vanzo, Andrea, Bastianelli, Emanuele, Desmond Elliott, Stella Frank and Oliver Lemon},
          booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
          year={2020}
        }
    """

    _DESCRIPTION = """
        CompGuessWhat?! is an instance of a multi-task framework for evaluating the quality of learned neural representations,
        in particular concerning attribute grounding. Use this dataset if you want to use the set of games whose reference
        scene is an image in VisualGenome. Visit the website for more details: https://compguesswhat.github.io
    """

    BUILDER_CONFIGS = [
        CompguesswhatConfig(
            name="compguesswhat-original",
            gameplay_scenario="original",
            description="CompGuessWhat?! subset of games from the original GuessWhat?! dataset",
            data_url="https://www.dropbox.com/s/l0nc13udml6vs0w/compguesswhat-original.zip?dl=1",
            splits={
                "train": "compguesswhat.train.jsonl.gz",
                "valid": "compguesswhat.valid.jsonl.gz",
                "test": "compguesswhat.test.jsonl.gz",
            },
        ),
        CompguesswhatConfig(
            name="compguesswhat-zero_shot",
            gameplay_scenario="zero_shot",
            description="CompGuessWhat?! reference set of games for zero-shot evaluation using NOCAPS images",
            data_url="https://www.dropbox.com/s/gd46azul7o7iip4/compguesswhat-zero_shot.zip?dl=1",
            splits={
                "nd_valid": "compguesswhat.nd_valid.jsonl.gz",
                "nd_test": "compguesswhat.nd_test.jsonl.gz",
                "od_valid": "compguesswhat.od_valid.jsonl.gz",
                "od_test": "compguesswhat.od_test.jsonl.gz",
            },
        ),
    ]

    VERSION = datasets.Version("0.2.0")

    def _info(self):
        if self.config.gameplay_scenario == "original":
            return datasets.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=self._DESCRIPTION,
                # datasets.features.FeatureConnectors
                features=datasets.Features(
                    {
                        "id": datasets.Value("int32"),
                        "target_id": datasets.Value("int32"),
                        "timestamp": datasets.Value("string"),
                        "status": datasets.Value("string"),
                        "image": {
                            # this is the image ID in GuessWhat?! which corresponds to the MSCOCO id
                            "id": datasets.Value("int32"),
                            "file_name": datasets.Value("string"),
                            "flickr_url": datasets.Value("string"),
                            "coco_url": datasets.Value("string"),
                            "height": datasets.Value("int32"),
                            "width": datasets.Value("int32"),
                            # this field represents the corresponding image metadata that can be found in VisualGenome
                            # in the file image_data.json
                            # We copy it over so that we avoid any confusion or possible wrong URL
                            # Please use the original image files to resolve photos
                            "visual_genome": {
                                "width": datasets.Value("int32"),
                                "height": datasets.Value("int32"),
                                "url": datasets.Value("string"),
                                "coco_id": datasets.Value("int32"),
                                # this is the actual VisualGenome image ID
                                # because we can't rely store it as an integer we same it as string
                                "flickr_id": datasets.Value("string"),
                                "image_id": datasets.Value("string"),
                            },
                        },
                        "qas": datasets.features.Sequence(
                            {
                                "question": datasets.Value("string"),
                                "answer": datasets.Value("string"),
                                "id": datasets.Value("int32"),
                            }
                        ),
                        "objects": datasets.features.Sequence(
                            {
                                "id": datasets.Value("int32"),
                                "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                                "category": datasets.Value("string"),
                                "area": datasets.Value("float32"),
                                "category_id": datasets.Value("int32"),
                                "segment": datasets.features.Sequence(
                                    datasets.features.Sequence(datasets.Value("float32"))
                                ),
                            }
                        ),
                    }
                ),
                # If there's a common (input, target) tuple from the features,
                # specify them here. They'll be used if as_supervised=True in
                # builder.as_dataset.
                supervised_keys=None,
                # Homepage of the dataset for documentation
                homepage="https://compguesswhat.github.io/",
                citation=self._CITATION,
            )
        elif self.config.gameplay_scenario == "zero_shot":
            return datasets.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=self._DESCRIPTION,
                # datasets.features.FeatureConnectors
                features=datasets.Features(
                    {
                        "id": datasets.Value("int32"),
                        "target_id": datasets.Value("string"),
                        "status": datasets.Value("string"),
                        "image": {
                            "id": datasets.Value("int32"),
                            "file_name": datasets.Value("string"),
                            "coco_url": datasets.Value("string"),
                            "height": datasets.Value("int32"),
                            "width": datasets.Value("int32"),
                            "license": datasets.Value("int32"),
                            "open_images_id": datasets.Value("string"),
                            "date_captured": datasets.Value("string"),
                        },
                        "objects": datasets.features.Sequence(
                            {
                                "id": datasets.Value("string"),
                                "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                                "category": datasets.Value("string"),
                                "area": datasets.Value("float32"),
                                "category_id": datasets.Value("int32"),
                                "IsOccluded": datasets.Value("int32"),
                                "IsTruncated": datasets.Value("int32"),
                                "segment": datasets.features.Sequence(
                                    {
                                        "MaskPath": datasets.Value("string"),
                                        "LabelName": datasets.Value("string"),
                                        "BoxID": datasets.Value("string"),
                                        "BoxXMin": datasets.Value("string"),
                                        "BoxXMax": datasets.Value("string"),
                                        "BoxYMin": datasets.Value("string"),
                                        "BoxYMax": datasets.Value("string"),
                                        "PredictedIoU": datasets.Value("string"),
                                        "Clicks": datasets.Value("string"),
                                    }
                                ),
                            }
                        ),
                    }
                ),
                # If there's a common (input, target) tuple from the features,
                # specify them here. They'll be used if as_supervised=True in
                # builder.as_dataset.
                supervised_keys=None,
                # Homepage of the dataset for documentation
                homepage="https://compguesswhat.github.io/",
                citation=self._CITATION,
            )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_dir = dl_manager.download_and_extract(self.config.data_url)

        splits_gen = []

        for split_id, split_filename in self.config.splits.items():
            if self.config.gameplay_scenario == "original":
                if "train" in split_id:
                    split_name = datasets.Split.TRAIN
                elif "valid" in split_id:
                    split_name = datasets.Split.VALIDATION
                elif "test" in split_id:
                    split_name = datasets.Split.TEST
            else:
                split_name = datasets.Split(split_id)

            full_split_name = "-".join(["compguesswhat", self.config.gameplay_scenario])
            splits_gen.append(
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "filepath": os.path.join(
                            dl_dir,
                            full_split_name,
                            self.VERSION.version_str,
                            split_filename,
                        )
                    },
                )
            )

        return splits_gen

    def _generate_examples(self, filepath):
        def _extract_game_tuple(data):
            data = data.decode("utf-8")
            game = json.loads(data.strip("\n"))

            # we refactor the data structure a bit to fit with the new version
            game["target_id"] = game["object_id"]
            if "object_id" in game:
                del game["object_id"]

            if "questioner_id" in game:
                del game["questioner_id"]
            ###

            if "visual_genome" in game["image"]:
                # We need to cast it to string so that we avoid issues with int size
                game["image"]["visual_genome"]["image_id"] = str(game["image"]["visual_genome"]["image_id"])
                game["image"]["visual_genome"]["flickr_id"] = str(game["image"]["visual_genome"]["flickr_id"])

            return game["id"], game

        """Yields examples."""
        with gzip.open(filepath) as in_file:
            for data in in_file:
                yield _extract_game_tuple(data)
