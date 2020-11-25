import logging
import xml.etree.ElementTree as ET

import datasets


_CITATION = """\
@inproceedings{DBLP:conf/aaai/RogersKDR20,
  author    = {Anna Rogers and
               Olga Kovaleva and
               Matthew Downey and
               Anna Rumshisky},
  title     = {Getting Closer to {AI} Complete Question Answering: {A} Set of Prerequisite
               Real Tasks},
  booktitle = {The Thirty-Fourth {AAAI} Conference on Artificial Intelligence, {AAAI}
               2020, The Thirty-Second Innovative Applications of Artificial Intelligence
               Conference, {IAAI} 2020, The Tenth {AAAI} Symposium on Educational
               Advances in Artificial Intelligence, {EAAI} 2020, New York, NY, USA,
               February 7-12, 2020},
  pages     = {8722--8731},
  publisher = {{AAAI} Press},
  year      = {2020},
  url       = {https://aaai.org/ojs/index.php/AAAI/article/view/6398},
  timestamp = {Thu, 04 Jun 2020 13:18:48 +0200},
  biburl    = {https://dblp.org/rec/conf/aaai/RogersKDR20.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
QuAIL is a  reading comprehension dataset. \
QuAIL contains 15K multi-choice questions in texts 300-350 tokens \
long 4 domains (news, user stories, fiction, blogs).\
QuAIL is balanced and annotated for question types.\
"""


class QuailConfig(datasets.BuilderConfig):
    """BuilderConfig for QuAIL."""

    def __init__(self, **kwargs):
        """BuilderConfig for QuAIL.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(QuailConfig, self).__init__(**kwargs)


class Quail(datasets.GeneratorBasedBuilder):
    """QuAIL: The Stanford Question Answering Dataset. Version 1.1."""

    _CHALLENGE_SET = "https://raw.githubusercontent.com/text-machine-lab/quail/master/quail_v1.3/xml/randomized/quail_1.3_challenge_randomized.xml"
    _DEV_SET = "https://raw.githubusercontent.com/text-machine-lab/quail/master/quail_v1.3/xml/randomized/quail_1.3_dev_randomized.xml"
    _TRAIN_SET = "https://raw.githubusercontent.com/text-machine-lab/quail/master/quail_v1.3/xml/randomized/quail_1.3_train_randomized.xml"

    BUILDER_CONFIGS = [
        QuailConfig(
            name="quail",
            version=datasets.Version("1.3.0", ""),
            description="Quail dataset 1.3.0",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context_id": datasets.Value("string"),
                    "question_id": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    "metadata": {
                        "author": datasets.Value("string"),
                        "title": datasets.Value("string"),
                        "url": datasets.Value("string"),
                    },
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "question_type": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        datasets.Value("string"),
                    ),
                    "correct_answer_id": datasets.Value("int32"),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://text-machine-lab.github.io/blog/2020/quail/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls_to_download = {"train": self._TRAIN_SET, "dev": self._DEV_SET, "challenge": self._CHALLENGE_SET}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name="challenge", gen_kwargs={"filepath": downloaded_files["challenge"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        root = ET.parse(filepath).getroot()
        for text_tag in root.iterfind("text"):
            text_id = text_tag.get("id")
            domain = text_tag.get("domain")
            metadata_tag = text_tag.find("metadata")
            author = metadata_tag.find("author").text.strip()
            title = metadata_tag.find("title").text.strip()
            url = metadata_tag.find("url").text.strip()
            text_body = text_tag.find("text_body").text.strip()
            questions_tag = text_tag.find("questions")
            for q_tag in questions_tag.iterfind("q"):
                question_type = q_tag.get("type", None)
                question_text = q_tag.text.strip()
                question_id = q_tag.get("id")
                answers = []
                answer_id = None
                for i, a_tag in enumerate(q_tag.iterfind("a")):
                    if a_tag.get("correct") == "True":
                        answer_id = i
                    answers.append(a_tag.text.strip())

                id_ = f"{text_id}_{question_id}"
                yield id_, {
                    "id": id_,
                    "context_id": text_id,
                    "question_id": question_id,
                    "question_type": question_type,
                    "domain": domain,
                    "metadata": {"author": author, "title": title, "url": url},
                    "context": text_body,
                    "question": question_text,
                    "answers": answers,
                    "correct_answer_id": answer_id,
                }
