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

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{vivos:2016,
Address = {Ho Chi Minh, Vietnam}
title = {VIVOS: 15 hours of recording speech prepared for Vietnamese Automatic Speech Recognition},
author={Prof. Vu Hai Quan},
year={2016}
}
"""

_DESCRIPTION = """\
VIVOS is a free Vietnamese speech corpus consisting of 15 hours of recording speech prepared for
Vietnamese Automatic Speech Recognition task.
The corpus was prepared by AILAB, a computer science lab of VNUHCM - University of Science, with Prof. Vu Hai Quan is the head of.
We publish this corpus in hope to attract more scientists to solve Vietnamese speech recognition problems.
"""

_HOMEPAGE = "https://ailab.hcmus.edu.vn/vivos"

_LICENSE = "cc-by-sa-4.0"

_DATA_URL = "https://ailab.hcmus.edu.vn/assets/vivos.tar.gz"

_PROMPTS_URLS = {
    "train": "https://s3.amazonaws.com/datasets.huggingface.co/vivos/train/prompts.txt",
    "test": "https://s3.amazonaws.com/datasets.huggingface.co/vivos/test/prompts.txt",
}


class VivosDataset(datasets.GeneratorBasedBuilder):
    """VIVOS is a free Vietnamese speech corpus consisting of 15 hours of recording speech prepared for
    Vietnamese Automatic Speech Recognition task."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "speaker_id": datasets.Value("string"),
                    "path": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "sentence": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        prompts_paths = dl_manager.download(_PROMPTS_URLS)
        archive = dl_manager.download(_DATA_URL)
        train_dir = "vivos/train"
        test_dir = "vivos/test"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "prompts_path": prompts_paths["train"],
                    "path_to_clips": train_dir + "/waves",
                    "audio_files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "prompts_path": prompts_paths["test"],
                    "path_to_clips": test_dir + "/waves",
                    "audio_files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, prompts_path, path_to_clips, audio_files):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        examples = {}
        with open(prompts_path, encoding="utf-8") as f:
            for row in f:
                data = row.strip().split(" ", 1)
                speaker_id = data[0].split("_")[0]
                audio_path = "/".join([path_to_clips, speaker_id, data[0] + ".wav"])
                examples[audio_path] = {
                    "speaker_id": speaker_id,
                    "path": audio_path,
                    "sentence": data[1],
                }
        inside_clips_dir = False
        id_ = 0
        for path, f in audio_files:
            if path.startswith(path_to_clips):
                inside_clips_dir = True
                if path in examples:
                    audio = {"path": path, "bytes": f.read()}
                    yield id_, {**examples[path], "audio": audio}
                    id_ += 1
            elif inside_clips_dir:
                break
