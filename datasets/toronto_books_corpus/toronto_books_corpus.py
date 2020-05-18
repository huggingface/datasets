"""TODO(toronto_books_corpus): Add a description here."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nlp
import os
import codecs
import requests
from lxml import etree

# TODO(toronto_books_corpus): BibTeX citation
_CITATION = """\
@InProceedings{TIEDEMANN12.463,
  author = {J�rg Tiedemann},
  title = {Parallel Data, Tools and Interfaces in OPUS},
  booktitle = {Proceedings of the Eight International Conference on Language Resources and Evaluation (LREC'12)},
  year = {2012},
  month = {may},
  date = {23-25},
  address = {Istanbul, Turkey},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Mehmet Ugur Dogan and Bente Maegaard and Joseph Mariani and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-7-7},
  language = {english}
 }
"""

# TODO(toronto_books_corpus):
_DESCRIPTION = """\
This is a collection of copyright free books aligned by Andras Farkas, which are available from http://www.farkastranslations.com/bilingual_books.php
Note that the texts are rather dated due to copyright issues and that some of them are manually reviewed (check the meta-data at the top of the corpus files in XML). The source is multilingually aligned, which is available from http://www.farkastranslations.com/bilingual_books.php. In OPUS, the alignment is formally bilingual but the multilingual alignment can be recovered from the XCES sentence alignment files. Note also that the alignment units from the original source may include multi-sentence paragraphs, which are split and sentence-aligned in OPUS.
Terms of Use
All texts are freely available for personal, educational and research use. Commercial use (e.g. reselling as parallel books) and mass redistribution without explicit permission are not granted. Please acknowledge the source when using the data!

16 languages, 64 bitexts
total number of files: 158
total number of tokens: 19.50M
total number of sentence fragments: 0.91M
"""

_LANG = ['ca', 'de', 'el', 'en', 'eo', 'es', 'fi', 'fr', 'hu', 'it', 'nl', 'no', 'pl', 'pt', 'ru', 'sv']
_LAN_DICT = {
    'ca':'Catalan',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Spanish',
    'fi': 'Finnish',
    'fr': 'French',
    'hu': 'Hungarian',
    'it': 'Italian',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'sv': 'Swedish'

}

_CONFIG_NAMES = []
for i in range(1, len(_LANG)):
    for j in range(i):
        _CONFIG_NAMES.append('Moses-'+_LANG[j]+'-'+_LANG[i])
for i in range(len(_LANG)):
    for j in range(i+1, len(_LANG)):
        _CONFIG_NAMES.append('TMX-'+_LANG[i]+'-'+_LANG[j])

_BASE_URL = 'http://opus.nlpl.eu/download.php?f=Books/v1/'
_URLS = {}
for name in _CONFIG_NAMES:
    input_lang = name.split('-')[1]
    target_lang = name.split('-')[2]
    if name.startswith('TMX'):
        url = os.path.join(_BASE_URL, 'tmx',input_lang + '-' + target_lang + '.tmx.gz')
    else:
        url = os.path.join(_BASE_URL, 'moses',input_lang + '-' + target_lang + '.txt.zip')

    conn = requests.get(url)
    if conn.status_code == 200:
        _URLS[name] = url



class TorontoBooksCorpusConfig(nlp.BuilderConfig):
  """BuilderConfig for TorontoBooksCorpusConfig."""

  def __init__(self, url, input_lang, target_lang,  **kwargs):
    """BuilderConfig for TorontoBooksCorpusConfig.

    Args:
        url: url to download the file
        input_lang: input lang of the current config file
        target_lang: target lang of current confile file

      **kwargs: keyword arguments forwarded to super.
    """

    super(TorontoBooksCorpusConfig, self).__init__(
        version=nlp.Version("1.0.0"), **kwargs)
    self.url = url
    self.input_lang = input_lang
    self.target_lang = target_lang

class TorontoBooksCorpus(nlp.GeneratorBasedBuilder):
  """TODO(toronto_books_corpus): Short description of my dataset."""

  # TODO(toronto_books_corpus): Set up version.
  VERSION = nlp.Version('1.0.0')
  BUILDER_CONFIGS = [
      TorontoBooksCorpusConfig(
          name=name,
          url=_URLS[name],
          input_lang=name.split('-')[1],
          target_lang = name.split('-')[2],
          description=_LAN_DICT[name.split('-')[1]]+'-'+ _LAN_DICT[name.split('-')[2]] +' format ' + name.split('-')[0]
      )for name in _URLS
  ]

  def _info(self):
    # TODO(toronto_books_corpus): Specifies the nlp.DatasetInfo object
    return nlp.DatasetInfo(
        # This is the description that will appear on the datasets page.
        description=_DESCRIPTION,
        # nlp.features.FeatureConnectors
        features=nlp.Features({
            # These are the features of your dataset like images, labels ...
            'source': nlp.Value('string'),
            'target': nlp.Value('string')
        }),
        # If there's a common (input, target) tuple from the features,
        # specify them here. They'll be used if as_supervised=True in
        # builder.as_dataset.
        supervised_keys=(self.config.input_lang, self.config.target_lang),
        # Homepage of the dataset for documentation
        homepage='http://opus.nlpl.eu/Books.php',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    # TODO(toronto_books_corpus): Downloads the data and defines the splits
    # dl_manager is a nlp.download.DownloadManager that can be used to
    # download and extract URLs

    dl_dir = dl_manager.download_and_extract(self.config.url)
    if self.config.name.startswith('TMX'):
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'input_filepath': dl_dir,
                    'target_filepath': None
                },
            ),
        ]
    else:
        # data_dir = os.path.join(dl_dir, self.config.input_lang + '-' +
        #                                      self.config.target_lang + '.txt')
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    'input_filepath':os.path.join(dl_dir, 'Books.'+self.config.input_lang +
                                                  '-'+self.config.target_lang+'.'+self.config.input_lang ),
                    'target_filepath': os.path.join(dl_dir, 'Books.'+self.config.input_lang +
                                                  '-'+self.config.target_lang+'.'+self.config.target_lang )

                },
            ),
        ]



  def _generate_examples(self, input_filepath, target_filepath):
    """Yields examples."""
    # TODO(toronto_books_corpus): Yields (key, example) tuples from the dataset

    if self.config.name.startswith('TMX'):
        parser = etree.HTMLParser()
        tree = etree.parse(input_filepath, parser)
        root = tree.xpath('//body')[0]
        all_segs = []
        for i in root.getiterator():
          if i.tag == 'seg':
              all_segs.append(i.text)
        i = 0
        while i < len(all_segs) - 1:
            yield i, {
              'source': all_segs[i],
              'target': all_segs[i + 1]
            }
            i += 2
    else:
        with open(input_filepath) as f:
            input_text = f.read()
        with open(target_filepath) as f1:
            target_text = f1.read()
        lang = self.config.input_lang + '-' + self.config.target_lang
        yield lang, {
            'source': input_text,
            'target': target_text
        }



