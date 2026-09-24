from datasets.utils.track import tracked_str


def test_tracked_str_repr_without_origin():
    path = tracked_str("/tmp/datasets-track-repr-plain.tar")
    assert repr(path) == repr("/tmp/datasets-track-repr-plain.tar")


def test_tracked_str_str_is_local_path():
    local = "/tmp/datasets-track-repr-str.tar"
    origin = "hf://datasets/org/name@main/data/file.tar"
    path = tracked_str(local)
    path.set_origin(origin)
    assert str(path) == local
    assert origin not in str(path)


def test_tracked_str_repr_includes_hf_origin():
    path = tracked_str("/tmp/datasets-track-repr-hf.tar")
    origin = "hf://datasets/org/name@main/data/file.tar"
    path.set_origin(origin)
    assert repr(path) == f"{'/tmp/datasets-track-repr-hf.tar'!r} (origin={origin})"


def test_tracked_str_repr_strips_userinfo_and_query():
    path = tracked_str("/tmp/datasets-track-repr-secret.tar")
    origin = "https://user:pass@example.com/bucket/file.tar?X-Amz-Signature=abc&Expires=1"
    path.set_origin(origin)
    message = repr(path)
    assert message == f"{'/tmp/datasets-track-repr-secret.tar'!r} (origin=https://example.com/bucket/file.tar)"
    assert "user:pass" not in message
    assert "X-Amz-Signature" not in message


def test_tracked_str_repr_omits_origin_when_same_as_path():
    local = "/tmp/datasets-track-repr-same.tar"
    path = tracked_str(local)
    path.set_origin(local)
    assert repr(path) == repr(local)
    assert "origin=" not in repr(path)


def test_tracked_str_get_origin_keeps_raw_url():
    path = tracked_str("/tmp/datasets-track-repr-raw.tar")
    origin = "https://user:pass@example.com/file.tar?token=secret"
    path.set_origin(origin)
    assert path.get_origin() == origin
