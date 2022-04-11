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
"""Visual Genome dataset."""


import json
import os
import re
from urllib.parse import urlparse
from pathlib import Path

import datasets


_CITATION = """\
@inproceedings{krishnavisualgenome,
  title={Visual Genome: Connecting Language and Vision Using Crowdsourced Dense Image Annotations},
  author={Krishna, Ranjay and Zhu, Yuke and Groth, Oliver and Johnson, Justin and Hata, Kenji and Kravitz, Joshua and Chen, Stephanie and Kalantidis, Yannis and Li, Li-Jia and Shamma, David A and Bernstein, Michael and Fei-Fei, Li},
  year = {2016},
  url = {https://arxiv.org/abs/1602.07332},
}
"""

_DESCRIPTION = """\
Visual Genome enable to model objects and relationshipt between objects.
They collect dense annotations of objects, attributes, and relationships within each image.
Specifically, the dataset contains over 108K images where each image has an average of 35 objects, 26 attributes, and 21 pairwise relationships between objects.
"""

_HOMEPAGE = "https://visualgenome.org/"

_LICENSE = "Creative Commons Attribution 4.0 International License"

_BASE_IMAGE_URLS = [
    "https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip",
    "https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip"
]
_BASE_IMAGE_METADATA_URL = "https://visualgenome.org/static/data/dataset/image_data.json.zip"

_BASE_FEATURES = {
    "image_id": datasets.Value("int32"),
    "url": datasets.Value("string"),
    "width": datasets.Value("int32"),
    "height": datasets.Value("int32"),
    "coco_id": datasets.Value("int64"),
    "flickr_id": datasets.Value("int64"),
}

_SYNTET_FEATURES = {
    "synset_name": datasets.Value("string"),
    "entity_name": datasets.Value("string"),
    "entity_idx_start": datasets.Value("int32"),
    "entity_idx_end": datasets.Value("int32")
}

_OBJECT_FEATURES = {
    "object_id": datasets.Value("int32"),
    "x": datasets.Value("int32"),
    "y": datasets.Value("int32"),
    "w": datasets.Value("int32"),
    "h": datasets.Value("int32"),
    "names": datasets.Sequence(feature=datasets.Value("string")),
    "synsets": datasets.Sequence(feature=datasets.Value("string"))
}

def _get_decompressed_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    compressed_filename = os.path.basename(parsed_url.path)

    # Remove `.zip` suffix
    assert compressed_filename.endswith(".zip")
    uncompressed_filename = compressed_filename[:-4]

    # Remove version.
    unversioned_uncompressed_filename = re.sub(r"_v[0-9]+_[0-9]+\.json$", ".json", uncompressed_filename)

    return unversioned_uncompressed_filename

class VisualGenomeConfig(datasets.BuilderConfig):
    """BuilderConfig for Visual Genome."""

    def __init__(
        self, 
        name: str, 
        annotation_features: datasets.Features,
        annotations_url: str,
        version: datasets.Version, 
        merge_with_image_metadata: bool = True,
        **kwargs
    ):
        super(VisualGenomeConfig, self).__init__(version=version, name=name, **kwargs)
        self.annotations_features = annotation_features
        self.annotations_url = annotations_url
        self.merge_with_image_metadata = merge_with_image_metadata

    @property
    def features(self):
        return datasets.Features({
            **_BASE_FEATURES,
            **self.annotations_features
        })

class VisualGenome(datasets.GeneratorBasedBuilder):
    """Visual Genome dataset."""

    BUILDER_CONFIGS = [
        VisualGenomeConfig(
            name="region-descriptions",
            annotation_features=datasets.Features({
                "regions": datasets.Sequence(
                    feature={
                        "region_id": datasets.Value("int32"),
                        "image_id": datasets.Value("int32"),
                        "phrase": datasets.Value("string"),
                        "x": datasets.Value("int32"),
                        "y": datasets.Value("int32"),
                        "width": datasets.Value("int32"),
                        "height": datasets.Value("int32"),
                        # "synsets": datasets.Sequence(
                        #     feature=_SYNTET_FEATURES
                        # )
                    }
                )
            }),
            annotations_url="https://visualgenome.org/static/data/dataset/region_descriptions.json.zip",
            version=datasets.Version("1.2.0")
        ),
        VisualGenomeConfig(
            name="question-answering",
            annotation_features=datasets.Features({
                "qas": datasets.Sequence(
                    feature={
                        "qa_id": datasets.Value("int32"),
                        "image_id": datasets.Value("int32"),
                        "question": datasets.Value("string"),
                        "answer": datasets.Value("string"),
                        "a_objects": datasets.Sequence(
                            feature=_OBJECT_FEATURES
                        ),
                        "q_objects": datasets.Sequence(
                            feature=_OBJECT_FEATURES
                        )
                    }
                )
            }),
            annotations_url="https://visualgenome.org/static/data/dataset/question_answers.json.zip",
            version=datasets.Version("1.2.0")
        ),
        VisualGenomeConfig(
            name="objects",
            annotation_features=datasets.Features({
                "objects": datasets.Sequence(
                    feature=_OBJECT_FEATURES
                )
            }),
            annotations_url="https://visualgenome.org/static/data/dataset/objects_v1_2.json.zip",
            version=datasets.Version("1.2.0")
        ),
        VisualGenomeConfig(
            name="objects-attributes",
            annotation_features=datasets.Features({
                "attributes": datasets.Sequence(
                    feature={
                        **_OBJECT_FEATURES,
                        "attributes": datasets.Sequence(feature=datasets.Value("string")),
                    }
                )
            }),
            annotations_url="https://visualgenome.org/static/data/dataset/attributes.json.zip",
            version=datasets.Version("1.2.0")
        ),
        VisualGenomeConfig(
            name="relationships",
            annotation_features=datasets.Features({
                "relationships": datasets.Sequence(
                    feature={
                        "relationship_id": datasets.Value("int32"),
                        "predicate": datasets.Value("string"),
                        "synsets": datasets.Value("string"),
                        "subject": _OBJECT_FEATURES,
                        "object": _OBJECT_FEATURES
                    }
                )
            }),
            annotations_url="https://visualgenome.org/static/data/dataset/relationships_v1_2.json.zip",
            version=datasets.Version("1.2.0")
        ),
        # VisualGenomeConfig(
        #     name="synsets",
        #     annotation_features=datasets.Features({
        #         "synset_name": datasets.Value("string"),
        #         "synset_definition":datasets.Value("string"),
        #     }),
        #     merge_with_image_metadata=False,
        #     annotations_url="https://visualgenome.org/static/data/dataset/synsets.json.zip",
        #     version=datasets.Version("1.2.0")
        # ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=self.config.features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        image_metadatas_dir = dl_manager.download_and_extract(_BASE_IMAGE_METADATA_URL)
        image_metadatas_file = f"{image_metadatas_dir}/{_get_decompressed_filename_from_url(_BASE_IMAGE_METADATA_URL)}"
        print(image_metadatas_file)
        annotations_dir = dl_manager.download_and_extract(self.config.annotations_url)
        annotations_file = f"{annotations_dir}/{_get_decompressed_filename_from_url(self.config.annotations_url)}"
        print(annotations_file)
        image_dirs = dl_manager.download_and_extract(_BASE_IMAGE_URLS)
        print(image_dirs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "image_dirs": image_dirs,
                    "image_metadatas_file": image_metadatas_file,
                    "annotations_file": annotations_file,
                },
            ),
        ]

    def _generate_examples(self, image_dirs, image_metadatas_file, annotations_file):
        with open(annotations_file, "r", encoding="utf-8") as fi:
            annotations = json.load(fi)

        with open(image_metadatas_file, "r", encoding="utf-8") as fi:
            image_metadatas = json.load(fi)

        assert len(image_metadatas) == len(annotations)
        for idx, (image_metadata, annotation) in enumerate(zip(image_metadatas, annotations)):

            if "id" in annotation:
                # annotation["id"] corresponds to `image_id`
                assert image_metadata["image_id"] == annotation[
                    "id"], f"Annotations doesn't match with image metadataset. Got image_metadata['image_id']: {image_metadata['image_id']} and annotations['id']: {annotation['id']}"
                del annotation["id"]
            elif "image_id" in annotation:
                assert image_metadata["image_id"] == annotation[
                    "image_id"], f"Annotations doesn't match with image metadataset. Got image_metadata['image_id']: {image_metadata['image_id']} and annotations['image_id']: {annotation['image_id']}"

            # For some reason relationships objects have a single name instead of a list of names.
            if "relationships" in annotation:
                for relationship in annotation["relationships"]:
                    subject = relationship["subject"]
                    object_ = relationship["object"]

                    subject["names"] = [subject["name"]]
                    del subject["name"]

                    object_["names"] = [object_["name"]]
                    del object_["name"]

            # TODO: @thomasw21 sometimes attributes isn't here when annotation is attributes ...
            if "attributes" in annotation:
                for attribute in annotation["attributes"]:
                    if "attributes" not in attribute:
                        attribute["attributes"] = None

            yield idx, {
                **image_metadata,
                **annotation
            }
        # return
