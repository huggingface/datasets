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


import datasets


_CITATION = """\
@InProceedings{hindencorp05:lrec:2014,
  author = {Ond{\v{r}}ej Bojar and Vojt{\v{e}}ch Diatka
            and Pavel Rychl{\'{y}} and Pavel Stra{\v{n}}{\'{a}}k
            and V{\'{}}t Suchomel and Ale{\v{s}} Tamchyna and Daniel Zeman},
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

_DESCRIPTION = """\
HindEnCorp parallel texts (sentence-aligned) come from the following sources:
Tides, which contains 50K sentence pairs taken mainly from news articles. This dataset was originally col- lected for the DARPA-TIDES surprise-language con- test in 2002, later refined at IIIT Hyderabad and provided for the NLP Tools Contest at ICON 2008 (Venkatapathy, 2008).

Commentaries by Daniel Pipes contain 322 articles in English written by a journalist Daniel Pipes and translated into Hindi.

EMILLE. This corpus (Baker et al., 2002) consists of three components: monolingual, parallel and annotated corpora. There are fourteen monolingual sub- corpora, including both written and (for some lan- guages) spoken data for fourteen South Asian lan- guages. The EMILLE monolingual corpora contain in total 92,799,000 words (including 2,627,000 words of transcribed spoken data for Bengali, Gujarati, Hindi, Punjabi and Urdu). The parallel corpus consists of 200,000 words of text in English and its accompanying translations into Hindi and other languages.

Smaller datasets as collected by Bojar et al. (2010) include the corpus used at ACL 2005 (a subcorpus of EMILLE), a corpus of named entities from Wikipedia (crawled in 2009), and Agriculture domain parallel corpus.
￼
For the current release, we are extending the parallel corpus using these sources:
Intercorp (Čermák and Rosen,2012) is a large multilingual parallel corpus of 32 languages including Hindi. The central language used for alignment is Czech. Intercorp’s core texts amount to 202 million words. These core texts are most suitable for us because their sentence alignment is manually checked and therefore very reliable. They cover predominately short sto- ries and novels. There are seven Hindi texts in Inter- corp. Unfortunately, only for three of them the English translation is available; the other four are aligned only with Czech texts. The Hindi subcorpus of Intercorp contains 118,000 words in Hindi.

TED talks 3 held in various languages, primarily English, are equipped with transcripts and these are translated into 102 languages. There are 179 talks for which Hindi translation is available.

The Indic multi-parallel corpus (Birch et al., 2011; Post et al., 2012) is a corpus of texts from Wikipedia translated from the respective Indian language into English by non-expert translators hired over Mechanical Turk. The quality is thus somewhat mixed in many respects starting from typesetting and punctuation over capi- talization, spelling, word choice to sentence structure. A little bit of control could be in principle obtained from the fact that every input sentence was translated 4 times. We used the 2012 release of the corpus.

Launchpad.net is a software collaboration platform that hosts many open-source projects and facilitates also collaborative localization of the tools. We downloaded all revisions of all the hosted projects and extracted the localization (.po) files.

Other smaller datasets. This time, we added Wikipedia entities as crawled in 2013 (including any morphological variants of the named entitity that appears on the Hindi variant of the Wikipedia page) and words, word examples and quotes from the Shabdkosh online dictionary.
"""

_HOMEPAGE = "https://lindat.mff.cuni.cz/repository/xmlui/handle/11858/00-097C-0000-0023-625F-0"

_LICENSE = "CC BY-NC-SA 3.0"

_URLs = "https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11858/00-097C-0000-0023-625F-0/hindencorp05.plaintext.gz?sequence=3&isAllowed=y"


class HindEncorp(datasets.GeneratorBasedBuilder):
    """Short description of my dataset."""

    def _info(self):

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "source": datasets.Value("string"),
                "alignment_type": datasets.Value("string"),
                "alignment_quality": datasets.Value("string"),
                "translation": datasets.features.Translation(languages=["en", "hi"]),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = dl_manager.download_and_extract(_URLs)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_dir},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                splits = line.strip().split("\t")
                yield id_, {
                    "id": str(id_),
                    "source": splits[0],
                    "alignment_type": splits[1],
                    "alignment_quality": splits[2],
                    "translation": {"en": splits[3], "hi": splits[4]},
                }
