import pickle

import pytest

from datasets import Dataset, load_from_disk
from datasets.fingerprint import Hasher
from datasets.utils._dill import dumps


torch = pytest.importorskip("torch")


@pytest.mark.parametrize("dtype", [torch.complex64, torch.complex128])
@pytest.mark.parametrize("view_kind", ["conjugate", "negative"])
@pytest.mark.parametrize("strided", [False, True])
def test_lazy_tensor_views_hash_their_logical_values_without_changing_inputs(dtype, view_kind, strided):
    real_dtype = torch.float32 if dtype == torch.complex64 else torch.float64
    values = torch.arange(16, dtype=real_dtype).reshape(4, 4)
    base = torch.complex(values, values + 1).requires_grad_()
    view = base.conj() if view_kind == "conjugate" else base.conj().imag
    if strided:
        view = view[::2, 1::2]
    flags = (view.is_conj(), view.is_neg(), view.requires_grad, view.stride(), view.data_ptr())
    original = base.detach().clone()
    materialized = view.detach().clone()

    assert Hasher.hash(view) == Hasher.hash(materialized)
    assert Hasher.hash(view) != Hasher.hash(materialized + 1)
    restored = pickle.loads(dumps([view, view]))

    assert restored[0] is restored[1]
    torch.testing.assert_close(restored[0], materialized, rtol=0, atol=0)
    assert (view.is_conj(), view.is_neg(), view.requires_grad, view.stride(), view.data_ptr()) == flags
    torch.testing.assert_close(base, original, rtol=0, atol=0)
    assert base.grad is None


@pytest.mark.parametrize("dtype", [torch.int64, torch.float32, torch.bfloat16, torch.complex128])
def test_ordinary_tensor_hashing_and_dtype_round_trip_are_preserved(dtype):
    tensor = torch.tensor([1, 2, 3], dtype=dtype)

    assert Hasher.hash(tensor) == Hasher.hash(tensor.clone())
    assert Hasher.hash(tensor) != Hasher.hash(tensor + 1)
    restored = pickle.loads(dumps(tensor))

    assert restored.dtype == dtype
    torch.testing.assert_close(restored, tensor, rtol=0, atol=0)


@pytest.mark.parametrize("view_kind", ["conjugate", "negative"])
def test_map_reuses_cache_for_tensor_views_and_invalidates_changed_values(tmp_path, view_kind):
    source = Dataset.from_dict({"x": [[1, 0], [0, 1], [2, 1]]})
    source.save_to_disk(tmp_path / "source")
    dataset = load_from_disk(tmp_path / "source")
    base = torch.tensor([1 + 2j, 3 + 4j])
    coefficients = base.conj() if view_kind == "conjugate" else base.conj().imag
    calls_file = tmp_path / "calls.txt"

    def transform(example):
        with calls_file.open("a", encoding="utf-8") as handle:
            handle.write("called\n")
        result = (coefficients * torch.tensor(example["x"], dtype=coefficients.dtype)).sum()
        return {"value": float(result.imag if coefficients.is_complex() else result)}

    first = dataset.map(transform)
    second = dataset.map(transform)

    assert first["value"][:] == [-2.0, -4.0, -8.0]
    assert second["value"][:] == first["value"][:]
    assert first.cache_files and first.cache_files == second.cache_files
    assert first._fingerprint == second._fingerprint
    assert calls_file.read_text().splitlines() == ["called"] * 3

    base.add_(1j)
    changed = dataset.map(transform)

    assert changed["value"][:] == [-3.0, -5.0, -11.0]
    assert changed._fingerprint != first._fingerprint
    assert changed.cache_files != first.cache_files
    assert calls_file.read_text().splitlines() == ["called"] * 6
