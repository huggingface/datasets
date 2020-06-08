"""TODO(flue): Add a description here."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nlp
import os
import csv
import base64

# TODO(flue): BibTeX citation
_CITATION = """\
@misc{le2019flaubert,
title={FlauBERT: Unsupervised Language Model Pre-training for French},
author={Hang Le and Loïc Vial and Jibril Frej and Vincent Segonne and Maximin Coavoux and Benjamin Lecouteux and Alexandre Allauzen and 
        Benoît Crabbé and Laurent Besacier and Didier Schwab},
year={2019},
eprint={1912.05372},
archivePrefix={arXiv},
primaryClass={cs.CL}
}


"""

# TODO(flue):
_DESCRIPTION = """\
FLUE is an evaluation setup for French NLP systems similar to the popular GLUE benchmark. The goal is to enable further reproducible experiments 
in the future and to share models and progress on the French language. The tasks and data are obtained from existing works, please refer to our 
Flaubert paper for a complete list of references.
"""

_CLASSIFICATION_DESC = """\
This is a binary classification task. It consists in classifying Amazon reviews for three product categories: books, DVD, and music. Each sample 
contains a review text and the associated rating from 1 to 5 stars. Reviews rated above 3 is labeled as positive, and those rated less than 3 is 
labeled as negative.
The train and test sets are balanced, including around 1k positive and 1k negative reviews for a total of 2k reviews in each dataset. We take 
the French portion to create the binary text classification task in FLUE and report the accuracy on the test set.

"""
_PARAPHRASE_DESC = """\
The task consists in identifying whether the two sentences in a pair are semantically equivalent or not.
The train set includes 49.4k examples, the dev and test sets each comprises nearly 2k examples. We take the related datasets for French to 
perform the paraphrasing task and report the accuracy on the test set.

"""
_NLI_DESC = """\
The Natural Language Inference (NLI) task, also known as recognizing textual entailment (RTE), is to determine whether a premise entails, contradicts or 
neither entails nor contradicts a hypothesis. We take the French part of the XNLI corpus to form the development and test sets for the NLI task in FLUE.
The train set includes 392.7k examples, the dev and test sets comprises 2.5k and 5k examples respectively. We take the related datasets for French to 
perform the NLI task and report the accuracy on the test set.
"""

_CLASSIFICATION_CITATION = """\
@misc{le2019flaubert,
    title={FlauBERT: Unsupervised Language Model Pre-training for French},
    author={Hang Le and Loïc Vial and Jibril Frej and Vincent Segonne and Maximin Coavoux and Benjamin Lecouteux and Alexandre Allauzen and Benoît Crabbé and Laurent Besacier and Didier Schwab},
    year={2019},
    eprint={1912.05372},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""
_PARAPHRASE_CITATION = """\
@InProceedings{pawsx2019emnlp,
title = {{PAWS-X: A Cross-lingual Adversarial Dataset for Paraphrase Identification}},
author = {Yang, Yinfei and Zhang, Yuan and Tar, Chris and Baldridge, Jason},
booktitle = {Proc. of EMNLP},
year = {2019}
}
"""
_NLI_CITATION = """\
@InProceedings{conneau2018xnli,
author = {Conneau, Alexis and Rinott, Ruty and Lample, Guillaume and Williams, Adina and Bowman, Samuel R. and Schwenk, Holger and Stoyanov, Veselin},
title = {XNLI: Evaluating Cross-lingual Sentence Representations},
booktitle = {Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing},
year = {2018},
publisher = {Association for Computational Linguistics},
location = {Brussels, Belgium},
}
"""
_VSD_CITATION = """\
@inproceedings{segonne-etal-2019-using,
    title = "Using {W}iktionary as a resource for {WSD} : the case of {F}rench verbs",
    author = "Segonne, Vincent  and
      Candito, Marie  and
      Crabb{\'e}, Beno{\^\i}t",
    booktitle = "Proceedings of the 13th International Conference on Computational Semantics - Long Papers",
    month = may,
    year = "2019",
    address = "Gothenburg, Sweden",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-0422",
    doi = "10.18653/v1/W19-0422",
    pages = "259--270"
    }
"""
_NSD_CITATION = """\
@dataset{loic_vial_2019_3549806,
    author = {Loïc Vial},
    title = {{French Word Sense Disambiguation with Princeton
    WordNet Identifiers}},
    month = nov,
    year = 2019,
    publisher = {Zenodo},
    version = {1.0},
    doi = {10.5281/zenodo.3549806},
    url = {https://doi.org/10.5281/zenodo.3549806}
}
"""

_RES_ID = {
    'book_test': '45B4CBA79872918D!1394',
    'book_train': '45B4CBA79872918D!1393',
    'dvd_test': '45B4CBA79872918D!1395',
    'dvd_train': '45B4CBA79872918D!1396',
    'music_train': '45B4CBA79872918D!1400',
    'music_test': '45B4CBA79872918D!1398',
    'paws-x_train': '45B4CBA79872918D!1404',
    'paws-x_test': '45B4CBA79872918D!1403',
    'paws-x_dev': '45B4CBA79872918D!1401',
    'nsd_semcor': '45B4CBA79872918D!1407',
    'nsd_semeval': '45B4CBA79872918D!1405',
    'nsd_wgc':     '45B4CBA79872918D!1410',
    'vsd_train': '45B4CBA79872918D!1412',
    'vsd_test': '45B4CBA79872918D!1406',
    'xnli_train': '45B4CBA79872918D!1411',
    'xnli_test': '45B4CBA79872918D!1409',
    'xnli_dev': '45B4CBA79872918D!1408'
}

_AUT_KEYS = '!APKmrvD4ttdyzH0'


def generate_url(resid):
    sharingUrl = "https://onedrive.live.com/redir?resid="+resid+"&authKey="+_AUT_KEYS

    base64Value = base64.b64encode(sharingUrl.encode())
    encodedUrl = "u!" + base64Value.decode().lstrip('=').replace('/', '_').replace('+', '-')
    url = os.path.join("https://api.onedrive.com/v1.0/shares", encodedUrl, "root/content")
    return url


class FlueConfig(nlp.BuilderConfig):
        """BuilderConfig for Flue."""

        def __init__(self, task,text_features, citation, **kwargs):
            """BuilderConfig for Flue.

            Args:
                task: string
                text_features: list
                citation: string
              **kwargs: keyword arguments forwarded to super.
            """
            super(FlueConfig, self).__init__(version=nlp.Version("1.0.0"), **kwargs)
            self.task = task
            self.text_features = text_features
            self.citation = citation


class Flue(nlp.GeneratorBasedBuilder):
  """TODO(flue): Short description of my dataset."""

  # TODO(flue): Set up version.
  VERSION = nlp.Version('1.1.0')
  BUILDER_CONFIGS = [
      FlueConfig(
          name='book',
          description=_CLASSIFICATION_DESC,
          task='classification',
          citation=_CLASSIFICATION_CITATION,
          text_features= ['texte', 'note']
      ),
      FlueConfig(
          name='dvd',
          description=_CLASSIFICATION_DESC,
          task='classification',
          citation=_CLASSIFICATION_CITATION,
          text_features=['texte', 'note']
      ),
      FlueConfig(
          name='music',
          description=_CLASSIFICATION_DESC,
          task='classification',
          citation=_CLASSIFICATION_CITATION,
          text_features=['texte', 'note']
      ),
      FlueConfig(
          name='paws-x',
          description=_PARAPHRASE_DESC,
          task='paraphrase',
          citation=_PARAPHRASE_CITATION,
          text_features=['sentence1', 'sentence2', 'label']
      ),
      FlueConfig(
          name='xnli',
          description=_NLI_DESC,
          task='NLI',
          citation=_NLI_CITATION,
          text_features=['premise', 'hypo', 'label']
      ),
      FlueConfig(
          name='vsd',
          description="Verb Sense Disambiguation",
          task='word_sense_disambiguation',
          citation=_VSD_CITATION,
          text_features=['sentence', 'word', 'document', 'lemma']
      ),
      FlueConfig(
          name='nsd_wgc',
          description="Noun Sense Disambiguation, WordNet Gloss Corpus dataset",
          task='word_sense_disambiguation',
          citation=_NSD_CITATION,
          text_features=['paragraph', 'word', 'sentence', 'document']
      ),
      FlueConfig(
          name='nsd_semcor',
          description="Noun Sense Disambiguation, SemCor dataset",
          task='word_sense_disambiguation',
          citation=_NSD_CITATION,
          text_features=['paragraph', 'word', 'sentence', 'document']
      ),
      
      FlueConfig(
          name='nsd_semeval',
          description="Noun Sense Disambiguation, SemEval dataset",
          task='word_sense_disambiguation',
          citation=_NSD_CITATION,
          text_features=['paragraph', 'word', 'sentence', 'document']
      )
  ]

  def _info(self):
    # TODO(flue): Specifies the nlp.DatasetInfo object
    features = {
        feature: nlp.Value('string') for feature in self.config.text_features
    }
    if self.config.task == 'classification':
        features['note'] = nlp.Value('float32')
    return nlp.DatasetInfo(
        # This is the description that will appear on the datasets page.
        description=_DESCRIPTION + '\n\n' + self.config.description,
        # nlp.features.FeatureConnectors
        features=nlp.Features(
                features
            # These are the features of your dataset like images, labels ...
        ),
        # If there's a common (input, target) tuple from the features,
        # specify them here. They'll be used if as_supervised=True in
        # builder.as_dataset.
        supervised_keys=None,
        # Homepage of the dataset for documentation
        homepage='https://github.com/getalp/Flaubert/tree/master/flue',
        citation=_CITATION + '\n\n' + self.config.citation,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    # TODO(flue): Downloads the data and defines the splits
    # dl_manager is a nlp.download.DownloadManager that can be used to
    # download and extract URLs
    if self.config.task == 'classification' or self.config.name == 'vsd':
        urls_to_download = {
            'train': generate_url(_RES_ID[self.config.name+'_train']),
            'test': generate_url(_RES_ID[self.config.name+'_test'])
        }
        dl_files = dl_manager.download_and_extract(urls_to_download)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'filepath': dl_files['train']
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'filepath': dl_files['test']
                },
            ),
        ]
    if self.config.name in ['paws-x', 'xnli']:
        urls_to_download = {
            'train': generate_url(_RES_ID[self.config.name + '_train']),
            'test': generate_url(_RES_ID[self.config.name + '_test']),
            'dev': generate_url(_RES_ID[self.config.name + '_dev'])
        }
        dl_files = dl_manager.download_and_extract(urls_to_download)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'filepath': dl_files['train']
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'filepath': dl_files['test']
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'filepath': dl_files['dev']
                },
            ),
        ]
    if self.config.name in ['nsd_semcor', 'nsd_wgc']:
        urls_to_download = {
            'train': generate_url(_RES_ID[self.config.name]),
        }
        dl_files = dl_manager.download_and_extract(urls_to_download)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'filepath': dl_files['train']
                },
            )
        ]
    if self.config.name == 'nsd_semeval':
        urls_to_download = {
            'test': generate_url(_RES_ID[self.config.name]),

        }
        dl_files = dl_manager.download_and_extract(urls_to_download)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'filepath': dl_files['test']
                },
            )
        ]



  def _generate_examples(self, filepath):
    """Yields examples."""
    # TODO(flue): Yields (key, example) tuples from the dataset
    with open(filepath) as f:
        data = csv.DictReader(f)
        for _id, row in enumerate(data):
            out = {}
            try:
                out['label'] = row['gold_label']
                out['premise'] = row['sentence1']
                out['hypo'] = row['sentence2']
            except KeyError:
                
                out = {
                    feature: row[feature] for feature in self.config.text_features
                }
            yield _id, out

