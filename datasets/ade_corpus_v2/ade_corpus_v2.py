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

""" Adverse Drug Reaction Data: ADE-Corpus-V2  """


import re

import datasets


_CITATION = """\
@article{GURULINGAPPA2012885,
title = "Development of a benchmark corpus to support the automatic extraction of drug-related adverse effects from medical case reports",
journal = "Journal of Biomedical Informatics",
volume = "45",
number = "5",
pages = "885 - 892",
year = "2012",
note = "Text Mining and Natural Language Processing in Pharmacogenomics",
issn = "1532-0464",
doi = "https://doi.org/10.1016/j.jbi.2012.04.008",
url = "http://www.sciencedirect.com/science/article/pii/S1532046412000615",
author = "Harsha Gurulingappa and Abdul Mateen Rajput and Angus Roberts and Juliane Fluck and Martin Hofmann-Apitius and Luca Toldo",
keywords = "Adverse drug effect, Benchmark corpus, Annotation, Harmonization, Sentence classification",
abstract = "A significant amount of information about drug-related safety issues such as adverse effects are published in medical case reports that can only be explored by human readers due to their unstructured nature. The work presented here aims at generating a systematically annotated corpus that can support the development and validation of methods for the automatic extraction of drug-related adverse effects from medical case reports. The documents are systematically double annotated in various rounds to ensure consistent annotations. The annotated documents are finally harmonized to generate representative consensus annotations. In order to demonstrate an example use case scenario, the corpus was employed to train and validate models for the classification of informative against the non-informative sentences. A Maximum Entropy classifier trained with simple features and evaluated by 10-fold cross-validation resulted in the F1 score of 0.70 indicating a potential useful application of the corpus."
}
"""

_DESCRIPTION = """\
 ADE-Corpus-V2  Dataset: Adverse Drug Reaction Data.
 This is a dataset for Classification if a sentence is ADE-related (True) or not (False) and Relation Extraction between Adverse Drug Event and Drug.
 DRUG-AE.rel provides relations between drugs and adverse effects.
 DRUG-DOSE.rel provides relations between drugs and dosages.
 ADE-NEG.txt provides all sentences in the ADE corpus that DO NOT contain any drug-related adverse effects.
"""

_DOWNLOAD_URL = "https://raw.githubusercontent.com/trunghlt/AdverseDrugReaction/master/ADE-Corpus-V2/{}-{}.{}"

# Different usage configs/
configs = {
    "classification": "Ade_corpus_v2_classification",
    "RE_ade": "Ade_corpus_v2_drug_ade_relation",
    "RE_dosage": "Ade_corpus_v2_drug_dosage_relation",
}


class ADE_Corpus_V2Config(datasets.BuilderConfig):
    """BuilderConfig for ADE_Corpus_V2."""

    def __init__(self, **kwargs):
        """BuilderConfig for ADE_Corpus_V2.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ADE_Corpus_V2Config, self).__init__(**kwargs)


class ADECorpusV2(datasets.GeneratorBasedBuilder):
    """ADE_Corpus_V2 Dataset: Adverse Drug Reaction Data for Classification and Relation Extraction tasks ."""

    BUILDER_CONFIGS = [
        ADE_Corpus_V2Config(
            name="Ade_corpus_v2_classification",
            version=datasets.Version("1.0.0"),
            description="ADE_Corpus_V2 Dataset for Classification if a sentence is ADE-related or not.",
        ),
        ADE_Corpus_V2Config(
            name="Ade_corpus_v2_drug_ade_relation",
            version=datasets.Version("1.0.0"),
            description="ADE_Corpus_V2 Dataset for Relation Extraction between Adverse Drug Event and Drug.",
        ),
        ADE_Corpus_V2Config(
            name="Ade_corpus_v2_drug_dosage_relation",
            version=datasets.Version("1.0.0"),
            description="ADE_Corpus_V2 Dataset for Relation Extraction between Drug dosage and Drug.",
        ),
    ]

    def _info(self):

        if self.config.name == configs["classification"]:
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["Not-Related", "Related"]),
                }
            )

        if self.config.name == configs["RE_ade"]:
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "drug": datasets.Value("string"),
                    "effect": datasets.Value("string"),
                    "indexes": {
                        "drug": datasets.Sequence(
                            {
                                "start_char": datasets.Value("int32"),
                                "end_char": datasets.Value("int32"),
                            }
                        ),
                        "effect": datasets.Sequence(
                            {
                                "start_char": datasets.Value("int32"),
                                "end_char": datasets.Value("int32"),
                            }
                        ),
                    },
                }
            )

        if self.config.name == configs["RE_dosage"]:
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "drug": datasets.Value("string"),
                    "dosage": datasets.Value("string"),
                    "indexes": {
                        "drug": datasets.Sequence(
                            {
                                "start_char": datasets.Value("int32"),
                                "end_char": datasets.Value("int32"),
                            }
                        ),
                        "dosage": datasets.Sequence(
                            {
                                "start_char": datasets.Value("int32"),
                                "end_char": datasets.Value("int32"),
                            }
                        ),
                    },
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://www.sciencedirect.com/science/article/pii/S1532046412000615",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        DAE_path = dl_manager.download_and_extract(_DOWNLOAD_URL.format("DRUG", "AE", "rel"))
        DD_path = dl_manager.download_and_extract(_DOWNLOAD_URL.format("DRUG", "DOSE", "rel"))
        DAE_NEG_path = dl_manager.download_and_extract(_DOWNLOAD_URL.format("ADE", "NEG", "txt"))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"DRUG_AE_file": DAE_path, "DRUG_DOSAGE_file": DD_path, "NEG_DRUG_AE_file": DAE_NEG_path},
            ),
        ]

    def _generate_examples(self, DRUG_AE_file, DRUG_DOSAGE_file, NEG_DRUG_AE_file):
        """Generate ADE_Corpus_V2 examples."""

        # For Classification task with ade dataset.
        if self.config.name == configs["classification"]:
            texts, labels = [], []
            with open(DRUG_AE_file, encoding="utf-8") as f:
                for line in f:
                    pubmed_id, text = line.strip().split("|")[:2]
                    texts.append(text)
                    labels.append("Related")

            with open(NEG_DRUG_AE_file, encoding="utf-8") as f:
                for line in f:
                    pubmed_id, neg = line.strip().split(" ")[:2]
                    text = " ".join(line.strip().split(" ")[2:])
                    texts.append(text)
                    labels.append("Not-Related")

            for i in range(len(labels)):
                text, label = texts[i], labels[i]
                yield i, {"text": text, "label": label}

        # For Relation Extraction between drug and its effect.
        elif self.config.name == configs["RE_ade"]:

            texts, drugs, effects, drug_indexes, effect_indexes = [], [], [], [], []
            with open(DRUG_AE_file, encoding="utf-8") as f:
                for line in f:
                    value = line.strip().split("|")
                    text = value[1]
                    effect = value[2]
                    drug = value[5]

                    # add index of drug and effect from text
                    effect_matches, drug_matches = [], []
                    for match in re.finditer(effect, text):
                        effect_matches.append({"start_char": match.start(), "end_char": match.end()})
                    effect_indexes.append(effect_matches)

                    for match in re.finditer(drug, text):
                        drug_matches.append({"start_char": match.start(), "end_char": match.end()})
                    drug_indexes.append(drug_matches)

                    texts.append(text)
                    drugs.append(drug)
                    effects.append(effect)

            for idx, (text, drug, effect, drug_index, effect_index) in enumerate(
                zip(texts, drugs, effects, drug_indexes, effect_indexes)
            ):

                output = {
                    "text": text,
                    "drug": drug,
                    "effect": effect,
                    "indexes": {"drug": drug_index, "effect": effect_index},
                }

                yield idx, output

        # For Relation Extraction between drug and its dosage.
        elif self.config.name == configs["RE_dosage"]:

            texts, drugs, dosages, drug_indexes, dosage_indexes = [], [], [], [], []
            with open(DRUG_DOSAGE_file, encoding="utf-8") as f:
                for line in f:
                    value = line.strip().split("|")
                    text = value[1]
                    dosage = value[2]
                    drug = value[5]

                    # add index of drug and effect from text
                    dosage_matches, drug_matches = [], []
                    for match in re.finditer(dosage, text):
                        dosage_matches.append({"start_char": match.start(), "end_char": match.end()})
                    dosage_indexes.append(dosage_matches)

                    for match in re.finditer(drug, text):
                        drug_matches.append({"start_char": match.start(), "end_char": match.end()})
                    drug_indexes.append(drug_matches)

                    texts.append(text)
                    drugs.append(drug)
                    dosages.append(dosage)

            for idx, (text, drug, dosage, drug_index, dosage_index) in enumerate(
                zip(texts, drugs, dosages, drug_indexes, dosage_indexes)
            ):
                output = {
                    "text": text,
                    "drug": drug,
                    "dosage": dosage,
                    "indexes": {"drug": drug_index, "dosage": dosage_index},
                }
                yield idx, output
