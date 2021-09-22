# Lint as: python3
""" HuggingFace/Datasets is an open library of NLP datasets.

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

1. Change the version in:
   - __init__.py
   - setup.py
   - docs/source/conf.py

2. Commit these changes: "git commit -m 'Release: VERSION'"

3. Add a tag in git to mark the release: "git tag VERSION -m 'Add tag VERSION for pypi'"
   Push the tag to remote: git push --tags origin master

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

8. Update the documentation commit in .circleci/deploy.sh for the accurate documentation to be displayed.
   Update the version mapping in docs/source/_static/js/custom.js with: "python utils/release.py --version VERSION"
   Set version to X.X.X+1.dev0 (e.g. 1.8.0 -> 1.8.1.dev0) in:
   - setup.py
   - __init__.py

9. Commit these changes: "git commit -m 'Release docs'"
   Push the commit to remote: "git push origin master"
"""

import datetime
import itertools
import os
import sys

from setuptools import find_packages, setup


DOCLINES = __doc__.split("\n")


REQUIRED_PKGS = [
    # We use numpy>=1.17 to have np.random.Generator (Dataset shuffling)
    "numpy>=1.17",
    # Backend and serialization.
    # Minimum 3.0.0 to support mix of struct and list types in parquet, and batch iterators of parquet data
    # pyarrow 4.0.0 introduced segfault bug, see: https://github.com/huggingface/datasets/pull/2268
    "pyarrow>=1.0.0,!=4.0.0",
    # For smart caching dataset processing
    "dill",
    # For performance gains with apache arrow
    "pandas",
    # for downloading datasets over HTTPS
    "requests>=2.19.0",
    # progress bars in download and scripts
    "tqdm>=4.62.1",
    # dataclasses for Python versions that don't have it
    "dataclasses;python_version<'3.7'",
    # for fast hashing
    "xxhash",
    # for better multiprocessing
    "multiprocess",
    # to get metadata of optional dependencies such as torch or tensorflow for Python versions that don't have it
    "importlib_metadata;python_version<'3.8'",
    # to save datasets locally or on any filesystem
    # minimum 2021.05.0 to have the AbstractArchiveFileSystem
    "fsspec[http]>=2021.05.0",
    # for data streaming via http
    "aiohttp",
    # To get datasets from the Datasets Hub on huggingface.co
    "huggingface_hub>=0.0.14,<0.1.0",
    # Utilities from PyPA to e.g., compare versions
    "packaging",
]

BENCHMARKS_REQUIRE = [
    "numpy==1.18.5",
    "tensorflow==2.3.0",
    "torch==1.6.0",
    "transformers==3.0.2",
]

TESTS_REQUIRE = [
    # test dependencies
    "absl-py",
    "pytest",
    "pytest-xdist",
    # optional dependencies
    "apache-beam>=2.26.0",
    "elasticsearch",
    "aiobotocore",
    "boto3",
    "botocore",
    "faiss-cpu",
    "fsspec[s3]",
    "moto[s3,server]==2.0.4",
    "rarfile>=4.0",
    "s3fs==2021.08.1",
    "tensorflow>=2.3",
    "torch",
    "transformers",
    # datasets dependencies
    "bs4",
    "conllu",
    "langdetect",
    "lxml",
    "mwparserfromhell",
    "nltk",
    "openpyxl",
    "py7zr",
    "tldextract",
    "zstandard",
    # metrics dependencies
    "bert_score>=0.3.6",
    "rouge_score",
    "sacrebleu",
    "scipy",
    "seqeval",
    "scikit-learn",
    "jiwer",
    "sentencepiece",  # for bleurt
    # to speed up pip backtracking
    "toml>=0.10.1",
    "requests_file>=1.5.1",
    "tldextract>=3.1.0",
    "texttable>=1.6.3",
    "Werkzeug>=1.0.1",
    "six~=1.15.0",
    # metadata validation
    "importlib_resources;python_version<'3.7'",
]

if os.name == "nt":  # windows
    TESTS_REQUIRE.remove("faiss-cpu")  # faiss doesn't exist on windows
else:
    # dependencies of unbabel-comet
    # only test if not on windows since there're issues installing fairseq on windows
    TESTS_REQUIRE.extend(
        [
            "wget>=3.2",
            "pytorch-nlp==0.5.0",
            "pytorch_lightning",
            "fastBPE==0.1.0",
            "fairseq",
        ]
    )


QUALITY_REQUIRE = ["black==21.4b0", "flake8==3.7.9", "isort", "pyyaml>=5.3.1"]


EXTRAS_REQUIRE = {
    "apache-beam": ["apache-beam>=2.26.0"],
    "tensorflow": ["tensorflow>=2.2.0"],
    "tensorflow_gpu": ["tensorflow-gpu>=2.2.0"],
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
        "docutils==0.16.0",
        "recommonmark",
        "sphinx==3.1.2",
        "sphinx-markdown-tables",
        "sphinx-rtd-theme==0.4.3",
        "sphinxext-opengraph==0.4.1",
        "sphinx-copybutton",
        "fsspec",
        "s3fs",
        "sphinx-panels",
        "sphinx-inline-tabs",
        "myst-parser",
    ],
}

setup(
    name="datasets",
    version="1.12.2.dev0",  # expected format is one of x.y.z.dev0, or x.y.z.rc1 or x.y.z (no to dashes, yes to dots)
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    long_description_content_type='text/markdown',
    author="HuggingFace Inc.",
    author_email="thomas@huggingface.co",
    url="https://github.com/huggingface/datasets",
    download_url="https://github.com/huggingface/datasets/tags",
    license="Apache 2.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    package_data={"datasets": ["py.typed", "scripts/templates/*"], "datasets.utils.resources": ["*.json", "*.yaml"]},
    entry_points={"console_scripts": ["datasets-cli=datasets.commands.datasets_cli:main"]},
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
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="datasets machine learning datasets metrics",
    zip_safe=False,  # Required for mypy to find the py.typed file
)
