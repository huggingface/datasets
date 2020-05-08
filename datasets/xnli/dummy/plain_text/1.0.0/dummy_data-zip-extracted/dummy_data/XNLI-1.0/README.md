This folder contains the "Cross-lingual Natural Language Inference" (XNLI) data.
XNLI consists of dev and test sets for the MNLI task, in 15 languages:

ar: Arabic
bg: Bulgarian
de: German
el: Greek
en: English
es: Spanish
fr: French
hi: Hindi
ru: Russian
sw: Swahili
th: Thai
tr: Turkish
ur: Urdu
vi: Vietnamese
zh: Chinese (Simplified)

Please consider citing [1] if using this dataset:

@InProceedings{conneau2018xnli,
  author =  "Conneau, Alexis
                  and Rinott, Ruty
                  and Lample, Guillaume
                  and Williams, Adina
                  and Bowman, Samuel R.
                  and Schwenk, Holger
                  and Stoyanov, Veselin",
  title =   "XNLI: Evaluating Cross-lingual Sentence Representations",
  booktitle =   "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
  year =    "2018",
  publisher =   "Association for Computational Linguistics",
  location =    "Brussels, Belgium",
}

** The XNLI corpus (XNLI-1.0.zip) **
The files xnli.dev.{tsv,jsonl} and xnli.test.{tsv,jsonl} contain the dev and test sets of the 15 languages of XNLI. Each language has 2490 dev samples and 5010 test samples.
If you plan to report results publicly, you should not use the test set for tuning, early stopping, or model selection.

The format follows that of MultiNLI [2], with additional columns for tokenized text. We use the MOSES tokenizer [3] for all languages, falling back to the default English tokenizer when necessary, except for Chinese where we used the Stanford `pku` segmenter. Some columns are deliberately left empty.
These dev and test sets are new, and are not derived from the dev and test sets of MultiNLI.
XNLI was created using professional translators who translated the new English dev and test sets.

** Machine Translation Baselines (XNLI-MT-1.0.zip) **
We provide machine-translated data for people to reproduce the MT baselines of the XNLI paper.
The XNLI-MT-1.0/XNLI subfolder corresponds to the XNLI dev/test data where the premise and hypothesis in $lg have been translated automatically to English.
These datasets are used in the "test-translation" baseline of the XNLI paper.
The XNLI-MT-1.0/multiNLI subfolder contains neural machine-translation of multiNLI training data to $lg.
These datasets are used in the "train-translation" baseline of the XNLI paper.

** References  **
[2] Adina Williams, Nikita Nangia, and Samuel R. Bowman. 2017. A broad-coverage challenge corpus for sentence understanding through inference. In NAACL.
[3] Koehn P., H. Hoang, A. Birch, C. Callison-Burch, M. Federico, N. Bertoldi, B. Cowan, W. Shen, C. Moran, R. Zens, C. Dyer, O. Bojar, A. Constantin, E. Herbst, Moses: Open
    Source Toolkit for Statistical Machine Translation. In ACL07. (2007)
[4] https://nlp.stanford.edu/software/segmenter.shtml
