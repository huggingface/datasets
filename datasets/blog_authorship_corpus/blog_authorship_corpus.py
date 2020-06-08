from __future__ import absolute_import, division, print_function

import glob
import logging
import os

import nlp


_CITATION = """\
@inproceedings{schler2006effects,
    title={Effects of age and gender on blogging.},
    author={Schler, Jonathan and Koppel, Moshe and Argamon, Shlomo and Pennebaker, James W},
    booktitle={AAAI spring symposium: Computational approaches to analyzing weblogs},
    volume={6},
    pages={199--205},
    year={2006}
}
"""

_DESCRIPTION = """\
The Blog Authorship Corpus consists of the collected posts of 19,320 bloggers gathered from blogger.com in August 2004. The corpus incorporates a total of 681,288 posts and over 140 million words - or approximately 35 posts and 7250 words per person.

Each blog is presented as a separate file, the name of which indicates a blogger id# and the blogger’s self-provided gender, age, industry and astrological sign. (All are labeled for gender and age but for many, industry and/or sign is marked as unknown.)

All bloggers included in the corpus fall into one of three age groups:

·          8240 "10s" blogs (ages 13-17),

·          8086 "20s" blogs(ages 23-27)

·          2994 "30s" blogs (ages 33-47).

For each age group there are an equal number of male and female bloggers.

Each blog in the corpus includes at least 200 occurrences of common English words. All formatting has been stripped with two exceptions. Individual posts within a single blogger are separated by the date of the following post and links within a post are denoted by the label urllink.

The corpus may be freely used for non-commercial research purposes
"""
_URL = "https://u.cs.biu.ac.il/~koppel/BlogCorpus.htm"
_DATA_URL = "http://www.cs.biu.ac.il/~koppel/blogs/blogs.zip"


class BlogAuthorshipCorpusConfig(nlp.BuilderConfig):
    """BuilderConfig for BlogAuthorship."""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for BlogAuthorship

        Args:
          data_url: `string`, url to the dataset (word or raw level)
          **kwargs: keyword arguments forwarded to super.
        """
        super(BlogAuthorshipCorpusConfig, self).__init__(version=nlp.Version("1.0.0",), **kwargs)
        self.data_url = data_url


class BlogAuthorshipCorpus(nlp.GeneratorBasedBuilder):
    """TODO(BlogAuthorship): Short description of my dataset."""

    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        BlogAuthorshipCorpusConfig(
            name="blog-authorship-corpus",
            data_url=_DATA_URL,
            description="word level dataset. No processing is needed other than replacing newlines with <eos> tokens.",
        ),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "text": nlp.Value("string"),
                    "date": nlp.Value("string"),
                    "gender": nlp.Value("string"),
                    "age": nlp.Value("int32"),
                    "horoscope": nlp.Value("string"),
                    "job": nlp.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if self.config.name == "blog-authorship-corpus":
            data = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(data, "blogs")
            files = sorted(glob.glob(os.path.join(data_dir, "*.xml")))
            train_files = []
            validation_files = []

            for i, file_path in enumerate(files):
                # 95% / 5% (train / val) split
                if i % 20 == 0:
                    validation_files.append(file_path)
                else:
                    train_files.append(file_path)

            return [
                nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"files": train_files, "split": "train"},),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION, gen_kwargs={"files": validation_files, "split": "validation"},
                ),
            ]
        else:
            raise ValueError("{} does not exist".format(self.config.name))

    def _generate_examples(self, files, split):
        def parse_date(line):
            # parse line to date
            return line.strip().split("<date>")[-1].split("</date>")[0]

        for file_path in files:
            counter = 0
            file_name = os.path.basename(file_path)
            logging.info("generating examples from = %s", file_path)
            file_id, gender, age, job, horoscope = tuple(file_name.split(".")[:-1])

            # Note: import xml.etree.ElementTree as etree does not work. File cannot be parsed
            # use open instead
            with open(file_path) as f:
                # some files are corrupted, so have to work with python`s try here
                try:
                    date = ""
                    for line in f:
                        line = line.strip()
                        if "<date>" in line:
                            date = parse_date(line)
                        elif line != "" and not line.startswith("<"):
                            # need sub_id to be certain that no tf_records is identical
                            sub_id = counter
                            counter += 1
                            if date == "":
                                logging.warning("Date missing for {} in {}".format(line, file_name))
                            assert date is not None, "Date is missing before {}".format(line)
                            blog = {
                                "text": line,
                                "date": date,
                                "gender": gender,
                                "age": int(age),
                                "job": job,
                                "horoscope": horoscope,
                            }
                            yield "{}_{}_{}".format(file_id, sub_id, date), blog
                        else:
                            continue
                except UnicodeDecodeError as e:
                    logging.warning("{} cannot be loaded. Error message: {}".format(file_path, e))
