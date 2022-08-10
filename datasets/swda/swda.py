# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""
Switchboard Dialog Act Corpus
The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2,
with turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information
about the associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s.

This script is a modified version of the original swda.py from https://github.com/cgpotts/swda/blob/master/swda.py from
the original corpus repo. Modifications are made to accommodate the HuggingFace Dataset project format.
"""


import csv
import datetime
import glob
import io
import os
import re

import datasets


# Citation as described here: https://github.com/cgpotts/swda#citation.
_CITATION = """\
@techreport{Jurafsky-etal:1997,
    Address = {Boulder, CO},
    Author = {Jurafsky, Daniel and Shriberg, Elizabeth and Biasca, Debra},
    Institution = {University of Colorado, Boulder Institute of Cognitive Science},
    Number = {97-02},
    Title = {Switchboard {SWBD}-{DAMSL} Shallow-Discourse-Function Annotation Coders Manual, Draft 13},
    Year = {1997}}

@article{Shriberg-etal:1998,
    Author = {Shriberg, Elizabeth and Bates, Rebecca and Taylor, Paul and Stolcke, Andreas and Jurafsky, Daniel and Ries, Klaus and Coccaro, Noah and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
    Journal = {Language and Speech},
    Number = {3--4},
    Pages = {439--487},
    Title = {Can Prosody Aid the Automatic Classification of Dialog Acts in Conversational Speech?},
    Volume = {41},
    Year = {1998}}

@article{Stolcke-etal:2000,
    Author = {Stolcke, Andreas and Ries, Klaus and Coccaro, Noah and Shriberg, Elizabeth and Bates, Rebecca and Jurafsky, Daniel and Taylor, Paul and Martin, Rachel and Meteer, Marie and Van Ess-Dykema, Carol},
    Journal = {Computational Linguistics},
    Number = {3},
    Pages = {339--371},
    Title = {Dialogue Act Modeling for Automatic Tagging and Recognition of Conversational Speech},
    Volume = {26},
    Year = {2000}}
"""

# Description of dataset gathered from: https://github.com/cgpotts/swda#overview.
_DESCRIPTION = """\
The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2 with
turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information about the
associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s.
The SwDA is not inherently linked to the Penn Treebank 3 parses of Switchboard, and it is far from straightforward to
align the two resources. In addition, the SwDA is not distributed with the Switchboard's tables of metadata about the
conversations and their participants.
"""

# Homepage gathered from: https://github.com/cgpotts/swda#overview.
_HOMEPAGE = "http://compprag.christopherpotts.net/swda.html"

# More details about the license: https://creativecommons.org/licenses/by-nc-sa/3.0/.
_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License"

# Dataset main url.
_URL = "https://github.com/cgpotts/swda/raw/master/swda.zip"

# Dialogue act tags - long version 217 dialogue acts labels.
_ACT_TAGS = [
    "b^m^r",
    "qw^r^t",
    "aa^h",
    "br^m",
    "fa^r",
    "aa,ar",
    "sd^e(^q)^r",
    "^2",
    "sd;qy^d",
    "oo",
    "bk^m",
    "aa^t",
    "cc^t",
    "qy^d^c",
    "qo^t",
    "ng^m",
    "qw^h",
    "qo^r",
    "aa",
    "qy^d^t",
    "qrr^d",
    "br^r",
    "fx",
    "sd,qy^g",
    "ny^e",
    "^h^t",
    "fc^m",
    "qw(^q)",
    "co",
    "o^t",
    "b^m^t",
    "qr^d",
    "qw^g",
    "ad(^q)",
    "qy(^q)",
    "na^r",
    "am^r",
    "qr^t",
    "ad^c",
    "qw^c",
    "bh^r",
    "h^t",
    "ft^m",
    "ba^r",
    "qw^d^t",
    "%",
    "t3",
    "nn",
    "bd",
    "h^m",
    "h^r",
    "sd^r",
    "qh^m",
    "^q^t",
    "sv^2",
    "ft",
    "ar^m",
    "qy^h",
    "sd^e^m",
    "qh^r",
    "cc",
    "fp^m",
    "ad",
    "qo",
    "na^m^t",
    "fo^c",
    "qy",
    "sv^e^r",
    "aap",
    "no",
    "aa^2",
    "sv(^q)",
    "sv^e",
    "nd",
    '"',
    "bf^2",
    "bk",
    "fp",
    "nn^r^t",
    "fa^c",
    "ny^t",
    "ny^c^r",
    "qw",
    "qy^t",
    "b",
    "fo",
    "qw^r",
    "am",
    "bf^t",
    "^2^t",
    "b^2",
    "x",
    "fc",
    "qr",
    "no^t",
    "bk^t",
    "bd^r",
    "bf",
    "^2^g",
    "qh^c",
    "ny^c",
    "sd^e^r",
    "br",
    "fe",
    "by",
    "^2^r",
    "fc^r",
    "b^m",
    "sd,sv",
    "fa^t",
    "sv^m",
    "qrr",
    "^h^r",
    "na",
    "fp^r",
    "o",
    "h,sd",
    "t1^t",
    "nn^r",
    "cc^r",
    "sv^c",
    "co^t",
    "qy^r",
    "sv^r",
    "qy^d^h",
    "sd",
    "nn^e",
    "ny^r",
    "b^t",
    "ba^m",
    "ar",
    "bf^r",
    "sv",
    "bh^m",
    "qy^g^t",
    "qo^d^c",
    "qo^d",
    "nd^t",
    "aa^r",
    "sd^2",
    "sv;sd",
    "qy^c^r",
    "qw^m",
    "qy^g^r",
    "no^r",
    "qh(^q)",
    "sd;sv",
    "bf(^q)",
    "+",
    "qy^2",
    "qw^d",
    "qy^g",
    "qh^g",
    "nn^t",
    "ad^r",
    "oo^t",
    "co^c",
    "ng",
    "^q",
    "qw^d^c",
    "qrr^t",
    "^h",
    "aap^r",
    "bc^r",
    "sd^m",
    "bk^r",
    "qy^g^c",
    "qr(^q)",
    "ng^t",
    "arp",
    "h",
    "bh",
    "sd^c",
    "^g",
    "o^r",
    "qy^c",
    "sd^e",
    "fw",
    "ar^r",
    "qy^m",
    "bc",
    "sv^t",
    "aap^m",
    "sd;no",
    "ng^r",
    "bf^g",
    "sd^e^t",
    "o^c",
    "b^r",
    "b^m^g",
    "ba",
    "t1",
    "qy^d(^q)",
    "nn^m",
    "ny",
    "ba,fe",
    "aa^m",
    "qh",
    "na^m",
    "oo(^q)",
    "qw^t",
    "na^t",
    "qh^h",
    "qy^d^m",
    "ny^m",
    "fa",
    "qy^d",
    "fc^t",
    "sd(^q)",
    "qy^d^r",
    "bf^m",
    "sd(^q)^t",
    "ft^t",
    "^q^r",
    "sd^t",
    "sd(^q)^r",
    "ad^t",
]

# Damsl dialogue act tags version - short version 43 dialogue acts labels.
_DAMSL_ACT_TAGS = [
    "ad",
    "qo",
    "qy",
    "arp_nd",
    "sd",
    "h",
    "bh",
    "no",
    "^2",
    "^g",
    "ar",
    "aa",
    "sv",
    "bk",
    "fp",
    "qw",
    "b",
    "ba",
    "t1",
    "oo_co_cc",
    "+",
    "ny",
    "qw^d",
    "x",
    "qh",
    "fc",
    'fo_o_fw_"_by_bc',
    "aap_am",
    "%",
    "bf",
    "t3",
    "nn",
    "bd",
    "ng",
    "^q",
    "br",
    "qy^d",
    "fa",
    "^h",
    "b^m",
    "ft",
    "qrr",
    "na",
]


class Swda(datasets.GeneratorBasedBuilder):
    """
    This is the HuggingFace Dataset class for swda.

    Switchboard Dialog Act Corpus Hugging Face Dataset class.
    The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2,
    with turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information
    about the associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s.

    """

    # Urls for each split train-dev-test.
    _URLS = {
        "train": "https://github.com/NathanDuran/Probabilistic-RNN-DA-Classifier/raw/master/data/train_split.txt",
        "dev": "https://github.com/NathanDuran/Probabilistic-RNN-DA-Classifier/raw/master/data/dev_split.txt",
        "test": "https://github.com/NathanDuran/Probabilistic-RNN-DA-Classifier/raw/master/data/test_split.txt",
    }

    def _info(self):
        """
        Specify the datasets.DatasetInfo object which contains information and typings for the dataset.
        """

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types.
            features=datasets.Features(
                {
                    "swda_filename": datasets.Value("string"),
                    "ptb_basename": datasets.Value("string"),
                    "conversation_no": datasets.Value("int64"),
                    "transcript_index": datasets.Value("int64"),
                    "act_tag": datasets.ClassLabel(num_classes=217, names=_ACT_TAGS),
                    "damsl_act_tag": datasets.ClassLabel(num_classes=43, names=_DAMSL_ACT_TAGS),
                    "caller": datasets.Value("string"),
                    "utterance_index": datasets.Value("int64"),
                    "subutterance_index": datasets.Value("int64"),
                    "text": datasets.Value("string"),
                    "pos": datasets.Value("string"),
                    "trees": datasets.Value("string"),
                    "ptb_treenumbers": datasets.Value("string"),
                    "talk_day": datasets.Value("string"),
                    "length": datasets.Value("int64"),
                    "topic_description": datasets.Value("string"),
                    "prompt": datasets.Value("string"),
                    "from_caller": datasets.Value("int64"),
                    "from_caller_sex": datasets.Value("string"),
                    "from_caller_education": datasets.Value("int64"),
                    "from_caller_birth_year": datasets.Value("int64"),
                    "from_caller_dialect_area": datasets.Value("string"),
                    "to_caller": datasets.Value("int64"),
                    "to_caller_sex": datasets.Value("string"),
                    "to_caller_education": datasets.Value("int64"),
                    "to_caller_birth_year": datasets.Value("int64"),
                    "to_caller_dialect_area": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """
        Returns SplitGenerators.
        This method is tasked with downloading/extracting the data and defining the splits.

         Args:
            dl_manager (:obj:`datasets.utils.download_manager.DownloadManager`):
                Download manager to download and extract data files from urls.

        Returns:
            :obj:`list[str]`:
                List of paths to data.
        """

        # Download extract and return path of data file.
        dl_dir = dl_manager.download_and_extract(_URL)
        # Use swda/ folder.
        data_dir = os.path.join(dl_dir, "swda")
        # Handle partitions files.
        urls_to_download = self._URLS
        # Download extract and return paths of split files.
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            # Return whole data path and train splits file downloaded path.
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"data_dir": data_dir, "split_file": downloaded_files["train"]}
            ),
            # Return whole data path and dev splits file downloaded path.
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_dir": data_dir, "split_file": downloaded_files["dev"]},
            ),
            # Return whole data path and train splits file downloaded path.
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"data_dir": data_dir, "split_file": downloaded_files["test"]}
            ),
        ]

    def _generate_examples(self, data_dir, split_file):
        """
        Yields examples.
        This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        The key is not important, it's more here for legacy reason (legacy from tfds).

        Args:
            data_dir (:obj:`str`):
                Path where is downloaded dataset.

            split_file (:obj:`str`):
                Path of split file used for train-dev-test.

        Returns:
            :obj:`list[str]`:
                List of paths to data.
        """

        # Read in the split file.
        split_file = io.open(file=split_file, mode="r", encoding="utf-8").read().splitlines()
        # Read in corpus data using split files.
        corpus = CorpusReader(src_dirname=data_dir, split_file=split_file)
        # Generate examples.
        for i_trans, trans in enumerate(corpus.iter_transcripts()):
            for i_utt, utt in enumerate(trans.utterances):
                id_ = str(i_trans) + ":" + str(i_utt)
                yield id_, {feature: utt[feature] for feature in self.info.features.keys()}


class CorpusReader:
    """Class for reading in the corpus and iterating through its values."""

    def __init__(self, src_dirname, split_file=None):
        """
        Reads in the data from `src_dirname` (should be the root of the
        corpus).  Assumes that the metadata file `swda-metadata.csv` is
        in the main directory of the corpus, using that file to build
        the `Metadata` object used throughout.

        Args:
            src_dirname (:obj:`str`):
                Path where swda folder with all data.

            split_file (:obj:`list[str`, `optional`):
                List of file names used in a split (train, dev or test). This argument is optional and it will have a None value attributed inside the function.

        """

        self.src_dirname = src_dirname
        metadata_filename = os.path.join(src_dirname, "swda-metadata.csv")
        self.metadata = Metadata(metadata_filename)
        self.split_file = split_file

    def iter_transcripts(
        self,
    ):
        """
        Iterate through the transcripts.

        Returns:
            :obj:`Transcript`:
                Transcript instance.
        """

        # All files names.
        filenames = glob.glob(os.path.join(self.src_dirname, "sw*", "*.csv"))
        # If no split files are mentioned just use all files.
        self.split_file = filenames if self.split_file is None else self.split_file
        # Filter out desired file names
        filenames = [
            file for file in filenames if os.path.basename(file).split("_")[-1].split(".")[0] in self.split_file
        ]
        for filename in sorted(filenames):
            # Yield the Transcript instance:
            yield Transcript(filename, self.metadata)

    def iter_utterances(
        self,
    ):
        """
        Iterate through the utterances.

        Returns:
            :obj:`Transcript.utterances`:
                Utterance instance object.
        """

        for trans in self.iter_transcripts():
            for utt in trans.utterances:
                # Yield the Utterance instance:
                yield utt


class Metadata:
    """
    Basically an internal method for organizing the tables of metadata
    from the original Switchboard transcripts and linking them with
    the dialog acts.
    """

    def __init__(self, metadata_filename):
        """
        Turns the CSV file into a dictionary mapping Switchboard
        conversation_no integers values to dictionaries of values. All
        the keys correspond to the column names in the original
        tables.

        Args:
            metadata_filename (:obj:`str`):
                The CSV file swda-metadata.csv (should be in the main
                folder of the swda directory).

        """
        self.metadata_filename = metadata_filename
        self.metadata = {}
        self.get_metadata()

    def get_metadata(self):
        """
        Build the dictionary self.metadata mapping conversation_no to
        dictionaries of values (str, int, or datatime, as
        appropriate).
        """

        csvreader = csv.reader(open(self.metadata_filename))
        header = next(csvreader)
        for row in csvreader:
            d = dict(list(zip(header, row)))
            # Add integer number features to metadata.
            for key in (
                "conversation_no",
                "length",
                "from_caller",
                "to_caller",
                "from_caller_education",
                "to_caller_education",
            ):
                d[key] = int(d[key])
            talk_day = d["talk_day"]
            talk_year = int("19" + talk_day[:2])
            talk_month = int(talk_day[2:4])
            talk_day = int(talk_day[4:])
            # Make sure to convert date time to string to match PyArrow data formats.
            d["talk_day"] = datetime.datetime(year=talk_year, month=talk_month, day=talk_day).strftime("%m/%d/%Y")
            d["from_caller_birth_year"] = int(d["from_caller_birth_year"])
            d["to_caller_birth_year"] = int(d["to_caller_birth_year"])
            self.metadata[d["conversation_no"]] = d

    def __getitem__(self, val):
        """
        Val should be a key in self.metadata; returns the
        corresponding value.

        Args:
            val (:obj:`str`):
                Key in self.metadata.

        Returns:
            :obj::
                Corresponding value.

        """

        return self.metadata[val]


class Utterance:
    """
    The central object of interest. The attributes correspond to the
    values of the class variable header:

    """

    # Metadata header file.
    header = [
        "swda_filename",
        "ptb_basename",
        "conversation_no",
        "transcript_index",
        "act_tag",
        "caller",
        "utterance_index",
        "subutterance_index",
        "text",
        "pos",
        "trees",
        "ptb_treenumbers",
    ]

    def __init__(self, row, transcript_metadata):
        """
        Args:
            row (:obj:`list`):
                A row from one of the corpus CSV files.

            transcript_metadata (:obj:`dict`):
                A Metadata value based on the current `conversation_no`.

        """

        # Utterance data:
        for i in range(len(Utterance.header)):
            att_name = Utterance.header[i]
            row_value = None
            if i < len(row):
                row_value = row[i].strip()
            # Special handling of non-string values.
            if att_name == "trees":
                if row_value:
                    # Origianl code returned list of nltk.tree and used `[Tree.fromstring(t) for t in row_value.split("|||")]`.
                    # Since we're returning str we don't need to make any mondifications to row_value.
                    row_value = row_value
                else:
                    row_value = ""  # []
            elif att_name == "ptb_treenumbers":
                if row_value:
                    row_value = row_value  # list(map(int, row_value.split("|||")))
                else:
                    row_value = ""  # []
            elif att_name == "act_tag":
                # I thought these conjoined tags were meant to be split.
                # The docs suggest that they are single tags, thought,
                # so skip this conditional and let it be treated as a str.
                # row_value = re.split(r"\s*[,;]\s*", row_value)
                # `` Transcription errors (typos, obvious mistranscriptions) are
                # marked with a "*" after the discourse tag.''
                # These are removed for this version.
                row_value = row_value.replace("*", "")
            elif att_name in ("conversation_no", "transcript_index", "utterance_index", "subutterance_index"):
                row_value = int(row_value)
            # Add attribute.
            setattr(self, att_name, row_value)
        # Make sure conversation number matches.
        assert self.conversation_no == transcript_metadata["conversation_no"]
        # Add rest of missing metadata
        [setattr(self, key, value) for key, value in transcript_metadata.items()]
        # Add damsl tags.
        setattr(self, "damsl_act_tag", self.damsl_act_tag())

    def __getitem__(self, feature):
        """
        Return utterance features as dictionary. It allows us to call an utterance object as a dictionary.
        It contains same keys as attributes.

        Args:
            feature (:obj:`str`):
                Feature value of utterance that is part of attributes.

        Returns:
            :obj:
                Value of feature from utterance. Value type can vary.
        """

        return vars(self)[feature]

    def damsl_act_tag(
        self,
    ):
        """
        Seeks to duplicate the tag simplification described at the
        Coders' Manual: http://www.stanford.edu/~jurafsky/ws97/manual.august1.html
        """

        d_tags = []
        tags = re.split(r"\s*[,;]\s*", self.act_tag)
        for tag in tags:
            if tag in ("qy^d", "qw^d", "b^m"):
                pass
            elif tag == "nn^e":
                tag = "ng"
            elif tag == "ny^e":
                tag = "na"
            else:
                tag = re.sub(r"(.)\^.*", r"\1", tag)
                tag = re.sub(r"[\(\)@*]", "", tag)
                if tag in ("qr", "qy"):
                    tag = "qy"
                elif tag in ("fe", "ba"):
                    tag = "ba"
                elif tag in ("oo", "co", "cc"):
                    tag = "oo_co_cc"
                elif tag in ("fx", "sv"):
                    tag = "sv"
                elif tag in ("aap", "am"):
                    tag = "aap_am"
                elif tag in ("arp", "nd"):
                    tag = "arp_nd"
                elif tag in ("fo", "o", "fw", '"', "by", "bc"):
                    tag = 'fo_o_fw_"_by_bc'
            d_tags.append(tag)
        # Dan J says (p.c.) that it makes sense to take the first;
        # there are only a handful of examples with 2 tags here.
        return d_tags[0]


class Transcript:
    """
    Transcript instances are basically just containers for lists of
    utterances and transcript-level metadata, accessible via
    attributes.
    """

    def __init__(self, swda_filename, metadata):
        """
        Sets up all the attribute values:

        Args:
            swda_filename (:obj:`str`):
                The filename for this transcript.

            metadata (:obj:`str` or `Metadata`):
                If a string, then assumed to be the metadata filename, and
                the metadata is created from that filename. If a `Metadata`
                object, then used as the needed metadata directly.

        """

        self.swda_filename = swda_filename
        # If the supplied value is a filename:
        if isinstance(metadata, str) or isinstance(metadata, str):
            self.metadata = Metadata(metadata)
        else:  # Where the supplied value is already a Metadata object.
            self.metadata = metadata
        # Get the file rows:
        rows = list(csv.reader(open(self.swda_filename, "rt")))
        # Ge the header and remove it from the rows:
        self.header = rows[0]
        rows.pop(0)
        # Extract the conversation_no to get the meta-data. Use the
        # header for this in case the column ordering is ever changed:
        row0dict = dict(list(zip(self.header, rows[1])))
        self.conversation_no = int(row0dict["conversation_no"])
        # The ptd filename in the right format for the current OS:
        self.ptd_basename = os.sep.join(row0dict["ptb_basename"].split("/"))
        # The dictionary of metadata for this transcript:
        transcript_metadata = self.metadata[self.conversation_no]
        for key, val in transcript_metadata.items():
            setattr(self, key, transcript_metadata[key])
        # Create the utterance list:
        self.utterances = [Utterance(x, transcript_metadata) for x in rows]
        # Coder's Manual: ``We also removed any line with a "@"
        # (since @ marked slash-units with bad segmentation).''
        self.utterances = [u for u in self.utterances if not re.search(r"[@]", u.act_tag)]
