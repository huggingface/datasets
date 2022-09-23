---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
- token-classification
- text-classification
task_ids:
- named-entity-recognition
- slot-filling
- topic-classification
paperswithcode_id: null
pretty_name: SofcMaterialsArticles
dataset_info:
  features:
  - name: text
    dtype: string
  - name: sentence_offsets
    sequence:
    - name: begin_char_offset
      dtype: int64
    - name: end_char_offset
      dtype: int64
  - name: sentences
    sequence: string
  - name: sentence_labels
    sequence: int64
  - name: token_offsets
    sequence:
    - name: offsets
      sequence:
      - name: begin_char_offset
        dtype: int64
      - name: end_char_offset
        dtype: int64
  - name: tokens
    sequence:
      sequence: string
  - name: entity_labels
    sequence:
      sequence:
        class_label:
          names:
            0: B-DEVICE
            1: B-EXPERIMENT
            2: B-MATERIAL
            3: B-VALUE
            4: I-DEVICE
            5: I-EXPERIMENT
            6: I-MATERIAL
            7: I-VALUE
            8: O
  - name: slot_labels
    sequence:
      sequence:
        class_label:
          names:
            0: B-anode_material
            1: B-cathode_material
            2: B-conductivity
            3: B-current_density
            4: B-degradation_rate
            5: B-device
            6: B-electrolyte_material
            7: B-experiment_evoking_word
            8: B-fuel_used
            9: B-interlayer_material
            10: B-interconnect_material
            11: B-open_circuit_voltage
            12: B-power_density
            13: B-resistance
            14: B-support_material
            15: B-thickness
            16: B-time_of_operation
            17: B-voltage
            18: B-working_temperature
            19: I-anode_material
            20: I-cathode_material
            21: I-conductivity
            22: I-current_density
            23: I-degradation_rate
            24: I-device
            25: I-electrolyte_material
            26: I-experiment_evoking_word
            27: I-fuel_used
            28: I-interlayer_material
            29: I-interconnect_material
            30: I-open_circuit_voltage
            31: I-power_density
            32: I-resistance
            33: I-support_material
            34: I-thickness
            35: I-time_of_operation
            36: I-voltage
            37: I-working_temperature
            38: O
  - name: links
    sequence:
    - name: relation_label
      dtype:
        class_label:
          names:
            0: coreference
            1: experiment_variation
            2: same_experiment
            3: thickness
    - name: start_span_id
      dtype: int64
    - name: end_span_id
      dtype: int64
  - name: slots
    sequence:
    - name: frame_participant_label
      dtype:
        class_label:
          names:
            0: anode_material
            1: cathode_material
            2: current_density
            3: degradation_rate
            4: device
            5: electrolyte_material
            6: fuel_used
            7: interlayer_material
            8: open_circuit_voltage
            9: power_density
            10: resistance
            11: support_material
            12: time_of_operation
            13: voltage
            14: working_temperature
    - name: slot_id
      dtype: int64
  - name: spans
    sequence:
    - name: span_id
      dtype: int64
    - name: entity_label
      dtype:
        class_label:
          names:
            0: ''
            1: DEVICE
            2: MATERIAL
            3: VALUE
    - name: sentence_id
      dtype: int64
    - name: experiment_mention_type
      dtype:
        class_label:
          names:
            0: ''
            1: current_exp
            2: future_work
            3: general_info
            4: previous_work
    - name: begin_char_offset
      dtype: int64
    - name: end_char_offset
      dtype: int64
  - name: experiments
    sequence:
    - name: experiment_id
      dtype: int64
    - name: span_id
      dtype: int64
    - name: slots
      sequence:
      - name: frame_participant_label
        dtype:
          class_label:
            names:
              0: anode_material
              1: cathode_material
              2: current_density
              3: degradation_rate
              4: conductivity
              5: device
              6: electrolyte_material
              7: fuel_used
              8: interlayer_material
              9: open_circuit_voltage
              10: power_density
              11: resistance
              12: support_material
              13: time_of_operation
              14: voltage
              15: working_temperature
      - name: slot_id
        dtype: int64
  splits:
  - name: test
    num_bytes: 2650700
    num_examples: 11
  - name: train
    num_bytes: 7402373
    num_examples: 26
  - name: validation
    num_bytes: 1993857
    num_examples: 8
  download_size: 3733137
  dataset_size: 12046930
---


# Dataset Card for SofcMaterialsArticles

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:**  [boschresearch/sofc-exp_textmining_resources](https://github.com/boschresearch/sofc-exp_textmining_resources)
- **Repository:** [boschresearch/sofc-exp_textmining_resources](https://github.com/boschresearch/sofc-exp_textmining_resources)
- **Paper:** [The SOFC-Exp Corpus and Neural Approaches to Information Extraction in the Materials Science Domain](https://arxiv.org/abs/2006.03039)
- **Leaderboard:**
- **Point of Contact:** [Annemarie Friedrich](annemarie.friedrich@de.bosch.com)

### Dataset Summary

> The SOFC-Exp corpus contains 45 scientific publications about solid oxide fuel cells (SOFCs), published between 2013 and 2019 as open-access articles all with a CC-BY license. The dataset was manually annotated by domain experts with the following information:
> 
> * Mentions of relevant experiments have been marked using a graph structure corresponding to instances of an Experiment frame (similar to the ones used in FrameNet.) We assume that an Experiment frame is introduced to the discourse by mentions of words such as report, test or measure (also called the frame-evoking elements). The nodes corresponding to the respective tokens are the heads of the graphs representing the Experiment frame.
> * The Experiment frame related to SOFC-Experiments defines a set of 16 possible participant slots. Participants are annotated as dependents of links between the frame-evoking element and the participant node.
> * In addition, we provide coarse-grained entity/concept types for all frame participants, i.e, MATERIAL, VALUE or DEVICE. Note that this annotation has not been performed on the full texts but only on sentences containing information about relevant experiments, and a few sentences in addition. In the paper, we run experiments for both tasks only on the set of sentences marked as experiment-describing in the gold standard, which is admittedly a slightly simplified setting. Entity types are only partially annotated on other sentences. Slot filling could of course also be evaluated in a fully automatic setting with automatic experiment sentence detection as a first step.

### Supported Tasks and Leaderboards

- `topic-classification`: The dataset can be used to train a model for topic-classification, to identify sentences that mention SOFC-related experiments. 
- `named-entity-recognition`: The dataset can be used to train a named entity recognition model to detect `MATERIAL`, `VALUE`, `DEVICE`, and `EXPERIMENT` entities. 
- `slot-filling`: The slot-filling task is approached as fine-grained entity-typing-in-context, assuming that each sentence represents a single experiment frame. Sequence tagging architectures are utilized for tagging the tokens of each experiment-describing sentence with the set of slot types.


The paper experiments with BiLSTM architectures with `BERT`- and `SciBERT`- generated token embeddings, as well as with `BERT` and `SciBERT` directly for the modeling task. A simple CRF architecture is used as a baseline for sequence-tagging tasks. Implementations of the transformer-based architectures can be found in the `huggingface/transformers` library: [BERT](https://huggingface.co/bert-base-uncased), [SciBERT](https://huggingface.co/allenai/scibert_scivocab_uncased)

### Languages

This corpus is in English. 

## Dataset Structure

### Data Instances

As each example is a full text of an academic paper, plus annotations, a json formatted example is space-prohibitive for this README. 

### Data Fields

- `text`: The full text of the paper
- `sentence_offsets`: Start and end character offsets for each sentence in the text. 
  - `begin_char_offset`: a `int64` feature.
  - `end_char_offset`: a `int64` feature.
- `sentences`: A sequence of the sentences in the text (using `sentence_offsets`)
- `sentence_labels`: Sequence of binary labels for whether a sentence contains information of interest.
- `token_offsets`: Sequence of sequences containing start and end character offsets for each token in each sentence in the text. 
  - `offsets`: a dictionary feature containing:
    - `begin_char_offset`: a `int64` feature.
    - `end_char_offset`: a `int64` feature.
- `tokens`: Sequence of sequences containing the tokens for each sentence in the text.
  - `feature`: a `string` feature.
- `entity_labels`: a dictionary feature containing:
  - `feature`: a classification label, with possible values including `B-DEVICE`, `B-EXPERIMENT`, `B-MATERIAL`, `B-VALUE`, `I-DEVICE`.
- `slot_labels`: a dictionary feature containing:
  - `feature`: a classification label, with possible values including `B-anode_material`, `B-cathode_material`, `B-conductivity`, `B-current_density`, `B-degradation_rate`.
- `links`: a dictionary feature containing:
  - `relation_label`: a classification label, with possible values including `coreference`, `experiment_variation`, `same_experiment`, `thickness`.
  - `start_span_id`: a `int64` feature.
  - `end_span_id`: a `int64` feature.
- `slots`: a dictionary feature containing:
  - `frame_participant_label`: a classification label, with possible values including `anode_material`, `cathode_material`, `current_density`, `degradation_rate`, `device`.
  - `slot_id`: a `int64` feature.
- `spans`: a dictionary feature containing:
  - `span_id`: a `int64` feature.
  - `entity_label`: a classification label, with possible values including ``, `DEVICE`, `MATERIAL`, `VALUE`.
  - `sentence_id`: a `int64` feature.
  - `experiment_mention_type`: a classification label, with possible values including ``, `current_exp`, `future_work`, `general_info`, `previous_work`.
  - `begin_char_offset`: a `int64` feature.
  - `end_char_offset`: a `int64` feature.
- `experiments`: a dictionary feature containing:
  - `experiment_id`: a `int64` feature.
  - `span_id`: a `int64` feature.
  - `slots`: a dictionary feature containing:
    - `frame_participant_label`: a classification label, with possible values including `anode_material`, `cathode_material`, `current_density`, `degradation_rate`, `conductivity`.
    - `slot_id`: a `int64` feature.

Very detailed information for each of the fields can be found in the [corpus file formats section](https://github.com/boschresearch/sofc-exp_textmining_resources#corpus-file-formats) of the associated dataset repo

### Data Splits

This dataset consists of three splits:

|                            | Train  | Valid | Test |
| -----                      | ------ | ----- | ---- |
| Input Examples             |  26    |   8   |  11  |


The authors propose the experimental setting of using the training data in a 5-fold cross validation setting for development and tuning, and finally applying tte model(s) to the independent test set.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

The corpus consists of 45
open-access scientific publications about SOFCs
and related research, annotated by domain experts.

### Annotations

#### Annotation process

For manual annotation, the authors use the InCeption annotation tool (Klie et al., 2018).

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]
## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

[More Information Needed]

### Licensing Information

The manual annotations created for the SOFC-Exp corpus are licensed under a [Creative Commons Attribution 4.0 International License (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/).

### Citation Information

```
@misc{friedrich2020sofcexp,
      title={The SOFC-Exp Corpus and Neural Approaches to Information Extraction in the Materials Science Domain},
      author={Annemarie Friedrich and Heike Adel and Federico Tomazic and Johannes Hingerl and Renou Benteau and Anika Maruscyk and Lukas Lange},
      year={2020},
      eprint={2006.03039},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

### Contributions

Thanks to [@ZacharySBrown](https://github.com/ZacharySBrown) for adding this dataset.