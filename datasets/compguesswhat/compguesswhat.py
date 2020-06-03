from __future__ import absolute_import, division, print_function

import gzip
import json
import os

import nlp


class Compguesswhat(nlp.GeneratorBasedBuilder):
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
    _URL = "https://www.dropbox.com/s/gawk420r77huc01/compguesswhat_games.zip?dl=1"
    _TRAIN_FILE = "compguesswhat.train.jsonl.gz"
    _VALIDATION_FILE = "compguesswhat.valid.jsonl.gz"
    _TEST_FILE = "compguesswhat.test.jsonl.gz"

    VERSION = nlp.Version("0.1.0")

    def _info(self):
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=self._DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "id": nlp.Value("int32"),
                    "target_id": nlp.Value("int32"),
                    "timestamp": nlp.Value("string"),
                    "status": nlp.Value("string"),
                    "image": {
                        "id": nlp.Value("int32"),
                        "file_name": nlp.Value("string"),
                        "flickr_url": nlp.Value("string"),
                        "coco_url": nlp.Value("string"),
                        "height": nlp.Value("int32"),
                        "width": nlp.Value("int32"),
                        "vg_id": nlp.Value("int32"),
                        "vg_url": nlp.Value("string")
                    },
                    "qas": nlp.features.Sequence({
                        "question": nlp.Value("string"),
                        "answer": nlp.Value("string"),
                        "id": nlp.Value("int32")
                    }),
                    "objects": nlp.features.Sequence({
                        "id": nlp.Value("int32"),
                        "bbox": nlp.Sequence(nlp.Value("float32"), length=4),
                        "category": nlp.Value("string"),
                        "area": nlp.Value("float32"),
                        "category_id": nlp.Value("int32"),
                        "segment": nlp.features.Sequence(nlp.features.Sequence(nlp.Value("float32")))
                    })
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
        dl_dir = dl_manager.download_and_extract(self._URL)

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(
                    dl_dir,
                    self._TRAIN_FILE
                )},
            ),

            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(
                    dl_dir,
                    self._VALIDATION_FILE
                )},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={"filepath": os.path.join(
                    dl_dir,
                    self._TEST_FILE
                )},
            )
        ]

    def _generate_examples(self, filepath):
        def _extract_game_tuple(data):
            data = data.decode("utf-8")
            game = json.loads(data.strip("\n"))

            # we refactor the data structure a bit to fit with the new version
            game["target_id"] = game["object_id"]
            del game["object_id"]
            del game["questioner_id"]
            ###

            return game["id"], game

        """Yields examples."""
        with gzip.open(filepath) as in_file:
            for data in in_file:
                yield _extract_game_tuple(data)
