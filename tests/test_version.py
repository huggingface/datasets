import pytest

from datasets.utils.version import Version


@pytest.mark.parametrize(
    "other, expected_equality",
    [
        (Version("1.0.0"), True),
        ("1.0.0", True),
        (Version("2.0.0"), False),
        ("2.0.0", False),
        ("1", False),
        ("a", False),
        (1, False),
        (None, False),
    ],
)
def test_version_equality_and_hash(other, expected_equality):
    version = Version("1.0.0")
    assert (version == other) is expected_equality
    assert (version != other) is not expected_equality
    assert (hash(version) == hash(other)) is expected_equality
