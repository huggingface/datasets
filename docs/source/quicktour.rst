Quick tour
==========

Let's have a quick look at the 🤗nlp library features. The library provide datasets and metrics for Natural Language Processing (NLP) that can be efficiently explored and processed. It also provides methods to create a dataset from raw files or in-memory data either to process or explore it using the efficient methods providing by 🤗nlp or to upload it on HuggingFace dataset and metrics Hub in order to share it with the community.

Let's list all the provided datasets using :obj:``list_datasets``:

.. code-block::

    >>> from nlp import list_datasets, load_dataset

    >>> datasets_list = list_datasets()
    >>> len(datasets_list)
    136
    >>> print(', '.join(dataset.id for dataset in datasets_list))
    aeslc, ag_news, ai2_arc, allocine, anli, arcd, art, billsum, blended_skill_talk, blimp, blog_authorship_corpus, bookcorpus, boolq, break_data, c4, cfq, civil_comments, cmrc2018, cnn_dailymail, coarse_discourse, com_qa, commonsense_qa, compguesswhat, coqa, cornell_movie_dialog, cos_e, cosmos_qa, crime_and_punish, csv, definite_pronoun_resolution, discofuse, docred, drop, eli5, empathetic_dialogues, eraser_multi_rc, esnli, event2Mind, fever, flores, fquad, gap, germeval_14, ghomasHudson/cqc, gigaword, glue, hansards, hellaswag, hyperpartisan_news_detection, imdb, jeopardy, json, k-halid/ar, kor_nli, lc_quad, lhoestq/c4, librispeech_lm, lm1b, math_dataset, math_qa, mlqa, movie_rationales, multi_news, multi_nli, multi_nli_mismatch, mwsc, natural_questions, newsroom, openbookqa, opinosis, pandas, para_crawl, pg19, piaf, qa4mre, qa_zre, qangaroo, qanta, qasc, quarel, quartz, quoref, race, reclor, reddit, reddit_tifu, rotten_tomatoes, scan, scicite, scientific_papers, scifact, sciq, scitail, sentiment140, snli, social_i_qa, squad, squad_es, squad_it, squad_v1_pt, squad_v2, squadshifts, super_glue, ted_hrlr, ted_multi, tiny_shakespeare, trivia_qa, tydiqa, ubuntu_dialogs_corpus, webis/tl_dr, wiki40b, wiki_dpr, wiki_qa, wiki_snippets, wiki_split, wikihow, wikipedia, wikisql, wikitext, winogrande, wiqa, wmt14, wmt15, wmt16, wmt17, wmt18, wmt19, wmt_t2t, wnut_17, x_stance, xcopa, xnli, xquad, xsum, xtreme, yelp_polarity

Let's load one dataset to see