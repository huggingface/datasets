import asyncio
from functools import partial

import pytest

from datasets import Dataset, IterableDataset


class AsyncCallable:
    def __init__(self, function):
        self.function = function

    async def __call__(self, *args, **kwargs):
        return await self.function(*args, **kwargs)


@pytest.mark.parametrize("dataset_type", ["map", "iterable_python", "iterable_arrow"])
@pytest.mark.parametrize("batched", [False, True])
@pytest.mark.parametrize("operation", ["map", "filter"])
@pytest.mark.parametrize("callback_type", ["function", "callable", "partial"])
def test_async_callbacks(dataset_type, batched, operation, callback_type):
    rows = [{"x": i} for i in range(5)]
    dataset = Dataset.from_list(rows)
    if dataset_type == "iterable_python":
        dataset = IterableDataset.from_generator(lambda: iter(rows))
    elif dataset_type == "iterable_arrow":
        dataset = dataset.to_iterable_dataset()

    async def callback(example):
        await asyncio.sleep(0)
        if operation == "map":
            return {"y": [x + 1 for x in example["x"]]} if batched else {"y": example["x"] + 1}
        return [x % 2 == 0 for x in example["x"]] if batched else example["x"] % 2 == 0

    function = callback
    if callback_type != "function":
        function = AsyncCallable(function)
    if callback_type == "partial":
        function = partial(function)

    kwargs = {"batch_size": 2} if batched else {}
    actual = list(getattr(dataset, operation)(function, batched=batched, **kwargs))
    expected = (
        [{"x": row["x"], "y": row["x"] + 1} for row in rows]
        if operation == "map"
        else [row for row in rows if row["x"] % 2 == 0]
    )
    assert actual == expected


@pytest.mark.parametrize("iterable", [False, True])
@pytest.mark.parametrize("operation", ["map", "filter"])
def test_async_callable_error(iterable, operation):
    dataset = Dataset.from_dict({"x": [0, 1, 2]})
    if iterable:
        dataset = dataset.to_iterable_dataset()

    async def callback(example):
        await asyncio.sleep(0)
        raise RuntimeError("callback failed")

    with pytest.raises(RuntimeError, match="callback failed"):
        list(getattr(dataset, operation)(AsyncCallable(callback)))


@pytest.mark.parametrize("iterable", [False, True])
@pytest.mark.parametrize("batched", [False, True])
def test_async_callable_class_constructor_stays_synchronous(iterable, batched):
    class AsyncDict(dict):
        async def __call__(self, example):
            return example

    dataset = Dataset.from_dict({"x": [0, 1, 2]})
    if iterable:
        dataset = dataset.to_iterable_dataset()
    assert list(dataset.map(AsyncDict, batched=batched)) == [{"x": 0}, {"x": 1}, {"x": 2}]
