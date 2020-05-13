"""TODO(wiki_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


# TODO(wiki_qa): BibTeX citation
_CITATION = """\
@InProceedings{YangYihMeek:EMNLP2015:WikiQA,
       author = {{Yi}, Yang and {Wen-tau},  Yih and {Christopher} Meek},
        title = "{WikiQA: A Challenge Dataset for Open-Domain Question Answering}",
      journal = {Association for Computational Linguistics},
         year = 2015,
          doi = {10.18653/v1/D15-1237},
        pages = {2013–2018},
}
"""

# TODO(wiki_qa):
_DESCRIPTION = """\
Wiki Question Answering corpus from Microsoft
"""

_DATA_URL = "https://download.microsoft.com/download/E/5/f/E5FCFCEE-7005-4814-853D-DAA7C66507E0/WikiQACorpus.zip"  #'https://www.microsoft.com/en-us/download/confirmation.aspx?id=52419'


class WikiQa(nlp.GeneratorBasedBuilder):
    """TODO(wiki_qa): Short description of my dataset."""

    # TODO(wiki_qa): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(wiki_qa): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "question_id": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "document_title": nlp.Value("string"),
                    "answer": nlp.Value("string"),
                    "label": nlp.features.ClassLabel(num_classes=2),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://www.microsoft.com/en-us/download/details.aspx?id=52419",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(wiki_qa): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        dl_dir = os.path.join(dl_dir, "WikiQACorpus")
        # dl_dir = os.path.join(dl_dir, '')
        return [
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": os.path.join(dl_dir, "WikiQA-test.tsv")}),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(dl_dir, "WikiQA-dev.tsv")}
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "WikiQA-train.tsv")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(wiki_qa): Yields (key, example) tuples from the dataset

        with open(filepath) as f:
            print("==" * 100, filepath)
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for idx, row in enumerate(reader):
                yield idx, {
                    "question_id": row["QuestionID"],
                    "question": row["Question"],
                    "document_title": row["DocumentTitle"],
                    "answer": row["Sentence"],
                    "label": row["Label"],
                }
