import csv

import datasets


csv.field_size_limit(int(1e6))  # to accommodate large fields


_CITATION = """\
@misc{aliannejadi2020convai3,
      title={ConvAI3: Generating Clarifying Questions for Open-Domain Dialogue Systems (ClariQ)},
      author={Mohammad Aliannejadi and Julia Kiseleva and Aleksandr Chuklin and Jeff Dalton and Mikhail Burtsev},
      year={2020},
      eprint={2009.11352},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
The Conv AI 3 challenge is organized as part of the Search-oriented Conversational AI (SCAI) EMNLP workshop in 2020. The main aim of the conversational systems is to return an appropriate answer in response to the user requests. However, some user requests might be ambiguous. In Information Retrieval (IR) settings such a situation is handled mainly through the diversification of search result page. It is however much more challenging in dialogue settings. Hence, we aim to study the following situation for dialogue settings:
- a user is asking an ambiguous question (where ambiguous question is a question to which one can return > 1 possible answers)
- the system must identify that the question is ambiguous, and, instead of trying to answer it directly, ask a good clarifying question.
"""


class ConvAi_3_Config(datasets.BuilderConfig):
    """BuilderConfig for ConvAi_3."""

    def __init__(self, **kwargs):
        """BuilderConfig for ConvAi_3.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ConvAi_3_Config, self).__init__(**kwargs)


class ConvAi_3(datasets.GeneratorBasedBuilder):

    _TRAIN_FILE = "https://github.com/aliannejadi/ClariQ/raw/master/data/train.tsv"
    _VAL_FILE = "https://github.com/aliannejadi/ClariQ/raw/master/data/dev.tsv"

    BUILDER_CONFIGS = [
        ConvAi_3_Config(
            name="conv_ai_3",
            version=datasets.Version("1.0.0"),
            description="Conv AI 3: Full training set with Dev set",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "topic_id": datasets.Value("int32"),
                    "initial_request": datasets.Value("string"),
                    "topic_desc": datasets.Value("string"),
                    "clarification_need": datasets.Value("int32"),
                    "facet_id": datasets.Value("string"),
                    "facet_desc": datasets.Value("string"),
                    "question_id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/aliannejadi/ClariQ",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_train = dl_manager.download(self._TRAIN_FILE)
        downloaded_dev = dl_manager.download(self._VAL_FILE)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_train},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloaded_dev},
            ),
        ]

    def _generate_examples(self, filepath):
        """Generate examples."""
        with open(filepath, encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter="\t")
            next(csv_reader)  # skip header
            for id_, row in enumerate(csv_reader):
                if len(row) < 9:  # checking because some rows are blank with just id
                    continue
                yield id_, {
                    "topic_id": row[0],
                    "initial_request": row[1],
                    "topic_desc": row[2],
                    "clarification_need": row[3],
                    "facet_id": row[4],
                    "facet_desc": row[5],
                    "question_id": row[6],
                    "question": row[7],
                    "answer": row[8],
                }
