# Quickstart

This quickstart is intended for developers who are ready to dive into the code and see an example of how to integrate 🤗 Datasets into their model training workflow. If you're a beginner, we recommend starting with our [tutorials](./tutorial), where you'll get a more thorough introduction.

Each dataset is unique, and depending on the task, some datasets may require additional steps to prepare it for training. But you can always use 🤗 Datasets tools to load and process a dataset. The fastest and easiest way to get started is by loading an existing dataset from the [Hugging Face Hub](https://huggingface.co/datasets). There are thousands of datasets to choose from, spanning many tasks. Choose the type of dataset you want to work with, and let's get started!

<div class="mt-4">
   <div class="w-full flex flex-col space-y-4 md:space-y-0 md:grid md:grid-cols-3 md:gap-y-4 md:gap-x-5">
      <a class="!no-underline border dark:border-gray-700 p-5 rounded-lg shadow hover:shadow-lg" href="#audio"
         ><div class="w-full text-center bg-gradient-to-r from-violet-300 via-sky-400 to-green-500 rounded-lg py-1.5 font-semibold mb-5 text-white text-lg leading-relaxed">Audio</div>
         <p class="text-gray-700">Resample an audio dataset and get it ready for a model to classify what type of banking issue a speaker is calling about.</p>
      </a>
      <a class="!no-underline border dark:border-gray-700 p-5 rounded-lg shadow hover:shadow-lg" href="#vision"
         ><div class="w-full text-center bg-gradient-to-r from-pink-400 via-purple-400 to-blue-500 rounded-lg py-1.5 font-semibold mb-5 text-white text-lg leading-relaxed">Vision</div>
         <p class="text-gray-700">Apply data augmentation to an image dataset and get it ready for a model to diagnose disease in bean plants.</p>
      </a>
      <a class="!no-underline border dark:border-gray-700 p-5 rounded-lg shadow hover:shadow-lg" href="#nlp"
         ><div class="w-full text-center bg-gradient-to-r from-orange-300 via-red-400 to-violet-500 rounded-lg py-1.5 font-semibold mb-5 text-white text-lg leading-relaxed">NLP</div>
         <p class="text-gray-700">Tokenize a dataset and get it ready for a model to determine whether a pair of sentences have the same meaning.</p>
      </a>
   </div>
</div>

<Tip>

Check out [Chapter 5](https://huggingface.co/course/chapter5/1?fw=pt) of the Hugging Face course to learn more about other important topics such as loading remote or local datasets, tools for cleaning up a dataset, and creating your own dataset.

</Tip>

Start by installing 🤗 Datasets:

```bash
pip install datasets
```

To work with audio datasets, install the [`Audio`] feature:

```bash
pip install datasets[audio]
```

To work with image datasets, install the [`Image`] feature:

```bash
pip install datasets[vision]
```

## Audio

Audio datasets are loaded just like text datasets. However, an audio dataset is preprocessed a bit differently. Instead of a tokenizer, you'll need a [feature extractor](https://huggingface.co/docs/transformers/main_classes/feature_extractor#feature-extractor). An audio input may also require resampling its sampling rate to match the sampling rate of the pretrained model you're using. In this quickstart, you'll prepare the [MInDS-14](https://huggingface.co/datasets/PolyAI/minds14) dataset for a model train on and classify the banking issue a customer is having.

**1**. Load the MInDS-14 dataset by providing the [`load_dataset`] function with the dataset name, dataset configuration (not all datasets will have a configuration), and a dataset split:

```py
>>> from datasets import load_dataset, Audio

>>> dataset = load_dataset("PolyAI/minds14", "en-US", split="train")
```

**2**. Next, load a pretrained [Wav2Vec2](https://huggingface.co/facebook/wav2vec2-base) model and its corresponding feature extractor from the [🤗 Transformers](https://huggingface.co/transformers/) library. It is totally normal to see a warning after you load the model about some weights not being initialized. This is expected because you are loading this model checkpoint for training with another task.

```py
>>> from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

>>> model = AutoModelForAudioClassification.from_pretrained("facebook/wav2vec2-base")
>>> feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base")
```

**3**. The [MInDS-14](https://huggingface.co/datasets/PolyAI/minds14) dataset card indicates the sampling rate is 8kHz, but the Wav2Vec2 model was pretrained on a sampling rate of 16kHZ. You'll need to upsample the `audio` column with the [`~Dataset.cast_column`] function and [`Audio`] feature to match the model's sampling rate.

```py
>>> dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
>>> dataset[0]["audio"]
{'array': array([ 2.3443763e-05,  2.1729663e-04,  2.2145823e-04, ...,
         3.8356509e-05, -7.3497440e-06, -2.1754686e-05], dtype=float32),
 'path': '/root/.cache/huggingface/datasets/downloads/extracted/f14948e0e84be638dd7943ac36518a4cf3324e8b7aa331c5ab11541518e9368c/en-US~JOINT_ACCOUNT/602ba55abb1e6d0fbce92065.wav',
 'sampling_rate': 16000}
```

**4**. Create a function to preprocess the audio `array` with the feature extractor, and truncate and pad the sequences into tidy rectangular tensors. The most important thing to remember is to call the audio `array` in the feature extractor since the `array` - the actual speech signal - is the model input.

Once you have a preprocessing function, use the [`~Dataset.map`] function to speed up processing by applying the function to batches of examples in the dataset.

```py
>>> def preprocess_function(examples):
...     audio_arrays = [x["array"] for x in examples["audio"]]
...     inputs = feature_extractor(
...         audio_arrays,
...         sampling_rate=16000,
...         padding=True,
...         max_length=100000,
...         truncation=True,
...     )
...     return inputs

>>> dataset = dataset.map(preprocess_function, batched=True)
```

**5**. Use the [`~Dataset.rename_column`] function to rename the `intent_class` column to `labels`, which is the expected input name in [Wav2Vec2ForSequenceClassification](https://huggingface.co/docs/transformers/main/en/model_doc/wav2vec2#transformers.Wav2Vec2ForSequenceClassification):

```py
>>> dataset = dataset.rename_column("intent_class", "labels")
```

**6**. Set the dataset format according to the machine learning framework you're using.

<frameworkcontent>
<pt>
Use the [`~Dataset.set_format`] function to set the dataset format to `torch` and specify the columns you want to format. This function applies formatting on-the-fly. After converting to PyTorch tensors, wrap the dataset in [`torch.utils.data.DataLoader`](https://alband.github.io/doc_view/data.html?highlight=torch%20utils%20data%20dataloader#torch.utils.data.DataLoader):

```py
>>> from torch.utils.data import DataLoader

>>> dataset.set_format(type="torch", columns=["input_values", "labels"])
>>> dataloader = DataLoader(dataset, batch_size=4)
```
</pt>
<tf>
Use the [`~Dataset.to_tf_dataset`] function to set the dataset format to be compatible with TensorFlow. You'll also need to import a [data collator](https://huggingface.co/docs/transformers/main_classes/data_collator#transformers.DataCollatorWithPadding) from 🤗 Transformers to combine the varying sequence lengths into a single batch of equal lengths:

```py
>>> import tensorflow as tf

>>> tf_dataset = dataset.to_tf_dataset(
...     columns=["input_values"],
...     label_cols=["labels"],
...     batch_size=4,
...     shuffle=True)
```
</tf>
</frameworkcontent>

**7**. Start training with your machine learning framework! Check out the 🤗 Transformers [audio classification guide](https://huggingface.co/docs/transformers/tasks/audio_classification) for an end-to-end example of how to train a model on an audio dataset.

## Vision

Image datasets are loaded just like text datasets. However, instead of a tokenizer, you'll need a [feature extractor](https://huggingface.co/docs/transformers/main_classes/feature_extractor#feature-extractor) to preprocess the dataset. Applying data augmentation to an image is common in computer vision to make the model more robust against overfitting. You're free to use any data augmentation library you want, and then you can apply the augmentations with 🤗 Datasets. In this quickstart, you'll load the [Beans](https://huggingface.co/datasets/beans) dataset and get it ready for the model to train on and identify disease from the leaf images.

**1**. Load the Beans dataset by providing the [`load_dataset`] function with the dataset name and a dataset split:

```py
>>> from datasets import load_dataset, Image

>>> dataset = load_dataset("beans", split="train")
```

**2**. Now you can add some data augmentations with any library ([Albumentations](https://albumentations.ai/), [imgaug](https://imgaug.readthedocs.io/en/latest/), [Kornia](https://kornia.readthedocs.io/en/latest/)) you like. Here, you'll use [torchvision](https://pytorch.org/vision/stable/transforms.html) to randomly change the color properties of an image:

```py
>>> from torchvision.transforms import Compose, ColorJitter, ToTensor

>>> jitter = Compose(
...     [ColorJitter(brightness=0.5, hue=0.5), ToTensor()]
... )
```

**3**. Create a function to apply your transform to the dataset and generate the model input: `pixel_values`.

```python
>>> def transforms(examples):
...     examples["pixel_values"] = [jitter(image.convert("RGB")) for image in examples["image"]]
...     return examples
```

**4**. Use the [`~Dataset.with_transform`] function to apply the data augmentations on-the-fly:

```py
>>> dataset = dataset.with_transform(transforms)
```

**5**. Set the dataset format according to the machine learning framework you're using.

<frameworkcontent>
<pt>
Wrap the dataset in [`torch.utils.data.DataLoader`](https://alband.github.io/doc_view/data.html?highlight=torch%20utils%20data%20dataloader#torch.utils.data.DataLoader). You'll also need to create a collate function to collate the samples into batches:

```py
>>> from torch.utils.data import DataLoader

>>> def collate_fn(examples):
...     images = []
...     labels = []
...     for example in examples:
...         images.append((example["pixel_values"]))
...         labels.append(example["labels"])
...         
...     pixel_values = torch.stack(images)
...     labels = torch.tensor(labels)
...     return {"pixel_values": pixel_values, "labels": labels}
>>> dataloader = DataLoader(dataset, collate_fn=collate_fn, batch_size=4)
```
</pt>
</frameworkcontent>

**6**. Start training with your machine learning framework! Check out the 🤗 Transformers [image classification guide](https://huggingface.co/docs/transformers/tasks/image_classification) for an end-to-end example of how to train a model on an image dataset.

## NLP

Text needs to be tokenized into individual tokens by a [tokenizer](https://huggingface.co/docs/transformers/main_classes/tokenizer). For the quickstart, you'll load the [Microsoft Research Paraphrase Corpus (MRPC)](https://huggingface.co/datasets/glue/viewer/mrpc) training dataset to train a model to determine whether a pair of sentences mean the same thing.

**1**. Load the MRPC dataset by providing the [`load_dataset`] function with the dataset name, dataset configuration (not all datasets will have a configuration), and dataset split:

```py
>>> from datasets import load_dataset

>>> dataset = load_dataset("glue", "mrpc", split="train")
```

**2**. Next, load a pretrained [BERT](https://huggingface.co/bert-base-uncased) model and its corresponding tokenizer from the [🤗 Transformers](https://huggingface.co/transformers/) library. It is totally normal to see a warning after you load the model about some weights not being initialized. This is expected because you are loading this model checkpoint for training with another task.

```py
>>> from transformers import AutoModelForSequenceClassification, AutoTokenizer

>>> model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
>>> tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
===PT-TF-SPLIT===
>>> from transformers import TFAutoModelForSequenceClassification, AutoTokenizer

>>> model = TFAutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
>>> tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
```

**3**. Create a function to tokenize the dataset, and you should also truncate and pad the text into tidy rectangular tensors. The tokenizer generates three new columns in the dataset: `input_ids`, `token_type_ids`, and an `attention_mask`. These are the model inputs.

Use the [`~Dataset.map`] function to speed up processing by applying your tokenization function to batches of examples in the dataset:

```py
>>> def encode(examples):
...     return tokenizer(examples["sentence1"], examples["sentence2"], truncation=True, padding="max_length")

>>> dataset = dataset.map(encode, batched=True)
>>> dataset[0]
{'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
'label': 1,
'idx': 0,
'input_ids': array([  101,  7277,  2180,  5303,  4806,  1117,  1711,   117,  2292, 1119,  1270,   107,  1103,  7737,   107,   117,  1104,  9938, 4267, 12223, 21811,  1117,  2554,   119,   102, 11336,  6732, 3384,  1106,  1140,  1112,  1178,   107,  1103,  7737,   107, 117,  7277,  2180,  5303,  4806,  1117,  1711,  1104,  9938, 4267, 12223, 21811,  1117,  2554,   119,   102]),
'token_type_ids': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
'attention_mask': array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])}
```

**4**. Rename the `label` column to `labels`, which is the expected input name in [BertForSequenceClassification](https://huggingface.co/docs/transformers/main/en/model_doc/bert#transformers.BertForSequenceClassification):

```py
>>> dataset = dataset.map(lambda examples: {"labels": examples["label"]}, batched=True)
```

**5**. Set the dataset format according to the machine learning framework you're using.

<frameworkcontent>
<pt>
Use the [`~Dataset.set_format`] function to set the dataset format to `torch` and specify the columns you want to format. This function applies formatting on-the-fly. After converting to PyTorch tensors, wrap the dataset in [`torch.utils.data.DataLoader`](https://alband.github.io/doc_view/data.html?highlight=torch%20utils%20data%20dataloader#torch.utils.data.DataLoader):

```py
>>> import torch

>>> dataset.set_format(type="torch", columns=["input_ids", "token_type_ids", "attention_mask", "labels"])
>>> dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)
```
</pt>
<tf>
Use the [`~Dataset.to_tf_dataset`] function to set the dataset format to be compatible with TensorFlow. You'll also need to import a [data collator](https://huggingface.co/docs/transformers/main_classes/data_collator#transformers.DataCollatorWithPadding) from 🤗 Transformers to combine the varying sequence lengths into a single batch of equal lengths:

```py
>>> import tensorflow as tf
>>> from transformers import DataCollatorWithPadding

>>> data_collator = DataCollatorWithPadding(tokenizer=tokenizer, return_tensors="tf")
>>> tf_dataset = dataset.to_tf_dataset(
...     columns=["input_ids", "token_type_ids", "attention_mask"],
...     label_cols=["labels"],
...     batch_size=2,
...     collate_fn=data_collator,
...     shuffle=True)
```
</tf>
</frameworkcontent>

**6**. Start training with your machine learning framework! Check out the 🤗 Transformers [text classification guide](https://huggingface.co/docs/transformers/tasks/sequence_classification) for an end-to-end example of how to train a model on a text dataset.

## What's next?

This completes the 🤗 Datasets quickstart! You can load any text, audio, or image dataset with a single function and get it ready for your model to train on.

For your next steps, take a look at our [How-to guides](./how_to) and learn how to do more specific things like loading different dataset formats, aligning labels, and streaming large datasets. If you're interested in learning more about 🤗 Datasets core concepts, grab a cup of coffee and read our [Conceptual Guides](./about_arrow)!
