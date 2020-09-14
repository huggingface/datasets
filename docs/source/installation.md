# Installation

🤗datasets is tested on Python 3.6+.

You should install 🤗datasets in a [virtual environment](https://docs.python.org/3/library/venv.html). If you're
unfamiliar with Python virtual environments, check out the [user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). Create a virtual environment with the version of Python you're going 
to use and activate it.

Now, if you want to use 🤗datasets, you can install it with pip. If you'd like to play with the examples, you
must install it from source.

## Installation with pip

🤗datasets can be installed using pip as follows:

```bash
pip install datasets
```

To check 🤗 Transformers is properly installed, run the following command:

```bash
python -c "from datasets import load_dataset; print(load_dataset('squad', split='train')[0])"
```

It should download version 1 of the [Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/), load its training split and print the first training example:

```python
{'id': '5733be284776f41900661182', 'title': 'University_of_Notre_Dame', 'context': 'Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend "Venite Ad Me Omnes". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.', 'question': 'To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?', 'answers': {'text': array(['Saint Bernadette Soubirous'], dtype=object), 'answer_start': array([515], dtype=int32)}}
```

If you want to use the 🤗datasets library with TensorFlow 2.0 or PyTorch, you will need to install these seperately.
Please refer to [TensorFlow installation page](https://www.tensorflow.org/install/pip#tensorflow-2.0-rc-is-available) 
and/or [PyTorch installation page](https://pytorch.org/get-started/locally/#start-locally) regarding the specific 
install command for your platform.


## Installing from source

To install from source, clone the repository and install with the following commands:

``` bash
git clone https://github.com/huggingface/datasets.git
cd datasets
pip install -e .
```

Again, you can run 

```bash
python -c "from datasets import load_dataset; print(load_dataset('squad', split='train')[0])"
```

to check 🤗datasets is properly installed.

## Caching datasets and metrics

This library will download and cache datasets and metrics processing scripts and data locally.

Unless you specify a location with `cache_dir=...` when you use methods like `load_dataset` and `load_metric`, these datasets and metrics will automatically be downloaded in the folders respectively given by the shell environment variables ``HF_DATASETS_CACHE`` and ``HF_METRICS_CACHE``. The default value for it will be the HuggingFace cache home followed by ``/datasets/`` for datasets scripts and data, and ``/metrics/`` for metrics scripts and data.

The HuggingFace cache home is (by order of priority):

  * shell environment variable ``HF_HOME``
  * shell environment variable ``ENV_XDG_CACHE_HOME`` + ``/huggingface/``
  * default: ``~/.cache/huggingface/``

So if you don't have any specific environment variable set, the cache directory for datasets scripts and data will be at ``~/.cache/huggingface/datasets/``.
