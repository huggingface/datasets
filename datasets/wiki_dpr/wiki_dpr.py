import logging
import os

import numpy as np

import datasets


_CITATION = """
@misc{karpukhin2020dense,
    title={Dense Passage Retrieval for Open-Domain Question Answering},
    author={Vladimir Karpukhin and Barlas Oğuz and Sewon Min and Patrick Lewis and Ledell Wu and Sergey Edunov and Danqi Chen and Wen-tau Yih},
    year={2020},
    eprint={2004.04906},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
This is the wikipedia split used to evaluate the Dense Passage Retrieval (DPR) model.
It contains 21M passages from wikipedia along with their DPR embeddings.
The wikipedia articles were split into multiple, disjoint text blocks of 100 words as passages.
"""

_LICENSE = """DPR is CC-BY-NC 4.0 licensed."""

_DATA_URL = "https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz"

_NQ_VECTORS_URL = "https://dl.fbaipublicfiles.com/dpr/data/wiki_encoded/single/nq/wiki_passages_{i}"

_MULTISET_VECTORS_URL = "https://dl.fbaipublicfiles.com/rag/rag_multiset_embeddings/wiki_passages_{i}"

_INDEX_URL = "https://storage.googleapis.com/huggingface-nlp/datasets/wiki_dpr"


class WikiDprConfig(datasets.BuilderConfig):
    """BuilderConfig for WikiDprConfig."""

    def __init__(
        self,
        with_embeddings=True,
        with_index=True,
        wiki_split="psgs_w100",
        embeddings_name="nq",
        index_name="compressed",
        index_train_size=262144,
        dummy=False,
        **kwargs,
    ):
        """BuilderConfig for WikiSnippets.
        Args:
            with_embeddings (`bool`, defaults to `True`): Load the 768-dimensional embeddings from DPR.
            with_index (`bool`, defaults to `True`): Load the faiss index trained on the embeddings.
            wiki_split (`str`, defaults to `psgs_w100`): name of the splitting method of wiki articles.
            embeddings_name (`str`, defaults to `nq`): "nq" or "multiset", depending on which dataset DPR was trained on.
            index_name (`str`, defaults to `compressed`): "compressed" or "exact", the configuration of the faiss index to use.
            index_train_size (`int`, defaults to `262144`): Size of the subset to use to train the index, if it is trainable.
            dummy (`bool`, defaults to `False`): Dummy uses only 10 000 examples for testing purposes.
          **kwargs: keyword arguments forwarded to super.
        """
        self.with_embeddings = with_embeddings
        self.with_index = with_index
        self.wiki_split = wiki_split
        self.embeddings_name = embeddings_name
        self.index_name = index_name if with_index else "no_index"
        self.index_train_size = index_train_size
        self.dummy = dummy
        name = [self.wiki_split, self.embeddings_name, self.index_name]
        if self.dummy:
            name = ["dummy"] + name
            assert (
                self.index_name != "compressed" or not self.with_index
            ), "Please use `index_name='exact' for dummy wiki_dpr`"
        assert wiki_split == "psgs_w100"
        assert embeddings_name in ("nq", "multiset")
        assert index_name in ("compressed", "exact", "no_index")
        kwargs["name"] = ".".join(name)
        super(WikiDprConfig, self).__init__(**kwargs)

        prefix = f"{wiki_split}.{embeddings_name}."
        if self.index_name == "exact":
            self.index_file = prefix + "HNSW128_SQ8-IP-{split}.faiss"
        else:
            self.index_file = prefix + "IVF4096_HNSW128_PQ128-IP-{split}.faiss"
        if self.dummy:
            self.index_file = "dummy." + self.index_file


class WikiDpr(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = WikiDprConfig
    BUILDER_CONFIGS = [
        WikiDprConfig(
            embeddings_name=embeddings_name,
            with_index=(index_name != "no_index"),
            index_name=index_name,
            version=datasets.Version("0.0.0"),
        )
        for embeddings_name in ("nq", "multiset")
        for index_name in ("exact", "compressed", "no_index")
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "embeddings": datasets.Sequence(datasets.Value("float32")),
                }
            )
            if self.config.with_embeddings
            else datasets.Features(
                {"id": datasets.Value("string"), "text": datasets.Value("string"), "title": datasets.Value("string")}
            ),
            supervised_keys=None,
            homepage="https://github.com/facebookresearch/DPR",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        files_to_download = {"data_file": _DATA_URL}
        downloaded_files = dl_manager.download_and_extract(files_to_download)
        if self.config.with_embeddings:
            vectors_url = _NQ_VECTORS_URL if self.config.embeddings_name == "nq" else _MULTISET_VECTORS_URL
            if self.config.dummy:
                downloaded_files["vectors_files"] = dl_manager.download([vectors_url.format(i=0)])
            else:
                downloaded_files["vectors_files"] = dl_manager.download([vectors_url.format(i=i) for i in range(50)])
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs=downloaded_files),
        ]

    def _generate_examples(self, data_file, vectors_files=None):
        vec_idx = 0
        vecs = []
        lines = open(data_file, "r", encoding="utf-8")
        next(lines)  # skip headers
        for i, line in enumerate(lines):
            if self.config.dummy and i == 10000:
                break
            if i == 21015300:
                break  # ignore the last 24 examples for which the embeddings are missing.
            id, text, title = line.strip().split("\t")
            text = text[1:-1]  # remove " symbol at the beginning and the end
            text = text.replace('""', '"')  # replace double quotes by simple quotes
            if self.config.with_embeddings:
                if vec_idx >= len(vecs):
                    if len(vectors_files) == 0:
                        logging.warning("Ran out of vector files at index {}".format(i))
                        break
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

    def _post_processing_resources(self, split):
        if self.config.with_index:
            return {"embeddings_index": self.config.index_file.format(split=split)}
        else:
            return {}

    def _download_post_processing_resources(self, split, resource_name, dl_manager):
        if resource_name == "embeddings_index":
            try:
                downloaded_resources = dl_manager.download_and_extract(
                    {"embeddings_index": _INDEX_URL + "/" + self.config.index_file.format(split=split)}
                )
                return downloaded_resources["embeddings_index"]
            except (FileNotFoundError, ConnectionError):  # index doesn't exist
                pass

    def _post_process(self, dataset, resources_paths):
        if self.config.with_index:
            index_file = resources_paths["embeddings_index"]
            if os.path.exists(index_file):
                dataset.load_faiss_index("embeddings", index_file)
            else:
                if "embeddings" not in dataset.column_names:
                    raise ValueError("Couldn't build the index because there are no embeddings.")
                import faiss

                d = 768
                train_size = self.config.index_train_size
                logging.info("Building wiki_dpr faiss index")
                if self.config.index_name == "exact":
                    index = faiss.IndexHNSWFlat(d, 128, faiss.METRIC_INNER_PRODUCT)
                    index.hnsw.efConstruction = 200
                    index.hnsw.efSearch = 128
                    dataset.add_faiss_index("embeddings", custom_index=index)
                else:
                    quantizer = faiss.IndexHNSWFlat(d, 128, faiss.METRIC_INNER_PRODUCT)
                    quantizer.hnsw.efConstruction = 200
                    quantizer.hnsw.efSearch = 128
                    ivf_index = faiss.IndexIVFPQ(quantizer, d, 4096, 128, 8, faiss.METRIC_INNER_PRODUCT)
                    ivf_index.nprobe = 64
                    ivf_index.own_fields = True
                    quantizer.this.disown()
                    dataset.add_faiss_index(
                        "embeddings",
                        train_size=train_size,
                        custom_index=ivf_index,
                    )
                logging.info("Saving wiki_dpr faiss index")
                dataset.save_faiss_index("embeddings", index_file)
        return dataset
