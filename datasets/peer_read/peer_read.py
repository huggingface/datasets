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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
authors={huggingface, Inc.
},
year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve this great NLP task and is crafted with a lot of care. 
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "dataset_repo": "https://github.com/allenai/PeerRead/archive/master.zip",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class NewDataset(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="parsed_pdfs", version=VERSION, description="This part of my dataset covers a first domain"),
        datasets.BuilderConfig(name="reviews", version=VERSION, description="This part of my dataset covers a second domain"),
    ]

    def _info(self):
        # TODO: This method pecifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "parsed_pdfs":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "name": datasets.Value("string"),
                    "metadata": {
                        "source": datasets.Value("string"),
                        "title": datasets.Value("string"),
                        "authors": datasets.features.Sequence(datasets.Value("string")),
                        "emails": datasets.features.Sequence(datasets.Value("string")),
                        "sections": datasets.features.Sequence({
                            "heading": datasets.Value("string"),
                            "text": datasets.Value("string"),
                        }),
                        "references": datasets.features.Sequence({
                            "title": datasets.Value("string"),
                            "author": datasets.features.Sequence(datasets.Value("string")),
                            "venue": datasets.Value("string"),
                            "citeRegEx": datasets.Value("string"),
                            "shortCiteRegEx": datasets.Value("string"),
                            "year": datasets.Value("int32"),
                        }),
                        "referenceMentions": datasets.features.Sequence({
                            "referenceID": datasets.Value("int32"),
                            "context": datasets.Value("string"),
                            "startOffset": datasets.Value("int32"),
                            "endOffset": datasets.Value("int32"),
                        }),
                        "year": datasets.Value("int32"),
                        "abstractText": datasets.Value("string"),
                        "creator": datasets.Value("string"),
                    }
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
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
                    "histories": datasets.features.Sequence(
                        datasets.features.Sequence(datasets.Value("string"))
                    ),
                    "reviews": datasets.features.Sequence({
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
                    })
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    @staticmethod
    def _get_paths(data_dir, domain):
        paths = {
            'train': [], 'test': [], 'dev': [],
        }
        parent_dirpth, conferences, _ = next(os.walk(f'{data_dir}/PeerRead-master/data'))
        for conference in conferences:
            dirpth, data_types, _ = next(os.walk(f'{parent_dirpth}/{conference}'))
            for data_type in data_types:
                for sub_dirpth, _, fnames in sorted(os.walk(f'{dirpth}/{data_type}/{domain}')):
                    for fname in sorted(fnames):
                        paths[data_type].append(f'{sub_dirpth}/{fname}')

        return paths

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        url = _URLs["dataset_repo"]
        # data_dir = dl_manager.download_and_extract(url)
        data_dir = '/Users/vinay/.cache/huggingface/datasets/downloads/extracted/64c0256152da8883e4ab77c89dd07012e40c69f8b514f74411001e4375e94e17'
        paths = self._get_paths(
            data_dir=data_dir, domain=self.config.name,
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
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": paths["test"],
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": paths["dev"],
                    "split": "dev",
                },
            ),
        ]

    @staticmethod
    def _parse_histories(histories):
        if histories is None:
            return [[]]
        if isinstance(histories, str):
            return [[histories]]
        return histories

    def _generate_examples(self, filepaths, split):
        """ Yields examples. """
        for id_, filepath in enumerate(filepaths):
            print(id_)
            try:
                with open(filepath, encoding="utf-8") as f:
                    data = json.load(f)
                    if id_ == 9999:
                        print(filepath)
                    if self.config.name == "parsed_pdfs":
                        temp = {
                            "name": data.get("name", ""),
                            "metadata": {
                                "source": data.get("metadata", {}).get("source", ""),
                                "title": data.get("metadata", {}).get("title", ""),
                                "authors": data.get("metadata", {}).get("authors", []),
                                "emails": data.get("metadata", {}).get("emails", []),
                                "sections": [{
                                    "heading": section.get("heading", ""),
                                    "text": section.get("text", ""),
                                } if isinstance(section, dict) else {}
                                     for section in data.get("metadata", {}).get("sections", [])] if isinstance(data.get("metadata", {}).get("sections", []), list) else [],
                                "references": [{
                                    "title": reference.get("title", ""),
                                    "author": reference.get("author", []),
                                    "venue": reference.get("venue", ""),
                                    "citeRegEx": reference.get("citeRegEx", ""),
                                    "shortCiteRegEx": reference.get("shortCiteRegEx", ""),
                                    "year": reference.get("year", ""),
                                } if isinstance(reference, dict) else {} for reference in data.get("metadata", {}).get("references", [])],
                                "referenceMentions": [{
                                    "referenceID": reference_mention.get("referenceID", ""),
                                    "context": reference_mention.get("context", ""),
                                    "startOffset": reference_mention.get("startOffset", ""),
                                    "endOffset": reference_mention.get("endOffset", ""),
                                } if isinstance(reference_mention, dict) else {} for reference_mention in data.get("metadata", {}).get("referenceMentions", [])],
                                "year": data.get("metadata", {}).get("year", ""),
                                "abstractText": data.get("metadata", {}).get("abstractText", ""),
                                "creator": data.get("metadata", {}).get("creator", ""),
                            }
                        }
                        print('done')
                        yield id_, temp
                    else:
                        temp2 = {
                            "id": data.get("id", ""),
                            "conference": data.get("conference", ""),
                            "comments": data.get("comments", ""),
                            "subjects": data.get("subjects", ""),
                            "version": data.get("version", ""),
                            "date_of_submission": data.get("date_of_submission", ""),
                            "title": data.get("title", ""),
                            "authors": data.get("authors", []) if isinstance(data.get("authors"), list) else [data.get("authors", "")],
                            "accepted": data.get("accepted", ""),
                            "abstract": data.get("abstract", ""),
                            "histories": self._parse_histories(data.get("histories", [])),
                            "reviews": [{
                                "date": review.get("date", ""),
                                "title": review.get("title", ""),
                                "other_keys": review.get("other_keys", ""),
                                "originality": review.get("originality", ""),
                                "comments": review.get("comments", ""),
                                "is_meta_review": review.get("is_meta_review", ""),
                                "is_annotated": review.get("is_annotated", ""),
                                "recommendation": review.get("recommendation", ""),
                                "replicability": review.get("replicability", ""),
                                "presentation_format": review.get("presentation_format", ""),
                                "clarity": review.get("clarity", ""),
                                "meaningful_comparison": review.get("meaningful_comparison", ""),
                                "substance": review.get("substance", ""),
                                "reviewer_confidence": review.get("reviewer_confidence", ""),
                                "soundness_correctness": review.get("soundness_correctness", ""),
                                "appropriateness": review.get("appropriateness", ""),
                                "impact": review.get("impact"),
                            } if isinstance(review, dict) else {} for review in data.get("metadata", {}).get("reviews", [])]
                        }
                        if id_ >= 9998:
                            print(f'fp: {filepath}')
                            print(temp2)
                        yield id_, temp2
            except Exception as e:
                print(e)
