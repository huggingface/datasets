import pytest

from datasets.utils.sharding import _distribute_shards, _number_of_shards_in_gen_kwargs, _split_gen_kwargs


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"num_shards": 0, "max_num_jobs": 1}, []),
        ({"num_shards": 10, "max_num_jobs": 1}, [range(10)]),
        ({"num_shards": 10, "max_num_jobs": 10}, [range(i, i + 1) for i in range(10)]),
        ({"num_shards": 1, "max_num_jobs": 10}, [range(1)]),
        ({"num_shards": 10, "max_num_jobs": 3}, [range(0, 4), range(4, 7), range(7, 10)]),
        ({"num_shards": 3, "max_num_jobs": 10}, [range(0, 1), range(1, 2), range(2, 3)]),
    ],
)
def test_distribute_shards(kwargs, expected):
    out = _distribute_shards(**kwargs)
    assert out == expected


@pytest.mark.parametrize(
    "gen_kwargs, max_num_jobs, expected",
    [
        ({"foo": 0}, 10, [{"foo": 0}]),
        ({"shards": [0, 1, 2, 3]}, 1, [{"shards": [0, 1, 2, 3]}]),
        ({"shards": [0, 1, 2, 3]}, 4, [{"shards": [0]}, {"shards": [1]}, {"shards": [2]}, {"shards": [3]}]),
        ({"shards": [0, 1]}, 4, [{"shards": [0]}, {"shards": [1]}]),
        ({"shards": [0, 1, 2, 3]}, 2, [{"shards": [0, 1]}, {"shards": [2, 3]}]),
    ],
)
def test_split_gen_kwargs(gen_kwargs, max_num_jobs, expected):
    out = _split_gen_kwargs(gen_kwargs, max_num_jobs)
    assert out == expected


@pytest.mark.parametrize(
    "gen_kwargs, expected",
    [
        ({"foo": 0}, 1),
        ({"shards": [0]}, 1),
        ({"shards": [0, 1, 2, 3]}, 4),
        ({"shards": [0, 1, 2, 3], "foo": 0}, 4),
        ({"shards": [0, 1, 2, 3], "other": (0, 1)}, 4),
        ({"shards": [0, 1, 2, 3], "shards2": [0, 1]}, RuntimeError),
    ],
)
def test_number_of_shards_in_gen_kwargs(gen_kwargs, expected):
    if expected is RuntimeError:
        with pytest.raises(expected):
            _number_of_shards_in_gen_kwargs(gen_kwargs)
    else:
        out = _number_of_shards_in_gen_kwargs(gen_kwargs)
        assert out == expected
