---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 1M<n<10M
source_datasets:
- original
task_categories:
- text2text-generation
- text-generation
- fill-mask
- text-retrieval
- summarization
task_ids:
- document-retrieval
- entity-linking-retrieval
- explanation-generation
- language-modeling
- masked-language-modeling
paperswithcode_id: recipenlg
pretty_name: RecipeNLG
---


# Dataset Card for RecipeNLG

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

- **Homepage:** https://recipenlg.cs.put.poznan.pl/
- **Repository:** https://github.com/Glorf/recipenlg
- **Paper:** https://www.aclweb.org/anthology/volumes/2020.inlg-1/
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [More Information Needed]

### Dataset Summary

RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation.

While the RecipeNLG dataset is based on the Recipe1M+ dataset, it greatly expands the number of recipes available.
The new dataset provides over 1 million new, preprocessed and deduplicated recipes on top of the Recipe1M+ dataset.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is in English.

## Dataset Structure

### Data Instances

```
{'id': 0,
 'title': 'No-Bake Nut Cookies',
 'ingredients': ['1 c. firmly packed brown sugar',
  '1/2 c. evaporated milk',
  '1/2 tsp. vanilla',
  '1/2 c. broken nuts (pecans)',
  '2 Tbsp. butter or margarine',
  '3 1/2 c. bite size shredded rice biscuits'],
 'directions': ['In a heavy 2-quart saucepan, mix brown sugar, nuts, evaporated milk and butter or margarine.',
  'Stir over medium heat until mixture bubbles all over top.',
  'Boil and stir 5 minutes more. Take off heat.',
  'Stir in vanilla and cereal; mix well.',
  'Using 2 teaspoons, drop and shape into 30 clusters on wax paper.',
  'Let stand until firm, about 30 minutes.'],
 'link': 'www.cookbooks.com/Recipe-Details.aspx?id=44874',
 'source': 0,
 'ner': ['brown sugar',
  'milk',
  'vanilla',
  'nuts',
  'butter',
  'bite size shredded rice biscuits']}
```

### Data Fields

- `id` (`int`): ID.
- `title` (`str`): Title of the recipe.
- `ingredients` (`list` of `str`): Ingredients.
- `directions` (`list` of `str`): Instruction steps.
- `link` (`str`): URL link.
- `source` (`ClassLabel`): Origin of each recipe record, with possible value {"Gathered", "Recipes1M"}:
  - "Gathered" (0): Additional recipes gathered from multiple cooking web pages, using automated scripts in a web scraping process.
  - "Recipes1M" (1): Recipes from "Recipe1M+" dataset.
- `ner` (`list` of `str`): NER food entities.

### Data Splits

The dataset contains a single `train` split.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

### Annotations

[More Information Needed]

#### Annotation process

[More Information Needed]

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

I (the "Researcher") have requested permission to use the RecipeNLG dataset (the "Dataset") at Poznań University of Technology (PUT). In exchange for such permission, Researcher hereby agrees to the following terms and conditions:

1. Researcher shall use the Dataset only for non-commercial research and educational purposes.
2. PUT makes no representations or warranties regarding the Dataset, including but not limited to warranties of non-infringement or fitness for a particular purpose.
3. Researcher accepts full responsibility for his or her use of the Dataset and shall defend and indemnify PUT, including its employees, Trustees, officers and agents, against any and all claims arising from Researcher's use of the Dataset including but not limited to Researcher's use of any copies of copyrighted images or text that he or she may create from the Dataset.
4. Researcher may provide research associates and colleagues with access to the Dataset provided that they first agree to be bound by these terms and conditions.
5. If Researcher is employed by a for-profit, commercial entity, Researcher's employer shall also be bound by these terms and conditions, and Researcher hereby represents that he or she is fully authorized to enter into this agreement on behalf of such employer.

### Citation Information

```bibtex
@inproceedings{bien-etal-2020-recipenlg,
    title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
    author = "Bie{\'n}, Micha{\l}  and
      Gilski, Micha{\l}  and
      Maciejewska, Martyna  and
      Taisner, Wojciech  and
      Wisniewski, Dawid  and
      Lawrynowicz, Agnieszka",
    booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
    month = dec,
    year = "2020",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.inlg-1.4",
    pages = "22--28",
}
```

### Contributions

Thanks to [@abhishekkrthakur](https://github.com/abhishekkrthakur) for adding this dataset.
