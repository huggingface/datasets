from __future__ import absolute_import, division, print_function

import csv
import os
import logging

import datasets

_ARTICLES_URL = "https://github.com/wjko2/INQUISITIVE/raw/master/articles.tgz"
_QUESTIONS_URL = "https://github.com/wjko2/INQUISITIVE/raw/master/questions.txt"

class InquisitiveConfig(datasets.BuilderConfig):
    def __init__(self, **kwrags):
        super(InquisitiveConfig, self).__init__(**kwrags)

class Inquisitive(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        InquisitiveConfig(
            name="inquisitive",
            version=datasets.Version("1.0.0", ""),
            description="TODO"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "Article_Id": datasets.Value("int32"),
                    "Article": datasets.Value("string"),
                    "Sentence_Id": datasets.Value("int32"),
                    "Sentence": datasets.Value("string"),
                    "Span": datasets.Value("string"),
                    "Question": datasets.Value("string"),
                    "Span_Start_Position": datasets.Value("int32"),
                    "Span_End_Position": datasets.Value("int32"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/wjko2/INQUISITIVE",
            citation="",
        )
    
    def _split_generators(self, dl_manager):
        questions_file = dl_manager.download(_QUESTIONS_URL)
        articles_dir = dl_manager.download_and_extract(_ARTICLES_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"articles_path": articles_dir, "questions_file": questions_file, "ids": [1, 2, 3]})
        ]
    
    def _generate_examples(self, articles_path, questions_file, ids):
        with open(questions_file, encoding="utf-8") as f:
            questions_count = 0
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                example = dict(row)
                example["Article"] = str(articles_path)
                example["id"] = str(questions_count)
                questions_count += 1
                print(example)
                yield questions_count, example
