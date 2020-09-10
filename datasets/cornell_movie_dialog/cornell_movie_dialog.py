"""TODO(cornell_movie_dialog): Add a description here."""

from __future__ import absolute_import, division, print_function

import ast
import os

import datasets


# TODO(cornell_movie_dialog): BibTeX citation
_CITATION = """\
  @InProceedings{Danescu-Niculescu-Mizil+Lee:11a,

  author={Cristian Danescu-Niculescu-Mizil and Lillian Lee},

  title={Chameleons in imagined conversations:
  A new approach to understanding coordination of linguistic style in dialogs.},

  booktitle={Proceedings of the

        Workshop on Cognitive Modeling and Computational Linguistics, ACL 2011},

  year={2011}

}
"""

# TODO(cornell_movie_dialog):
_DESCRIPTION = """\
This corpus contains a large metadata-rich collection of fictional conversations extracted from raw movie scripts:
- 220,579 conversational exchanges between 10,292 pairs of movie characters
- involves 9,035 characters from 617 movies
- in total 304,713 utterances
- movie metadata included:
    - genres
    - release year
    - IMDB rating
    - number of IMDB votes
    - IMDB rating
- character metadata included:
    - gender (for 3,774 characters)
    - position on movie credits (3,321 characters)
"""

_URL = "https://www.cs.cornell.edu/~cristian/data/cornell_movie_dialogs_corpus.zip"


class CornellMovieDialog(datasets.GeneratorBasedBuilder):
    """TODO(cornell_movie_dialog): Short description of my dataset."""

    # TODO(cornell_movie_dialog): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(cornell_movie_dialog): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "movieID": datasets.Value("string"),
                    "movieTitle": datasets.Value("string"),
                    "movieYear": datasets.Value("string"),
                    "movieIMDBRating": datasets.Value("string"),
                    "movieNoIMDBVotes": datasets.Value("string"),
                    "movieGenres": datasets.features.Sequence(datasets.Value("string")),
                    "characterID1": datasets.Value("string"),
                    "characterID2": datasets.Value("string"),
                    "characterName1": datasets.Value("string"),
                    "characterName2": datasets.Value("string"),
                    "utterance": datasets.features.Sequence(
                        {"text": datasets.Value("string"), "LineID": datasets.Value("string")}
                    )
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(cornell_movie_dialog): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepaths": os.path.join(dl_dir, "cornell movie-dialogs corpus")},
            ),
        ]

    def _generate_examples(self, filepaths):
        """Yields examples."""
        # TODO(cornell_movie_dialog): Yields (key, example) tuples from the dataset
        movie_char_file = os.path.join(filepaths, "movie_characters_metadata.txt")
        movie_conv_file = os.path.join(filepaths, "movie_conversations.txt")
        movie_lines_file = os.path.join(filepaths, "movie_lines.txt")
        movie_titles_file = os.path.join(filepaths, "movie_titles_metadata.txt")

        with open(movie_char_file, "rb") as f:
            movie_char_data = [x.decode("latin").split("+++$+++") for x in f.readlines()]

        with open(movie_conv_file, "rb") as f:
            movie_conv_data = [x.decode("latin").split("+++$+++") for x in f.readlines()]

        with open(movie_lines_file, "rb") as f:
            movie_lines_data = [x.decode("latin").split("+++$+++") for x in f.readlines()]

        with open(movie_titles_file, "rb") as f:
            movie_titles_data = [x.decode("latin").split("+++$+++") for x in f.readlines()]
        # looping over movie conversation file
        for id_, conv in enumerate(movie_conv_data):
            char_id_1 = conv[0]
            char_id_2 = conv[1]
            movie_id = conv[2]
            line_ids = conv[-1].replace("\n", "")
            line_ids = ast.literal_eval(line_ids.strip())
            lines_texts = []
            # searching text corresponding to each lineID in line_ids in movie lines file
            for line_id in line_ids:
                i = 0
                while i < len(movie_lines_data) and movie_lines_data[i][0].strip() != line_id:
                    i += 1
                lines_texts.append(movie_lines_data[i][0])  # if i < len(movie_lines_data) else '')
            # look for char names in movie character file
            j = 0
            while j < len(movie_char_data) and movie_char_data[j][0].strip() != char_id_1.strip():
                j += 1
            char_name_1 = movie_char_data[j][1]  # if j < len(movie_char_data) else ''
            movie_title = movie_char_data[j][3]  # if j < len(movie_char_data) else ''

            k = 0
            while k < len(movie_char_data) and movie_char_data[k][0].strip() != char_id_2.strip():
                k += 1
            char_name_2 = movie_char_data[k][1]

            # look for movie year, IMDBRating, genre, no_imdb_voting in movie tiles file
            li = 0
            while li < len(movie_titles_data) and movie_titles_data[li][0].strip() != movie_id.strip():
                li += 1
            movie_year = movie_titles_data[li][2]
            imdb_rating = movie_titles_data[li][3]
            no_imdb_vote = movie_titles_data[li][4]
            genre = movie_titles_data[li][5].replace("\n", "").strip()
            movie_genres = ast.literal_eval(genre)

            yield id_, {
                "movieID": movie_id,
                "movieTitle": movie_title,
                "movieYear": movie_year,
                "movieIMDBRating": imdb_rating,
                "movieNoIMDBVotes": no_imdb_vote,
                "movieGenres": movie_genres,
                "characterID1": char_id_1,
                "characterID2": char_id_2,
                "characterName1": char_name_1,
                "characterName2": char_name_2,
                "utterance": {"text": lines_texts, "LineID": line_ids},
            }
