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
"""Write & Improve (Yannakoudakis et al., 2018) is an online web platform that assists non-native
English students with their writing. Specifically, students from around the world submit letters,
stories, articles and essays in response to various prompts, and the W&I system provides instant
feedback. Since W&I went live in 2014, W&I annotators have manually annotated some of these
submissions and assigned them a CEFR level.

The LOCNESS corpus (Granger, 1998) consists of essays written by native English students.
It was originally compiled by researchers at the Centre for English Corpus Linguistics at the
University of Louvain. Since native English students also sometimes make mistakes, we asked
the W&I annotators to annotate a subsection of LOCNESS so researchers can test the effectiveness
of their systems on the full range of English levels and abilities."""


import json

import datasets


_CITATION = """\
@inproceedings{bryant-etal-2019-bea,
    title = "The {BEA}-2019 Shared Task on Grammatical Error Correction",
    author = "Bryant, Christopher  and
        Felice, Mariano  and
        Andersen, {\\O}istein E.  and
        Briscoe, Ted",
    booktitle = "Proceedings of the Fourteenth Workshop on Innovative Use of NLP for Building Educational Applications",
    month = aug,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-4406",
    doi = "10.18653/v1/W19-4406",
    pages = "52--75",
    abstract = "This paper reports on the BEA-2019 Shared Task on Grammatical Error Correction (GEC). As with the CoNLL-2014 shared task, participants are required to correct all types of errors in test data. One of the main contributions of the BEA-2019 shared task is the introduction of a new dataset, the Write{\\&}Improve+LOCNESS corpus, which represents a wider range of native and learner English levels and abilities. Another contribution is the introduction of tracks, which control the amount of annotated data available to participants. Systems are evaluated in terms of ERRANT F{\\_}0.5, which allows us to report a much wider range of performance statistics. The competition was hosted on Codalab and remains open for further submissions on the blind test set.",
}
"""

_DESCRIPTION = """\
Write & Improve (Yannakoudakis et al., 2018) is an online web platform that assists non-native
English students with their writing. Specifically, students from around the world submit letters,
stories, articles and essays in response to various prompts, and the W&I system provides instant
feedback. Since W&I went live in 2014, W&I annotators have manually annotated some of these
submissions and assigned them a CEFR level.
"""

_HOMEPAGE = "https://www.cl.cam.ac.uk/research/nl/bea2019st/#data"

_LICENSE = ""

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://www.cl.cam.ac.uk/research/nl/bea2019st/data/wi+locness_v2.1.bea19.tar.gz"


class WiLocness(datasets.GeneratorBasedBuilder):
    """\
Write & Improve (Yannakoudakis et al., 2018) is an online web platform that assists non-native
English students with their writing. Specifically, students from around the world submit letters,
stories, articles and essays in response to various prompts, and the W&I system provides instant
feedback. Since W&I went live in 2014, W&I annotators have manually annotated some of these
submissions and assigned them a CEFR level."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="wi",
            version=VERSION,
            description="This part of the dataset includes the Write & Improve data for levels A, B and C",
        ),
        datasets.BuilderConfig(
            name="locness",
            version=VERSION,
            description="This part of the dataset includes the Locness part of the W&I-Locness dataset",
        ),
    ]

    # DEFAULT_CONFIG_NAME = "first_domain"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        if self.config.name == "wi":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "userid": datasets.Value("string"),
                    "cefr": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "edits": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                        }
                    ),
                }
            )
        elif self.config.name == "locness":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "cefr": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "edits": datasets.Sequence(
                        {
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "text": datasets.Value("string"),
                        }
                    ),
                }
            )
        else:
            assert False
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

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        archive = dl_manager.download(_URL)
        data_dir = "wi+locness/json"

        if self.config.name == "wi":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"data_dir": data_dir, "split": "train", "files": dl_manager.iter_archive(archive)},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "data_dir": data_dir,
                        "split": "validation",
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]
        elif self.config.name == "locness":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "data_dir": data_dir,
                        "split": "validation",
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]
        else:
            assert False

    def _generate_examples(self, data_dir, split, files):
        """Yields examples."""

        if split == "validation":
            split = "dev"

        if self.config.name == "wi":
            levels = ["A", "B", "C"]
        elif self.config.name == "locness":
            levels = ["N"]
        else:
            assert False
        filepaths = [f"{data_dir}/{level}.{split}.json" for level in levels]
        id_ = 0
        for path, fp in files:
            if not filepaths:
                break
            if path in filepaths:
                filepaths.remove(path)
                for line in fp:
                    o = json.loads(line.decode("utf-8"))

                    edits = []
                    for (start, end, text) in o["edits"][0][1:][0]:
                        edits.append({"start": start, "end": end, "text": text})

                    out = {
                        "id": o["id"],
                        "cefr": o["cefr"],
                        "text": o["text"],
                        "edits": edits,
                    }

                    if self.config.name == "wi":
                        out["userid"] = o.get("userid", "")

                    yield id_, out
                    id_ += 1
