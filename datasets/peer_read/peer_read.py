# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""A Dataset of Peer Reviews (PeerRead): Collection, Insights and NLP Applications"""


import glob
import json
import os

import datasets


_CITATION = """\
@inproceedings{kang18naacl,
  title = {A Dataset of Peer Reviews (PeerRead): Collection, Insights and NLP Applications},
  author = {Dongyeop Kang and Waleed Ammar and Bhavana Dalvi and Madeleine van Zuylen and Sebastian Kohlmeier and Eduard Hovy and Roy Schwartz},
  booktitle = {Meeting of the North American Chapter of the Association for Computational Linguistics (NAACL)},
  address = {New Orleans, USA},
  month = {June},
  url = {https://arxiv.org/abs/1804.09635},
  year = {2018}
}
"""

_DESCRIPTION = """\
PearRead is a dataset of scientific peer reviews available to help researchers study this important artifact. The dataset consists of over 14K paper drafts and the corresponding accept/reject decisions in top-tier venues including ACL, NIPS and ICLR, as well as over 10K textual peer reviews written by experts for a subset of the papers.
"""

_HOMEPAGE = "https://github.com/allenai/PeerRead"

_LICENSE = "Creative Commons Public License"

_URLs = {
    "dataset_repo": "https://github.com/allenai/PeerRead/archive/master.zip",
}


class PeerRead(datasets.GeneratorBasedBuilder):
    """A Dataset of Peer Reviews (PeerRead): Collection, Insights and NLP Applications"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="parsed_pdfs",
            version=VERSION,
            description="Research paper drafts",
        ),
        datasets.BuilderConfig(
            name="reviews",
            version=VERSION,
            description="Accept/reject decisions in top-tier venues including ACL, NIPS and ICLR",
        ),
    ]

    @staticmethod
    def _get_paths(data_dir, domain):
        paths = {"train": [], "test": [], "dev": []}
        conference_paths = glob.glob(os.path.join(data_dir, "PeerRead-master/data/*"))
        for conference_path in conference_paths:
            for dtype in ["test", "train", "dev"]:
                file_paths = glob.glob(os.path.join(conference_path, dtype, domain, "*.json"))
                for file_path in file_paths:
                    paths[dtype].append(file_path)
        return paths

    @staticmethod
    def _parse_histories(histories):
        if histories is None:
            return [[]]
        if isinstance(histories, str):
            return [[histories]]
        return histories

    @staticmethod
    def _parse_reviews(data):
        reviews = []
        for review in data.get("metadata", {}).get("reviews", []):
            if isinstance(review, dict):
                reviews.append(
                    {
                        "date": str(review.get("date", "")),
                        "title": str(review.get("title", "")),
                        "other_keys": str(review.get("other_keys", "")),
                        "originality": str(review.get("originality", "")),
                        "comments": str(review.get("comments", "")),
                        "is_meta_review": str(review.get("is_meta_review", "")),
                        "is_annotated": str(review.get("is_annotated", "")),
                        "recommendation": str(review.get("recommendation", "")),
                        "replicability": str(review.get("replicability", "")),
                        "presentation_format": str(review.get("presentation_format", "")),
                        "clarity": str(review.get("clarity", "")),
                        "meaningful_comparison": str(review.get("meaningful_comparison", "")),
                        "substance": str(review.get("substance", "")),
                        "reviewer_confidence": str(review.get("reviewer_confidence", "")),
                        "soundness_correctness": str(review.get("soundness_correctness", "")),
                        "appropriateness": str(review.get("appropriateness", "")),
                        "impact": str(review.get("impact")),
                    }
                )
        return reviews

    @staticmethod
    def _decode(text):
        return str(text).encode("utf-8", "replace").decode("utf-8")

    def _info(self):
        if (
            self.config.name == "parsed_pdfs"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "name": datasets.Value("string"),
                    "metadata": {
                        "source": datasets.Value("string"),
                        "title": datasets.Value("string"),
                        "authors": datasets.features.Sequence(datasets.Value("string")),
                        "emails": datasets.features.Sequence(datasets.Value("string")),
                        "sections": datasets.features.Sequence(
                            {
                                "heading": datasets.Value("string"),
                                "text": datasets.Value("string"),
                            }
                        ),
                        "references": datasets.features.Sequence(
                            {
                                "title": datasets.Value("string"),
                                "author": datasets.features.Sequence(datasets.Value("string")),
                                "venue": datasets.Value("string"),
                                "citeRegEx": datasets.Value("string"),
                                "shortCiteRegEx": datasets.Value("string"),
                                "year": datasets.Value("int32"),
                            }
                        ),
                        "referenceMentions": datasets.features.Sequence(
                            {
                                "referenceID": datasets.Value("int32"),
                                "context": datasets.Value("string"),
                                "startOffset": datasets.Value("int32"),
                                "endOffset": datasets.Value("int32"),
                            }
                        ),
                        "year": datasets.Value("int32"),
                        "abstractText": datasets.Value("string"),
                        "creator": datasets.Value("string"),
                    },
                }
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "conference": datasets.Value("string"),
                    "comments": datasets.Value("string"),
                    "subjects": datasets.Value("string"),
                    "version": datasets.Value("string"),
                    "date_of_submission": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "authors": datasets.features.Sequence(datasets.Value("string")),
                    "accepted": datasets.Value("bool"),
                    "abstract": datasets.Value("string"),
                    "histories": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                    "reviews": datasets.features.Sequence(
                        {
                            "date": datasets.Value("string"),
                            "title": datasets.Value("string"),
                            "other_keys": datasets.Value("string"),
                            "originality": datasets.Value("string"),
                            "comments": datasets.Value("string"),
                            "is_meta_review": datasets.Value("bool"),
                            "is_annotated": datasets.Value("bool"),
                            "recommendation": datasets.Value("string"),
                            "replicability": datasets.Value("string"),
                            "presentation_format": datasets.Value("string"),
                            "clarity": datasets.Value("string"),
                            "meaningful_comparison": datasets.Value("string"),
                            "substance": datasets.Value("string"),
                            "reviewer_confidence": datasets.Value("string"),
                            "soundness_correctness": datasets.Value("string"),
                            "appropriateness": datasets.Value("string"),
                            "impact": datasets.Value("string"),
                        }
                    ),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        url = _URLs["dataset_repo"]
        data_dir = dl_manager.download_and_extract(url)
        paths = self._get_paths(
            data_dir=data_dir,
            domain=self.config.name,
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths": paths["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepaths": paths["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepaths": paths["dev"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepaths, split):
        """Yields examples."""
        for id_, filepath in enumerate(sorted(filepaths)):
            with open(filepath, encoding="utf-8", errors="replace") as f:
                data = json.load(f)
                if self.config.name == "parsed_pdfs":
                    metadata = data.get(
                        "metadata",
                        {
                            "source": "",
                            "authors": [],
                            "title": [],
                            "sections": [],
                            "references": [],
                            "referenceMentions": [],
                            "year": "",
                            "abstractText": "",
                            "creator": "",
                        },
                    )
                    metadata["sections"] = [] if metadata["sections"] is None else metadata["sections"]
                    metadata["sections"] = [
                        {
                            "heading": self._decode(section.get("heading", "")),
                            "text": self._decode(section.get("text", "")),
                        }
                        for section in metadata["sections"]
                    ]
                    metadata["references"] = [] if metadata["references"] is None else metadata["references"]
                    metadata["references"] = [
                        {
                            "title": reference.get("title", ""),
                            "author": reference.get("author", []),
                            "venue": reference.get("venue", ""),
                            "citeRegEx": reference.get("citeRegEx", ""),
                            "shortCiteRegEx": reference.get("shortCiteRegEx", ""),
                            "year": reference.get("year", ""),
                        }
                        for reference in metadata["references"]
                    ]
                    metadata["referenceMentions"] = (
                        [] if metadata["referenceMentions"] is None else metadata["referenceMentions"]
                    )
                    metadata["referenceMentions"] = [
                        {
                            "referenceID": self._decode(reference_mention.get("referenceID", "")),
                            "context": self._decode(reference_mention.get("context", "")),
                            "startOffset": self._decode(reference_mention.get("startOffset", "")),
                            "endOffset": self._decode(reference_mention.get("endOffset", "")),
                        }
                        for reference_mention in metadata["referenceMentions"]
                    ]

                    yield id_, {
                        "name": data.get("name", ""),
                        "metadata": metadata,
                    }
                elif self.config.name == "reviews":
                    yield id_, {
                        "id": str(data.get("id", "")),
                        "conference": str(data.get("conference", "")),
                        "comments": str(data.get("comments", "")),
                        "subjects": str(data.get("subjects", "")),
                        "version": str(data.get("version", "")),
                        "date_of_submission": str(data.get("date_of_submission", "")),
                        "title": str(data.get("title", "")),
                        "authors": data.get("authors", [])
                        if isinstance(data.get("authors"), list)
                        else ([data.get("authors")] if data.get("authors") else []),
                        "accepted": str(data.get("accepted", "")),
                        "abstract": str(data.get("abstract", "")),
                        "histories": self._parse_histories(data.get("histories", [])),
                        "reviews": self._parse_reviews(data),
                    }
