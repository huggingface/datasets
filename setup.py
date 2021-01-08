# Lint as: python3
""" HuggingFace/Datasets is an open library of NLP datasets.

Note:

   VERSION needs to be formatted following the MAJOR.MINOR.PATCH convention
   (we need to follow this convention to be able to retrieve versioned scripts)

Simple check list for release from AllenNLP repo: https://github.com/allenai/allennlp/blob/master/setup.py

To create the package for pypi.

1. Change the version in __init__.py, setup.py as well as docs/source/conf.py.

2. Commit these changes with the message: "Release: VERSION"

3. Add a tag in git to mark the release: "git tag VERSION -m'Adds tag VERSION for pypi' "
   Push the tag to git: git push --tags origin master

4. Build both the sources and the wheel. Do not change anything in setup.py between
   creating the wheel and the source distribution (obviously).

   First pin the SCRIPTS_VERSION to VERSION in __init__.py (but don't commit this change)

   For the wheel, run: "python setup.py bdist_wheel" in the top level directory.
   (this will build a wheel for the python version you use to build it).

   For the sources, run: "python setup.py sdist"
   You should now have a /dist directory with both .whl and .tar.gz source versions.

   Then change the SCRIPTS_VERSION back to to "master" in __init__.py (but don't commit this change)

5. Check that everything looks correct by uploading the package to the pypi test server:

   twine upload dist/* -r pypitest
   (pypi suggest using twine as other methods upload files via plaintext.)
   You may have to specify the repository url, use the following command then:
   twine upload dist/* -r pypitest --repository-url=https://test.pypi.org/legacy/

   Check that you can install it in a virtualenv by running:
   pip install -i https://testpypi.python.org/pypi datasets

6. Upload the final version to actual pypi:
   twine upload dist/* -r pypi

7. Copy the release notes from RELEASE.md to the tag in github once everything is looking hunky-dory.

8. Update the documentation commit in .circleci/deploy.sh for the accurate documentation to be displayed
   Update the version mapping in docs/source/_static/js/custom.js

9. Update README.md to redirect to correct documentation.
"""

import datetime
import itertools
import os
import sys

from setuptools import find_packages
from setuptools import setup

DOCLINES = __doc__.split('\n')

REQUIRED_PKGS = [
    # We use numpy>=1.17 to have np.random.Generator (Dataset shuffling)
    'numpy>=1.17',
    # Backend and serialization. Minimum 0.17.1 to support extension array
    'pyarrow>=0.17.1',
    # For smart caching dataset processing
    'dill',
    # For performance gains with apache arrow
    'pandas',
    # for downloading datasets over HTTPS
    'requests>=2.19.0',
    # progress bars in download and scripts
    # tqdm 4.50.0 introduced permission errors on windows
    # see https://app.circleci.com/pipelines/github/huggingface/datasets/235/workflows/cfb6a39f-68eb-4802-8b17-2cd5e8ea7369/jobs/1111
    "tqdm>=4.27,<4.50.0",
    # dataclasses for Python versions that don't have it
    "dataclasses;python_version<'3.7'",
    # for fast hashing
    "xxhash",
    # for better multiprocessing
    "multiprocess",
    # to get metadata of optional dependencies such as torch or tensorflow for Python versions that don't have it
    "importlib_metadata;python_version<'3.8'"
]

BENCHMARKS_REQUIRE = [
    'numpy==1.18.5',
    'tensorflow==2.3.0',
    'torch==1.6.0',
    'transformers==3.0.2',
]

TESTS_REQUIRE = [
    'apache-beam',
    'absl-py',
    'bs4',
    'conllu',
    'elasticsearch',
    'faiss-cpu',
    'langdetect',
    'lxml',
    'mwparserfromhell',
    'nltk',
    'openpyxl',
    'py7zr',
    'pytest',
    'pytest-xdist',
    'tensorflow',
    'torch',
    'tldextract',
    'transformers',
    'zstandard',
    'rarfile',
]

if os.name == "nt":  # windows
    TESTS_REQUIRE.remove("faiss-cpu")  # faiss doesn't exist on windows


QUALITY_REQUIRE = [
    "black",
    "isort",
    "flake8==3.7.9",
]


EXTRAS_REQUIRE = {
    'apache-beam': ['apache-beam'],
    'tensorflow': ['tensorflow>=2.2.0'],
    'tensorflow_gpu': ['tensorflow-gpu>=2.2.0'],
    'torch': ['torch'],
    'dev': TESTS_REQUIRE + QUALITY_REQUIRE,
    'tests': TESTS_REQUIRE,
    'quality': QUALITY_REQUIRE,
    'benchmarks': BENCHMARKS_REQUIRE,
    'docs': ["recommonmark", "sphinx==3.1.2", "sphinx-markdown-tables", "sphinx-rtd-theme==0.4.3", "sphinx-copybutton"]
}

setup(
    name='datasets',
    version="1.2.0",
    description=DOCLINES[0],
    long_description='\n'.join(DOCLINES[2:]),
    author='HuggingFace Inc.',
    author_email='thomas@huggingface.co',
    url='https://github.com/huggingface/datasets',
    download_url='https://github.com/huggingface/datasets/tags',
    license='Apache 2.0',
    package_dir={"": "src"},
    packages=find_packages("src"),
    package_data={
        'datasets': [
            'scripts/templates/*',
        ],
    },
    scripts=["datasets-cli"],
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
    keywords='datasets machine learning datasets metrics',
)
