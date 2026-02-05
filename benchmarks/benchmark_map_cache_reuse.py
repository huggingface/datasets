import json
import os
import tempfile

from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import PreTrainedTokenizerFast

import datasets
from utils import get_duration


RESULTS_BASEPATH, RESULTS_FILENAME = os.path.split(__file__)
RESULTS_FILE_PATH = os.path.join(RESULTS_BASEPATH, "results", RESULTS_FILENAME.replace(".py", ".json"))


def _make_tokenizer() -> PreTrainedTokenizerFast:
    vocab = {"[UNK]": 0, "[PAD]": 1, "hello": 2, "world": 3}
    backend = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))
    backend.pre_tokenizer = Whitespace()
    return PreTrainedTokenizerFast(tokenizer_object=backend, unk_token="[UNK]", pad_token="[PAD]")


@get_duration
def map_once(dataset: datasets.Dataset, tok: PreTrainedTokenizerFast):
    def tokenize(examples):
        return tok(examples["text"], truncation=True, padding="max_length", max_length=8)

    _ = dataset.map(tokenize, batched=True, load_from_cache_file=True, remove_columns=["text"])


def benchmark_map_cache_reuse():
    times = {}
    tok = _make_tokenizer()

    with tempfile.TemporaryDirectory() as tmp_dir:
        raw = datasets.Dataset.from_dict({"text": ["hello world"] * 200_000})
        stored = os.path.join(tmp_dir, "stored")
        raw.save_to_disk(stored)
        dataset = datasets.Dataset.load_from_disk(stored)

        # First run: cache miss (writes cache file)
        times["map tokenize (cache miss)"] = map_once(dataset, tok)
        # Second run: cache hit (should be much faster if fingerprint is stable)
        times["map tokenize (cache hit)"] = map_once(dataset, tok)

    with open(RESULTS_FILE_PATH, "wb") as f:
        f.write(json.dumps(times).encode("utf-8"))


if __name__ == "__main__":
    benchmark_map_cache_reuse()
