# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""BioCreative II gene mention recognition Corpus"""

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{smith2008overview,
        title={Overview of BioCreative II gene mention recognition},
        author={Smith, Larry and Tanabe, Lorraine K and nee Ando, Rie Johnson and Kuo, Cheng-Ju and Chung, I-Fang and Hsu, Chun-Nan and Lin, Yu-Shi and Klinger, Roman and Friedrich, Christoph M and Ganchev, Kuzman and others},
        journal={Genome biology},
        volume={9},
        number={S2},
        pages={S2},
        year={2008},
        publisher={Springer}
}
"""

_DESCRIPTION = """\
Nineteen teams presented results for the Gene Mention Task at the BioCreative II Workshop.
In this task participants designed systems to identify substrings in sentences corresponding to gene name mentions.
A variety of different methods were used and the results varied with a highest achieved F1 score of 0.8721.
Here we present brief descriptions of all the methods used and a statistical analysis of the results.
We also demonstrate that, by combining the results from all submissions, an F score of 0.9066 is feasible,
and furthermore that the best result makes use of the lowest scoring submissions.

For more details, see: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2559986/

The original dataset can be downloaded from: https://biocreative.bioinformatics.udel.edu/resources/corpora/biocreative-ii-corpus/
This dataset has been converted to CoNLL format for NER using the following tool: https://github.com/spyysalo/standoff2conll
"""

_HOMEPAGE = "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2559986/"
_URL = "https://github.com/spyysalo/bc2gm-corpus/raw/master/conll/"
_TRAINING_FILE = "train.tsv"
_DEV_FILE = "devel.tsv"
_TEST_FILE = "test.tsv"


class Bc2gmCorpusConfig(datasets.BuilderConfig):
    """BuilderConfig for Bc2gmCorpus"""

    def __init__(self, **kwargs):
        """BuilderConfig for Bc2gmCorpus.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Bc2gmCorpusConfig, self).__init__(**kwargs)


class Bc2gmCorpus(datasets.GeneratorBasedBuilder):
    """Bc2gmCorpus dataset."""

    BUILDER_CONFIGS = [
        Bc2gmCorpusConfig(name="bc2gm_corpus", version=datasets.Version("1.0.0"), description="bc2gm corpus"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-GENE",
                                "I-GENE",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    # tokens are tab separated
                    splits = line.split("\t")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
