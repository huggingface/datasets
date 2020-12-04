import os

import datasets


_DESCRIPTION = """\
"""
_HOMEPAGE_URL = "https://github.com/elenanereiss/Legal-Entity-Recognition"
_CITATION = """\
@inproceedings{leitner2019fine,
  author = {Elena Leitner and Georg Rehm and Julian Moreno-Schneider},
  title = {{Fine-grained Named Entity Recognition in Legal Documents}},
  booktitle = {Semantic Systems. The Power of AI and Knowledge
                  Graphs. Proceedings of the 15th International Conference
                  (SEMANTiCS 2019)},
  year = 2019,
  editor = {Maribel Acosta and Philippe Cudré-Mauroux and Maria
                  Maleshkova and Tassilo Pellegrini and Harald Sack and York
                  Sure-Vetter},
  keywords = {aip},
  publisher = {Springer},
  series = {Lecture Notes in Computer Science},
  number = {11702},
  address = {Karlsruhe, Germany},
  month = 9,
  note = {10/11 September 2019},
  pages = {272--287},
  pdf = {https://link.springer.com/content/pdf/10.1007%2F978-3-030-33220-4_20.pdf}}
"""
_DATA_URL = "https://raw.githubusercontent.com/elenanereiss/Legal-Entity-Recognition/master/data/dataset_courts.zip"
_VERSION = "1.0.0"
_COURTS = ["bag", "bfh", "bgh", "bpatg", "bsg", "bverfg", "bverwg"]
_COURTS_FILEPATHS = {court: f"{court}.conll" for court in _COURTS}
_ALL = "all"


class GermanLegalEntityRecognitionConfig(datasets.BuilderConfig):
    def __init__(self, *args, courts=None, **kwargs):
        super().__init__(*args, version=datasets.Version(_VERSION, ""), **kwargs)
        self.courts = courts

    @property
    def filepaths(self):
        return [_COURTS_FILEPATHS[court] for court in self.courts]


class GermanLegalEntityRecognition(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        GermanLegalEntityRecognitionConfig(name=court, courts=[court], description=f"Court. {court}.")
        for court in _COURTS
    ] + [GermanLegalEntityRecognitionConfig(name=_ALL, courts=_COURTS, description=f"All courts included.")]
    BUILDER_CONFIG_CLASS = GermanLegalEntityRecognitionConfig
    DEFAULT_CONFIG_NAME = _ALL

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
                                "B-AN",
                                "B-EUN",
                                "B-GRT",
                                "B-GS",
                                "B-INN",
                                "B-LD",
                                "B-LDS",
                                "B-LIT",
                                "B-MRK",
                                "B-ORG",
                                "B-PER",
                                "B-RR",
                                "B-RS",
                                "B-ST",
                                "B-STR",
                                "B-UN",
                                "B-VO",
                                "B-VS",
                                "B-VT",
                                "I-AN",
                                "I-EUN",
                                "I-GRT",
                                "I-GS",
                                "I-INN",
                                "I-LD",
                                "I-LDS",
                                "I-LIT",
                                "I-MRK",
                                "I-ORG",
                                "I-PER",
                                "I-RR",
                                "I-RS",
                                "I-ST",
                                "I-STR",
                                "I-UN",
                                "I-VO",
                                "I-VS",
                                "I-VT",
                                "O",
                            ]
                        )
                    ),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_DATA_URL)
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"datapath": path})]

    def _generate_examples(self, datapath):
        sentence_counter = 0
        for filepath in self.config.filepaths:
            filepath = os.path.join(datapath, filepath)
            with open(filepath, encoding="utf-8") as f:
                current_words = []
                current_labels = []
                for row in f:
                    row = row.rstrip()
                    row_split = row.split()
                    if len(row_split) == 2:
                        token, label = row_split
                        current_words.append(token)
                        current_labels.append(label)
                    else:
                        if not current_words:
                            continue
                        assert len(current_words) == len(current_labels), "word len doesnt match label length"
                        sentence = (
                            sentence_counter,
                            {
                                "id": str(sentence_counter),
                                "tokens": current_words,
                                "ner_tags": current_labels,
                            },
                        )
                        sentence_counter += 1
                        current_words = []
                        current_labels = []
                        yield sentence

                # if something remains:
                if current_words:
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "tokens": current_words,
                            "ner_tags": current_labels,
                        },
                    )
                    yield sentence
