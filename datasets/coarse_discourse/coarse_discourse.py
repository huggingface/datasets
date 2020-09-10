"""TODO(coarse_discourse): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(coarse_discourse): BibTeX citation
_CITATION = """\
@inproceedings{coarsediscourse, title={Characterizing Online Discussion Using Coarse Discourse Sequences}, author={Zhang, Amy X. and Culbertson, Bryan and Paritosh, Praveen}, booktitle={Proceedings of the 11th International AAAI Conference on Weblogs and Social Media}, series={ICWSM '17}, year={2017}, location = {Montreal, Canada} }
"""

# TODO(coarse_discourse):
_DESCRIPTION = """\
dataset contains discourse annotation and relation on threads from reddit during 2016
"""
_URL = "https://github.com/google-research-datasets/coarse-discourse/archive/master.zip"


class CoarseDiscourse(datasets.GeneratorBasedBuilder):
    """TODO(coarse_discourse): Short description of my dataset."""

    # TODO(coarse_discourse): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(coarse_discourse): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "title": datasets.Value("string"),
                    "is_self_post": datasets.Value("bool"),
                    "subreddit": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "majority_link": datasets.Value("string"),
                    "is_first_post": datasets.Value("bool"),
                    "majority_type": datasets.Value("string"),
                    "id_post": datasets.Value("string"),
                    "post_depth": datasets.Value("int32"),
                    "in_reply_to": datasets.Value("string"),
                    "annotations": datasets.features.Sequence(
                        {
                            "annotator": datasets.Value("string"),
                            "link_to_post": datasets.Value("string"),
                            "main_type": datasets.Value("string"),
                        }
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/google-research-datasets/coarse-discourse",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(coarse_discourse): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(dl_dir, "coarse-discourse-master", "coarse_discourse_dataset.json")
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(coarse_discourse): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                url = data.get("url", "")
                is_self_post = data.get("is_self_post", "")
                subreddit = data.get("subreddit", "")
                title = data.get("title", "")
                posts = data.get("posts", "")
                for id1, post in enumerate(posts):
                    maj_link = post.get("majority_link", "")
                    maj_type = post.get("majority_type", "")
                    id_post = post.get("id", "")
                    is_first_post = post.get("is_firs_post", "")
                    post_depth = post.get("post_depth", -1)
                    in_reply_to = post.get("in_reply_to", "")
                    annotations = post["annotations"]
                    annotators = [annotation.get("annotator", "") for annotation in annotations]
                    main_types = [annotation.get("main_type", "") for annotation in annotations]
                    link_posts = [annotation.get("linkk_to_post", "") for annotation in annotations]

                    yield str(id_) + "_" + str(id1), {
                        "title": title,
                        "is_self_post": is_self_post,
                        "subreddit": subreddit,
                        "url": url,
                        "majority_link": maj_link,
                        "is_first_post": is_first_post,
                        "majority_type": maj_type,
                        "id_post": id_post,
                        "post_depth": post_depth,
                        "in_reply_to": in_reply_to,
                        "annotations": {"annotator": annotators, "link_to_post": link_posts, "main_type": main_types},
                    }
