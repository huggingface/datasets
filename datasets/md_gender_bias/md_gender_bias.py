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
"""Multi-Dimensional Gender Bias classification"""


import json

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{md_gender_bias,
  author    = {Emily Dinan and
               Angela Fan and
               Ledell Wu and
               Jason Weston and
               Douwe Kiela and
               Adina Williams},
  editor    = {Bonnie Webber and
               Trevor Cohn and
               Yulan He and
               Yang Liu},
  title     = {Multi-Dimensional Gender Bias Classification},
  booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural
               Language Processing, {EMNLP} 2020, Online, November 16-20, 2020},
  pages     = {314--331},
  publisher = {Association for Computational Linguistics},
  year      = {2020},
  url       = {https://www.aclweb.org/anthology/2020.emnlp-main.23/}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Machine learning models are trained to find patterns in data.
NLP models can inadvertently learn socially undesirable patterns when training on gender biased text.
In this work, we propose a general framework that decomposes gender bias in text along several pragmatic and semantic dimensions:
bias from the gender of the person being spoken about, bias from the gender of the person being spoken to, and bias from the gender of the speaker.
Using this fine-grained framework, we automatically annotate eight large scale datasets with gender information.
In addition, we collect a novel, crowdsourced evaluation benchmark of utterance-level gender rewrites.
Distinguishing between gender bias along multiple dimensions is important, as it enables us to train finer-grained gender bias classifiers.
We show our classifiers prove valuable for a variety of important applications, such as controlling for gender bias in generative models,
detecting gender bias in arbitrary text, and shed light on offensive language in terms of genderedness.
"""

_HOMEPAGE = "https://parl.ai/projects/md_gender/"

_LICENSE = "MIT License"

_URL = "http://parl.ai/downloads/md_gender/gend_multiclass_10072020.tgz"

_CONF_FILES = {
    "funpedia": {
        "train": "funpedia/train.jsonl",
        "validation": "funpedia/valid.jsonl",
        "test": "funpedia/test.jsonl",
    },
    "image_chat": {
        "train": "image_chat/engaging_imagechat_gender_captions_hashed.test.jsonl",
        "validation": "image_chat/engaging_imagechat_gender_captions_hashed.train.jsonl",
        "test": "image_chat/engaging_imagechat_gender_captions_hashed.valid.jsonl",
    },
    "wizard": {
        "train": "wizard/train.jsonl",
        "validation": "wizard/valid.jsonl",
        "test": "wizard/test.jsonl",
    },
    "convai2_inferred": {
        "train": (
            "inferred_about/convai2_train_binary.txt",
            "inferred_about/convai2_train.txt",
        ),
        "validation": (
            "inferred_about/convai2_valid_binary.txt",
            "inferred_about/convai2_valid.txt",
        ),
        "test": (
            "inferred_about/convai2_test_binary.txt",
            "inferred_about/convai2_test.txt",
        ),
    },
    "light_inferred": {
        "train": (
            "inferred_about/light_train_binary.txt",
            "inferred_about/light_train.txt",
        ),
        "validation": (
            "inferred_about/light_valid_binary.txt",
            "inferred_about/light_valid.txt",
        ),
        "test": (
            "inferred_about/light_test_binary.txt",
            "inferred_about/light_test.txt",
        ),
    },
    "opensubtitles_inferred": {
        "train": (
            "inferred_about/opensubtitles_train_binary.txt",
            "inferred_about/opensubtitles_train.txt",
        ),
        "validation": (
            "inferred_about/opensubtitles_valid_binary.txt",
            "inferred_about/opensubtitles_valid.txt",
        ),
        "test": (
            "inferred_about/opensubtitles_test_binary.txt",
            "inferred_about/opensubtitles_test.txt",
        ),
    },
    "yelp_inferred": {
        "train": (
            "inferred_about/yelp_train_binary.txt",
            "",
        ),
        "validation": (
            "inferred_about/yelp_valid_binary.txt",
            "",
        ),
        "test": (
            "inferred_about/yelp_test_binary.txt",
            "",
        ),
    },
}


class MdGenderBias(datasets.GeneratorBasedBuilder):
    """Multi-Dimensional Gender Bias classification"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="gendered_words",
            version=VERSION,
            description="A list of common nouns with a masculine and feminine variant.",
        ),
        datasets.BuilderConfig(
            name="name_genders",
            version=VERSION,
            description="A list of first names with their gender attribution by year in the US.",
        ),
        datasets.BuilderConfig(
            name="new_data", version=VERSION, description="Some data reformulated and annotated along all three axes."
        ),
        datasets.BuilderConfig(
            name="funpedia",
            version=VERSION,
            description="Data from Funpedia with ABOUT annotations based on Funpedia information on an entity's gender.",
        ),
        datasets.BuilderConfig(
            name="image_chat",
            version=VERSION,
            description="Data from ImageChat with ABOUT annotations based on image recognition.",
        ),
        datasets.BuilderConfig(
            name="wizard",
            version=VERSION,
            description="Data from WizardsOfWikipedia with ABOUT annotations based on Wikipedia information on an entity's gender.",
        ),
        datasets.BuilderConfig(
            name="convai2_inferred",
            version=VERSION,
            description="Data from the ConvAI2 challenge with ABOUT annotations inferred by a trined classifier.",
        ),
        datasets.BuilderConfig(
            name="light_inferred",
            version=VERSION,
            description="Data from LIGHT with ABOUT annotations inferred by a trined classifier.",
        ),
        datasets.BuilderConfig(
            name="opensubtitles_inferred",
            version=VERSION,
            description="Data from OpenSubtitles with ABOUT annotations inferred by a trined classifier.",
        ),
        datasets.BuilderConfig(
            name="yelp_inferred",
            version=VERSION,
            description="Data from Yelp reviews with ABOUT annotations inferred by a trined classifier.",
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "new_data"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if (
            self.config.name == "gendered_words"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "word_masculine": datasets.Value("string"),
                    "word_feminine": datasets.Value("string"),
                }
            )
        elif self.config.name == "name_genders":
            features = datasets.Features(
                {
                    "name": datasets.Value("string"),
                    "assigned_gender": datasets.ClassLabel(names=["M", "F"]),
                    "count": datasets.Value("int32"),
                }
            )
        elif self.config.name == "new_data":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "original": datasets.Value("string"),
                    "labels": [
                        datasets.ClassLabel(
                            names=[
                                "ABOUT:female",
                                "ABOUT:male",
                                "PARTNER:female",
                                "PARTNER:male",
                                "SELF:female",
                                "SELF:male",
                            ]
                        )
                    ],
                    "class_type": datasets.ClassLabel(names=["about", "partner", "self"]),
                    "turker_gender": datasets.ClassLabel(
                        names=["man", "woman", "nonbinary", "prefer not to say", "no answer"]
                    ),
                    "episode_done": datasets.Value("bool_"),
                    "confidence": datasets.Value("string"),
                }
            )
        elif self.config.name == "funpedia":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "persona": datasets.Value("string"),
                    "gender": datasets.ClassLabel(names=["gender-neutral", "female", "male"]),
                }
            )
        elif self.config.name == "image_chat":
            features = datasets.Features(
                {
                    "caption": datasets.Value("string"),
                    "id": datasets.Value("string"),
                    "male": datasets.Value("bool_"),
                    "female": datasets.Value("bool_"),
                }
            )
        elif self.config.name == "wizard":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "chosen_topic": datasets.Value("string"),
                    "gender": datasets.ClassLabel(names=["gender-neutral", "female", "male"]),
                }
            )
        elif self.config.name == "yelp_inferred":
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "binary_label": datasets.ClassLabel(names=["ABOUT:female", "ABOUT:male"]),
                    "binary_score": datasets.Value("float"),
                }
            )
        else:  # data with inferred labels
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "binary_label": datasets.ClassLabel(names=["ABOUT:female", "ABOUT:male"]),
                    "binary_score": datasets.Value("float"),
                    "ternary_label": datasets.ClassLabel(names=["ABOUT:female", "ABOUT:male", "ABOUT:gender-neutral"]),
                    "ternary_score": datasets.Value("float"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archive = dl_manager.download(_URL)
        data_dir = "data_to_release"
        if self.config.name == "gendered_words":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": None,
                        "filepath_pair": (
                            data_dir + "/" + "word_list/male_word_file.txt",
                            data_dir + "/" + "word_list/female_word_file.txt",
                        ),
                        "files": dl_manager.iter_archive(archive),
                    },
                )
            ]
        elif self.config.name == "name_genders":
            return [
                datasets.SplitGenerator(
                    name=f"yob{yob}",
                    gen_kwargs={
                        "filepath": data_dir + "/" + f"names/yob{yob}.txt",
                        "filepath_pair": None,
                        "files": dl_manager.iter_archive(archive),
                    },
                )
                for yob in range(1880, 2019)
            ]
        elif self.config.name == "new_data":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": data_dir + "/" + "new_data/data.jsonl",
                        "filepath_pair": None,
                        "files": dl_manager.iter_archive(archive),
                    },
                )
            ]
        elif self.config.name in ["funpedia", "image_chat", "wizard"]:
            return [
                datasets.SplitGenerator(
                    name=spl,
                    gen_kwargs={
                        "filepath": data_dir + "/" + fname,
                        "filepath_pair": None,
                        "files": dl_manager.iter_archive(archive),
                    },
                )
                for spl, fname in _CONF_FILES[self.config.name].items()
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=spl,
                    gen_kwargs={
                        "filepath": None,
                        "filepath_pair": (
                            data_dir + "/" + fname_1,
                            data_dir + "/" + fname_2,
                        ),
                        "files": dl_manager.iter_archive(archive),
                    },
                )
                for spl, (fname_1, fname_2) in _CONF_FILES[self.config.name].items()
            ]

    def _generate_examples(self, filepath, filepath_pair, files):
        if self.config.name == "gendered_words":
            male_data, female_data = None, None
            for path, f in files:
                if path == filepath_pair[0]:
                    male_data = f.read().decode("utf-8").splitlines()
                elif path == filepath_pair[1]:
                    female_data = f.read().decode("utf-8").splitlines()
                if male_data is not None and female_data is not None:
                    for id_, (l_m, l_f) in enumerate(zip(male_data, female_data)):
                        yield id_, {
                            "word_masculine": l_m.strip(),
                            "word_feminine": l_f.strip(),
                        }
                    break
        elif self.config.name == "name_genders":
            for path, f in files:
                if path == filepath:
                    for id_, line in enumerate(f):
                        name, g, ct = line.decode("utf-8").strip().split(",")
                        yield id_, {
                            "name": name,
                            "assigned_gender": g,
                            "count": int(ct),
                        }
                    break
        elif "_inferred" in self.config.name:
            if "yelp" in self.config.name:
                for path, f in files:
                    if path == filepath_pair[0]:
                        for id_, line_b in enumerate(f):
                            text_b, label_b, score_b = line_b.decode("utf-8").split("\t")
                            yield id_, {
                                "text": text_b,
                                "binary_label": label_b,
                                "binary_score": float(score_b.strip()),
                            }
                        break
            else:
                binary_data, ternary_data = None, None
                for path, f in files:
                    if path == filepath_pair[0]:
                        binary_data = f.read().decode("utf-8").splitlines()
                    elif path == filepath_pair[1]:
                        ternary_data = f.read().decode("utf-8").splitlines()
                    if binary_data is not None and ternary_data is not None:
                        for id_, (line_b, line_t) in enumerate(zip(binary_data, ternary_data)):
                            text_b, label_b, score_b = line_b.split("\t")
                            text_t, label_t, score_t = line_t.split("\t")
                            yield id_, {
                                "text": text_b,
                                "binary_label": label_b,
                                "binary_score": float(score_b.strip()),
                                "ternary_label": label_t,
                                "ternary_score": float(score_t.strip()),
                            }
                        break
        else:
            for path, f in files:
                if path == filepath:
                    for id_, line in enumerate(f):
                        example = json.loads(line.decode("utf-8").strip())
                        if "turker_gender" in example and example["turker_gender"] is None:
                            example["turker_gender"] = "no answer"
                        yield id_, example
                    break
