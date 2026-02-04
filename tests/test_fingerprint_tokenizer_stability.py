import pytest
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.pre_tokenizers import Whitespace
from transformers import PreTrainedTokenizerFast

from datasets import Dataset
from datasets.fingerprint import Hasher


def _make_mutable_backend_tokenizer() -> PreTrainedTokenizerFast:
    # Build a tiny tokenizer entirely locally (no network), backed by `tokenizers.Tokenizer`.
    vocab = {"[UNK]": 0, "[PAD]": 1, "hello": 2, "world": 3}
    backend = Tokenizer(WordLevel(vocab=vocab, unk_token="[UNK]"))
    backend.pre_tokenizer = Whitespace()
    return PreTrainedTokenizerFast(tokenizer_object=backend, unk_token="[UNK]", pad_token="[PAD]")


def test_hasher_hash_tokenizer_stable_after_call():
    tok = _make_mutable_backend_tokenizer()
    h0 = Hasher.hash(tok)
    _ = tok(["hello world"], truncation=True, padding="max_length", max_length=8)
    h1 = Hasher.hash(tok)
    assert h0 == h1


def test_map_cache_reused_with_tokenizer_after_call(tmp_path):
    # Regression test for https://github.com/huggingface/datasets/issues/3847
    #
    # Tokenizers can mutate backend truncation/padding state when called, which used to make the
    # dataset transform fingerprint unstable and prevented cache reuse.
    tok = _make_mutable_backend_tokenizer()

    raw = Dataset.from_dict({"text": ["hello world"] * 1000})
    stored = tmp_path / "stored"
    raw.save_to_disk(stored)
    raw = Dataset.load_from_disk(stored)

    def tokenize(examples):
        return tok(examples["text"], truncation=True, padding="max_length", max_length=8)

    res1 = raw.map(tokenize, batched=True, load_from_cache_file=True, remove_columns=["text"])
    res2 = raw.map(tokenize, batched=True, load_from_cache_file=True, remove_columns=["text"])

    assert res1.cache_files and res2.cache_files
    assert res1.cache_files[0]["filename"] == res2.cache_files[0]["filename"]
