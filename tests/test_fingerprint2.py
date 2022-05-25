from datasets.fingerprint import Hasher


def test_dill():
    # AttributeError: module 'dill._dill' has no attribute 'stack'
    hasher = Hasher()
    hasher.update(lambda x: x)
