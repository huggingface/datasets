import datasets

_DESCRIPTION = """\
    Webbnyheter 2012 from Spraakbanken, semi-manually annotated and adapted for CoreNLP Swedish NER. Semi-manually defined in this case as: Bootstrapped from Swedish Gazetters then manually correcte/reviewed by two independent native speaking swedish annotators. No annotator agreement calculated.
"""
_HOMEPAGE_URL = "https://github.com/klintan/swedish-ner-corpus"
_TRAIN_URL = "https://raw.githubusercontent.com/klintan/swedish-ner-corpus/master/train_corpus.txt"
_TEST_URL = "https://raw.githubusercontent.com/klintan/swedish-ner-corpus/master/test_corpus.txt"


class SwedishNERCorpusDataset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "words": datasets.Sequence(datasets.Value("string")),
                    "labels": datasets.Sequence(datasets.Value("string")),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=None,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_URL)
        test_path = dl_manager.download_and_extract(_TEST_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"datapath": train_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"datapath": test_path},
            ),
        ]

    def _generate_examples(self, datapath):
        sentence_counter = 0
        with open(datapath, encoding="utf-8") as f:
            current_words = []
            current_labels = []
            for row in f:
                row = row.rstrip()
                row_split = row.split("\t")
                if len(row_split) > 1:
                    token, label = row_split
                    current_words.append(token)
                    current_labels.append(label)
                else:
                    if not current_words:
                        continue
                    assert len(current_words) == len(current_labels)
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "words": current_words,
                            "labels": current_labels,
                        },
                    )
                    sentence_counter += 1
                    current_words = []
                    current_labels = []
                    yield sentence
            if current_words:
                yield sentence_counter, {
                    "id": str(sentence_counter),
                    "words": current_words,
                    "labels": current_labels,
                }
