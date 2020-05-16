"""TODO(lc_quad): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(lc_quad): BibTeX citation
_CITATION = """
@inproceedings{dubey2017lc2,
title={LC-QuAD 2.0: A Large Dataset for Complex Question Answering over Wikidata and DBpedia},
author={Dubey, Mohnish and Banerjee, Debayan and Abdelkawi, Abdelrahman and Lehmann, Jens},
booktitle={Proceedings of the 18th International Semantic Web Conference (ISWC)},
year={2019},
organization={Springer}
}
"""

# TODO(lc_quad):
_DESCRIPTION = """\
LC-QuAD 2.0 is a Large Question Answering dataset with 30,000 pairs of question and its corresponding SPARQL query. The target knowledge base is Wikidata and DBpedia, specifically the 2018 version. Please see our paper for details about the dataset creation process and framework.
"""
_URL = "https://github.com/AskNowQA/LC-QuAD2.0/archive/master.zip"


class LcQuad(nlp.GeneratorBasedBuilder):
    """TODO(lc_quad): Short description of my dataset."""

    # TODO(lc_quad): Set up version.
    VERSION = nlp.Version("2.0.0")

    def _info(self):
        # TODO(lc_quad): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "NNQT_question": nlp.Value("string"),
                    "uid": nlp.Value("int32"),
                    "subgraph": nlp.Value("string"),
                    "template_index": nlp.Value("int32"),
                    "question": nlp.Value("string"),
                    "sparql_wikidata": nlp.Value("string"),
                    "sparql_dbpedia18": nlp.Value("string"),
                    "template": nlp.Value("string"),
                    # "template_id": nlp.Value('string'),
                    "paraphrased_question": nlp.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://lc-quad.sda.tech/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(lc_quad): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        dl_dir = os.path.join(dl_dir, "LC-QuAD2.0-master", "dataset")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "train.json")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "test.json")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(lc_quad): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = json.load(f)
            for id_, row in enumerate(data):
                is_list = False
                for key in row:
                    if key != "answer" and isinstance(row[key], list):
                        is_list = True
                if is_list:
                    continue
                yield id_, {
                    "NNQT_question": row["NNQT_question"],
                    "uid": row["uid"],
                    "subgraph": row["subgraph"],
                    "template_index": row["template_index"],
                    "question": row["question"],
                    "sparql_wikidata": row["sparql_wikidata"],
                    "sparql_dbpedia18": row["sparql_dbpedia18"],
                    "template": row["template"],
                    # "template_id": str(row['template_id']),
                    "paraphrased_question": row["paraphrased_question"],
                }
