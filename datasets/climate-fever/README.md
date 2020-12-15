---
annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- found
languages:
- en
licenses: []
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets: []
task_categories:
- text-classification
- text-retrieval
- text-scoring
task_ids:
- fact-checking
- fact-checking-retrieval
- semantic-similarity-scoring
---

# Dataset Card for [Dataset Name]

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Languages](#languages)
- [Additional Information](#additional-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** <http://climatefever.ai>
- **Repository:** <https://github.com/tdiggelm/climate-fever-dataset>
- **Paper:**: <https://arxiv.org/abs/2012.00614>
- **Point of Contact:** Thomas Diggelmann <thomasdi@student.ethz.ch>

### Dataset Summary

A dataset adopting the FEVER methodology that consists of 1,535 real-world claims regarding climate-change collected on the internet. Each claim is accompanied by five manually annotated evidence sentences retrieved from the English Wikipedia that support, refute or do not give enough information to validate the claim totalling in 7,675 claim-evidence pairs. The dataset features challenging claims that relate multiple facets and disputed cases of claims where both supporting and refuting evidence are present.

### Languages

- en (English)

## Additional Information

### Citation Information

```bibtex
@misc{diggelmann2020climatefever,
      title={CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims},
      author={Thomas Diggelmann and Jordan Boyd-Graber and Jannis Bulian and Massimiliano Ciaramita and Markus Leippold},
      year={2020},
      eprint={2012.00614},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
