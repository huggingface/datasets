# Lint as: python3
""" HuggingFace/Datasets is an open library of datasets.

Note:

   VERSION needs to be formatted following the MAJOR.MINOR.PATCH convention
   (we need to follow this convention to be able to retrieve versioned scripts)

Simple check list for release from AllenNLP repo: https://github.com/allenai/allennlp/blob/master/setup.py

Steps to make a release:

0. Prerequisites:
   - Dependencies:
     - twine: `pip install twine`
   - Create an account in (and join the 'datasets' project):
     - PyPI: https://pypi.org/
     - Test PyPI: https://test.pypi.org/
   - Don't break `transformers`: run the `transformers` CI using the `main` branch and make sure it's green.
     - In `transformers`, use `datasets @ git+https://github.com/huggingface/datasets@main#egg=datasets`
       in both:
       - setup.py and
       - src/transformers/dependency_versions_table.py
     - and then run the CI

1. Create the release branch from main branch:
     ```
     git checkout main
     git pull upstream main
     git checkout -b release-VERSION
     ```

2. Change the version to the release VERSION in:
   - __init__.py
   - setup.py

3. Commit these changes, push and create a Pull Request:
     ```
     git add -u
     git commit -m "Release: VERSION"
     git push upstream release-VERSION
     ```
   - Go to: https://github.com/huggingface/datasets/pull/new/release
   - Create pull request

4. From your local release branch, build both the sources and the wheel. Do not change anything in setup.py between
   creating the wheel and the source distribution (obviously).
   - First, delete any building directories that may exist from previous builds:
     - build
     - dist
   - From the top level directory, build the wheel and the sources:
       ```
       python setup.py bdist_wheel
       python setup.py sdist
       ```
   - You should now have a /dist directory with both .whl and .tar.gz source versions.

5. Check that everything looks correct by uploading the package to the test PyPI server:
     ```
     twine upload dist/* -r pypitest --repository-url=https://test.pypi.org/legacy/
     ```
   Check that you can install it in a virtualenv/notebook by running:
     ```
     pip install huggingface_hub fsspec aiohttp
     pip install -U tqdm
     pip install -i https://testpypi.python.org/pypi datasets
     ```

6. Upload the final version to the actual PyPI:
     ```
     twine upload dist/* -r pypi
     ```

7. Make the release on GitHub once everything is looking hunky-dory:
   - Merge the release Pull Request
   - Create a new release: https://github.com/huggingface/datasets/releases/new
   - Choose a tag: Introduce the new VERSION as tag, that will be created when you publish the release
     - Create new tag VERSION on publish
   - Release title: Introduce the new VERSION as well
   - Describe the release
     - Use "Generate release notes" button for automatic generation
   - Publish release

8. Set the dev version
   - Create the dev-version branch from the main branch:
       ```
       git checkout main
       git pull upstream main
       git branch -D dev-version
       git checkout -b dev-version
       ```
   - Change the version to X.X.X+1.dev0 (e.g. VERSION=1.18.3 -> 1.18.4.dev0) in:
     - __init__.py
     - setup.py
   - Commit these changes, push and create a Pull Request:
       ```
       git add -u
       git commit -m "Set dev version"
       git push upstream dev-version
       ```
     - Go to: https://github.com/huggingface/datasets/pull/new/dev-version
     - Create pull request
   - Merge the dev version Pull Request
"""

from setuptools import find_packages, setup


REQUIRED_PKGS = [
    # We use numpy>=1.17 to have np.random.Generator (Dataset shuffling)
    "numpy>=1.17",
    # Backend and serialization.
    # Minimum 8.0.0 to be able to use .to_reader()
    "pyarrow>=8.0.0",
    # For smart caching dataset processing
    "dill>=0.3.0,<0.3.8",  # tmp pin until dill has official support for determinism see https://github.com/uqfoundation/dill/issues/19
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
    # to save datasets locally or on any filesystem
    # minimum 2021.11.1 so that BlockSizeError is fixed: see https://github.com/fsspec/filesystem_spec/pull/830
    "fsspec[http]>=2021.11.1",
    # for data streaming via http
    "aiohttp",
    # To get datasets from the Datasets Hub on huggingface.co
    # minimum 0.14.0 to support HfFileSystem
    "huggingface-hub>=0.14.0,<1.0.0",
    # Utilities from PyPA to e.g., compare versions
    "packaging",
    # To parse YAML metadata from dataset cards
    "pyyaml>=5.1",
]

AUDIO_REQUIRE = [
    "soundfile>=0.12.1",
    "librosa",
]

VISION_REQUIRE = [
    "Pillow>=6.2.1",
]

BENCHMARKS_REQUIRE = [
    "tensorflow==2.12.0",
    "torch==2.0.1",
    "transformers==4.30.1",
]

TESTS_REQUIRE = [
    # test dependencies
    "absl-py",
    "joblib<1.3.0",  # joblibspark doesn't support recent joblib versions
    "joblibspark",
    "pytest",
    "pytest-datadir",
    "pytest-xdist",
    # optional dependencies
    "apache-beam>=2.26.0,<2.44.0;python_version<'3.10'",  # doesn't support recent dill versions for recent python versions
    "elasticsearch<8.0.0",  # 8.0 asks users to provide hosts or cloud_id when instantiating ElasticSearch()
    "faiss-cpu>=1.6.4",
    "lz4",
    "pyspark>=3.4",  # https://issues.apache.org/jira/browse/SPARK-40991 fixed in 3.4.0
    "py7zr",
    "rarfile>=4.0",
    "sqlalchemy<2.0.0",
    "s3fs>=2021.11.1",  # aligned with fsspec[http]>=2021.11.1; test only on python 3.7 for now
    "tensorflow>=2.3,!=2.6.0,!=2.6.1; sys_platform != 'darwin' or platform_machine != 'arm64'",
    "tensorflow-macos; sys_platform == 'darwin' and platform_machine == 'arm64'",
    "tiktoken",
    "torch",
    "soundfile>=0.12.1",
    "transformers",
    "zstandard",
]


METRICS_TESTS_REQUIRE = [
    # metrics dependencies
    "accelerate",  # for frugalscore (calls transformers' Trainer)
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
    "spacy>=3.0.0",
    "tldextract",
    # to speed up pip backtracking
    "toml>=0.10.1",
    "typer<0.5.0",  # pinned to work with Spacy==3.4.3 on Windows: see https://github.com/tiangolo/typer/issues/427
    "requests_file>=1.5.1",
    "tldextract>=3.1.0",
    "texttable>=1.6.3",
    "Werkzeug>=1.0.1",
    "six~=1.15.0",
]

TESTS_REQUIRE.extend(VISION_REQUIRE)
TESTS_REQUIRE.extend(AUDIO_REQUIRE)

QUALITY_REQUIRE = ["black~=23.1", "ruff>=0.0.241", "pyyaml>=5.3.1"]

DOCS_REQUIRE = [
    # Might need to add doc-builder and some specific deps in the future
    "s3fs",
    # Following dependencies are required for the Python reference to be built properly
    "transformers",
    "torch",
    "tensorflow>=2.2.0,!=2.6.0,!=2.6.1; sys_platform != 'darwin' or platform_machine != 'arm64'",
    "tensorflow-macos; sys_platform == 'darwin' and platform_machine == 'arm64'",
]

EXTRAS_REQUIRE = {
    "audio": AUDIO_REQUIRE,
    "vision": VISION_REQUIRE,
    "apache-beam": ["apache-beam>=2.26.0,<2.44.0"],
    "tensorflow": [
        "tensorflow>=2.2.0,!=2.6.0,!=2.6.1; sys_platform != 'darwin' or platform_machine != 'arm64'",
        "tensorflow-macos; sys_platform == 'darwin' and platform_machine == 'arm64'",
    ],
    "tensorflow_gpu": ["tensorflow-gpu>=2.2.0,!=2.6.0,!=2.6.1"],
    "torch": ["torch"],
    "jax": ["jax>=0.2.8,!=0.3.2,<=0.3.25", "jaxlib>=0.1.65,<=0.3.25"],
    "s3": ["s3fs"],
    "streaming": [],  # for backward compatibility
    "dev": TESTS_REQUIRE + QUALITY_REQUIRE + DOCS_REQUIRE,
    "tests": TESTS_REQUIRE,
    "metrics-tests": METRICS_TESTS_REQUIRE,
    "quality": QUALITY_REQUIRE,
    "benchmarks": BENCHMARKS_REQUIRE,
    "docs": DOCS_REQUIRE,
}

setup(
    name="datasets",
    version="2.14.1",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
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
    package_data={
        "datasets": ["py.typed"],
        "datasets.utils.resources": ["*.json", "*.yaml", "*.tsv"],
    },
    entry_points={"console_scripts": ["datasets-cli=datasets.commands.datasets_cli:main"]},
    python_requires=">=3.8.0",
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="datasets machine learning datasets metrics",
    zip_safe=False,  # Required for mypy to find the py.typed file
)
