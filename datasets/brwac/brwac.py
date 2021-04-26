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
"""BrWaC dataset"""


import os
import re

import datasets


_CITATION = """
@inproceedings{wagner2018brwac,
  title={The brwac corpus: A new open resource for brazilian portuguese},
  author={Wagner Filho, Jorge A and Wilkens, Rodrigo and Idiart, Marco and Villavicencio, Aline},
  booktitle={Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
  year={2018}
}
"""

_DESCRIPTION = """
The BrWaC (Brazilian Portuguese Web as Corpus) is a large corpus constructed following the Wacky framework,
which was made public for research purposes. The current corpus version, released in January 2017, is composed by
3.53 million documents, 2.68 billion tokens and 5.79 million types. Please note that this resource is available
solely for academic research purposes, and you agreed not to use it for any commercial applications.
Manually download at https://www.inf.ufrgs.br/pln/wiki/index.php?title=BrWaC
"""

_HOMEPAGE = "https://www.inf.ufrgs.br/pln/wiki/index.php?title=BrWaC"

_LICENSE = ""


class Brwac(datasets.GeneratorBasedBuilder):
    """BrWaC dataset"""

    VERSION = datasets.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """
        You need to
        1. Manually download `brwac.vert.gz` from https://www.inf.ufrgs.br/pln/wiki/index.php?title=BrWaC
        2. Extract the brwac.vert.gz in; this will result in the file brwac.vert in a folder <path/to/folder>
        The <path/to/folder> can e.g. be `~/Downloads`.
        BrWaC can then be loaded using the following command `datasets.load_dataset("brwac", data_dir="<path/to/folder>")`.
        """

    def _info(self):
        features = datasets.Features(
            {
                "doc_id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "uri": datasets.Value("string"),
                "text": datasets.Sequence({"paragraphs": datasets.Sequence(datasets.Value("string"))}),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        # check if manual folder exists
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasetts.load_dataset('brwac', data_dir=...)`. Manual download instructions: {self.manual_download_instructions})"
            )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "brwac.vert"),
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:

            add_space = 1
            doc_id, title, uri = None, None, None
            current_sentence, current_paragraph_sentences, text = "", [], []
            id_ = 0
            for line in f:

                line = line.strip()

                if line not in ["<p>", "<s>"]:  # skip these tags

                    if line.startswith("<doc"):  # doc begin
                        doc_id = re.findall('docid="(.*?)"', line)[0]
                        title = re.findall('title="(.*?)"', line)[0]
                        uri = re.findall('uri="(.*?)"', line)[0]

                    elif line == "<g/>":  # don't add space with <g/> occurrence
                        add_space = 0

                    elif line == "</s>":  # end sentence
                        current_paragraph_sentences.append(current_sentence)
                        current_sentence = ""

                    elif line == "</p>":  # end paragraph
                        text.append({"paragraphs": current_paragraph_sentences})
                        current_paragraph_sentences = []

                    elif len(current_sentence) == 0:
                        current_sentence = line

                    else:
                        current_sentence = (add_space * " ").join([current_sentence, line])
                        add_space = 1

                    if line.strip() == "</doc>":  # doc end
                        yield id_, {"doc_id": doc_id, "title": title, "uri": uri, "text": text}
                        id_ += 1
                        add_space = 1
                        doc_id, title, uri = None, None, None
                        current_sentence, current_paragraph_sentences, text = "", [], []
