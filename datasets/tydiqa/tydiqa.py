"""TODO(tydiqa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os
import textwrap

import nlp


# TODO(tydiqa): BibTeX citation
_CITATION = """\
@article{tydiqa,
title   = {TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages},
author  = {Jonathan H. Clark and Eunsol Choi and Michael Collins and Dan Garrette and Tom Kwiatkowski and Vitaly Nikolaev and Jennimaria Palomaki}
year    = {2020},
journal = {Transactions of the Association for Computational Linguistics}
}
"""

# TODO(tydiqa):
_DESCRIPTION = """\
TyDi QA is a question answering dataset covering 11 typologically diverse languages with 204K question-answer pairs. 
The languages of TyDi QA are diverse with regard to their typology -- the set of linguistic features that each language 
expresses -- such that we expect models performing well on this set to generalize across a large number of the languages 
in the world. It contains language phenomena that would not be found in English-only corpora. To provide a realistic 
information-seeking task and avoid priming effects, questions are written by people who want to know the answer, but 
don’t know the answer yet, (unlike SQuAD and its descendents) and the data is collected directly in each language without
the use of translation (unlike MLQA and XQuAD).
"""
_URL = "https://storage.googleapis.com/tydiqa/"
_PRIMARY_TASK_TRAIN = "v1.0/tydiqa-v1.0-train.jsonl.gz"
_PRIMARY_TASK_DEV = "v1.0/tydiqa-v1.0-dev.jsonl.gz"
_SECONDARY_TASK_TRAIN = "v1.1/tydiqa-goldp-v1.1-train.json"
_SECONDARY_TASK_DEV = "v1.1/tydiqa-goldp-v1.1-dev.json"


class TydiqaConfig(nlp.BuilderConfig):

    """ BuilderConfig for Tydiqa"""

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(TydiqaConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )


class Tydiqa(nlp.GeneratorBasedBuilder):
    """TODO(tydiqa): Short description of my dataset."""

    # TODO(tydiqa): Set up version.
    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        TydiqaConfig(
            name="primary_task",
            description=textwrap.dedent(
                """\
          Passage selection task (SelectP): Given a list of the passages in the article, return either (a) the index of 
          the passage that answers the question or (b) NULL if no such passage exists.
          Minimal answer span task (MinSpan): Given the full text of an article, return one of (a) the start and end 
          byte indices of the minimal span that completely answers the question; (b) YES or NO if the question requires 
          a yes/no answer and we can draw a conclusion from the passage; (c) NULL if it is not possible to produce a 
          minimal answer for this question."""
            ),
        ),
        TydiqaConfig(
            name="secondary_task",
            description=textwrap.dedent(
                """\Gold passage task (GoldP): Given a passage that is guaranteed to contain the 
          answer, predict the single contiguous span of characters that answers the question. This is more similar to 
          existing reading comprehension datasets (as opposed to the information-seeking task outlined above). 
          This task is constructed with two goals in mind: (1) more directly comparing with prior work and (2) providing 
          a simplified way for researchers to use TyDi QA by providing compatibility with existing code for SQuAD 1.1, 
          XQuAD, and MLQA. Toward these goals, the gold passage task differs from the primary task in several ways:
          only the gold answer passage is provided rather than the entire Wikipedia article;
          unanswerable questions have been discarded, similar to MLQA and XQuAD;
          we evaluate with the SQuAD 1.1 metrics like XQuAD; and
         Thai and Japanese are removed since the lack of whitespace breaks some tools.
          """
            ),
        ),
    ]

    def _info(self):
        # TODO(tydiqa): Specifies the nlp.DatasetInfo object
        if self.config.name == "primary_task":
            return nlp.DatasetInfo(
                # This is the description that will appear on the datasets page.
                description=_DESCRIPTION,
                # nlp.features.FeatureConnectors
                features=nlp.Features(
                    {
                        "passage_answer_candidates": nlp.features.Sequence(
                            {"plaintext_start_byte": nlp.Value("int32"), "plaintext_end_byte": nlp.Value("int32")}
                        ),
                        "question_text": nlp.Value("string"),
                        "document_title": nlp.Value("string"),
                        "language": nlp.Value("string"),
                        "annotations": nlp.features.Sequence(
                            {
                                #'annotation_id': nlp.Value('variant'),
                                "passage_answer_candidate_index": nlp.Value("int32"),
                                "minimal_answers_start_byte": nlp.Value("int32"),
                                "minimal_answers_end_byte": nlp.Value("int32"),
                                "yes_no_answer": nlp.Value("string"),
                            }
                        ),
                        "document_plaintext": nlp.Value("string"),
                        # 'example_id': nlp.Value('variant'),
                        "document_url": nlp.Value("string")
                        # These are the features of your dataset like images, labels ...
                    }
                ),
                # If there's a common (input, target) tuple from the features,
                # specify them here. They'll be used if as_supervised=True in
                # builder.as_dataset.
                supervised_keys=None,
                # Homepage of the dataset for documentation
                homepage="https://github.com/google-research-datasets/tydiqa",
                citation=_CITATION,
            )
        elif self.config.name == "secondary_task":
            return nlp.DatasetInfo(
                description=_DESCRIPTION,
                features=nlp.Features(
                    {
                        "id": nlp.Value("string"),
                        "title": nlp.Value("string"),
                        "context": nlp.Value("string"),
                        "question": nlp.Value("string"),
                        "answers": nlp.features.Sequence(
                            {"text": nlp.Value("string"), "answer_start": nlp.Value("int32"),}
                        ),
                    }
                ),
                # No default supervised_keys (as we have to pass both question
                # and context as input).
                supervised_keys=None,
                homepage="https://github.com/google-research-datasets/tydiqa",
                citation=_CITATION,
            )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(tydiqa): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        primary_urls_to_download = {
            "train": os.path.join(_URL, _PRIMARY_TASK_TRAIN),
            "dev": os.path.join(_URL, _PRIMARY_TASK_DEV),
        }
        secondary_urls_to_download = {
            "train": os.path.join(_URL, _SECONDARY_TASK_TRAIN),
            "dev": os.path.join(_URL, _SECONDARY_TASK_DEV),
        }
        primary_downloaded = dl_manager.download_and_extract(primary_urls_to_download)
        secondary_downloaded = dl_manager.download_and_extract(secondary_urls_to_download)
        if self.config.name == "primary_task":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": primary_downloaded["train"]},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": primary_downloaded["dev"]},
                ),
            ]
        elif self.config.name == "secondary_task":
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": secondary_downloaded["train"]},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": secondary_downloaded["dev"]},
                ),
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(tydiqa): Yields (key, example) tuples from the dataset
        if self.config.name == "primary_task":
            with open(filepath) as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    passages = data["passage_answer_candidates"]
                    end_byte = [passage["plaintext_end_byte"] for passage in passages]
                    start_byte = [passage["plaintext_start_byte"] for passage in passages]
                    title = data["document_title"]
                    lang = data["language"]
                    question = data["question_text"]
                    annotations = data["annotations"]
                    annot_ids = [annotation["annotation_id"] for annotation in annotations]
                    yes_no_answers = [annotation["yes_no_answer"] for annotation in annotations]
                    min_answers_end_byte = [
                        annotation["minimal_answer"]["plaintext_end_byte"] for annotation in annotations
                    ]
                    min_answers_start_byte = [
                        annotation["minimal_answer"]["plaintext_start_byte"] for annotation in annotations
                    ]
                    passage_cand_answers = [
                        annotation["passage_answer"]["candidate_index"] for annotation in annotations
                    ]
                    doc = data["document_plaintext"]
                    example_id = data["example_id"]
                    url = data["document_url"]
                    yield id_, {
                        "passage_answer_candidates": {
                            "plaintext_start_byte": start_byte,
                            "plaintext_end_byte": end_byte,
                        },
                        "question_text": question,
                        "document_title": title,
                        "language": lang,
                        "annotations": {
                            #'annotation_id': annot_ids,
                            "passage_answer_candidate_index": passage_cand_answers,
                            "minimal_answers_start_byte": min_answers_start_byte,
                            "minimal_answers_end_byte": min_answers_end_byte,
                            "yes_no_answer": yes_no_answers,
                        },
                        "document_plaintext": doc,
                        #'example_id': example_id,
                        "document_url": url,
                    }
        elif self.config.name == "secondary_task":
            with open(filepath) as f:
                data = json.load(f)
                for article in data["data"]:
                    title = article.get("title", "").strip()
                    for paragraph in article["paragraphs"]:
                        context = paragraph["context"].strip()
                        for qa in paragraph["qas"]:
                            question = qa["question"].strip()
                            id_ = qa["id"]

                            answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                            answers = [answer["text"].strip() for answer in qa["answers"]]

                            # Features currently used are "context", "question", and "answers".
                            # Others are extracted here for the ease of future expansions.
                            yield id_, {
                                "title": title,
                                "context": context,
                                "question": question,
                                "id": id_,
                                "answers": {"answer_start": answer_starts, "text": answers,},
                            }
