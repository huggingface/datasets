# Linguistic Probing
10 probing tasks designed to capture simple linguistic features of sentences
https://www.aclweb.org/anthology/P18-1198.pdf


annotations_creators:
- machine-generated
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
  bigram_shift:
  - 100K<n<1M
  coordination_inversion:
  - 100K<n<1M
  obj_number:
  - 10K<n<100K
  odd_man_out:
  - 100K<n<1M
  past_present:
  - 100K<n<1M
  sentence_length:
  - 100K<n<1M
  subj_number:
  - 10K<n<100K
  top_constituents:
  - 10K<n<100K
  tree_depth:
  - 100K<n<1M
  word_content:
  - 100K<n<1M
source_datasets:
- original
task_categories:
- text-classification
task_ids:
  bigram_shift:
  - text-classification-other-word order shift prediction
  coordination_inversion: []
  obj_number:
  - text-classification-other-objects number prediction
  odd_man_out:
  - text-classification-other-noun substitution prediction
  past_present:
  - text-classification-other-tense prediction
  sentence_length:
  - text-classification-other-sentence length prediction
  subj_number:
  - text-classification-other-subjects number prediction
  top_constituents:
  - text-classification-other-constituents prediction
  tree_depth:
  - text-classification-other-syntactic tree depth prediction
  word_content:
  - text-classification-other-words prediction
