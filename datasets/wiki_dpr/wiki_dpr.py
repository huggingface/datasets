import numpy as np

import nlp


_CITATION = """"""

_DESCRIPTION = """"""

_LICENSE = """"""

_DATA_URL = "https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz"

_VECTORS_URL = "https://dl.fbaipublicfiles.com/dpr/data/wiki_encoded/single/nq/wiki_passages_{i}"


class WikiDprConfig(nlp.BuilderConfig):
    """BuilderConfig for WikiDprConfig."""

    def __init__(self, with_embeddings=True, **kwargs):
        """BuilderConfig for WikiSnippets.
    Args:
        with_embeddings (`bool`, defaults to `True`): Load the 768-dimensional embeddings from DPR trained on NQ.
      **kwargs: keyword arguments forwarded to super.
    """
        super(WikiDprConfig, self).__init__(**kwargs)
        self.with_embeddings = with_embeddings


class WikiDpr(nlp.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = WikiDprConfig
    BUILDER_CONFIGS = [WikiDprConfig(name="psgs_w100_with_nq_embeddings", with_embeddings=True)]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "text": nlp.Value("string"),
                    "title": nlp.Value("string"),
                    "embeddings": nlp.Sequence(nlp.Value("float32")),
                }
            )
            if self.config.with_embeddings
            else nlp.Features({"id": nlp.Value("string"), "text": nlp.Value("string"), "title": nlp.Value("string"),}),
            supervised_keys=None,
            homepage="https://dumps.wikimedia.org",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        files_to_download = {"data_file": _DATA_URL}
        downloaded_files = dl_manager.download_and_extract(files_to_download)
        if self.config.with_embeddings:
            downloaded_files["vectors_files"] = dl_manager.download([_VECTORS_URL.format(i=i) for i in range(50)])
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs=downloaded_files),
        ]

    def _generate_examples(self, data_file, vectors_files=None):
        vec_idx = 0
        vecs = []
        lines = open(data_file, "r")
        next(lines)  # skip headers
        for i, line in enumerate(lines):
            id, text, title = line.strip().split("\t")
            text = text[1:-1]  # remove " symbol at the beginning and the end
            text = text.replace('""', '"')
            if self.config.with_embeddings:
                if vec_idx >= len(vecs):
                    assert len(vectors_files) > 0, "Couldn't find vector for index {}".format(i)
                    vecs = np.load(open(vectors_files.pop(0), "rb"), allow_pickle=True)
                    vec_idx = 0
                vec_id, vec = vecs[vec_idx]
                assert int(id) == int(vec_id), "ID mismatch between lines {} and vector {}".format(id, vec_id)
                yield id, {"id": id, "text": text, "title": title, "embeddings": vec}
                vec_idx += 1
            else:
                yield id, {
                    "id": id,
                    "text": text,
                    "title": title,
                }
