# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Natural Questions: A Benchmark for Question Answering Research."""


import html
import json
import re

import datasets


_CITATION = """
@article{47761,
title	= {Natural Questions: a Benchmark for Question Answering Research},
author	= {Tom Kwiatkowski and Jennimaria Palomaki and Olivia Redfield and Michael Collins and Ankur Parikh and Chris Alberti and Danielle Epstein and Illia Polosukhin and Matthew Kelcey and Jacob Devlin and Kenton Lee and Kristina N. Toutanova and Llion Jones and Ming-Wei Chang and Andrew Dai and Jakob Uszkoreit and Quoc Le and Slav Petrov},
year	= {2019},
journal	= {Transactions of the Association of Computational Linguistics}
}
"""

_DESCRIPTION = """
The NQ corpus contains questions from real users, and it requires QA systems to
read and comprehend an entire Wikipedia article that may or may not contain the
answer to the question. The inclusion of real user questions, and the
requirement that solutions should read an entire page to find the answer, cause
NQ to be a more realistic and challenging task than prior QA datasets.
"""

_URL = "https://ai.google.com/research/NaturalQuestions/dataset"

_BASE_DOWNLOAD_URL = "https://storage.googleapis.com/natural_questions/v1.0"
_DOWNLOAD_URLS = {
    "train": ["%s/train/nq-train-%02d.jsonl.gz" % (_BASE_DOWNLOAD_URL, i) for i in range(50)],
    "validation": ["%s/dev/nq-dev-%02d.jsonl.gz" % (_BASE_DOWNLOAD_URL, i) for i in range(5)],
}

_VERSION = datasets.Version("0.0.4")


class NaturalQuestions(datasets.BeamBasedBuilder):
    """Natural Questions: A Benchmark for Question Answering Research."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="default", version=_VERSION),
        datasets.BuilderConfig(name="dev", version=_VERSION, description="Only dev split"),
    ]
    DEFAULT_CONFIG_NAME = "default"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "document": {
                        "title": datasets.Value("string"),
                        "url": datasets.Value("string"),
                        "html": datasets.Value("string"),
                        "tokens": datasets.features.Sequence(
                            {
                                "token": datasets.Value("string"),
                                "is_html": datasets.Value("bool"),
                                "start_byte": datasets.Value("int64"),
                                "end_byte": datasets.Value("int64"),
                            }
                        ),
                    },
                    "question": {
                        "text": datasets.Value("string"),
                        "tokens": datasets.features.Sequence(datasets.Value("string")),
                    },
                    "long_answer_candidates": datasets.features.Sequence(
                        {
                            "start_token": datasets.Value("int64"),
                            "end_token": datasets.Value("int64"),
                            "start_byte": datasets.Value("int64"),
                            "end_byte": datasets.Value("int64"),
                            "top_level": datasets.Value("bool"),
                        }
                    ),
                    "annotations": datasets.features.Sequence(
                        {
                            "id": datasets.Value("string"),
                            "long_answer": {
                                "start_token": datasets.Value("int64"),
                                "end_token": datasets.Value("int64"),
                                "start_byte": datasets.Value("int64"),
                                "end_byte": datasets.Value("int64"),
                                "candidate_index": datasets.Value("int64"),
                            },
                            "short_answers": datasets.features.Sequence(
                                {
                                    "start_token": datasets.Value("int64"),
                                    "end_token": datasets.Value("int64"),
                                    "start_byte": datasets.Value("int64"),
                                    "end_byte": datasets.Value("int64"),
                                    "text": datasets.Value("string"),
                                }
                            ),
                            "yes_no_answer": datasets.features.ClassLabel(
                                names=["NO", "YES"]
                            ),  # Can also be -1 for NONE.
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager, pipeline):
        """Returns SplitGenerators."""
        urls = _DOWNLOAD_URLS
        if self.config.name == "dev":
            urls = {"validation": urls["validation"]}
        files = dl_manager.download(urls)
        if not pipeline.is_local():
            files = dl_manager.ship_files_with_pipeline(files, pipeline)
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={"filepaths": files[split]},
            )
            for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION]
            if split in files
        ]

    def _build_pcollection(self, pipeline, filepaths):
        """Build PCollection of examples."""
        try:
            import apache_beam as beam
        except ImportError as err:
            raise ImportError(
                "To be able to load natural_questions, you need to install apache_beam: 'pip install apache_beam'"
            ) from err

        def _parse_example(line):
            """Parse a single json line and emit an example dict."""
            ex_json = json.loads(line)
            html_bytes = ex_json["document_html"].encode("utf-8")

            def _parse_short_answer(short_ans):
                """Extract text of short answer."""
                ans_bytes = html_bytes[short_ans["start_byte"] : short_ans["end_byte"]]
                # Remove non-breaking spaces.
                ans_bytes = ans_bytes.replace(b"\xc2\xa0", b" ")
                text = ans_bytes.decode("utf-8")
                # Remove HTML markup.
                text = re.sub("<([^>]*)>", "", html.unescape(text))
                # Replace \xa0 characters with spaces.
                return {
                    "start_token": short_ans["start_token"],
                    "end_token": short_ans["end_token"],
                    "start_byte": short_ans["start_byte"],
                    "end_byte": short_ans["end_byte"],
                    "text": text,
                }

            def _parse_annotation(an_json):
                return {
                    # Convert to str since some IDs cannot be represented by datasets.Value('int64').
                    "id": str(an_json["annotation_id"]),
                    "long_answer": {
                        "start_token": an_json["long_answer"]["start_token"],
                        "end_token": an_json["long_answer"]["end_token"],
                        "start_byte": an_json["long_answer"]["start_byte"],
                        "end_byte": an_json["long_answer"]["end_byte"],
                        "candidate_index": an_json["long_answer"]["candidate_index"],
                    },
                    "short_answers": [_parse_short_answer(ans) for ans in an_json["short_answers"]],
                    "yes_no_answer": (-1 if an_json["yes_no_answer"] == "NONE" else an_json["yes_no_answer"]),
                }

            beam.metrics.Metrics.counter("nq", "examples").inc()
            # Convert to str since some IDs cannot be represented by datasets.Value('int64').
            id_ = str(ex_json["example_id"])
            return (
                id_,
                {
                    "id": id_,
                    "document": {
                        "title": ex_json["document_title"],
                        "url": ex_json["document_url"],
                        "html": ex_json["document_html"],
                        "tokens": [
                            {
                                "token": t["token"],
                                "is_html": t["html_token"],
                                "start_byte": t["start_byte"],
                                "end_byte": t["end_byte"],
                            }
                            for t in ex_json["document_tokens"]
                        ],
                    },
                    "question": {"text": ex_json["question_text"], "tokens": ex_json["question_tokens"]},
                    "long_answer_candidates": [lac_json for lac_json in ex_json["long_answer_candidates"]],
                    "annotations": [_parse_annotation(an_json) for an_json in ex_json["annotations"]],
                },
            )

        return (
            pipeline
            | beam.Create(filepaths)
            | beam.io.ReadAllFromText(compression_type=beam.io.textio.CompressionTypes.GZIP)
            | beam.Map(_parse_example)
        )
