# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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

# Lint as: python3
"""The SuperGLUE benchmark."""

from __future__ import absolute_import, division, print_function

import json
import os

import six

import nlp


_SUPER_GLUE_CITATION = """\
@article{wang2019superglue,
  title={SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems},
  author={Wang, Alex and Pruksachatkun, Yada and Nangia, Nikita and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1905.00537},
  year={2019}
}

Note that each SuperGLUE dataset has its own citation. Please see the source to
get the correct citation for each contained dataset.
"""

_GLUE_DESCRIPTION = """\
SuperGLUE (https://super.gluebenchmark.com/) is a new benchmark styled after
GLUE with a new set of more difficult language understanding tasks, improved
resources, and a new public leaderboard.

"""

_BOOLQ_DESCRIPTION = """\
BoolQ (Boolean Questions, Clark et al., 2019a) is a QA task where each example consists of a short
passage and a yes/no question about the passage. The questions are provided anonymously and
unsolicited by users of the Google search engine, and afterwards paired with a paragraph from a
Wikipedia article containing the answer. Following the original work, we evaluate with accuracy."""

_CB_DESCRIPTION = """\
The CommitmentBank (De Marneffe et al., 2019) is a corpus of short texts in which at least
one sentence contains an embedded clause. Each of these embedded clauses is annotated with the
degree to which we expect that the person who wrote the text is committed to the truth of the clause.
The resulting task framed as three-class textual entailment on examples that are drawn from the Wall
Street Journal, fiction from the British National Corpus, and Switchboard. Each example consists
of a premise containing an embedded clause and the corresponding hypothesis is the extraction of
that clause. We use a subset of the data that had inter-annotator agreement above 0.85. The data is
imbalanced (relatively fewer neutral examples), so we evaluate using accuracy and F1, where for
multi-class F1 we compute the unweighted average of the F1 per class."""

_COPA_DESCRIPTION = """\
The Choice Of Plausible Alternatives (COPA, Roemmele et al., 2011) dataset is a causal
reasoning task in which a system is given a premise sentence and two possible alternatives. The
system must choose the alternative which has the more plausible causal relationship with the premise.
The method used for the construction of the alternatives ensures that the task requires causal reasoning
to solve. Examples either deal with alternative possible causes or alternative possible effects of the
premise sentence, accompanied by a simple question disambiguating between the two instance
types for the model. All examples are handcrafted and focus on topics from online blogs and a
photography-related encyclopedia. Following the recommendation of the authors, we evaluate using
accuracy."""

_RECORD_DESCRIPTION = """\
(Reading Comprehension with Commonsense Reasoning Dataset, Zhang et al., 2018) is a
multiple-choice QA task. Each example consists of a news article and a Cloze-style question about
the article in which one entity is masked out. The system must predict the masked out entity from a
given list of possible entities in the provided passage, where the same entity may be expressed using
multiple different surface forms, all of which are considered correct. Articles are drawn from CNN
and Daily Mail. Following the original work, we evaluate with max (over all mentions) token-level
F1 and exact match (EM)."""

_RTE_DESCRIPTION = """\
The Recognizing Textual Entailment (RTE) datasets come from a series of annual competitions
on textual entailment, the problem of predicting whether a given premise sentence entails a given
hypothesis sentence (also known as natural language inference, NLI). RTE was previously included
in GLUE, and we use the same data and format as before: We merge data from RTE1 (Dagan
et al., 2006), RTE2 (Bar Haim et al., 2006), RTE3 (Giampiccolo et al., 2007), and RTE5 (Bentivogli
et al., 2009). All datasets are combined and converted to two-class classification: entailment and
not_entailment. Of all the GLUE tasks, RTE was among those that benefited from transfer learning
the most, jumping from near random-chance performance (~56%) at the time of GLUE's launch to
85% accuracy (Liu et al., 2019c) at the time of writing. Given the eight point gap with respect to
human performance, however, the task is not yet solved by machines, and we expect the remaining
gap to be difficult to close."""

_MULTIRC_DESCRIPTION = """\
The Multi-Sentence Reading Comprehension dataset (MultiRC, Khashabi et al., 2018)
is a true/false question-answering task. Each example consists of a context paragraph, a question
about that paragraph, and a list of possible answers to that question which must be labeled as true or
false. Question-answering (QA) is a popular problem with many datasets. We use MultiRC because
of a number of desirable properties: (i) each question can have multiple possible correct answers,
so each question-answer pair must be evaluated independent of other pairs, (ii) the questions are
designed such that answering each question requires drawing facts from multiple context sentences,
and (iii) the question-answer pair format more closely matches the API of other SuperGLUE tasks
than span-based extractive QA does. The paragraphs are drawn from seven domains including news,
fiction, and historical text."""

_WIC_DESCRIPTION = """\
The Word-in-Context (WiC, Pilehvar and Camacho-Collados, 2019) dataset supports a word
sense disambiguation task cast as binary classification over sentence pairs. Given two sentences and a
polysemous (sense-ambiguous) word that appears in both sentences, the task is to determine whether
the word is used with the same sense in both sentences. Sentences are drawn from WordNet (Miller,
1995), VerbNet (Schuler, 2005), and Wiktionary. We follow the original work and evaluate using
accuracy."""

_WSC_DESCRIPTION = """\
The Winograd Schema Challenge (WSC, Levesque et al., 2012) is a reading comprehension
task in which a system must read a sentence with a pronoun and select the referent of that pronoun
from a list of choices. Given the difficulty of this task and the headroom still left, we have included
WSC in SuperGLUE and recast the dataset into its coreference form. The task is cast as a binary
classification problem, as opposed to N-multiple choice, in order to isolate the model's ability to
understand the coreference links within a sentence as opposed to various other strategies that may
come into play in multiple choice conditions. With that in mind, we create a split with 65% negative
majority class in the validation set, reflecting the distribution of the hidden test set, and 52% negative
class in the training set. The training and validation examples are drawn from the original Winograd
Schema dataset (Levesque et al., 2012), as well as those distributed by the affiliated organization
Commonsense Reasoning. The test examples are derived from fiction books and have been shared
with us by the authors of the original dataset. Previously, a version of WSC recast as NLI as included
in GLUE, known as WNLI. No substantial progress was made on WNLI, with many submissions
opting to submit only majority class predictions. WNLI was made especially difficult due to an
adversarial train/dev split: Premise sentences that appeared in the training set sometimes appeared
in the development set with a different hypothesis and a flipped label. If a system memorized the
training set without meaningfully generalizing, which was easy due to the small size of the training
set, it could perform far below chance on the development set. We remove this adversarial design
in the SuperGLUE version of WSC by ensuring that no sentences are shared between the training,
validation, and test sets.

However, the validation and test sets come from different domains, with the validation set consisting
of ambiguous examples such that changing one non-noun phrase word will change the coreference
dependencies in the sentence. The test set consists only of more straightforward examples, with a
high number of noun phrases (and thus more choices for the model), but low to no ambiguity."""

_AXB_DESCRIPTION = """\
An expert-constructed,
diagnostic dataset that automatically tests models for a broad range of linguistic, commonsense, and
world knowledge. Each example in this broad-coverage diagnostic is a sentence pair labeled with
a three-way entailment relation (entailment, neutral, or contradiction) and tagged with labels that
indicate the phenomena that characterize the relationship between the two sentences. Submissions
to the GLUE leaderboard are required to include predictions from the submission's MultiNLI
classifier on the diagnostic dataset, and analyses of the results were shown alongside the main
leaderboard. Since this broad-coverage diagnostic task has proved difficult for top models, we retain
it in SuperGLUE. However, since MultiNLI is not part of SuperGLUE, we collapse contradiction
and neutral into a single not_entailment label, and request that submissions include predictions
on the resulting set from the model used for the RTE task.
"""

_AXG_DESCRIPTION = """\
Winogender is designed to measure gender
bias in coreference resolution systems. We use the Diverse Natural Language Inference Collection
(DNC; Poliak et al., 2018) version that casts Winogender as a textual entailment task. Each example
consists of a premise sentence with a male or female pronoun and a hypothesis giving a possible
antecedent of the pronoun. Examples occur in minimal pairs, where the only difference between
an example and its pair is the gender of the pronoun in the premise. Performance on Winogender
is measured with both accuracy and the gender parity score: the percentage of minimal pairs for
which the predictions are the same. We note that a system can trivially obtain a perfect gender parity
score by guessing the same class for all examples, so a high gender parity score is meaningless unless
accompanied by high accuracy. As a diagnostic test of gender bias, we view the schemas as having high
positive predictive value and low negative predictive value; that is, they may demonstrate the presence
of gender bias in a system, but not prove its absence.
"""

_BOOLQ_CITATION = """\
@inproceedings{clark2019boolq,
  title={BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions},
  author={Clark, Christopher and Lee, Kenton and Chang, Ming-Wei, and Kwiatkowski, Tom and Collins, Michael, and Toutanova, Kristina},
  booktitle={NAACL},
  year={2019}
}"""

_CB_CITATION = """\
@article{de marneff_simons_tonhauser_2019,
  title={The CommitmentBank: Investigating projection in naturally occurring discourse},
  journal={proceedings of Sinn und Bedeutung 23},
  author={De Marneff, Marie-Catherine and Simons, Mandy and Tonhauser, Judith},
  year={2019}
}"""

_COPA_CITATION = """\
@inproceedings{roemmele2011choice,
  title={Choice of plausible alternatives: An evaluation of commonsense causal reasoning},
  author={Roemmele, Melissa and Bejan, Cosmin Adrian and Gordon, Andrew S},
  booktitle={2011 AAAI Spring Symposium Series},
  year={2011}
}"""

_RECORD_CITATION = """\
@article{zhang2018record,
  title={Record: Bridging the gap between human and machine commonsense reading comprehension},
  author={Zhang, Sheng and Liu, Xiaodong and Liu, Jingjing and Gao, Jianfeng and Duh, Kevin and Van Durme, Benjamin},
  journal={arXiv preprint arXiv:1810.12885},
  year={2018}
}"""

_RTE_CITATION = """\
@inproceedings{dagan2005pascal,
  title={The PASCAL recognising textual entailment challenge},
  author={Dagan, Ido and Glickman, Oren and Magnini, Bernardo},
  booktitle={Machine Learning Challenges Workshop},
  pages={177--190},
  year={2005},
  organization={Springer}
}
@inproceedings{bar2006second,
  title={The second pascal recognising textual entailment challenge},
  author={Bar-Haim, Roy and Dagan, Ido and Dolan, Bill and Ferro, Lisa and Giampiccolo, Danilo and Magnini, Bernardo and Szpektor, Idan},
  booktitle={Proceedings of the second PASCAL challenges workshop on recognising textual entailment},
  volume={6},
  number={1},
  pages={6--4},
  year={2006},
  organization={Venice}
}
@inproceedings{giampiccolo2007third,
  title={The third pascal recognizing textual entailment challenge},
  author={Giampiccolo, Danilo and Magnini, Bernardo and Dagan, Ido and Dolan, Bill},
  booktitle={Proceedings of the ACL-PASCAL workshop on textual entailment and paraphrasing},
  pages={1--9},
  year={2007},
  organization={Association for Computational Linguistics}
}
@inproceedings{bentivogli2009fifth,
  title={The Fifth PASCAL Recognizing Textual Entailment Challenge.},
  author={Bentivogli, Luisa and Clark, Peter and Dagan, Ido and Giampiccolo, Danilo},
  booktitle={TAC},
  year={2009}
}"""

_MULTIRC_CITATION = """\
@inproceedings{MultiRC2018,
    author = {Daniel Khashabi and Snigdha Chaturvedi and Michael Roth and Shyam Upadhyay and Dan Roth},
    title = {Looking Beyond the Surface:A Challenge Set for Reading Comprehension over Multiple Sentences},
    booktitle = {Proceedings of North American Chapter of the Association for Computational Linguistics (NAACL)},
    year = {2018}
}"""

_WIC_CITATION = """\
@article{DBLP:journals/corr/abs-1808-09121,
  author={Mohammad Taher Pilehvar and os{\'{e}} Camacho{-}Collados},
  title={WiC: 10, 000 Example Pairs for Evaluating Context-Sensitive Representations},
  journal={CoRR},
  volume={abs/1808.09121},
  year={2018},
  url={http://arxiv.org/abs/1808.09121},
  archivePrefix={arXiv},
  eprint={1808.09121},
  timestamp={Mon, 03 Sep 2018 13:36:40 +0200},
  biburl={https://dblp.org/rec/bib/journals/corr/abs-1808-09121},
  bibsource={dblp computer science bibliography, https://dblp.org}
}"""

_WSC_CITATION = """\
@inproceedings{levesque2012winograd,
  title={The winograd schema challenge},
  author={Levesque, Hector and Davis, Ernest and Morgenstern, Leora},
  booktitle={Thirteenth International Conference on the Principles of Knowledge Representation and Reasoning},
  year={2012}
}"""

_AXG_CITATION = """\
@inproceedings{rudinger-EtAl:2018:N18,
  author    = {Rudinger, Rachel  and  Naradowsky, Jason  and  Leonard, Brian  and  {Van Durme}, Benjamin},
  title     = {Gender Bias in Coreference Resolution},
  booktitle = {Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies},
  month     = {June},
  year      = {2018},
  address   = {New Orleans, Louisiana},
  publisher = {Association for Computational Linguistics}
}
"""


class SuperGlueConfig(nlp.BuilderConfig):
    """BuilderConfig for SuperGLUE."""

    def __init__(self, features, data_url, citation, url, label_classes=("False", "True"), **kwargs):
        """BuilderConfig for SuperGLUE.

    Args:
      features: `list[string]`, list of the features that will appear in the
        feature dict. Should not include "label".
      data_url: `string`, url to download the zip file from.
      citation: `string`, citation for the data set.
      url: `string`, url for information about the data set.
      label_classes: `list[string]`, the list of classes for the label if the
        label is present as a string. Non-string labels will be cast to either
        'False' or 'True'.
      **kwargs: keyword arguments forwarded to super.
    """
        # Version history:
        # 1.0.2: Fixed non-nondeterminism in ReCoRD.
        # 1.0.1: Change from the pre-release trial version of SuperGLUE (v1.9) to
        #        the full release (v2.0).
        # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
        # 0.0.2: Initial version.
        super(SuperGlueConfig, self).__init__(version=nlp.Version("1.0.2"), **kwargs)
        self.features = features
        self.label_classes = label_classes
        self.data_url = data_url
        self.citation = citation
        self.url = url


class SuperGlue(nlp.GeneratorBasedBuilder):
    """The SuperGLUE benchmark."""

    BUILDER_CONFIGS = [
        SuperGlueConfig(
            name="boolq",
            description=_BOOLQ_DESCRIPTION,
            features=["question", "passage"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/BoolQ.zip",
            citation=_BOOLQ_CITATION,
            url="https://github.com/google-research-datasets/boolean-questions",
        ),
        SuperGlueConfig(
            name="cb",
            description=_CB_DESCRIPTION,
            features=["premise", "hypothesis"],
            label_classes=["entailment", "contradiction", "neutral"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/CB.zip",
            citation=_CB_CITATION,
            url="https://github.com/mcdm/CommitmentBank",
        ),
        SuperGlueConfig(
            name="copa",
            description=_COPA_DESCRIPTION,
            label_classes=["choice1", "choice2"],
            # Note that question will only be the X in the statement "What's
            # the X for this?".
            features=["premise", "choice1", "choice2", "question"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/COPA.zip",
            citation=_COPA_CITATION,
            url="http://people.ict.usc.edu/~gordon/copa.html",
        ),
        SuperGlueConfig(
            name="multirc",
            description=_MULTIRC_DESCRIPTION,
            features=["paragraph", "question", "answer"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/MultiRC.zip",
            citation=_MULTIRC_CITATION,
            url="https://cogcomp.org/multirc/",
        ),
        SuperGlueConfig(
            name="record",
            description=_RECORD_DESCRIPTION,
            # Note that entities and answers will be a sequences of strings. Query
            # will contain @placeholder as a substring, which represents the word
            # to be substituted in.
            features=["passage", "query", "entities", "answers"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/ReCoRD.zip",
            citation=_RECORD_CITATION,
            url="https://sheng-z.github.io/ReCoRD-explorer/",
        ),
        SuperGlueConfig(
            name="rte",
            description=_RTE_DESCRIPTION,
            features=["premise", "hypothesis"],
            label_classes=["entailment", "not_entailment"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/RTE.zip",
            citation=_RTE_CITATION,
            url="https://aclweb.org/aclwiki/Recognizing_Textual_Entailment",
        ),
        SuperGlueConfig(
            name="wic",
            description=_WIC_DESCRIPTION,
            # Note that start1, start2, end1, and end2 will be integers stored as
            # nlp.Value('int32').
            features=["word", "sentence1", "sentence2", "start1", "start2", "end1", "end2"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/WiC.zip",
            citation=_WIC_CITATION,
            url="https://pilehvar.github.io/wic/",
        ),
        SuperGlueConfig(
            name="wsc",
            description=_WSC_DESCRIPTION,
            # Note that span1_index and span2_index will be integers stored as
            # nlp.Value('int32').
            features=["text", "span1_index", "span2_index", "span1_text", "span2_text"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/WSC.zip",
            citation=_WSC_CITATION,
            url="https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html",
        ),
        SuperGlueConfig(
            name="wsc.fixed",
            description=(
                _WSC_DESCRIPTION + "\n\nThis version fixes issues where the spans are not actually "
                "substrings of the text."
            ),
            # Note that span1_index and span2_index will be integers stored as
            # nlp.Value('int32').
            features=["text", "span1_index", "span2_index", "span1_text", "span2_text"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/WSC.zip",
            citation=_WSC_CITATION,
            url="https://cs.nyu.edu/faculty/davise/papers/WinogradSchemas/WS.html",
        ),
        SuperGlueConfig(
            name="axb",
            description=_AXB_DESCRIPTION,
            features=["sentence1", "sentence2"],
            label_classes=["entailment", "not_entailment"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/AX-b.zip",
            citation="",  # The GLUE citation is sufficient.
            url="https://gluebenchmark.com/diagnostics",
        ),
        SuperGlueConfig(
            name="axg",
            description=_AXG_DESCRIPTION,
            features=["premise", "hypothesis"],
            label_classes=["entailment", "not_entailment"],
            data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/AX-g.zip",
            citation=_AXG_CITATION,
            url="https://github.com/rudinger/winogender-schemas",
        ),
    ]

    def _info(self):
        features = {feature: nlp.Value("string") for feature in self.config.features}
        if self.config.name.startswith("wsc"):
            features["span1_index"] = nlp.Value("int32")
            features["span2_index"] = nlp.Value("int32")
        if self.config.name == "wic":
            features["start1"] = nlp.Value("int32")
            features["start2"] = nlp.Value("int32")
            features["end1"] = nlp.Value("int32")
            features["end2"] = nlp.Value("int32")
        if self.config.name == "multirc":
            features["idx"] = dict(
                {"paragraph": nlp.Value("int32"), "question": nlp.Value("int32"), "answer": nlp.Value("int32"),}
            )
        elif self.config.name == "record":
            features["idx"] = dict({"passage": nlp.Value("int32"), "query": nlp.Value("int32"),})
        else:
            features["idx"] = nlp.Value("int32")

        if self.config.name == "record":
            # Entities are the set of possible choices for the placeholder.
            features["entities"] = nlp.features.Sequence(nlp.Value("string"))
            # Answers are the subset of entities that are correct.
            features["answers"] = nlp.features.Sequence(nlp.Value("string"))
        else:
            features["label"] = nlp.features.ClassLabel(names=self.config.label_classes)

        return nlp.DatasetInfo(
            description=_GLUE_DESCRIPTION + self.config.description,
            features=nlp.Features(features),
            homepage=self.config.url,
            citation=self.config.citation + "\n" + _SUPER_GLUE_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(self.config.data_url) or ""
        task_name = _get_task_name_from_data_url(self.config.data_url)
        dl_dir = os.path.join(dl_dir, task_name)
        if self.config.name in ["axb", "axg"]:
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    gen_kwargs={
                        "data_file": os.path.join(dl_dir, "{}.jsonl".format(task_name)),
                        "split": nlp.Split.TEST,
                    },
                ),
            ]
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={"data_file": os.path.join(dl_dir, "train.jsonl"), "split": nlp.Split.TRAIN,},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                gen_kwargs={"data_file": os.path.join(dl_dir, "val.jsonl"), "split": nlp.Split.VALIDATION,},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={"data_file": os.path.join(dl_dir, "test.jsonl"), "split": nlp.Split.TEST,},
            ),
        ]

    def _generate_examples(self, data_file, split):
        with open(data_file) as f:
            for line in f:
                row = json.loads(line)

                if self.config.name == "multirc":
                    paragraph = row["passage"]
                    for question in paragraph["questions"]:
                        for answer in question["answers"]:
                            label = answer.get("label")
                            key = "%s_%s_%s" % (row["idx"], question["idx"], answer["idx"])
                            yield key, {
                                "paragraph": paragraph["text"],
                                "question": question["question"],
                                "answer": answer["text"],
                                "label": -1 if label is None else _cast_label(bool(label)),
                                "idx": {"paragraph": row["idx"], "question": question["idx"], "answer": answer["idx"]},
                            }
                elif self.config.name == "record":
                    passage = row["passage"]
                    for qa in row["qas"]:
                        yield qa["idx"], {
                            "passage": passage["text"],
                            "query": qa["query"],
                            "entities": _get_record_entities(passage),
                            "answers": _get_record_answers(qa),
                            "idx": {"passage": row["idx"], "query": qa["idx"]},
                        }
                else:
                    if self.config.name.startswith("wsc"):
                        row.update(row["target"])
                    example = {feature: row[feature] for feature in self.config.features}
                    if self.config.name == "wsc.fixed":
                        example = _fix_wst(example)
                    example["idx"] = row["idx"]

                    if "label" in row:
                        if self.config.name == "copa":
                            example["label"] = "choice2" if row["label"] else "choice1"
                        else:
                            example["label"] = _cast_label(row["label"])
                    else:
                        assert split == nlp.Split.TEST, row
                        example["label"] = -1
                    yield example["idx"], example


def _fix_wst(ex):
    """Fixes most cases where spans are not actually substrings of text."""

    def _fix_span_text(k):
        """Fixes a single span."""
        text = ex[k + "_text"]
        index = ex[k + "_index"]

        if text in ex["text"]:
            return

        if text in ("Kamenev and Zinoviev", "Kamenev, Zinoviev, and Stalin"):
            # There is no way to correct these examples since the subjects have
            # intervening text.
            return

        if "theyscold" in text:
            ex["text"].replace("theyscold", "they scold")
            ex["span2_index"] = 10
        # Make sure case of the first words match.
        first_word = ex["text"].split()[index]
        if first_word[0].islower():
            text = text[0].lower() + text[1:]
        else:
            text = text[0].upper() + text[1:]
        # Remove punctuation in span.
        text = text.rstrip(".")
        # Replace incorrect whitespace character in span.
        text = text.replace("\n", " ")
        ex[k + "_text"] = text
        assert ex[k + "_text"] in ex["text"], ex

    _fix_span_text("span1")
    _fix_span_text("span2")
    return ex


def _cast_label(label):
    """Converts the label into the appropriate string version."""
    if isinstance(label, six.string_types):
        return label
    elif isinstance(label, bool):
        return "True" if label else "False"
    elif isinstance(label, six.integer_types):
        assert label in (0, 1)
        return str(label)
    else:
        raise ValueError("Invalid label format.")


def _get_record_entities(passage):
    """Returns the unique set of entities."""
    text = passage["text"]
    entities = set()
    for entity in passage["entities"]:
        entities.add(text[entity["start"] : entity["end"] + 1])
    return sorted(entities)


def _get_record_answers(qa):
    """Returns the unique set of answers."""
    if "answers" not in qa:
        return []
    answers = set()
    for answer in qa["answers"]:
        answers.add(answer["text"])
    return sorted(answers)


def _get_task_name_from_data_url(data_url):
    return data_url.split("/")[-1].split(".")[0]
