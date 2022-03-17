---
pretty_name: Adversarial GLUE
languages:
- en
paperswithcode_id: adversarial-glue-a-multi-task-benchmark-for
---

# Dataset Card for Adversarial GLUE

## Dataset Description

- **Homepage:**  https://adversarialglue.github.io/
- **Repository:**
- **Paper:** [arXiv](https://arxiv.org/pdf/2111.02840.pdf)
- **Leaderboard:**
- **Point of Contact:**
Adversarial GLUE Benchmark (AdvGLUE) is a comprehensive robustness evaluation benchmark that focuses on the adversarial robustness evaluation of language models. It covers five natural language understanding tasks from the famous GLUE tasks and is an adversarial version of GLUE benchmark.

AdvGLUE considers textual adversarial attacks from different perspectives and hierarchies, including word-level transformations, sentence-level manipulations, and human-written adversarial examples, which provide comprehensive coverage of various adversarial linguistic phenomena.

### Supported Tasks and Leaderboards

Leaderboard available on the homepage: [https://adversarialglue.github.io/](https://adversarialglue.github.io/).

### Languages

AdvGLUE deviates from the GLUE dataset, which has a base language of English.
## Dataset Structure

We show detailed information for up to 5 configurations of the dataset.

### Data Instances

#### default

- **Size of downloaded dataset files:** 198 KB

### Data Fields

The data fields are the same as in the GLUE dataset, which differ by task.

### Data Splits

Adversarial GLUE provides only a 'dev' split.

### Citation Information

```
@article{Wang2021AdversarialGA,
  title={Adversarial GLUE: A Multi-Task Benchmark for Robustness Evaluation of Language Models},
  author={Boxin Wang and Chejian Xu and Shuohang Wang and Zhe Gan and Yu Cheng and Jianfeng Gao and Ahmed Hassan Awadallah and B. Li},
  journal={ArXiv},
  year={2021},
  volume={abs/2111.02840}
}
```


### Contributions

Thanks to [@jxmorris12](https://github.com/jxmorris12) for adding this dataset.