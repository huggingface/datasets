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
from collections import defaultdict
from typing import Dict, Any, Callable, Optional
from urllib.parse import urlparse

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

_BASE_IMAGE_URLS = {
    "https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip": "VG_100K",
    "https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip": "VG_100K_2",
}
_BASE_IMAGE_METADATA_URL = "https://visualgenome.org/static/data/dataset/image_data.json.zip"

_LATEST_VERSIONS = {
    "region_descriptions": "1.2.0",
    "objects": "1.4.0",
    "attributes": "1.2.0",
    "relationships": "1.4.0",
    "question_answers": "1.2.0"
}

# ---- Features ----

_BASE_FEATURES = {
    "image_id": datasets.Value("int32"),
    "url": datasets.Value("string"),
    "width": datasets.Value("int32"),
    "height": datasets.Value("int32"),
    "coco_id": datasets.Value("int64"),
    "flickr_id": datasets.Value("int64"),
}

_BASE_SYNTET_FEATURES = {
    "synset_name": datasets.Value("string"),
    "entity_name": datasets.Value("string"),
    "entity_idx_start": datasets.Value("int32"),
    "entity_idx_end": datasets.Value("int32")
}

_BASE_OBJECT_FEATURES = {
    "object_id": datasets.Value("int32"),
    "x": datasets.Value("int32"),
    "y": datasets.Value("int32"),
    "w": datasets.Value("int32"),
    "h": datasets.Value("int32"),
    "names": [datasets.Value("string")],
    "synsets": [datasets.Value("string")]
}

_BASE_QA_OBJECT_FEATURES = {
    "object_id": datasets.Value("int32"),
    "x": datasets.Value("int32"),
    "y": datasets.Value("int32"),
    "w": datasets.Value("int32"),
    "h": datasets.Value("int32"),
    "name": datasets.Value("string"),
    "synsets": [datasets.Value("string")]
}

_BASE_QA_OBJECT = {
    "qa_id": datasets.Value("int32"),
    "image_id": datasets.Value("int32"),
    "question": datasets.Value("string"),
    "answer": datasets.Value("string"),
    "a_objects": [_BASE_QA_OBJECT_FEATURES],
    "q_objects": [_BASE_QA_OBJECT_FEATURES],
}

_BASE_REGION_FEATURES = {
    "region_id": datasets.Value("int32"),
    "image_id": datasets.Value("int32"),
    "phrase": datasets.Value("string"),
    "x": datasets.Value("int32"),
    "y": datasets.Value("int32"),
    "width": datasets.Value("int32"),
    "height": datasets.Value("int32"),
}

_BASE_RELATIONSHIP_FEATURES = {
    "relationship_id": datasets.Value("int32"),
    "predicate": datasets.Value("string"),
    "synsets": datasets.Value("string"),
    "subject": _BASE_OBJECT_FEATURES,
    "object": _BASE_OBJECT_FEATURES
}

_NAME_VERSION_TO_ANNOTATION_FEATURES = {
    "region_descriptions": {
        "1.2.0": {"regions": [_BASE_REGION_FEATURES]},
        "1.0.0": {"regions": [_BASE_REGION_FEATURES]}
    },
    "objects": {
        "1.4.0": {"objects": [{**_BASE_OBJECT_FEATURES, "merged_object_ids": [datasets.Value("int32")]}]},
        "1.2.0": {"objects": [_BASE_OBJECT_FEATURES]},
        "1.0.0": {"objects": [_BASE_OBJECT_FEATURES]}
    },
    "attributes": {
        "1.2.0": {
            "objects": [{**_BASE_OBJECT_FEATURES, "attributes": [datasets.Value("string")]}]
        },
        "1.0.0": {
            "objects": [{**_BASE_OBJECT_FEATURES, "attributes": [datasets.Value("string")]}]
        }
    },
    "relationships": {
        "1.4.0": {"relationships": [{
            **_BASE_RELATIONSHIP_FEATURES,
            "subject": {**_BASE_OBJECT_FEATURES, "merged_object_ids": [datasets.Value("int32")]},
            "object": {**_BASE_OBJECT_FEATURES, "merged_object_ids": [datasets.Value("int32")]}
        }]},
        "1.2.0": {"relationships": [_BASE_RELATIONSHIP_FEATURES]},
        "1.0.0": {"relationships": [_BASE_RELATIONSHIP_FEATURES]}
    },
    "question_answers": {
        "1.2.0": {"qas": [_BASE_QA_OBJECT]},
        "1.0.0": {"qas": [_BASE_QA_OBJECT]}
    }
}

# ----- Helpers -----

def _get_decompressed_filename_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    compressed_filename = os.path.basename(parsed_url.path)

    # Remove `.zip` suffix
    assert compressed_filename.endswith(".zip")
    uncompressed_filename = compressed_filename[:-4]

    # Remove version.
    unversioned_uncompressed_filename = re.sub(r"_v[0-9]+_[0-9]+\.json$", ".json", uncompressed_filename)

    return unversioned_uncompressed_filename


def _get_local_image_path(img_url: str, folder_local_paths: Dict[str, str]) -> str:
    """
    Obtain image folder given an image url.

    For example:
      Given `https://cs.stanford.edu/people/rak248/VG_100K_2/1.jpg` as an image url, this method returns the local path for that image.
    """
    matches = re.fullmatch(r"^https://cs.stanford.edu/people/rak248/(VG_100K(?:_2)?)/([0-9]+\.jpg)$", img_url)
    assert matches is not None, matches
    folder, filename = matches.group(1), matches.group(2)
    return os.path.join(folder_local_paths[folder], filename)


# ----- Annotation normalizers ----

_BASE_ANNOTATION_URL = "https://visualgenome.org/static/data/dataset"

# def _normalize_relationship_annotation_(annotation: Dict[str, Any]) -> Dict[str, Any]:
#     """Normalizes relationship annotation in-place"""
#     # For some reason relationships objects have a single name instead of a list of names.
#     for relationship in annotation["relationships"]:
#         subject = relationship["subject"]
#         object_ = relationship["object"]
#
#         subject["names"] = [subject["name"]]
#         del subject["name"]
#
#         object_["names"] = [object_["name"]]
#         del object_["name"]
#     return annotation

def _normalize_attribute_annotation_(annotation: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes attributes annotation in-place"""
    # Some attributes annotations don't have an attribute field
    for attribute in annotation["attributes"]:
        if "attributes" not in attribute:
            attribute["attributes"] = None
    return annotation

_ANNOTATION_NORMALIZER = defaultdict(lambda: lambda x: x)
_ANNOTATION_NORMALIZER.update({
    # "relationships": _normalize_relationship_annotation_,
    "attributes": _normalize_attribute_annotation_
})

# ---- Visual Genome loading script ----

class VisualGenomeConfig(datasets.BuilderConfig):
    """BuilderConfig for Visual Genome."""

    def __init__(
        self,
        name: str,
        version: Optional[str] = None,
        annotations_url: Optional[str] = None,
        with_image: bool = True,
        **kwargs
    ):
        _version = _LATEST_VERSIONS[name] if version is None else version
        _name = f"{name}_v{_version}"
        super(VisualGenomeConfig, self).__init__(
            version=datasets.Version(_version),
            name=_name,
            **kwargs
        )
        self._name_without_version = name
        self.annotations_features = _NAME_VERSION_TO_ANNOTATION_FEATURES[self._name_without_version][self.version.version_str]
        self._annotations_url = annotations_url
        self.with_image = with_image
        
    @property
    def annotations_url(self):
        if self._annotations_url:
            return self._annotations_url

        if self.version.match(_LATEST_VERSIONS[self._name_without_version]):
            return f"{_BASE_ANNOTATION_URL}/{self._name_without_version}.json.zip"

        major, minor = self.version.major, self.version.minor
        return f"{_BASE_ANNOTATION_URL}/{self._name_without_version}_v{major}_{minor}.json.zip"

    @property
    def features(self):
        return datasets.Features({
            **({"image": datasets.Image() if self.with_image else {}}),
            **_BASE_FEATURES,
            **self.annotations_features
        })


class VisualGenome(datasets.GeneratorBasedBuilder):
    """Visual Genome dataset."""

    BUILDER_CONFIG_CLASS = VisualGenomeConfig
    BUILDER_CONFIGS = [
        *[
            VisualGenomeConfig(name="region_descriptions", version=version)
            for version in ["1.0.0", "1.2.0"]
        ],
        *[
            VisualGenomeConfig(name="question_answers", version=version)
            for version in ["1.0.0", "1.2.0"]
        ],
        *[
            VisualGenomeConfig(name="objects", version=version)
            # TODO: add support for 1.4.0
            for version in ["1.0.0", "1.2.0"]
        ],
        *[
            VisualGenomeConfig(name="attributes", version=version)
            for version in ["1.0.0", "1.2.0"]
        ],
        *[

            VisualGenomeConfig(name="relationships", version=version)
            # TODO: add support for 1.4.0
            for version in ["1.0.0", "1.2.0"]
        ],
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=self.config.features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            version=self.config.version
        )

    def _split_generators(self, dl_manager):
        # Download image meta datas.
        image_metadatas_dir = dl_manager.download_and_extract(_BASE_IMAGE_METADATA_URL)
        image_metadatas_file = os.path.join(
            image_metadatas_dir,
            _get_decompressed_filename_from_url(_BASE_IMAGE_METADATA_URL)
        )

        # Download annotations
        annotations_dir = dl_manager.download_and_extract(self.config.annotations_url)
        annotations_file = os.path.join(
            annotations_dir,
            _get_decompressed_filename_from_url(self.config.annotations_url)
        )

        # Optionally download images
        if self.config.with_image:
            image_folder_keys = list(_BASE_IMAGE_URLS.keys())
            image_dirs = dl_manager.download_and_extract(image_folder_keys)
            image_folder_local_paths = {
                _BASE_IMAGE_URLS[key]: os.path.join(dir_, _BASE_IMAGE_URLS[key])
                for key, dir_ in zip(image_folder_keys, image_dirs)
            }
        else:
            image_folder_local_paths = None

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "image_folder_local_paths": image_folder_local_paths,
                    "image_metadatas_file": image_metadatas_file,
                    "annotations_file": annotations_file,
                    "annotation_normalizer_": _ANNOTATION_NORMALIZER[self.config._name_without_version],
                },
            ),
        ]

    def _generate_examples(
        self,
        image_folder_local_paths: Optional[Dict[str, str]],
        image_metadatas_file: str,
        annotations_file: str,
        annotation_normalizer_: Callable[[Dict[str,Any]], Dict[str,Any]]
    ):
        with open(annotations_file, "r", encoding="utf-8") as fi:
            annotations = json.load(fi)

        with open(image_metadatas_file, "r", encoding="utf-8") as fi:
            image_metadatas = json.load(fi)

        assert len(image_metadatas) == len(annotations)
        for idx, (image_metadata, annotation) in enumerate(zip(image_metadatas, annotations)):

            # Normalize image_id across all annotations
            if "id" in annotation:
                # annotation["id"] corresponds to `image_id`
                assert image_metadata["image_id"] == annotation[
                    "id"], f"Annotations doesn't match with image metadataset. Got image_metadata['image_id']: {image_metadata['image_id']} and annotations['id']: {annotation['id']}"
                del annotation["id"]
            elif "image_id" in annotation:
                assert image_metadata["image_id"] == annotation[
                    "image_id"], f"Annotations doesn't match with image metadataset. Got image_metadata['image_id']: {image_metadata['image_id']} and annotations['image_id']: {annotation['image_id']}"

            # in-place operation to normalize annotations
            annotation_normalizer_(annotation)

            # optionally add image to the annotation
            if image_folder_local_paths is not None:
                filepath = _get_local_image_path(image_metadata["url"], image_folder_local_paths)
                image_dict = {"image": filepath}
            else:
                image_dict = {}

            yield idx, {
                **image_dict,
                **image_metadata,
                **annotation
            }
