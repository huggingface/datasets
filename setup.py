# Lint as: python3
"""HuggingFace/NLP is an open library of NLP datasets.

Simple check list for release from AllenNLP repo: https://github.com/allenai/allennlp/blob/master/setup.py

To create the package for pypi.

1. Change the version in __init__.py, setup.py as well as docs/source/conf.py.

2. Commit these changes with the message: "Release: VERSION"

3. Add a tag in git to mark the release: "git tag VERSION -m'Adds tag VERSION for pypi' "
   Push the tag to git: git push --tags origin master

4. Build both the sources and the wheel. Do not change anything in setup.py between
   creating the wheel and the source distribution (obviously).

   For the wheel, run: "python setup.py bdist_wheel" in the top level directory.
   (this will build a wheel for the python version you use to build it).

   For the sources, run: "python setup.py sdist"
   You should now have a /dist directory with both .whl and .tar.gz source versions.

5. Check that everything looks correct by uploading the package to the pypi test server:

   twine upload dist/* -r pypitest
   (pypi suggest using twine as other methods upload files via plaintext.)
   You may have to specify the repository url, use the following command then:
   twine upload dist/* -r pypitest --repository-url=https://test.pypi.org/legacy/

   Check that you can install it in a virtualenv by running:
   pip install -i https://testpypi.python.org/pypi nlp

6. Upload the final version to actual pypi:
   twine upload dist/* -r pypi

7. Copy the release notes from RELEASE.md to the tag in github once everything is looking hunky-dory.

8. Update the documentation commit in .circleci/deploy.sh for the accurate documentation to be displayed

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
    'numpy',
    # Backend and serialization
    'pyarrow>=0.16.0',
    # For smart caching dataset processing
    'dill',
    # for downloading datasets over HTTPS
    'requests>=2.19.0',
    # progress bars in download and scripts
    "tqdm >= 4.27",
    # dataclasses for Python versions that don't have it
    "dataclasses;python_version<'3.7'",
    # filesystem locks e.g. to prevent parallel downloads
    "filelock",
]

TESTS_REQUIRE = [
    'apache-beam',
    'absl-py',
    'bs4',
    'langdetect',
    'mwparserfromhell',
    'nltk',
    'pytest',
    'pytest-xdist',
    'tensorflow',
    'tldextract',
    'zstandard'
]


QUALITY_REQUIRE = [
    "black",
    "isort @ git+git://github.com/timothycrosley/isort.git@e63ae06ec7d70b06df9e528357650281a3d3ec22#egg=isort",
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
}

setup(
    name='nlp',
    version="0.3.0",
    description=DOCLINES[0],
    long_description='\n'.join(DOCLINES[2:]),
    author='HuggingFace Inc.',
    author_email='thomas@huggingface.co',
    url='https://github.com/huggingface/nlp',
    download_url='https://github.com/huggingface/nlp/tags',
    license='Apache 2.0',
    package_dir={"": "src"},
    packages=find_packages("src"),
    package_data={
        'nlp': [
            'scripts/templates/*',
        ],
    },
    scripts=["nlp-cli"],
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
    keywords='nlp machine learning datasets metrics',
)
