"""NarrativeQA Reading Comprehension Challenge"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@article{narrativeqa,
author = {Tom\\'a\\v s Ko\\v cisk\\'y and Jonathan Schwarz and Phil Blunsom and
          Chris Dyer and Karl Moritz Hermann and G\\'abor Melis and
          Edward Grefenstette},
title = {The {NarrativeQA} Reading Comprehension Challenge},
journal = {Transactions of the Association for Computational Linguistics},
url = {https://TBD},
volume = {TBD},
year = {2018},
pages = {TBD},
}
"""

_DESCRIPTION = """\
The NarrativeQA dataset for question answering on long documents (movie scripts, books). It includes the list of documents with Wikipedia summaries, links to full stories, and questions and answers.
"""

_URLS = {
    "full_text": "https://storage.googleapis.com/huggingface-nlp/datasets/narrative_qa/narrativeqa_full_text.zip",
    "repo": "https://github.com/deepmind/narrativeqa/archive/master.zip",
}


class NarrativeQa(datasets.GeneratorBasedBuilder):
    """NarrativeQA: Question answering on long-documents"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            features=datasets.Features(
                {
                    "document": {
                        "id": datasets.Value("string"),
                        "kind": datasets.Value("string"),
                        "url": datasets.Value("string"),
                        "file_size": datasets.Value("int32"),
                        "word_count": datasets.Value("int32"),
                        "start": datasets.Value("string"),
                        "end": datasets.Value("string"),
                        "summary": {
                            "text": datasets.Value("string"),
                            "tokens": datasets.features.Sequence(datasets.Value("string")),
                            "url": datasets.Value("string"),
                            "title": datasets.Value("string"),
                        },
                        "text": datasets.Value("string"),
                    },
                    "question": {
                        "text": datasets.Value("string"),
                        "tokens": datasets.features.Sequence(datasets.Value("string")),
                    },
                    "answers": [
                        {
                            "text": datasets.Value("string"),
                            "tokens": datasets.features.Sequence(datasets.Value("string")),
                        }
                    ],
                }
            ),
            homepage="https://github.com/deepmind/narrativeqa",
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(_URLS)
        dl_dir["repo"] = os.path.join(dl_dir["repo"], "narrativeqa-master")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"repo_dir": dl_dir["repo"], "full_text_dir": dl_dir["full_text"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"repo_dir": dl_dir["repo"], "full_text_dir": dl_dir["full_text"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"repo_dir": dl_dir["repo"], "full_text_dir": dl_dir["full_text"], "split": "valid"},
            ),
        ]

    def _generate_examples(self, repo_dir, full_text_dir, split):
        """Yields examples."""
        documents = {}
        with open(os.path.join(repo_dir, "documents.csv")) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["set"] != split:
                    continue
                documents[row["document_id"]] = row

        summaries = {}
        with open(os.path.join(repo_dir, "third_party", "wikipedia", "summaries.csv")) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["set"] != split:
                    continue
                summaries[row["document_id"]] = row

        with open(os.path.join(repo_dir, "qaps.csv")) as f:
            reader = csv.DictReader(f)
            for id_, row in enumerate(reader):
                if row["set"] != split:
                    continue
                document_id = row["document_id"]
                document = documents[document_id]
                summary = summaries[document_id]
                full_text = open(os.path.join(full_text_dir, document_id + ".content"), encoding="latin-1").read()
                res = {
                    "document": {
                        "id": document["document_id"],
                        "kind": document["kind"],
                        "url": document["story_url"],
                        "file_size": document["story_file_size"],
                        "word_count": document["story_word_count"],
                        "start": document["story_start"],
                        "end": document["story_end"],
                        "summary": {
                            "text": summary["summary"],
                            "tokens": summary["summary_tokenized"].split(),
                            "url": document["wiki_url"],
                            "title": document["wiki_title"],
                        },
                        "text": full_text,
                    },
                    "question": {"text": row["question"], "tokens": row["question_tokenized"].split()},
                    "answers": [
                        {"text": row["answer1"], "tokens": row["answer1_tokenized"].split()},
                        {"text": row["answer2"], "tokens": row["answer2_tokenized"].split()},
                    ],
                }
                yield id_, res
