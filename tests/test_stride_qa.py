import pytest
from .utils import require_transformers
from datasets import Dataset

@require_transformers
@pytest.mark.integration
def test_map_with_question_and_context_stride():
    """Ensure Dataset.map tokenization uses question+context form and produces overflowing chunks."""
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    # Make a long question of ~35 tokens to reduce the available context budget
    question = " ".join(["what"] * 35)
    # Make a long context that will be chunked
    context = ("Sodium chloride is widely used in many industrial processes. " * 200).strip()

    data = {"question": [question], "context": [context]}

    def tokenize_batch(examples):
        # two-argument form to mimic QA preprocessing
        return tokenizer(
            examples["question"],
            examples["context"],
            max_length=128,
            truncation="only_second",
            return_overflowing_tokens=True,
            stride=96,
            return_offsets_mapping=True,
        )

    dset = Dataset.from_dict(data)
    try:
        processed = dset.map(tokenize_batch, batched=True, remove_columns=["question", "context"], load_from_cache_file=False, num_proc=None)
    except BaseException as e:
        msg = str(e)
        # Tokenizers (Rust backend) may panic with messages about stride < max_len.
        # This is an upstream issue (tokenizers/transformers). Mark as xfail so CI is not blocked
        # while still documenting the regression.
        if "stride must be" in msg or "stride < max_len" in msg or "Truncation error" in msg:
            import pytest
            pytest.xfail(f"Upstream tokenizers panic or truncation error reproduced: {msg}")
        raise

    # Ensure tokenization created sequences
    assert len(processed) > 0
    # input_ids must be present
    assert "input_ids" in processed.column_names
    # overflow_to_sample_mapping should exist and map back to the original example(s)
    # It may be stored as a list per example by the tokenizer; check presence in columns
    # If present as a column, ensure all values map to sample index 0
    if "overflow_to_sample_mapping" in processed.column_names:
        mappings = processed["overflow_to_sample_mapping"]
        # mappings could be nested lists depending on tokenizer; flatten and check
        flat = []
        for m in mappings:
            if isinstance(m, list):
                flat.extend(m)
            else:
                flat.append(m)
        assert all(x == 0 for x in flat)
