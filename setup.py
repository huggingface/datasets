# Lint as: python3
"""HuggingFace/Datasets is an open library of datasets.

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
       Add a step to install `datasets@main` after `save_cache` in .circleci/create_circleci_config.py:
       ```
       steps.append({"run": {"name": "Install `datasets@main`", "command": 'pip uninstall datasets -y && pip install "datasets @ git+https://github.com/huggingface/datasets@main#egg=datasets"'}})
       ```
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
   - Go to: https://github.com/huggingface/datasets/pull/new/release-VERSION
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
     twine upload dist/* -r testpypi
     ```
   Check that you can install it in a virtualenv/notebook by running:
     ```
     !pip install -U --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ datasets
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
    # For file locking
    "filelock",
    # We use numpy>=1.17 to have np.random.Generator (Dataset shuffling)
    "numpy>=1.17",
    # Backend and serialization.
    # Minimum 15.0.0 to be able to cast dictionary types to their underlying types
    "pyarrow>=15.0.0",
    # For smart caching dataset processing
    "dill>=0.3.0,<0.3.9",  # tmp pin until dill has official support for determinism see https://github.com/uqfoundation/dill/issues/19
    # For performance gains with apache arrow
    "pandas",
    # for downloading datasets over HTTPS
    "requests>=2.32.2",
    # progress bars in download and scripts
    "tqdm>=4.66.3",
    # for fast hashing
    "xxhash",
    # for better multiprocessing
    "multiprocess<0.70.17",  # to align with dill<0.3.9 (see above)
    # to save datasets locally or on any filesystem
    # minimum 2023.1.0 to support protocol=kwargs in fsspec's `open`, `get_fs_token_paths`, etc.: see https://github.com/fsspec/filesystem_spec/pull/1143
    "fsspec[http]>=2023.1.0,<=2025.3.0",
    # To get datasets from the Datasets Hub on huggingface.co
    "huggingface-hub>=0.24.0",
    # Utilities from PyPA to e.g., compare versions
    "packaging",
    # To parse YAML metadata from dataset cards
    "pyyaml>=5.1",
]

AUDIO_REQUIRE = [
    "soundfile>=0.12.1",
    "librosa",
    "soxr>=0.4.0",  # Supports numpy-2
]

VISION_REQUIRE = [
    "Pillow>=9.4.0",  # When PIL.Image.ExifTags was introduced
]

BENCHMARKS_REQUIRE = [
    "tensorflow==2.12.0",
    "torch==2.0.1",
    "transformers==4.30.1",
]

TESTS_REQUIRE = [
    # test dependencies
    "absl-py",
    "decorator",
    "joblib<1.3.0",  # joblibspark doesn't support recent joblib versions
    "joblibspark",
    "pytest",
    "pytest-datadir",
    "pytest-xdist",
    # optional dependencies
    "aiohttp",
    "elasticsearch>=7.17.12,<8.0.0",  # 8.0 asks users to provide hosts or cloud_id when instantiating ElasticSearch(); 7.9.1 has legacy numpy.float_ which was fixed in https://github.com/elastic/elasticsearch-py/pull/2551.
    "faiss-cpu>=1.8.0.post1",  # Pins numpy < 2
    "jax>=0.3.14; sys_platform != 'win32'",
    "jaxlib>=0.3.14; sys_platform != 'win32'",
    "lz4",
    "moto[server]",
    "pyspark>=3.4",  # https://issues.apache.org/jira/browse/SPARK-40991 fixed in 3.4.0
    "py7zr",
    "rarfile>=4.0",
    "sqlalchemy",
    "s3fs>=2021.11.1",  # aligned with fsspec[http]>=2021.11.1; test only on python 3.7 for now
    "protobuf<4.0.0",  # 4.0.0 breaks compatibility with tensorflow<2.12
    "tensorflow>=2.6.0; python_version<'3.10'",  # numpy-2 is not supported for Python < 3.10
    "tensorflow>=2.16.0; python_version>='3.10'",  # Pins numpy < 2
    "tiktoken",
    "torch>=2.0.0",
    "torchdata",
    "soundfile>=0.12.1",
    "transformers>=4.42.0",  # Pins numpy < 2
    "zstandard",
    "polars[timezone]>=0.20.0",
    "torchvision",
    "pyav",
]


TESTS_REQUIRE.extend(VISION_REQUIRE)
TESTS_REQUIRE.extend(AUDIO_REQUIRE)

NUMPY2_INCOMPATIBLE_LIBRARIES = [
    "faiss-cpu",
    "librosa",  # librosa -> numba-0.60.0 requires numpy < 2.1 (see GH-7111)
    "tensorflow",
]
TESTS_NUMPY2_REQUIRE = [
    library for library in TESTS_REQUIRE if library.partition(">")[0] not in NUMPY2_INCOMPATIBLE_LIBRARIES
]

QUALITY_REQUIRE = ["ruff>=0.3.0"]

DOCS_REQUIRE = [
    # Might need to add doc-builder and some specific deps in the future
    "s3fs",
    # Following dependencies are required for the Python reference to be built properly
    "transformers",
    "torch",
    "tensorflow>=2.6.0",
]

PDFS_REQUIRE = ["pdfplumber>=0.11.4"]

EXTRAS_REQUIRE = {
    "audio": AUDIO_REQUIRE,
    "vision": VISION_REQUIRE,
    "tensorflow": [
        "tensorflow>=2.6.0",
    ],
    "tensorflow_gpu": ["tensorflow>=2.6.0"],
    "torch": ["torch"],
    "jax": ["jax>=0.3.14", "jaxlib>=0.3.14"],
    "s3": ["s3fs"],
    "streaming": [],  # for backward compatibility
    "dev": TESTS_REQUIRE + QUALITY_REQUIRE + DOCS_REQUIRE,
    "tests": TESTS_REQUIRE,
    "tests_numpy2": TESTS_NUMPY2_REQUIRE,
    "quality": QUALITY_REQUIRE,
    "benchmarks": BENCHMARKS_REQUIRE,
    "docs": DOCS_REQUIRE,
    "pdfs": PDFS_REQUIRE,
}

setup(
    name="datasets",
    version="3.6.0",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
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
    python_requires=">=3.9.0",
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="datasets machine learning datasets",
    zip_safe=False,  # Required for mypy to find the py.typed file
)
