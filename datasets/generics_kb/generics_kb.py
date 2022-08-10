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
"""Generics KB: A Knowledge Base of Generic Statements"""


import ast
import csv
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {GenericsKB: A Knowledge Base of Generic Statements},
authors={Sumithra Bhakthavatsalam, Chloe Anastasiades, Peter Clark},
year={2020},
publisher = {Allen Institute for AI},
}
"""

_DESCRIPTION = """\
The GenericsKB contains 3.4M+ generic sentences about the world, i.e., sentences expressing general truths such as "Dogs bark," and "Trees remove carbon dioxide from the atmosphere." Generics are potentially useful as a knowledge source for AI systems requiring general world knowledge. The GenericsKB is the first large-scale resource containing naturally occurring generic sentences (as opposed to extracted or crowdsourced triples), and is rich in high-quality, general, semantically complete statements. Generics were primarily extracted from three large text sources, namely the Waterloo Corpus, selected parts of Simple Wikipedia, and the ARC Corpus. A filtered, high-quality subset is also available in GenericsKB-Best, containing 1,020,868 sentences. We recommend you start with GenericsKB-Best.
"""

_HOMEPAGE = "https://allenai.org/data/genericskb"

_LICENSE = "cc-by-4.0"

_URL = "https://drive.google.com/u/0/uc?id={0}&export=download"

_FILEPATHS = {
    "generics_kb_best": _URL.format("12DfIzoWyHIQqssgUgDvz3VG8_ScSh6ng"),
    "generics_kb": _URL.format("1UOIEzQTid7SzKx2tbwSSPxl7g-CjpoZa"),
    "generics_kb_simplewiki": _URL.format("1SpN9Qc7XRy5xs4tIfXkcLOEAP2IVaK15"),
    "generics_kb_waterloo": "cskb-waterloo-06-21-with-bert-scores.jsonl",
}


class GenericsKb(datasets.GeneratorBasedBuilder):
    """The GenericsKB is the first large-scale resource containing naturally occurring generic sentences, and is rich in high-quality, general, semantically complete statements."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="generics_kb_best",
            version=VERSION,
            description="This is the default and recommended config.Comprises of GENERICSKB generics with a score > 0.234 ",
        ),
        datasets.BuilderConfig(
            name="generics_kb", version=VERSION, description="This GENERICSKB that contains 3,433,000 sentences."
        ),
        datasets.BuilderConfig(
            name="generics_kb_simplewiki",
            version=VERSION,
            description="SimpleWikipedia is a filtered scrape of SimpleWikipedia pages (simple.wikipedia.org)",
        ),
        datasets.BuilderConfig(
            name="generics_kb_waterloo",
            version=VERSION,
            description="The Waterloo corpus is 280GB of English plain text, gathered by Charles Clarke (Univ. Waterloo) using a webcrawler in 2001 from .edu domains.",
        ),
    ]

    @property
    def manual_download_instructions(self):
        return """\
      You need to manually download the files needed for the dataset config generics_kb_waterloo. The other configs like generics_kb_best don't need manual downloads.
      The <path/to/folder> can e.g. be `~/Downloads/GenericsKB`. Download the following required files from https://drive.google.com/drive/folders/1vqfVXhJXJWuiiXbUa4rZjOgQoJvwZUoT
      For working on "generics_kb_waterloo" data,
        1. Manually download 'GenericsKB-Waterloo-WithContext.jsonl.zip' into your <path/to/folder>.Please ensure the filename is as is.
           The Waterloo is also generics from GenericsKB.tsv, but expanded to also include their surrounding context (before/after sentences). The Waterloo generics are the majority of GenericsKB. This zip file is 1.4GB expanding to 5.5GB.
        2. Extract the GenericsKB-Waterloo-WithContext.jsonl.zip; It will create a file of 5.5 GB called cskb-waterloo-06-21-with-bert-scores.jsonl.
           Ensure you move this file into your <path/to/folder>.

      generics_kb can then be loaded using the following commands based on which data you want to work on. Data files must be present in the <path/to/folder> if using "generics_kb_waterloo" config.
      1. `datasets.load_dataset("generics_kb","generics_kb_best")`.
      2. `datasets.load_dataset("generics_kb","generics_kb")`
      3. `datasets.load_dataset("generics_kb","generics_kb_simplewiki")`
      4. `datasets.load_dataset("generics_kb","generics_kb_waterloo", data_dir="<path/to/folder>")`

      """

    DEFAULT_CONFIG_NAME = "generics_kb_best"

    def _info(self):
        if self.config.name == "generics_kb_waterloo" or self.config.name == "generics_kb_simplewiki":

            featuredict = {
                "source_name": datasets.Value("string"),
                "sentence": datasets.Value("string"),
                "sentences_before": datasets.Sequence(datasets.Value("string")),
                "sentences_after": datasets.Sequence(datasets.Value("string")),
                "concept_name": datasets.Value("string"),
                "quantifiers": datasets.Sequence(datasets.Value("string")),
                "id": datasets.Value("string"),
                "bert_score": datasets.Value("float64"),
            }
            if self.config.name == "generics_kb_simplewiki":
                featuredict["headings"] = datasets.Sequence(datasets.Value("string"))
                featuredict["categories"] = datasets.Sequence(datasets.Value("string"))

            features = datasets.Features(featuredict)

        else:

            features = datasets.Features(
                {
                    "source": datasets.Value("string"),
                    "term": datasets.Value("string"),
                    "quantifier_frequency": datasets.Value("string"),
                    "quantifier_number": datasets.Value("string"),
                    "generic_sentence": datasets.Value("string"),
                    "score": datasets.Value("float64"),
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

    def _split_generators(self, dl_manager):

        if self.config.name == "generics_kb_waterloo":
            data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
            # check if manual folder exists
            if not os.path.exists(data_dir):
                raise FileNotFoundError(
                    f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('generics_kb', data_dir=...)`. Manual download instructions: {self.manual_download_instructions})"
                )

            # Check if required files exist in the folder
            filepath = os.path.join(data_dir, _FILEPATHS[self.config.name])

            if not os.path.exists(filepath):
                raise FileNotFoundError(
                    f"{filepath} does not exist. Make sure you required files are present in {data_dir} `. Manual download instructions: {self.manual_download_instructions})"
                )
        else:
            filepath = dl_manager.download(_FILEPATHS[self.config.name])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepath,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        if self.config.name == "generics_kb_waterloo" or self.config.name == "generics_kb_simplewiki":

            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = ast.literal_eval(row)

                    result = {
                        "source_name": data["source"]["name"],
                        "sentence": data["knowledge"]["sentence"],
                        "sentences_before": data["knowledge"]["context"]["sentences_before"],
                        "sentences_after": data["knowledge"]["context"]["sentences_after"],
                        "concept_name": data["knowledge"]["key_concepts"][0]["concept_name"],
                        "quantifiers": data["knowledge"]["key_concepts"][0]["quantifiers"],
                        "id": data["id"],
                        "bert_score": data["bert_score"],
                    }
                    if self.config.name == "generics_kb_simplewiki":
                        result["headings"] = data["knowledge"]["context"]["headings"]
                        result["categories"] = data["knowledge"]["context"]["categories"]

                    yield id_, result
        else:

            with open(filepath, encoding="utf-8") as f:
                # Skip the header
                next(f)

                read_tsv = csv.reader(f, delimiter="\t")

                for id_, row in enumerate(read_tsv):

                    quantifier = row[2]
                    quantifier_frequency = ""
                    quantifier_number = ""

                    if quantifier != "":
                        quantifier = ast.literal_eval(quantifier)
                        if "frequency" in quantifier.keys():
                            quantifier_frequency = quantifier["frequency"]
                        if "number" in quantifier.keys():
                            quantifier_number = quantifier["number"]
                    yield id_, {
                        "source": row[0],
                        "term": row[1],
                        "quantifier_frequency": quantifier_frequency,
                        "quantifier_number": quantifier_number,
                        "generic_sentence": row[3],
                        "score": row[4],
                    }
