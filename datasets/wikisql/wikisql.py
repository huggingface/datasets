"""A large crowd-sourced dataset for developing natural language interfaces for relational databases"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@article{zhongSeq2SQL2017,
  author    = {Victor Zhong and
               Caiming Xiong and
               Richard Socher},
  title     = {Seq2SQL: Generating Structured Queries from Natural Language using
               Reinforcement Learning},
  journal   = {CoRR},
  volume    = {abs/1709.00103},
  year      = {2017}
}
"""

_DESCRIPTION = """\
A large crowd-sourced dataset for developing natural language interfaces for relational databases
"""

_DATA_URL = "https://github.com/salesforce/WikiSQL/raw/master/data.tar.bz2"

_AGG_OPS = ["", "MAX", "MIN", "COUNT", "SUM", "AVG"]
_COND_OPS = ["=", ">", "<", "OP"]


class WikiSQL(datasets.GeneratorBasedBuilder):
    """WikiSQL: A large crowd-sourced dataset for developing natural language interfaces for relational databases"""

    VERSION = datasets.Version("0.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "phase": datasets.Value("int32"),
                    "question": datasets.Value("string"),
                    "table": {
                        "header": datasets.features.Sequence(datasets.Value("string")),
                        "page_title": datasets.Value("string"),
                        "page_id": datasets.Value("string"),
                        "types": datasets.features.Sequence(datasets.Value("string")),
                        "id": datasets.Value("string"),
                        "section_title": datasets.Value("string"),
                        "caption": datasets.Value("string"),
                        "rows": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                        "name": datasets.Value("string"),
                    },
                    "sql": {
                        "human_readable": datasets.Value("string"),
                        "sel": datasets.Value("int32"),
                        "agg": datasets.Value("int32"),
                        "conds": datasets.features.Sequence(
                            {
                                "column_index": datasets.Value("int32"),
                                "operator_index": datasets.Value("int32"),
                                "condition": datasets.Value("string"),
                            }
                        ),
                    },
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/salesforce/WikiSQL",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        dl_dir = os.path.join(dl_dir, "data")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "main_filepath": os.path.join(dl_dir, "test.jsonl"),
                    "tables_filepath": os.path.join(dl_dir, "test.tables.jsonl"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "main_filepath": os.path.join(dl_dir, "dev.jsonl"),
                    "tables_filepath": os.path.join(dl_dir, "dev.tables.jsonl"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "main_filepath": os.path.join(dl_dir, "train.jsonl"),
                    "tables_filepath": os.path.join(dl_dir, "train.tables.jsonl"),
                },
            ),
        ]

    def _convert_to_human_readable(self, sel, agg, columns, conditions):
        """Make SQL query string. Based on https://github.com/salesforce/WikiSQL/blob/c2ed4f9b22db1cc2721805d53e6e76e07e2ccbdc/lib/query.py#L10"""

        rep = "SELECT {agg} {sel} FROM table".format(
            agg=_AGG_OPS[agg], sel=columns[sel] if columns is not None else "col{}".format(sel)
        )

        if conditions:
            rep += " WHERE " + " AND ".join(["{} {} {}".format(columns[i], _COND_OPS[o], v) for i, o, v in conditions])
        return " ".join(rep.split())

    def _generate_examples(self, main_filepath, tables_filepath):
        """Yields examples."""

        # Build dictionary to table_ids:tables
        with open(tables_filepath, encoding="utf-8") as f:
            tables = [json.loads(line) for line in f]
            id_to_tables = {x["id"]: x for x in tables}

        with open(main_filepath, encoding="utf-8") as f:
            for idx, line in enumerate(f):
                row = json.loads(line)
                row["table"] = id_to_tables[row["table_id"]]
                del row["table_id"]

                # Handle missing data
                row["table"]["page_title"] = row["table"].get("page_title", "")
                row["table"]["section_title"] = row["table"].get("section_title", "")
                row["table"]["caption"] = row["table"].get("caption", "")
                row["table"]["name"] = row["table"].get("name", "")
                row["table"]["page_id"] = str(row["table"].get("page_id", ""))

                # Fix row types
                row["table"]["rows"] = [[str(e) for e in r] for r in row["table"]["rows"]]

                # Get human-readable version
                row["sql"]["human_readable"] = self._convert_to_human_readable(
                    row["sql"]["sel"],
                    row["sql"]["agg"],
                    row["table"]["header"],
                    row["sql"]["conds"],
                )

                # Restructure sql->conds
                # - wikiSQL provides a tuple [column_index, operator_index, condition]
                #   as 'condition' can have 2 types (float or str) we convert to dict
                for i in range(len(row["sql"]["conds"])):
                    row["sql"]["conds"][i] = {
                        "column_index": row["sql"]["conds"][i][0],
                        "operator_index": row["sql"]["conds"][i][1],
                        "condition": str(row["sql"]["conds"][i][2]),
                    }
                yield idx, row
