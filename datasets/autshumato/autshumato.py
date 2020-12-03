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
"""Autshumato Parallel Corpora"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@article{groenewald2010processing,
  title={Processing parallel text corpora for three South African language pairs in the Autshumato project},
  author={Groenewald, Hendrik J and du Plooy, Liza},
  journal={AfLaT 2010},
  pages={27},
  year={2010}
}
"""

_DESCRIPTION = """\
Multilingual information access is stipulated in the South African constitution. In practise, this
is hampered by a lack of resources and capacity to perform the large volumes of translation
work required to realise multilingual information access. One of the aims of the Autshumato
project is to develop machine translation systems for three South African languages pairs.
"""


class AutshumatoConfig(datasets.BuilderConfig):
    """ BuilderConfig for NewDataset"""

    def __init__(self, langs, zip_file, **kwargs):
        """

        Args:
            pair: the language pair to consider
            zip_file: The location of zip file containing original data
            **kwargs: keyword arguments forwarded to super.
        """
        self.langs = langs
        self.zip_file = zip_file
        super().__init__(**kwargs)


class Autshumato(datasets.GeneratorBasedBuilder):
    """The IWSLT 2017 Evaluation Campaign includes a multilingual TED Talks MT task."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    BUILDER_CONFIG_CLASS = AutshumatoConfig
    BUILDER_CONFIGS = [
        AutshumatoConfig(
            name="autshumato-en-tn",
            description="Autshumato English-Setswana Parallel Corpora",
            version=datasets.Version("1.0.0"),
            langs=("en", "tn"),
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/404/autshumato_english-setswana_parallel_corpora.zip",
        ),
        # This data is protected by a form
        # AutshumatoConfig(
        #     name="autshumato-en-nso",
        #     description="Autshumato English-Sesotho sa Leboa Parallel Corpora",
        #     version=datasets.Version("1.0.0"),
        #     langs=("en", "nso"),
        #     zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/402/en-nso.release.zip",
        # ),
        # This data is protected by a form
        # AutshumatoConfig(
        #     name="autshumato-en-af",
        #     description="Autshumato English-Afrikaans Parallel Corpora",
        #     version=datasets.Version("1.0.0"),
        #     langs=("en", "af"),
        #     zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/397/en-af.release.zip",
        # ),
        AutshumatoConfig(
            name="autshumato-en-zu",
            description="Autshumato English-isiZulu Parallel Corpora",
            version=datasets.Version("1.0.0"),
            langs=("en", "zu"),
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/399/en-zu.release.zip",
        ),
        AutshumatoConfig(
            name="autshumato-en-ts",
            description="Autshumato English-Xitsonga Parallel Corpora",
            version=datasets.Version("1.0.0"),
            langs=("en", "ts"),
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/406/en-ts.completebilingualcorpus.zip",
        ),
        AutshumatoConfig(
            name="autshumato-en-ts-manual",
            description="Autshumato English-Xitsonga Manually Translated Parallel Corpora",
            version=datasets.Version("1.0.0"),
            langs=("en", "ts"),
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/405/en-ts.translationsonlycorpus.zip",
        ),
        AutshumatoConfig(
            name="autshumato-tn",
            description="Autshumato Setswana Monolingual Corpora",
            version=datasets.Version("1.0.0"),
            langs=["tn"],
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/413/autshumato_setswana_monolingual_corpora.zip",
        ),
        AutshumatoConfig(
            name="autshumato-ts",
            description="Autshumato Xitsonga Monolingual Corpora",
            version=datasets.Version("1.0.0"),
            langs=["ts"],
            zip_file="https://repo.sadilar.org/bitstream/handle/20.500.12185/418/ts.monolingualcorpus.zip",
        ),
    ]

    def _info(self):
        if len(self.config.langs) == 2:
            features = datasets.Features({"translation": datasets.features.Translation(languages=self.config.langs)})
        else:
            features = datasets.Features({"text": datasets.Value("string")})

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=features,
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://repo.sadilar.org/handle/20.500.12185/7/discover?filtertype=database&filter_relational_operator=equals&filter=Multilingual+Text+Corpora%3A+Aligned",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if len(self.config.langs) == 2:
            return self._split_generators_translation(dl_manager)
        if len(self.config.langs) == 1:
            return self._split_generators_mono(dl_manager)
        raise NotImplementedError("Can only handle 1 or 2 languages")

    def _split_generators_mono(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.zip_file)

        filenames = set()
        for root, dirs, files in os.walk(dl_dir):
            for filename in files:
                if filename == "README.txt":
                    continue
                filenames.add(os.path.join(dl_dir, root, filename))
        source_filenames = sorted(os.path.join(dl_dir, f) for f in filenames)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "source_files": source_filenames,
                    "target_files": [],
                    "split": "train",
                },
            ),
        ]

    def _split_generators_translation(self, dl_manager):
        source, target = self.config.langs
        dl_dir = dl_manager.download_and_extract(self.config.zip_file)

        filenames = set(os.listdir(dl_dir))
        if len(filenames) == 1:
            dl_dir = os.path.join(dl_dir, list(filenames)[0])
            filenames = set(os.listdir(dl_dir))
        if "README.txt" in filenames:
            filenames.remove("README.txt")

        source_filenames = sorted(
            os.path.join(dl_dir, f) for f in filenames if f.endswith(f"{source}.txt") or ".eng." in f
        )
        target_filenames = sorted(
            os.path.join(dl_dir, f) for f in filenames if f.endswith(f"{target}.txt") or ".zul." in f
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "source_files": source_filenames,
                    "target_files": target_filenames,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, source_files, target_files, split):
        """ Yields examples. """
        if len(self.config.langs) == 2:
            return self._generate_examples_translation(source_files, target_files, split)
        elif len(self.config.langs) == 1:
            return self._generate_examples_mono(source_files, target_files, split)
        raise NotImplementedError("Can only handle 1 or 2 langages")

    def _generate_examples_mono(self, source_files, target_files, split):
        for source_file in source_files:
            with open(source_file, "r", encoding="utf-8") as sf:
                for id_, source_row in enumerate(sf):
                    source_row = source_row.strip()
                    yield id_, {"text": source_row}

    def _generate_examples_translation(self, source_files, target_files, split):
        id_ = 0
        source, target = self.config.langs
        for source_file, target_file in zip(source_files, target_files):
            with open(source_file, "r", encoding="utf-8") as sf:
                with open(target_file, "r", encoding="utf-8") as tf:
                    for source_row, target_row in zip(sf, tf):
                        source_row = source_row.strip()
                        target_row = target_row.strip()

                        yield id_, {"translation": {source: source_row, target: target_row}}
                        id_ += 1
