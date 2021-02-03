---
---

# Dataset Card for "wikitext"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits Sample Size](#data-splits-sample-size)
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

## [Dataset Description](#dataset-description)

- **Homepage:** [https://blog.einstein.ai/the-wikitext-long-term-dependency-language-modeling-dataset/](https://blog.einstein.ai/the-wikitext-long-term-dependency-language-modeling-dataset/)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 373.28 MB
- **Size of the generated dataset:** 1072.25 MB
- **Total amount of disk used:** 1445.53 MB

### [Dataset Summary](#dataset-summary)

 The WikiText language modeling dataset is a collection of over 100 million tokens extracted from the set of verified
 Good and Featured articles on Wikipedia. The dataset is available under the Creative Commons Attribution-ShareAlike License.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### wikitext-103-raw-v1

- **Size of downloaded dataset files:** 183.09 MB
- **Size of the generated dataset:** 523.97 MB
- **Total amount of disk used:** 707.06 MB

An example of 'validation' looks as follows.
```
This example was too long and was cropped:

{
    "text": "\" The gold dollar or gold one @-@ dollar piece was a coin struck as a regular issue by the United States Bureau of the Mint from..."
}
```

#### wikitext-103-v1

- **Size of downloaded dataset files:** 181.42 MB
- **Size of the generated dataset:** 522.66 MB
- **Total amount of disk used:** 704.07 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "text": "\" Senjō no Valkyria 3 : <unk> Chronicles ( Japanese : 戦場のヴァルキュリア3 , lit . Valkyria of the Battlefield 3 ) , commonly referred to..."
}
```

#### wikitext-2-raw-v1

- **Size of downloaded dataset files:** 4.50 MB
- **Size of the generated dataset:** 12.91 MB
- **Total amount of disk used:** 17.41 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "text": "\" The Sinclair Scientific Programmable was introduced in 1975 , with the same case as the Sinclair Oxford . It was larger than t..."
}
```

#### wikitext-2-v1

- **Size of downloaded dataset files:** 4.27 MB
- **Size of the generated dataset:** 12.72 MB
- **Total amount of disk used:** 16.99 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "text": "\" Senjō no Valkyria 3 : <unk> Chronicles ( Japanese : 戦場のヴァルキュリア3 , lit . Valkyria of the Battlefield 3 ) , commonly referred to..."
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### wikitext-103-raw-v1
- `text`: a `string` feature.

#### wikitext-103-v1
- `text`: a `string` feature.

#### wikitext-2-raw-v1
- `text`: a `string` feature.

#### wikitext-2-v1
- `text`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|       name        | train |validation|test|
|-------------------|------:|---------:|---:|
|wikitext-103-raw-v1|1801350|      3760|4358|
|wikitext-103-v1    |1801350|      3760|4358|
|wikitext-2-raw-v1  |  36718|      3760|4358|
|wikitext-2-v1      |  36718|      3760|4358|

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Source Data](#source-data)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Annotations](#annotations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Other Known Limitations](#other-known-limitations)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Additional Information](#additional-information)

### [Dataset Curators](#dataset-curators)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Licensing Information](#licensing-information)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Citation Information](#citation-information)

```
@InProceedings{wikitext,
    author={Stephen, Merity and Caiming ,Xiong and James, Bradbury and Richard Socher}
    year=2016
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@lewtun](https://github.com/lewtun), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.