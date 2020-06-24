"""TODO(narrative_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import nlp


# TODO(narrative_qa): BibTeX citation
_CITATION = """\
@article{narrativeqa,
author = {Tom\'a\v s Ko\v cisk\'y and Jonathan Schwarz and Phil Blunsom and
          Chris Dyer and Karl Moritz Hermann and G\'abor Melis and
          Edward Grefenstette},
title = {The {NarrativeQA} Reading Comprehension Challenge},
journal = {Transactions of the Association for Computational Linguistics},
url = {https://TBD},
volume = {TBD},
year = {2018},
pages = {TBD},
}
"""

# TODO(narrative_qa):
_DESCRIPTION = """\
the NarrativeQA dataset. It includes the list of documents with Wikipedia summaries, links to full stories, and questions and answers.
"""


class NarrativeQa(nlp.GeneratorBasedBuilder):
    """TODO(narrative_qa): Short description of my dataset."""

    # TODO(narrative_qa): Set up version.
    _URL = "https://raw.githubusercontent.com/deepmind/narrativeqa/master/"

    keys = [
        "document_id",
        "question",
        "answer1",
        "answer2",
        "question_tokenized",
        "answer1_tokenized",
        "answer2_tokenized",
    ]
    doc_keys = [
        "kind",
        "story_url",
        "story_file_size",
        "wiki_url",
        "wiki_title",
        "story_word_count",
        "story_start",
        "story_end",
    ]
    summary_keys = ["summary", "summary_tokenized"]

    def _info(self):
        # TODO(narrative_qa): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            citation=_CITATION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "uniq_id": nlp.Value("string"),
                    "document_id": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answer1": nlp.Value("string"),
                    "answer2": nlp.Value("string"),
                    "question_tokenized": nlp.Value("string"),
                    "answer1_tokenized": nlp.Value("string"),
                    "answer2_tokenized": nlp.Value("string"),
                    "kind": nlp.Value("string"),
                    "story_url": nlp.Value("string"),
                    "story_file_size": nlp.Value("int32"),
                    "wiki_url": nlp.Value("string"),
                    "wiki_title": nlp.Value("string"),
                    "story_word_count": nlp.Value("int32"),
                    "story_start": nlp.Value("string"),
                    "story_end": nlp.Value("string"),
                    "summary": nlp.Value("string"),
                    "summary_tokenized": nlp.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=self._URL,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(narrative_qa): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {
            "documents": os.path.join(self._URL, "documents.csv"),
            "summaries": os.path.join(self._URL, "third_party/wikipedia/summaries.csv"),
            "qaps": os.path.join(self._URL, "qaps.csv"),
        }

        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        common_kwargs = {
            "documents_path": downloaded_files["documents"],
            "summaries_path": downloaded_files["summaries"],
            "qaps_path": downloaded_files["qaps"],
        }

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={**common_kwargs, "split": "train"}),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={**common_kwargs, "split": "test"}),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={**common_kwargs, "split": "valid"}),
        ]

    def _generate_examples(self, documents_path, summaries_path, qaps_path, split):
        """Yields examples."""
        # TODO(narrative_qa): Yields (key, example) tuples from the dataset
        documents = {}
        with open(documents_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["set"] != split:
                    continue
                documents[row["document_id"]] = row

        summaries = {}
        with open(summaries_path,) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["set"] != split:
                    continue
                summaries[row["document_id"]] = row

        with open(qaps_path) as f:
            reader = csv.DictReader(f)
            for id_, row in enumerate(reader):
                if row["set"] != split:
                    continue
                document_id = row["document_id"]
                res = {key: row[key] for key in self.keys}
                res = {**res, **{key: documents[document_id][key] for key in self.doc_keys}}
                res = {**res, **{key: summaries[document_id][key] for key in self.summary_keys}}
                res = {**res, "uniq_id": f"{document_id}-{split}-{id_}"}
                yield id_, res
