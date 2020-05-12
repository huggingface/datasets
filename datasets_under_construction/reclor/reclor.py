"""TODO(reclor): Add a description here."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nlp
import json
from pathlib import Path
import os

# TODO(reclor): BibTeX citation
_CITATION = """\
@inproceedings{yu2020reclor,
        author = {Yu, Weihao and Jiang, Zihang and Dong, Yanfei and Feng, Jiashi},
        title = {ReClor: A Reading Comprehension Dataset Requiring Logical Reasoning},
        booktitle = {International Conference on Learning Representations (ICLR)},
        month = {April},
        year = {2020}
    }

"""

# TODO(reclor):
_DESCRIPTION = """\
Logical reasoning is an important ability to examine, analyze, and critically evaluate arguments as they occur in ordinary 
language as the definition from LSAC. ReClor is a dataset extracted from logical reasoning questions of standardized graduate 
admission examinations. Empirical results show that the state-of-the-art models struggle on ReClor with poor performance 
indicating more research is needed to essentially enhance the logical reasoning ability of current models. We hope this 
dataset could help push Machine Reading Comprehension (MRC) towards more complicated reasonin
"""


class Reclor(nlp.GeneratorBasedBuilder):
  """TODO(reclor): Short description of my dataset."""

  # TODO(reclor): Set up version.
  VERSION = nlp.Version('0.1.0')
  MANUAL_DOWNLOAD_INSTRUCTIONS = """\
  to use ReClor you need to download it manually. Please go to its homepage (http://whyu.me/reclor/) fill the google 
  form and you will recive a download link and a password to extract it. Please create a folder named reclor_data at ~/reclor_data 
  and extract the downloaded data their.
  """

  def _info(self):
    # TODO(reclor): Specifies the nlp.DatasetInfo object
    return nlp.DatasetInfo(
        # This is the description that will appear on the datasets page.
        description=_DESCRIPTION,
        # nlp.features.FeatureConnectors
        features=nlp.Features({
            # These are the features of your dataset like images, labels ...
            'context': nlp.Value('string'),
            'question': nlp.Value('string'),
            'answers': nlp.features.Sequence({
                'answer': nlp.Value('string')
            }),
            'label': nlp.Value('string'),
            "id_string": nlp.Value('string')
        }),
        # If there's a common (input, target) tuple from the features,
        # specify them here. They'll be used if as_supervised=True in
        # builder.as_dataset.
        supervised_keys=None,
        # Homepage of the dataset for documentation
        homepage='http://whyu.me/reclor/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    # TODO(reclor): Downloads the data and defines the splits
    # dl_manager is a nlp.download.DownloadManager that can be used to
    # download and extract URLs
    dl_dir = str(Path.home())
    data_dir = os.path.join(dl_dir, 'reclor_data')
    return [
        nlp.SplitGenerator(
            name=nlp.Split.TRAIN,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={
                'filepath': os.path.join(data_dir, 'train.json')
            },
        ),
        nlp.SplitGenerator(
            name=nlp.Split.TEST,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={
                'filepath': os.path.join(data_dir, 'test.json')
            },
        ),
        nlp.SplitGenerator(
            name=nlp.Split.VALIDATION,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={
                'filepath': os.path.join(data_dir, 'val.json')
            },
        ),
    ]

  def _generate_examples(self, filepath):
    """Yields examples."""
    # TODO(reclor): Yields (key, example) tuples from the dataset
    with open(filepath) as f:
        data = json.load(f)
        for id_, row in enumerate(data):
            yield id_, {
                'context': row['context'],
                'question': row['question'],
                'answers': {
                    'answer': row['answers']
                },
                'label': str(row.get('label', '')),
                "id_string": row['id_string']
            }

