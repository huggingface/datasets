---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: MetaShift
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- image-classification
- other
task_ids:
- multi-label-image-classification
- other-other-domain-generalization
paperswithcode_id: metashift
---

# Dataset Card for MetaShift

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
  - [Data Splits](#data-instances)
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

## Dataset Description

- **Homepage:**  [MetaShift homepage](https://metashift.readthedocs.io/)
- **Repository:** [MetaShift repository](https://github.com/Weixin-Liang/MetaShift)
- **Paper:** [MetaShift paper](https://arxiv.org/abs/2202.06523v1)
- **Point of Contact:**  [Weixin Liang](mailto:wxliang@stanford.edu)

### Dataset Summary

The MetaShift dataset is a collection of 12,868 sets of natural images across 410 classes. It was created for understanding the performance of a machine learning model across diverse data distributions.

The authors leverage the natural heterogeneity of Visual Genome and its annotations to construct MetaShift.
The key idea is to cluster images using its metadata which provides context for each image.
For example : cats with cars or cats in bathroom.
The main advantage is the dataset contains many more coherent sets of data compared to other benchmarks.

Two important benefits of MetaShift :
- Contains orders of magnitude more natural data shifts than previously available.
- Provides explicit explanations of what is unique about each of its data sets and a distance score that measures the amount of distribution shift between any two of its data sets.

### Dataset Usage

The dataset has the following configuration parameters:
- selected_classes: `list[string]`, optional, list of the classes to generate the MetaShift dataset for. If `None`, the list is equal to `['cat', 'dog', 'bus', 'truck', 'elephant', 'horse']`.
- attributes_dataset: `bool`, default `False`, if `True`, the script generates the MetaShift-Attributes dataset. Refer [MetaShift-Attributes Dataset](https://github.com/Weixin-Liang/MetaShift#bonus-generate-the-metashift-attributes-dataset-subsets-defined-by-subject-attributes) for more information.
- attributes: `list[string]`, optional, list of attributes classes included in the Attributes dataset. If `None` and `attributes_dataset` is `True`, it's equal to `["cat(orange)", "cat(white)", "dog(sitting)", "dog(jumping)"]`. You can find the full attribute ontology in the above link. 
- with_image_metadata: `bool`, default `False`, whether to include image metadata. If set to `True`, this will give additional metadata about each image. See [Scene Graph](https://cs.stanford.edu/people/dorarad/gqa/download.html) for more information.
- image_subset_size_threshold: `int`, default `25`, the number of images required to be considered a subset. If the number of images is less than this threshold, the subset is ignored.
- min_local_groups: `int`, default `5`, the minimum number of local groups required to be considered an object class.

Consider the following examples to get an idea of how you can use the configuration parameters :

1. To generate the MetaShift Dataset :
```python
load_dataset("metashift", selected_classes=['cat', 'dog', 'bus'])
```
The full object vocabulary and its hierarchy can be seen [here](https://github.com/Weixin-Liang/MetaShift/blob/main/dataset/meta_data/class_hierarchy.json).

The default classes are `['cat', 'dog', 'bus', 'truck', 'elephant', 'horse']`

2. To generate the MetaShift-Attributes Dataset (subsets defined by subject attributes) :
```python
load_dataset("metashift", attributes_dataset = True, attributes=["dog(smiling)", "cat(resting)"])
```

The default attributes are `["cat(orange)", "cat(white)", "dog(sitting)", "dog(jumping)"]`

3. To generate the dataset with additional image metadata information :
```python
load_dataset("metashift", selected_classes=['cat', 'dog', 'bus'], with_image_metadata=True)
```
4. Further, you can specify your own configuration different from those used in the papers as follows:
```python
load_dataset("metashift", image_subset_size_threshold=20, min_local_groups=3)
```
### Dataset Meta-Graphs

From the MetaShift Github Repo :
> MetaShift splits the data points of each class (e.g., Cat) into many subsets based on visual contexts. Each node in the meta-graph represents one subset. The weight of each edge is the overlap coefficient between the corresponding two subsets. Node colors indicate the graph-based community detection results. Inter-community edges are colored. Intra-community edges are grayed out for better visualization. The border color of each example image indicates its community in the meta-graph. We have one such meta-graph for each of the 410 classes in the MetaShift.

The following are the metagraphs for the default classes, these have been generated using the `generate_full_MetaShift.py` file.

<p align='center'>
  <img width='75%' src='https://i.imgur.com/wrpezCK.jpg' alt="Cat Meta-graph" /> </br>
  <b>Figure: Meta-graph: visualizing the diverse data distributions within the “cat” class.  </b> 
</p>

<p align='center'>
  <img width='75%' src='https://i.imgur.com/FhuAwfT.jpg' alt="Dog Meta-graph" /> </br>
<b>Figure: Meta-graph for the “Dog” class, which captures meaningful semantics of the multi-modal data distribution of “Dog”. </b> 
</p>

<p align='center'>
  <img width='75%' src='https://i.imgur.com/FFCcN6L.jpg' alt="Bus Meta-graph" /> </br>
<b>Figure: Meta-graph for the “Bus” class. </b> 
</p>

<p align='center'>
  <img width='75%' src='https://i.imgur.com/rx5b5Vo.jpg' alt="Elephant Meta-graph" /> </br>
<b>Figure: Meta-graph for the "Elephant" class. </b> 
</p>

<p align='center'>
  <img width='75%' src='https://i.imgur.com/6f6U3S8.jpg' alt="Horse Meta-graph" /> </br>
<b>Figure: Meta-graph for the "Horse" class. </b> 
</p>

<p align='center'>
  <img width='75%' src='https://i.imgur.com/x9zhQD7.jpg' alt="Truck Meta-graph"/> </br>
<b>Figure: Meta-graph for the Truck class. </b> 
</p>

### Supported Tasks and Leaderboards

From the paper:
> MetaShift supports evaluation on both :
> - domain generalization and subpopulation shifts settings,
> - assessing training conflicts.

### Languages

 All the classes and subsets use English as their primary language.

## Dataset Structure

### Data Instances

A sample from the MetaShift dataset is provided below:

```
{
    'image_id': '2411520', 
    'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x375 at 0x7F99115B8D90>,
    'label': 2, 
    'context': 'fence'
}
```

A sample from the MetaShift-Attributes dataset is provided below:
```
{
    'image_id': '2401643', 
    'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x333 at 0x7FED371CE350>
    'label': 0
}
```

The format of the dataset with image metadata included by passing `with_image_metadata=True` to `load_dataset` is provided below:
```
{
    'image_id': '2365745', 
    'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=500x333 at 0x7FEBCD39E4D0>
    'label': 0, 
    'context': 'ground', 
    'width': 500, 
    'height': 333, 
    'location': None, 
    'weather': None, 
    'objects': 
    {
        'object_id': ['2676428', '3215330', '1962110', '2615742', '3246028', '3232887', '3215329', '1889633', '3882667', '3882663', '1935409', '3882668', '3882669'], 
        'name': ['wall', 'trailer', 'floor', 'building', 'walkway', 'head', 'tire', 'ground', 'dock', 'paint', 'tail', 'cat', 'wall'], 
        'x': [194, 12, 0, 5, 3, 404, 27, 438, 2, 142, 324, 328, 224], 
        'y': [1, 7, 93, 10, 100, 46, 215, 139, 90, 172, 157, 45, 246], 
        'w': [305, 477, 499, 492, 468, 52, 283, 30, 487, 352, 50, 122, 274], 
        'h': [150, 310, 72, 112, 53, 59, 117, 23, 240, 72, 107, 214, 85], 
        'attributes': [['wood', 'green'], [], ['broken', 'wood'], [], [], [], ['black'], [], [], [], ['thick'], ['small'], ['blue']], 
        'relations': [{'name': [], 'object': []}, {'name': [], 'object': []}, {'name': [], 'object': []}, {'name': [], 'object': []}, {'name': [], 'object': []}, {'name': ['of'], 'object': ['3882668']}, {'name': ['to the left of'], 'object': ['3882669']}, {'name': ['to the right of'], 'object': ['3882668']}, {'name': [], 'object': []}, {'name': [], 'object': []}, {'name': ['of'], 'object': ['3882668']}, {'name': ['perched on', 'to the left of'], 'object': ['3882667', '1889633']}, {'name': ['to the right of'], 'object': ['3215329']}]
    }
}
```

### Data Fields

- `image_id`: Unique numeric ID of the image in Base Visual Genome dataset.
- `image`:  A PIL.Image.Image object containing the image. 
- `label`: an int classification label.
- `context`: represents the context in which the label is seen. A given label could have multiple contexts.

Image Metadata format can be seen [here](https://cs.stanford.edu/people/dorarad/gqa/download.html) and a sample above has been provided for reference.

### Data Splits

All the data is contained in training set.

## Dataset Creation

### Curation Rationale

From the paper:
> We present MetaShift as an important resource for studying the behavior of
ML algorithms and training dynamics across data with heterogeneous contexts. In order to assess the reliability and fairness of a model, we need to evaluate
its performance and training behavior across heterogeneous types of data. MetaShift contains many more coherent sets of data compared to other benchmarks. Importantly, we have explicit annotations of what makes each subset unique (e.g. cats with cars or dogs next to a bench) as well as a score that measures the distance between any two subsets, which is not available in previous benchmarks of natural data.

### Source Data

#### Initial Data Collection and Normalization

From the paper:
> We leverage the natural heterogeneity of Visual Genome and its annotations to construct MetaShift. Visual Genome contains over 100k images across 1,702 object classes. MetaShift is constructed on a class-by-class basis.  For each class, say “cat”, we pull out all cat images and proceed with generating candidate subests, constructing meta-graphs and then duantify distances of distribution shifts.

#### Who are the source language producers?

 [More Information Needed]

### Annotations

The MetaShift dataset uses Visual Genome as its base, therefore the annotations process is same as the Visual Genome dataset.

#### Annotation process

From the Visual Genome paper :
> We used Amazon Mechanical Turk (AMT) as our primary source of annotations. Overall, a total of over 33,000 unique workers contributed to the dataset. The dataset was collected over the course of 6 months after 15 months of experimentation and iteration on the data representation. Approximately 800, 000 Human Intelligence Tasks (HITs) were launched on AMT, where each HIT involved creating descriptions, questions and answers, or region graphs.

#### Who are the annotators?

From the Visual Genome paper :
> Visual Genome was collected and verified entirely by crowd workers from Amazon Mechanical Turk. 

### Personal and Sensitive Information

 [More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

 [More Information Needed]

### Discussion of Biases

From the paper:
> One limitation is that our MetaShift might inherit existing biases in Visual Genome, which is the
base dataset of our MetaShift. Potential concerns include minority groups being under-represented
in certain classes (e.g., women with snowboard), or annotation bias where people in images are
by default labeled as male when gender is unlikely to be identifiable. Existing work in analyzing,
quantifying, and mitigating biases in general computer vision datasets can help with addressing this
potential negative societal impact.

### Other Known Limitations

 [More Information Needed]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

From the paper :
> Our MetaShift and the code would use the Creative Commons Attribution 4.0 International License. Visual Genome (Krishna et al., 2017) is licensed under a Creative Commons Attribution 4.0 International License. MS-COCO (Lin et al., 2014) is licensed under CC-BY 4.0. The Visual Genome dataset uses 108, 077 images from the intersection of the YFCC100M (Thomee et al., 2016) and MS-COCO. We use the pre-processed and cleaned version of Visual Genome by GQA (Hudson & Manning, 2019).

### Citation Information

```bibtex
@InProceedings{liang2022metashift,
title={MetaShift: A Dataset of Datasets for Evaluating Contextual Distribution Shifts and Training Conflicts},
author={Weixin Liang and James Zou},
booktitle={International Conference on Learning Representations},
year={2022},
url={https://openreview.net/forum?id=MTex8qKavoS}
}
```

### Contributions

Thanks to [@dnaveenr](https://github.com/dnaveenr) for adding this dataset.
