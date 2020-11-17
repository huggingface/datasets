Quick tour
==========

Let's have a quick look at the 🤗datasets library. This library has three main features:

- It provides a very **efficient way to load and process data** from raw files (CSV/JSON/text) or in-memory data (python dict, pandas dataframe) with a special focus on memory efficiency and speed. As a matter of example, loading a 18GB dataset like English Wikipedia allocate 9 MB in RAM and you can iterate over the dataset at 1-2 GBit/s in python.
- It provides a very **simple way to access and share datasets** with the research and practitioner communities (over 130 NLP datasets are already accessible in one line with the library as we'll see below).
- It was designed with a particular focus on interoperabilty with frameworks like **pandas, NumPy, PyTorch and TensorFlow**.

🤗datasets provides datasets for many NLP tasks like text classification, question answering, language modeling, etc and obviously these datasets can always be used to other tasks than their originally assigned task. Let's list all the currently provided datasets using :func:`datasets.list_datasets`:

.. code-block::

    >>> from datasets import list_datasets
    >>> datasets_list = list_datasets()
    >>> len(datasets_list)
    136
    >>> print(', '.join(dataset.id for dataset in datasets_list))
    aeslc, ag_news, ai2_arc, allocine, anli, arcd, art, billsum, blended_skill_talk, blimp, blog_authorship_corpus, bookcorpus, boolq, break_data,
    c4, cfq, civil_comments, cmrc2018, cnn_dailymail, coarse_discourse, com_qa, commonsense_qa, compguesswhat, coqa, cornell_movie_dialog, cos_e, 
    cosmos_qa, crime_and_punish, csv, definite_pronoun_resolution, discofuse, docred, drop, eli5, empathetic_dialogues, eraser_multi_rc, esnli, 
    event2Mind, fever, flores, fquad, gap, germeval_14, ghomasHudson/cqc, gigaword, glue, hansards, hellaswag, hyperpartisan_news_detection, 
    imdb, jeopardy, json, k-halid/ar, kor_nli, lc_quad, lhoestq/c4, librispeech_lm, lm1b, math_dataset, math_qa, mlqa, movie_rationales, 
    multi_news, multi_nli, multi_nli_mismatch, mwsc, natural_questions, newsroom, openbookqa, opinosis, pandas, para_crawl, pg19, piaf, qa4mre, 
    qa_zre, qangaroo, qanta, qasc, quarel, quartz, quoref, race, reclor, reddit, reddit_tifu, rotten_tomatoes, scan, scicite, scientific_papers, 
    scifact, sciq, scitail, sentiment140, snli, social_i_qa, squad, squad_es, squad_it, squad_v1_pt, squad_v2, squadshifts, super_glue, ted_hrlr, 
    ted_multi, tiny_shakespeare, trivia_qa, tydiqa, ubuntu_dialogs_corpus, webis/tl_dr, wiki40b, wiki_dpr, wiki_qa, wiki_snippets, wiki_split, 
    wikihow, wikipedia, wikisql, wikitext, winogrande, wiqa, wmt14, wmt15, wmt16, wmt17, wmt18, wmt19, wmt_t2t, wnut_17, x_stance, xcopa, xnli, 
    xquad, xsum, xtreme, yelp_polarity

All these datasets can also be browsed on the `HuggingFace Hub <https://huggingface.co/datasets>`__ and can be viewed and explored online with the `🤗datasets viewer <https://huggingface.co/nlp/viewer/>`__.

Loading a dataset
--------------------

Now let's load a simple dataset for classification, we'll use the MRPC dataset provided in the GLUE banchmark which is small enough for quick prototyping. You can explore this dataset and read more details `on the online viewer here <https://huggingface.co/nlp/viewer/?dataset=glue&config=mrpc>`__:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('glue', 'mrpc', split='train')

When typing this command for the first time, a processing script called a ``builder`` which is in charge of loading the MRPC/GLUE dataset will be downloaded, cached and imported. Then the dataset files themselves are downloaded and cached (usually from the original dataset URLs) and are processed to return a :class:`datasets.Dataset` comprising the training split of MRPC/GLUE as requested here.

If you want to create a :class:`datasets.Dataset` from local CSV, JSON, text or pandas files instead of a community provided dataset, you can use one of the ``csv``, ``json``, ``text`` or ``pandas`` builder. They all accept a variety of file paths as inputs: a path to a single file, a list of paths to files or a dict of paths to files for each split. Here are some examples to load from CSV files:

.. code-block::

    >>> from datasets import load_dataset
    >>> dataset = load_dataset('csv', data_files='my_file.csv')
    >>> dataset = load_dataset('csv', data_files=['my_file_1.csv', 'my_file_2.csv', 'my_file_3.csv'])
    >>> dataset = load_dataset('csv', data_files={'train': ['my_train_file_1.csv', 'my_train_file_2.csv'], 
    >>>                                           'test': 'my_test_file.csv'})

.. note::

    If you don't provide a :obj:`split` argument to :func:`datasets.load_dataset`, this method will return a dictionary containing a datasets for each split in the dataset. This dictionary is a :obj:`datasets.DatasetDict` object that lets you process all the splits at once using :func:`datasets.DatasetDict.map`, :func:`datasets.DatasetDict.filter`, etc.

Now let's have a look at our newly created :class:`datasets.Dataset` object. It basically behaves like a normal python container. You can query its length, get a single row but also get multiple rows and even index along columns (see all the details in :doc:`exploring </exploring>`):

.. code-block::

    >>> len(dataset)
    3668
    >>> dataset[0]
    {'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
     'label': 1,
     'idx': 0}

A lot of metadata are available in the dataset attributes (description, citation, split sizes, etc) and we'll dive in this in the :doc:`exploring </exploring>` page.
We'll just say here that :class:`datasets.Dataset` have columns which are typed with types which can be arbitrarily nested complex types (e.g. list of strings or list of lists of int64 values).

Let's take a look at the column in our dataset by printing its :func:`datasets.Dataset.features`:

.. code-block::

    >>> dataset.features
    {'idx': Value(dtype='int32', id=None),
     'label': ClassLabel(num_classes=2, names=['not_equivalent', 'equivalent'], names_file=None, id=None),
     'sentence1': Value(dtype='string', id=None),
     'sentence2': Value(dtype='string', id=None)}

Fine-tuning a deep-learning model
------------------------------------------

In the rest of this quick-tour we will use this dataset to fine-tune a Bert model on the sentence pair classification task of Paraphrase Classification. Let's have a quick look at our task.

As you can see from the above features, the labels are a :class:`datasets.ClassLabel` instance with two classes: ``not_equivalent`` and ``equivalent``. 

We can print one example of each class using :func:`datasets.Dataset.filter` and a name-to-integer conversion method of the feature :class:`datasets.ClassLabel` called :func:`datasets.ClassLabel.str2int` (that we detail these methods in :doc:`processing </processing>` and :doc:`exploring </exploring>`):

.. code-block::

    >>> dataset.filter(lambda example: example['label'] == dataset.features['label'].str2int('equivalent'))[0]
    {'idx': 0,
     'label': 1,
     'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .'
    }
    >>> dataset.filter(lambda example: example['label'] == dataset.features['label'].str2int('not_equivalent'))[0]
    {'idx': 1,
     'label': 0,
     'sentence1': "Yucaipa owned Dominick 's before selling the chain to Safeway in 1998 for $ 2.5 billion .",
     'sentence2': "Yucaipa bought Dominick 's in 1995 for $ 693 million and sold it to Safeway for $ 1.8 billion in 1998 ."
    }

Now our goal will be to train a model which can predict the correct label (``not_equivalent`` or ``equivalent``) from a pair of sentence.

Let's import a pretrained Bert model and its tokenizer using 🤗transformers.

.. code-block::

    >>> ## PYTORCH CODE
    >>> from transformers import AutoModelForSequenceClassification, AutoTokenizer
    >>> model = AutoModelForSequenceClassification.from_pretrained('bert-base-cased')
    Some weights of the model checkpoint at bert-base-cased were not used when initializing BertForSequenceClassification: ['cls.predictions.bias', 'cls.predictions.transform.dense.weight', 'cls.predictions.transform.dense.bias', 'cls.predictions.decoder.weight', 'cls.seq_relationship.weight', 'cls.seq_relationship.bias', 'cls.predictions.transform.LayerNorm.weight', 'cls.predictions.transform.LayerNorm.bias']
    - This IS expected if you are initializing BertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPretraining model).
    - This IS NOT expected if you are initializing BertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of BertForSequenceClassification were not initialized from the model checkpoint at bert-base-cased and are newly initialized: ['classifier.weight', 'classifier.bias']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    >>> tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')
    >>> ## TENSORFLOW CODE
    >>> from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
    >>> model = TFAutoModelForSequenceClassification.from_pretrained("bert-base-cased")
    Some weights of the model checkpoint at bert-base-cased were not used when initializing TFBertForSequenceClassification: ['nsp___cls', 'mlm___cls']
    - This IS expected if you are initializing TFBertForSequenceClassification from the checkpoint of a model trained on another task or with another architecture (e.g. initializing a BertForSequenceClassification model from a BertForPretraining model).
    - This IS NOT expected if you are initializing TFBertForSequenceClassification from the checkpoint of a model that you expect to be exactly identical (initializing a BertForSequenceClassification model from a BertForSequenceClassification model).
    Some weights of TFBertForSequenceClassification were not initialized from the model checkpoint at bert-base-cased and are newly initialized: ['dropout_37', 'classifier']
    You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
    >>> tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

🤗transformers warns us that we should probably train this model on a downstream task before using it which is exactly what we are going to do.
If you want more details on the models and tokenizers of 🤗transformers, you should refer to the documentation and tutorials of this library `which are available here <https://huggingface.co/transformers/>`__.

Tokenizing the dataset
^^^^^^^^^^^^^^^^^^^^^^

The first step is to tokenize our sentences in order to build sequences of integers that our model can digest from the pairs of sequences. Bert's tokenizer knows how to do that and we can simply feed it with a pair of sentences as inputs to generate the right inputs for our model:

.. code-block::

    >>> print(tokenizer(dataset[0]['sentence1'], dataset[0]['sentence2']))
    {'input_ids': [101, 7277, 2180, 5303, 4806, 1117, 1711, 117, 2292, 1119, 1270, 107, 1103, 7737, 107, 117, 1104, 9938, 4267, 12223, 21811, 1117, 2554, 119, 102, 11336, 6732, 3384, 1106, 1140, 1112, 1178, 107, 1103, 7737, 107, 117, 7277, 2180, 5303, 4806, 1117, 1711, 1104, 9938, 4267, 12223, 21811, 1117, 2554, 119, 102],
     'token_type_ids': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    >>> tokenizer.decode(tokenizer(dataset[0]['sentence1'], dataset[0]['sentence2'])['input_ids'])
    '[CLS] Amrozi accused his brother, whom he called " the witness ", of deliberately distorting his evidence. [SEP] Referring to him as only " the witness ", Amrozi accused his brother of deliberately distorting his evidence. [SEP]'

As you can see, the tokenizer has merged the pair of sequences in a single input separating them by some special tokens ``[CLS]`` and ``[SEP]`` expected by Bert. For more details on this, you can refer to `🤗transformers's documentation on data processing <https://huggingface.co/transformers/preprocessing.html#preprocessing-pairs-of-sentences>`__.

In our case, we want to tokenize our full dataset, so we will use a method called :func:`datasets.Dataset.map` to apply the encoding process to their whole dataset.
To be sure we can easily build tensors batches for our model, we will truncate and pad the inputs to the max length of our model.

.. code-block::

    >>> def encode(examples):
    >>>     return tokenizer(examples['sentence1'], examples['sentence2'], truncation=True, padding='max_length')
    >>>
    >>> dataset = dataset.map(encode, batched=True)
    100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:02<00:00,  1.75it/s]
    >>> dataset[0]
    {'sentence1': 'Amrozi accused his brother , whom he called " the witness " , of deliberately distorting his evidence .',
     'sentence2': 'Referring to him as only " the witness " , Amrozi accused his brother of deliberately distorting his evidence .',
     'label': 1,
     'idx': 0,
     'input_ids': array([  101,  7277,  2180,  5303,  4806,  1117,  1711,   117,  2292, 1119,  1270,   107,  1103,  7737,   107,   117,  1104,  9938, 4267, 12223, 21811,  1117,  2554,   119,   102, 11336,  6732, 3384,  1106,  1140,  1112,  1178,   107,  1103,  7737,   107, 117,  7277,  2180,  5303,  4806,  1117,  1711,  1104,  9938, 4267, 12223, 21811,  1117,  2554,   119,   102]),
     'token_type_ids': array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
     'attention_mask': array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])}

This operation has added three new columns to our dataset: ``input_ids``, ``token_type_ids`` and ``attention_mask``. These are the inputs our model need for training.

.. note::

    Note that this is not the most efficient padding strategy, we could also avoid padding at this stage and use ``tokenizer.pad`` as the ``collate_fn`` method in the ``torch.utils.data.DataLoader`` further below.

Formatting the dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have encoded our dataset, we want to use it in a ``torch.Dataloader`` or a ``tf.data.Dataset`` and use it to train our model.

To be able to train our model with this dataset and PyTorch, we will need to do three modifications:

- rename our ``label`` column in ``labels`` which is the expected input name for labels in `BertForSequenceClassification <https://huggingface.co/transformers/model_doc/bert.html?#transformers.BertForSequenceClassification.forward>`__ or `TFBertForSequenceClassification <https://huggingface.co/transformers/model_doc/bert.html?#tfbertforsequenceclassification>`__,
- get pytorch (or tensorflow) tensors out of our :class:`datasets.Dataset`, instead of python objects, and
- filter the columns to return only the subset of the columns that we need for our model inputs (``input_ids``, ``token_type_ids`` and ``attention_mask``).

.. note::

    We don't want the columns `sentence1` or `sentence2` as inputs to train our model, but we could still want to keep them in the dataset, for instance for the evaluation of the model. 🤗datasets let you control the output format of :func:`datasets.Dataset.__getitem__` to just mask them as detailed in :doc:`exploring <./exploring>`.

The first modification is just a matter of renaming the column as follow (we could have done it during the tokenization process as well:

.. code-block::

    >>> dataset = dataset.map(lambda examples: {'labels': examples['label']}, batched=True)

The two other modifications can be handled by the :func:`datasets.Dataset.set_format` method which will convert, on the fly, the returned output from :func:`datasets.Dataset.__getitem__` to filter the unwanted columns and convert python objects in PyTorch tensors.

Here is how we can apply the right format to our dataset using :func:`datasets.Dataset.set_format` and wrap it in a ``torch.utils.data.DataLoader`` or a ``tf.data.Dataset``:

.. code-block::

    >>> ## PYTORCH CODE
    >>> import torch
    >>> dataset.set_format(type='torch', columns=['input_ids', 'token_type_ids', 'attention_mask', 'labels'])
    >>> dataloader = torch.utils.data.DataLoader(dataset, batch_size=32)
    >>> next(iter(dataloader))
    {'attention_mask': tensor([[1, 1, 1,  ..., 0, 0, 0],
                               [1, 1, 1,  ..., 0, 0, 0],
                               [1, 1, 1,  ..., 0, 0, 0],
                               ...,
                               [1, 1, 1,  ..., 0, 0, 0],
                               [1, 1, 1,  ..., 0, 0, 0],
                               [1, 1, 1,  ..., 0, 0, 0]]),
    'input_ids': tensor([[  101,  7277,  2180,  ...,     0,     0,     0],
                         [  101, 10684,  2599,  ...,     0,     0,     0],
                         [  101,  1220,  1125,  ...,     0,     0,     0],
                         ...,
                         [  101, 16944,  1107,  ...,     0,     0,     0],
                         [  101,  1109, 11896,  ...,     0,     0,     0],
                         [  101,  1109,  4173,  ...,     0,     0,     0]]),
    'label': tensor([1, 0, 1, 0, 1, 1, 0, 1]),
    'token_type_ids': tensor([[0, 0, 0,  ..., 0, 0, 0],
                              [0, 0, 0,  ..., 0, 0, 0],
                              [0, 0, 0,  ..., 0, 0, 0],
                              ...,
                              [0, 0, 0,  ..., 0, 0, 0],
                              [0, 0, 0,  ..., 0, 0, 0],
                              [0, 0, 0,  ..., 0, 0, 0]])}
    >>> ## TENSORFLOW CODE
    >>> import tensorflow as tf
    >>> dataset.set_format(type='tensorflow', columns=['input_ids', 'token_type_ids', 'attention_mask', 'labels'])
    >>> features = {x: dataset[x].to_tensor(default_value=0, shape=[None, tokenizer.max_len]) for x in ['input_ids', 'token_type_ids', 'attention_mask']}
    >>> tfdataset = tf.data.Dataset.from_tensor_slices((features, dataset["labels"])).batch(32)
    >>> next(iter(tfdataset))
    ({'input_ids': <tf.Tensor: shape=(32, 512), dtype=int32, numpy=
    array([[  101,  7277,  2180, ...,     0,     0,     0],
           [  101, 10684,  2599, ...,     0,     0,     0],
           [  101,  1220,  1125, ...,     0,     0,     0],
           ...,
           [  101,  1109,  2026, ...,     0,     0,     0],
           [  101, 22263,  1107, ...,     0,     0,     0],
           [  101,   142,  1813, ...,     0,     0,     0]], dtype=int32)>, 'token_type_ids': <tf.Tensor: shape=(32, 512), dtype=int32, numpy=
    array([[0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           ...,
           [0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0],
           [0, 0, 0, ..., 0, 0, 0]], dtype=int32)>, 'attention_mask': <tf.Tensor: shape=(32, 512), dtype=int32, numpy=
    array([[1, 1, 1, ..., 0, 0, 0],
           [1, 1, 1, ..., 0, 0, 0],
           [1, 1, 1, ..., 0, 0, 0],
           ...,
           [1, 1, 1, ..., 0, 0, 0],
           [1, 1, 1, ..., 0, 0, 0],
           [1, 1, 1, ..., 0, 0, 0]], dtype=int32)>}, <tf.Tensor: shape=(32,), dtype=int64, numpy=
    array([1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1,
           0, 1, 1, 1, 0, 0, 1, 1, 1, 0])>)


We are now ready to train our model. Let's write a simple training loop and a start the training

.. code-block::

    >>> ## PYTORCH CODE
    >>> from tqdm import tqdm
    >>> device = 'cuda' if torch.cuda.is_available() else 'cpu' 
    >>> model.train().to(device)
    >>> optimizer = torch.optim.AdamW(params=model.parameters(), lr=1e-5)
    >>> for epoch in range(3):
    >>>     for i, batch in enumerate(tqdm(dataloader)):
    >>>         batch = {k: v.to(device) for k, v in batch.items()}
    >>>         outputs = model(**batch)
    >>>         loss = outputs[0]
    >>>         loss.backward()
    >>>         optimizer.step()
    >>>         optimizer.zero_grad()
    >>>         if i % 10 == 0:
    >>>             print(f"loss: {loss}")
    >>> ## TENSORFLOW CODE
    >>> loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(reduction=tf.keras.losses.Reduction.NONE, from_logits=True)
    >>> opt = tf.keras.optimizers.Adam(learning_rate=3e-5)
    >>> model.compile(optimizer=opt, loss=loss_fn, metrics=["accuracy"])
    >>> model.fit(tfdataset, epochs=3)


Now this was a very simple tour, you should continue with either the detailled notebook which is `here <https://colab.research.google.com/github/huggingface/datasets/blob/master/notebooks/Overview.ipynb#scrollTo=my95uHbLyjwR>`__ or the in-depth guides on

- :doc:`loading datasets <./loading_datasets>`
- :doc:`exploring the dataset object attributes <./exploring>`
- :doc:`processing dataset data <./processing>`
- :doc:`indexing a dataset with FAISS or Elastic Search <./faiss_and_ea>`
- :doc:`Adding new datasets <./add_dataset>`
- :doc:`Sharing datasets <./share_dataset>`
