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
"""An Urdu text corpus for machine learning, natural language processing and linguistic analysis."""

from __future__ import absolute_import, division, print_function


import xml.etree.ElementTree as ET
import logging

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
authors={huggingface, Inc.
},
year={2020}
}
"""

# You can copy an official description
_DESCRIPTION = """\
An Urdu text corpus for machine learning, natural language processing and linguistic analysis.
"""

_HOMEPAGE = "https://matnsaz.net/en/makhzan"

_LICENSE = "All files in the /text directory are covered under standard copyright. Each piece of text has been included in this repository with explicity permission of respective copyright holders, who are identified in the <meta> tag for each file. You are free to use this text for analysis, research and development, but you are not allowed to redistribute or republish this text. Some cases where a less restrictive license could apply to files in the /text directory are presented below. In some cases copyright free text has been digitally reproduced through the hard work of our collaborators. In such cases we have credited the appropriate people where possible in a notes field in the file's metadata, and we strongly encourage you to contact them before redistributing this text in any form. Where a separate license is provided along with the text, we have provided corresponding data in the publication field in a file's metadata."

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_BASE_URL = "https://raw.githubusercontent.com/zeerakahmed/makhzan/master/text/"
_URLs = {
    'train': [_BASE_URL + '{:04d}.xml'.format(i) for i in range(1, 5523)]
}


class Makhzan(datasets.GeneratorBasedBuilder):
    """Makhzan - An Urdu text corpus for machine learning, natural language processing and linguistic analysis."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="train", version=VERSION, description="This part of my dataset covers a first domain")    ]

    DEFAULT_CONFIG_NAME = "train"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
            {
                "file_id": datasets.Value("string"),
                "metadata": datasets.Value("string"),
                "title": datasets.Value("string"),
                'num-words': datasets.Value("int64"),
                'contains-non-urdu-languages': datasets.Value("string"),
                "document_body": datasets.Value("string")
                # These are the features of your dataset like images, labels ...
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
        my_urls = _URLs[self.config.name]
        dowloaded_files = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "file_paths": dowloaded_files
                }
            )
        ]

    def _generate_examples(self, file_paths):
        """ Yields examples. """
        for id_, file_path in enumerate(file_paths):
            with open(file_path, encoding="utf-8") as f:
                example = {'file_id': '',
                           'metadata': '',
                            'title': '',
                            'num-words': 0,
                            'contains-non-urdu-languages': ''}
                try:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    if root.tag == 'document':
                        example['file_id'] = '{:04d}.xml'.format(id_ + 1)
                        metadata = root.find('meta')
                        if metadata:
                            example['metadata'] = ET.tostring(metadata, encoding='unicode')
                            title = metadata.find('title')
                            if title:
                                example['title'] = title.text
                            example['num-words'] = int(metadata.find('num-words').text)
                            example['contains-non-urdu-languages'] = metadata.find('contains-non-urdu-languages').text
                        else:
                            raise ValueError('Missing tag "<meta>"')
                        document_body = root.find('body')
                        if document_body:
                            example['document_body'] = ET.tostring(document_body, encoding='unicode')
                    else:
                        raise ValueError('Missing tag "<document>"')
                    yield id_, example
                except ET.ParseError:
                    logging.warning('{:04d}.xml could not be parsed.'.format(id_ + 1))
