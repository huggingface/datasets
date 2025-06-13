---
dataset_info:
  features:
  - name: tokens
    list: string
  - name: ner_tags
    list:
      class_label:
        names:
          '0': O
          '1': B-PER
          '2': I-PER
          '3': B-ORG
          '4': I-ORG
          '5': B-LOC
          '6': I-LOC
  - name: langs
    list: string
  - name: spans
    list: string
  splits:
  - name: train
    num_bytes: 2351563
    num_examples: 10000
  - name: validation
    num_bytes: 238418
    num_examples: 1000
  download_size: 3940680
  dataset_size: 2589981
---
