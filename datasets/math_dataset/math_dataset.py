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
"""Mathematics database."""

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """
@article{2019arXiv,
  author = {Saxton, Grefenstette, Hill, Kohli},
  title = {Analysing Mathematical Reasoning Abilities of Neural Models},
  year = {2019},
  journal = {arXiv:1904.01557}
}
"""

_DESCRIPTION = """
Mathematics database.

This dataset code generates mathematical question and answer pairs,
from a range of question types at roughly school-level difficulty.
This is designed to test the mathematical learning and algebraic
reasoning skills of learning models.

Original paper: Analysing Mathematical Reasoning Abilities of Neural Models
(Saxton, Grefenstette, Hill, Kohli).

Example usage:
train_examples, val_examples = datasets.load_dataset(
    'math_dataset/arithmetic__mul',
    split=['train', 'test'],
    as_supervised=True)
"""

_DATA_URL = "https://storage.googleapis.com/mathematics-dataset/mathematics_dataset-v1.0.tar.gz"

_TRAIN_CATEGORY = [
    "train-easy",
    "train-medium",
    "train-hard",
]

_INTERPOLATE_CATEGORY = [
    "interpolate",
]

_MODULES = [
    # extrapolate
    "measurement__conversion",
    # interpolate
    "algebra__linear_1d",
    "algebra__linear_1d_composed",
    "algebra__linear_2d",
    "algebra__linear_2d_composed",
    "algebra__polynomial_roots",
    "algebra__polynomial_roots_composed",
    "algebra__sequence_next_term",
    "algebra__sequence_nth_term",
    "arithmetic__add_or_sub",
    "arithmetic__add_or_sub_in_base",
    "arithmetic__add_sub_multiple",
    "arithmetic__div",
    "arithmetic__mixed",
    "arithmetic__mul",
    "arithmetic__mul_div_multiple",
    "arithmetic__nearest_integer_root",
    "arithmetic__simplify_surd",
    "calculus__differentiate",
    "calculus__differentiate_composed",
    "comparison__closest",
    "comparison__closest_composed",
    "comparison__kth_biggest",
    "comparison__kth_biggest_composed",
    "comparison__pair",
    "comparison__pair_composed",
    "comparison__sort",
    "comparison__sort_composed",
    "measurement__conversion",
    "measurement__time",
    "numbers__base_conversion",
    "numbers__div_remainder",
    "numbers__div_remainder_composed",
    "numbers__gcd",
    "numbers__gcd_composed",
    "numbers__is_factor",
    "numbers__is_factor_composed",
    "numbers__is_prime",
    "numbers__is_prime_composed",
    "numbers__lcm",
    "numbers__lcm_composed",
    "numbers__list_prime_factors",
    "numbers__list_prime_factors_composed",
    "numbers__place_value",
    "numbers__place_value_composed",
    "numbers__round_number",
    "numbers__round_number_composed",
    "polynomials__add",
    "polynomials__coefficient_named",
    "polynomials__collect",
    "polynomials__compose",
    "polynomials__evaluate",
    "polynomials__evaluate_composed",
    "polynomials__expand",
    "polynomials__simplify_power",
    "probability__swr_p_level_set",
    "probability__swr_p_sequence",
    # train-easy train-medium train-hard
    "algebra__linear_1d",
    "algebra__linear_1d_composed",
    "algebra__linear_2d",
    "algebra__linear_2d_composed",
    "algebra__polynomial_roots",
    "algebra__polynomial_roots_composed",
    "algebra__sequence_next_term",
    "algebra__sequence_nth_term",
    "arithmetic__add_or_sub",
    "arithmetic__add_or_sub_in_base",
    "arithmetic__add_sub_multiple",
    "arithmetic__div",
    "arithmetic__mixed",
    "arithmetic__mul",
    "arithmetic__mul_div_multiple",
    "arithmetic__nearest_integer_root",
    "arithmetic__simplify_surd",
    "calculus__differentiate",
    "calculus__differentiate_composed",
    "comparison__closest",
    "comparison__closest_composed",
    "comparison__kth_biggest",
    "comparison__kth_biggest_composed",
    "comparison__pair",
    "comparison__pair_composed",
    "comparison__sort",
    "comparison__sort_composed",
    "measurement__conversion",
    "measurement__time",
    "numbers__base_conversion",
    "numbers__div_remainder",
    "numbers__div_remainder_composed",
    "numbers__gcd",
    "numbers__gcd_composed",
    "numbers__is_factor",
    "numbers__is_factor_composed",
    "numbers__is_prime",
    "numbers__is_prime_composed",
    "numbers__lcm",
    "numbers__lcm_composed",
    "numbers__list_prime_factors",
    "numbers__list_prime_factors_composed",
    "numbers__place_value",
    "numbers__place_value_composed",
    "numbers__round_number",
    "numbers__round_number_composed",
    "polynomials__add",
    "polynomials__coefficient_named",
    "polynomials__collect",
    "polynomials__compose",
    "polynomials__evaluate",
    "polynomials__evaluate_composed",
    "polynomials__expand",
    "polynomials__simplify_power",
    "probability__swr_p_level_set",
    "probability__swr_p_sequence",
]

_QUESTION = "question"
_ANSWER = "answer"

_DATASET_VERSION = "mathematics_dataset-v1.0"


def _generate_builder_configs():
    """Generate configs with different subsets of mathematics dataset."""
    configs = []
    for module in sorted(set(_MODULES)):
        configs.append(
            datasets.BuilderConfig(
                name=module,
                version=datasets.Version("1.0.0"),
                description=_DESCRIPTION,
            )
        )

    return configs


class MathDataset(datasets.GeneratorBasedBuilder):
    """Math Dataset."""

    BUILDER_CONFIGS = _generate_builder_configs()

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    _QUESTION: datasets.Value("string"),
                    _ANSWER: datasets.Value("string"),
                }
            ),
            supervised_keys=(_QUESTION, _ANSWER),
            homepage="https://github.com/deepmind/mathematics_dataset",
            citation=_CITATION,
        )

    def _get_filepaths_from_categories(self, config, categories):
        filepaths = []
        for category in categories:
            data_file = "/".join([_DATASET_VERSION, category, config])
            filepaths.append(data_file)
        return set(filepaths)

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        archive = dl_manager.download(_DATA_URL)
        config = self.config.name + ".txt"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "config": config,
                    "categories": _TRAIN_CATEGORY,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "config": config,
                    "categories": _INTERPOLATE_CATEGORY,
                },
            ),
        ]

    def _generate_examples(self, files, config, categories):
        """Yields examples based on directory, module file.."""

        idx = 0
        filepaths = self._get_filepaths_from_categories(config, categories)
        for path, f in files:
            if not filepaths:
                break
            elif path in filepaths:
                for question in f:
                    if not question:
                        continue
                    else:
                        for answer in f:
                            if not answer:
                                continue
                            else:
                                yield idx, {_QUESTION: question, _ANSWER: answer}
                                idx += 1
                                break
                filepaths.remove(path)
