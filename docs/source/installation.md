# Installation

Before you start, you'll need to setup your environment and install the appropriate packages. 🤗 Datasets is tested on **Python 3.7+**.

<Tip>

If you want to use 🤗 Datasets with TensorFlow or PyTorch, you'll need to install them separately. Refer to the [TensorFlow installation page](https://www.tensorflow.org/install/pip#tensorflow-2-packages-are-available) or the [PyTorch installation page](https://pytorch.org/get-started/locally/#start-locally) for the specific install command for your framework.

</Tip>

## Virtual environment

You should install 🤗 Datasets in a [virtual environment](https://docs.python.org/3/library/venv.html) to keep things tidy and avoid dependency conflicts.

1. Create and navigate to your project directory:

   ```bash
   mkdir ~/my-project
   cd ~/my-project
   ```

2. Start a virtual environment inside your directory:

   ```bash
   python -m venv .env
   ```

3. Activate and deactivate the virtual environment with the following commands:

   ```bash
   # Activate the virtual environment
   source .env/bin/activate
   
   # Deactivate the virtual environment
   source .env/bin/deactivate
   ```

Once you've created your virtual environment, you can install 🤗 Datasets in it.

## pip

The most straightforward way to install 🤗 Datasets is with pip:

```bash
pip install datasets
```

Run the following command to check if 🤗 Datasets has been properly installed:

```bash
python -c "from datasets import load_dataset; print(load_dataset('squad', split='train')[0])"
```

This command downloads version 1 of the [Stanford Question Answering Dataset (SQuAD)](https://rajpurkar.github.io/SQuAD-explorer/), loads the training split, and prints the first training example. You should see:

```python
{'answers': {'answer_start': [515], 'text': ['Saint Bernadette Soubirous']}, 'context': 'Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend "Venite Ad Me Omnes". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.', 'id': '5733be284776f41900661182', 'question': 'To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?', 'title': 'University_of_Notre_Dame'}
```

## Audio

To work with audio datasets, you need to install the [`Audio`] feature as an extra dependency:

```bash
pip install datasets[audio]
```

<Tip warning={true}>

On Linux, non-Python dependency on `libsndfile` package must be installed manually, using your distribution package manager, for example:

```bash
sudo apt-get install libsndfile1
```

</Tip>

To support loading audio datasets containing MP3 files, users should also install [torchaudio](https://pytorch.org/audio/stable/index.html) to handle the audio data with high performance:

```bash
pip install 'torchaudio<0.12.0'
```

<Tip warning={true}>

torchaudio's `sox_io` [backend](https://pytorch.org/audio/stable/backend.html#) supports decoding MP3 files. Unfortunately, the `sox_io` backend is only available on Linux/macOS and isn't supported by Windows.

You need to install it using your distribution package manager, for example:

```bash
sudo apt-get install sox
```

</Tip>

## Vision

To work with image datasets, you need to install the [`Image`] feature as an extra dependency:

```bash
pip install datasets[vision]
```

## source

Building 🤗 Datasets from source lets you make changes to the code base. To install from the source, clone the repository and install with the following commands:

```bash
git clone https://github.com/huggingface/datasets.git
cd datasets
pip install -e .
```

Again, you can check if 🤗 Datasets was properly installed with the following command:

```bash
python -c "from datasets import load_dataset; print(load_dataset('squad', split='train')[0])"
```

## conda

🤗 Datasets can also be installed from conda, a package management system:

```bash
conda install -c huggingface -c conda-forge datasets
```
