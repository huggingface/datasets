# Lint as: python3
""" HuggingFace/Datasets is an open library of datasets.

Note:

   VERSION needs to be formatted following the MAJOR.MINOR.PATCH convention
   (we need to follow this convention to be able to retrieve versioned scripts)

Simple check list for release from AllenNLP repo: https://github.com/allenai/allennlp/blob/master/setup.py

To create the package for pypi.

0. Prerequisites:
   - Dependencies:
     - twine: "pip install twine"
   - Create an account in (and join the 'datasets' project):
     - PyPI: https://pypi.org/
     - Test PyPI: https://test.pypi.org/
   - Don't break `transformers`
     - Run the `transformers` CI using the `main` branch and make sure it's green.
       In `transformers`, use "datasets @ git+https://github.com/huggingface/datasets@main#egg=datasets"
       in both setup.py and src/transformers/dependency_versions_table.py and then run the CI

1. Change the version in:
   - __init__.py
   - setup.py

2. Commit these changes: "git commit -m 'Release: VERSION'"

3. Add a tag in git to mark the release: "git tag VERSION -m 'Add tag VERSION for pypi'"
   Push the tag to remote: git push --tags origin main

4. Build both the sources and the wheel. Do not change anything in setup.py between
   creating the wheel and the source distribution (obviously).

   First, delete any "build" directory that may exist from previous builds.

   For the wheel, run: "python setup.py bdist_wheel" in the top level directory.
   (this will build a wheel for the python version you use to build it).

   For the sources, run: "python setup.py sdist"
   You should now have a /dist directory with both .whl and .tar.gz source versions.

5. Check that everything looks correct by uploading the package to the pypi test server:

   twine upload dist/* -r pypitest --repository-url=https://test.pypi.org/legacy/

   Check that you can install it in a virtualenv/notebook by running:
   pip install huggingface_hub fsspec aiohttp
   pip install -U tqdm
   pip install -i https://testpypi.python.org/pypi datasets

6. Upload the final version to actual pypi:
   twine upload dist/* -r pypi

7. Fill release notes in the tag in github once everything is looking hunky-dory.

8. Change the version in __init__.py and setup.py to X.X.X+1.dev0 (e.g. VERSION=1.18.3 -> 1.18.4.dev0).
   Then push the change with a message 'set dev version'
"""


from setuptools import find_packages, setup


REQUIRED_PKGS = [
    # We use numpy>=1.17 to have np.random.Generator (Dataset shuffling)
    "numpy>=1.17",
    # Backend and serialization.
    # Minimum 6.0.0 to support wrap_array which is needed for ArrayND features
    "pyarrow>=6.0.0",
    # For smart caching dataset processing
    "dill<0.3.6",  # tmp pin until 0.3.6 release: see https://github.com/huggingface/datasets/pull/4397
    # For performance gains with apache arrow
    "pandas",
    # for downloading datasets over HTTPS
    "requests>=2.19.0",
    # progress bars in download and scripts
    "tqdm>=4.62.1",
    # for fast hashing
    "xxhash",
    # for better multiprocessing
    "multiprocess",
    # to get metadata of optional dependencies such as torch or tensorflow for Python versions that don't have it
    "importlib_metadata;python_version<'3.8'",
    # to save datasets locally or on any filesystem
    # minimum 2021.11.1 so that BlockSizeError is fixed: see https://github.com/fsspec/filesystem_spec/pull/830
    "fsspec[http]>=2021.11.1",  # aligned s3fs with this
    # for data streaming via http
    "aiohttp",
    # To get datasets from the Datasets Hub on huggingface.co
    # minimum 0.2.0 for set_access_token
    "huggingface-hub>=0.2.0,<1.0.0",
    # Utilities from PyPA to e.g., compare versions
    "packaging",
    "responses<0.19",
    # To parse YAML metadata from dataset cards
    "pyyaml>=5.1",
]

AUDIO_REQUIRE = [
    "librosa",
]

VISION_REQURE = [
    "Pillow>=6.2.1",
]

BENCHMARKS_REQUIRE = [
    "numpy==1.18.5",
    "tensorflow==2.3.0",
    "torch==1.7.1",
    "transformers==3.0.2",
]

TESTS_REQUIRE = [
    # test dependencies
    "absl-py",
    "pytest",
    "pytest-datadir",
    "pytest-xdist",
    # optional dependencies
    "apache-beam>=2.26.0",
    "elasticsearch<8.0.0",  # 8.0 asks users to provide hosts or cloud_id when instantiating ElastictSearch()
    "aiobotocore>=2.0.1",  # required by s3fs>=2021.11.1
    "boto3>=1.19.8",  # to be compatible with aiobotocore>=2.0.1 - both have strong dependencies on botocore
    "botocore>=1.22.8",  # to be compatible with aiobotocore and boto3
    "faiss-cpu>=1.6.4",
    "fsspec[s3]",
    "lz4",
    "moto[s3,server]==2.0.4",
    "py7zr",
    "rarfile>=4.0",
    "s3fs>=2021.11.1",  # aligned with fsspec[http]>=2021.11.1
    "tensorflow>=2.3,!=2.6.0,!=2.6.1",
    "torch",
    "torchaudio<0.12.0",
    "soundfile",
    "transformers",
    "zstandard",
    # metrics dependencies
    "bert_score>=0.3.6",
    "jiwer",
    "langdetect",
    "mauve-text",
    "nltk",
    "rouge_score",
    "sacrebleu",
    "sacremoses",
    "scikit-learn",
    "scipy",
    "sentencepiece",  # for bleurt
    "seqeval",
    "sqlalchemy",
    "tldextract",
    # to speed up pip backtracking
    "toml>=0.10.1",
    "requests_file>=1.5.1",
    "tldextract>=3.1.0",
    "texttable>=1.6.3",
    "Werkzeug>=1.0.1",
    "six~=1.15.0",
]

TESTS_REQUIRE.extend(VISION_REQURE)
TESTS_REQUIRE.extend(AUDIO_REQUIRE)

QUALITY_REQUIRE = ["black~=22.0", "flake8>=3.8.3", "isort>=5.0.0", "pyyaml>=5.3.1"]


EXTRAS_REQUIRE = {
    "audio": AUDIO_REQUIRE,
    "vision": VISION_REQURE,
    "apache-beam": ["apache-beam>=2.26.0"],
    "tensorflow": ["tensorflow>=2.2.0,!=2.6.0,!=2.6.1"],
    "tensorflow_gpu": ["tensorflow-gpu>=2.2.0,!=2.6.0,!=2.6.1"],
    "torch": ["torch"],
    "s3": [
        "fsspec",
        "boto3",
        "botocore",
        "s3fs",
    ],
    "streaming": [],  # for backward compatibility
    "dev": TESTS_REQUIRE + QUALITY_REQUIRE,
    "tests": TESTS_REQUIRE,
    "quality": QUALITY_REQUIRE,
    "benchmarks": BENCHMARKS_REQUIRE,
    "docs": [
        # Might need to add doc-builder and some specific deps in the future
        "s3fs",
    ],
}

setup(
    name="datasets",
    version="2.6.2",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
    description="HuggingFace community-driven open-source library of datasets",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="HuggingFace Inc.",
    author_email="thomas@huggingface.co",
    url="https://github.com/huggingface/datasets",
    download_url="https://github.com/huggingface/datasets/tags",
    license="Apache 2.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    package_data={"datasets": ["py.typed", "scripts/templates/*"], "datasets.utils.resources": ["*.json", "*.yaml", "*.tsv"]},
    entry_points={"console_scripts": ["datasets-cli=datasets.commands.datasets_cli:main"]},
    python_requires=">=3.7.0",
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="datasets machine learning datasets metrics",
    zip_safe=False,  # Required for mypy to find the py.typed file
)
