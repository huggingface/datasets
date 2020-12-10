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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function
import datasets

# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{hindencorp05:lrec:2014,
  author = {Ond{\v{r}}ej Bojar and Vojt{\v{e}}ch Diatka
            and Pavel Rychl{\'{y}} and Pavel Stra{\v{n}}{\'{a}}k
            and V{\'{\i}}t Suchomel and Ale{\v{s}} Tamchyna and Daniel Zeman},
  title = "{HindEnCorp - Hindi-English and Hindi-only Corpus for Machine
            Translation}",
  booktitle = {Proceedings of the Ninth International Conference on Language
               Resources and Evaluation (LREC'14)},
  year = {2014},
  month = {may},
  date = {26-31},
  address = {Reykjavik, Iceland},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and
     Thierry Declerck and Hrafn Loftsson and Bente Maegaard and Joseph Mariani
     and Asuncion Moreno and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-8-4},
  language = {english}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve research in monolingual and multilingual translation task and is crafted with a lot of care."""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://lindat.mff.cuni.cz/repository/xmlui/handle/11858/00-097C-0000-0023-625F-0"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "CC BY-NC-SA 3.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11858/00-097C-0000-0023-625F-0/hindencorp05.plaintext.gz?sequence=3&isAllowed=y"

# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class HindEnCorp(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""
    

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.
    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig
    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    def _info(self):
        # TODO: This method pecifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        # This is the name of the configuration selected in BUILDER_CONFIGS above

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "source": datasets.Sequence(datasets.Value("string")),
                "alignment_type": datasets.Sequence(datasets.Value("string")),
                "alignment_quality": datasets.Sequence(datasets.Value("string")),
                "English": datasets.Sequence(datasets.Value("string")),
                "Hindi": datasets.Sequence(datasets.Value("string"))
                # These are the features of your dataset like images, labels ...
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URLs)
        # data_paths = [os.path.join(pth, f)
        # for pth, dirs, files in os.walk(data_dir) for f in files]
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        # for filepath in filepath:
        with open(filepath, encoding="utf-8") as f:
            id_ = 0
            source = []
            alignment_type = []
            alignment_quality = []
            English = []
            Hindi = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n" or line == "\t":
                    if source:
                        yield id_, {
                            "id": str(id_),
                            "source": source,
                            "alignment_type": alignment_type,
                            "alignment_quality": alignment_quality,
                            "English": English,
                            "Hindi": Hindi,
                        }
                        id_ += 1
                        source = []
                        alignment_type = []
                        alignment_quality = []
                        English = []
                        Hindi = []
                else:
                    # conll2003 tokens are space separated
                    splits = line.split("\t")
                    source.append(splits[0])
                    alignment_type.append(splits[1])
                    alignment_quality.append(splits[2])
                    English.append(splits[3])
                    Hindi.append(splits[4])
            # last exampleguid
            yield id_, {
                "id": str(id_),
                "source": source,
                "alignment_type": alignment_type,
                "alignment_quality": alignment_quality,
                "English": English,
                "Hindi": Hindi,
            }
