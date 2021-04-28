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
"""Over 25k semiautomatically generated sentence pairs illustrating well-studied pragmatic inference types. IMPPRES is an NLI dataset following the format of SNLI (Bowman et al., 2015), MultiNLI (Williams et al., 2018) and XNLI (Conneau et al., 2018), which was created to evaluate how well trained NLI models recognize several classes of presuppositions and scalar implicatures."""


import json
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{jeretic-etal-2020-natural,
    title = "Are Natural Language Inference Models {IMPPRESsive}? {L}earning {IMPlicature} and {PRESupposition}",
    author = "Jereti\v{c}, Paloma  and
      Warstadt, Alex  and
      Bhooshan, Suvrat  and
      Williams, Adina",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.768",
    doi = "10.18653/v1/2020.acl-main.768",
    pages = "8690--8705",
    abstract = "Natural language inference (NLI) is an increasingly important task for natural language understanding, which requires one to infer whether a sentence entails another. However, the ability of NLI models to make pragmatic inferences remains understudied. We create an IMPlicature and PRESupposition diagnostic dataset (IMPPRES), consisting of 32K semi-automatically generated sentence pairs illustrating well-studied pragmatic inference types. We use IMPPRES to evaluate whether BERT, InferSent, and BOW NLI models trained on MultiNLI (Williams et al., 2018) learn to make pragmatic inferences. Although MultiNLI appears to contain very few pairs illustrating these inference types, we find that BERT learns to draw pragmatic inferences. It reliably treats scalar implicatures triggered by {``}some{''} as entailments. For some presupposition triggers like {``}only{''}, BERT reliably recognizes the presupposition as an entailment, even when the trigger is embedded under an entailment canceling operator like negation. BOW and InferSent show weaker evidence of pragmatic reasoning. We conclude that NLI training encourages models to learn some, but not all, pragmatic inferences.",
}
"""

# You can copy an official description
_DESCRIPTION = """Over >25k semiautomatically generated sentence pairs illustrating well-studied pragmatic inference types. IMPPRES is an NLI dataset following the format of SNLI (Bowman et al., 2015), MultiNLI (Williams et al., 2018) and XNLI (Conneau et al., 2018), which was created to evaluate how well trained NLI models recognize several classes of presuppositions and scalar implicatures."""
_HOMEPAGE = "https://github.com/facebookresearch/Imppres"
_LICENSE = "Creative Commons Attribution-NonCommercial 4.0 International Public License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {"default": "https://github.com/facebookresearch/Imppres/blob/master/dataset/IMPPRES.zip?raw=true"}


class Imppres(datasets.GeneratorBasedBuilder):
    """Each sentence type in IMPPRES is generated according to a template that specifies the linear order of the constituents in the sentence. The constituents are sampled from a vocabulary of over 3000 lexical items annotated with grammatical features needed to ensure wellformedness. We semiautomatically generate IMPPRES using a codebase developed by Warstadt et al. (2019a) and significantly expanded for the BLiMP dataset (Warstadt et al., 2019b)."""

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
            name="presupposition_all_n_presupposition",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_both_presupposition",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_change_of_state",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_cleft_existence",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_cleft_uniqueness",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_only_presupposition",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_possessed_definites_existence",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_possessed_definites_uniqueness",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="presupposition_question_presupposition",
            version=VERSION,
            description="Presuppositions are facts that the speaker takes for granted when uttering a sentence.",
        ),
        datasets.BuilderConfig(
            name="implicature_connectives",
            version=VERSION,
            description="Scalar implicatures are inferences which can be drawn when one member of a memorized lexical scale is uttered.",
        ),
        datasets.BuilderConfig(
            name="implicature_gradable_adjective",
            version=VERSION,
            description="Scalar implicatures are inferences which can be drawn when one member of a memorized lexical scale is uttered.",
        ),
        datasets.BuilderConfig(
            name="implicature_gradable_verb",
            version=VERSION,
            description="Scalar implicatures are inferences which can be drawn when one member of a memorized lexical scale is uttered.",
        ),
        datasets.BuilderConfig(
            name="implicature_modals",
            version=VERSION,
            description="Scalar implicatures are inferences which can be drawn when one member of a memorized lexical scale is uttered.",
        ),
        datasets.BuilderConfig(
            name="implicature_numerals_10_100",
            version=VERSION,
            description="Scalar implicatures are inferences which can be drawn when one member of a memorized lexical scale is uttered.",
        ),
        datasets.BuilderConfig(
            name="implicature_numerals_2_3",
            version=VERSION,
            description="Scalar implicatures are inferences which can be drawn when one member of a memorized lexical scale is uttered.",
        ),
        datasets.BuilderConfig(
            name="implicature_quantifiers",
            version=VERSION,
            description="Scalar implicatures are inferences which can be drawn when one member of a memorized lexical scale is uttered.",
        ),
    ]

    def _info(self):
        if (
            "presupposition" in self.config.name
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "trigger": datasets.Value("string"),
                    "trigger1": datasets.Value("string"),
                    "trigger2": datasets.Value("string"),
                    "presupposition": datasets.Value("string"),
                    "gold_label": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                    "UID": datasets.Value("string"),
                    "pairID": datasets.Value("string"),
                    "paradigmID": datasets.Value("int16")
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "gold_label_log": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                    "gold_label_prag": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                    "spec_relation": datasets.Value("string"),
                    "item_type": datasets.Value("string"),
                    "trigger": datasets.Value("string"),
                    "lexemes": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
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
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs["default"]
        base_config = self.config.name.split("_")[0]
        secondary_config = self.config.name.split(base_config + "_")[1]
        data_dir = os.path.join(dl_manager.download_and_extract(my_urls), "IMPPRES", base_config)
        return [
            datasets.SplitGenerator(
                name=secondary_config,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, secondary_config + ".jsonl"),
                    "split": "test",
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if "presupposition" in self.config.name:
                    if "trigger1" not in list(data.keys()):
                        yield id_, {
                            "premise": data["sentence1"],
                            "hypothesis": data["sentence2"],
                            "trigger": data["trigger"],
                            "trigger1": "Not_In_Example",
                            "trigger2": "Not_In_Example",
                            "presupposition": data["presupposition"],
                            "gold_label": data["gold_label"],
                            "UID": data["UID"],
                            "pairID": data["pairID"],
                            "paradigmID": data["paradigmID"],
                        }
                    else:
                        yield id_, {
                            "premise": data["sentence1"],
                            "hypothesis": data["sentence2"],
                            "trigger": "Not_In_Example",
                            "trigger1": data["trigger1"],
                            "trigger2": data["trigger2"],
                            "presupposition": "Not_In_Example",
                            "gold_label": data["gold_label"],
                            "UID": data["UID"],
                            "pairID": data["pairID"],
                            "paradigmID": data["paradigmID"],
                        }

                else:
                    yield id_, {
                        "premise": data["sentence1"],
                        "hypothesis": data["sentence2"],
                        "gold_label_log": data["gold_label_log"],
                        "gold_label_prag": data["gold_label_prag"],
                        "spec_relation": data["spec_relation"],
                        "item_type": data["item_type"],
                        "trigger": data["trigger"],
                        "lexemes": data["lexemes"],
                    }
