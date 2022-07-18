# Process audio data

This guide shows specific methods for processing audio datasets. Learn how to:

- Resample the sampling rate.
- Use [`~Dataset.map`] with audio datasets.

For a guide on how to process any type of dataset, take a look at the <a class="underline decoration-sky-400 decoration-2 font-semibold" href="./process">general process guide</a>.


## Cast

The [`~Dataset.cast_column`] function is used to cast a column to another feature to be decoded. When you use this function with the [`Audio`] feature, you can resample the sampling rate:

```py
>>> from datasets import load_dataset, Audio

>>> dataset = load_dataset("PolyAI/minds14", "en-US", split="train")
>>> dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))
```

Audio files are decoded and resampled on-the-fly, so the next time you access an example, the audio file is resampled to 16kHz:

```py
>>> dataset[0]["audio"]
{'array': array([ 2.3443763e-05,  2.1729663e-04,  2.2145823e-04, ...,
         3.8356509e-05, -7.3497440e-06, -2.1754686e-05], dtype=float32),
 'path': '/root/.cache/huggingface/datasets/downloads/extracted/f14948e0e84be638dd7943ac36518a4cf3324e8b7aa331c5ab11541518e9368c/en-US~JOINT_ACCOUNT/602ba55abb1e6d0fbce92065.wav',
 'sampling_rate': 16000}
```

<div class="flex justify-center">
    <img class="block dark:hidden" src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/datasets/resample.gif"/>
    <img class="hidden dark:block" src="https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/datasets/resample-dark.gif"/>
</div>

## Map

The [`~Dataset.map`] function helps preprocess your entire dataset at once. Depending on the type of model you're working with, you'll need to either load a [feature extractor](https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoFeatureExtractor) or a [processor](https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoProcessor).

- For pretrained speech recognition models, load a feature extractor and tokenizer and combine them in a `processor`:

    ```py
    >>> from transformers import AutoTokenizer, AutoFeatureExtractor, AutoProcessor

    >>> model_checkpoint = "facebook/wav2vec2-large-xlsr-53"
    # after defining a vocab.json file you can instantiate a tokenizer object:
    >>> tokenizer = AutoTokenizer("./vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
    >>> feature_extractor = AutoFeatureExtractor.from_pretrained(model_checkpoint)
    >>> processor = AutoProcessor.from_pretrained(feature_extractor=feature_extractor, tokenizer=tokenizer)
    ```

- For fine-tuned speech recognition models, you only need to load a `processor`:

    ```py
    >>> from transformers import AutoProcessor

    >>> processor = AutoProcessor.from_pretrained("facebook/wav2vec2-base-960h")
    ```

When you use [`~Dataset.map`] with your preprocessing function, include the `audio` column to ensure you're actually resampling the audio data:

```py
>>> def prepare_dataset(batch):
...     audio = batch["audio"]
...     batch["input_values"] = processor(audio["array"], sampling_rate=audio["sampling_rate"]).input_values[0]
...     batch["input_length"] = len(batch["input_values"])
...     with processor.as_target_processor():
...         batch["labels"] = processor(batch["sentence"]).input_ids
...     return batch
>>> dataset = dataset.map(prepare_dataset, remove_columns=dataset.column_names)
```
