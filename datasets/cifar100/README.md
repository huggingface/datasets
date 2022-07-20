---
pretty_name: Cifar100
annotations_creators:
- crowdsourced
language_creators:
- found
language:
- en
license:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-80-Million-Tiny-Images
task_categories:
- image-classification
task_ids: []
paperswithcode_id: cifar-100
---
 
# Dataset Card for CIFAR-100

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

- **Homepage:** [CIFAR Datasets](https://www.cs.toronto.edu/~kriz/cifar.html)
- **Repository:** 
- **Paper:** [Paper](https://www.cs.toronto.edu/~kriz/learning-features-2009-TR.pdf)
- **Leaderboard:**
- **Point of Contact:**
 
### Dataset Summary
 
The CIFAR-100 dataset consists of 60000 32x32 colour images in 100 classes, with 600 images
per class. There are 500 training images and 100 testing images per class. There are 50000 training images and 10000 test images. The 100 classes are grouped into 20 superclasses. 
There are two labels per image - fine label (actual class) and coarse label (superclass).

### Supported Tasks and Leaderboards

- `image-classification`: The goal of this task is to classify a given image into one of 100 classes. The leaderboard is available [here](https://paperswithcode.com/sota/image-classification-on-cifar-100).

### Languages

English

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```
{
  'img': <PIL.PngImagePlugin.PngImageFile image mode=RGB size=32x32 at 0x2767F58E080>, 'fine_label': 19,
  'coarse_label': 11
}
```

### Data Fields

- `img`: A `PIL.Image.Image` object containing the 32x32 image. Note that when accessing the image column: `dataset[0]["image"]` the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the `"image"` column, *i.e.* `dataset[0]["image"]` should **always** be preferred over `dataset["image"][0]`
- `fine_label`: an `int` classification label with the following mapping:

  `0`: apple

  `1`: aquarium_fish

  `2`: baby

  `3`: bear

  `4`: beaver
  
  `5`: bed

  `6`: bee

  `7`: beetle

  `8`: bicycle

  `9`: bottle

  `10`: bowl

  `11`: boy

  `12`: bridge

  `13`: bus

  `14`: butterfly

  `15`: camel

  `16`: can

  `17`: castle

  `18`: caterpillar

  `19`: cattle

  `20`: chair

  `21`: chimpanzee

  `22`: clock

  `23`: cloud

  `24`: cockroach

  `25`: couch

  `26`: cra

  `27`: crocodile

  `28`: cup

  `29`: dinosaur

  `30`: dolphin

  `31`: elephant

  `32`: flatfish

  `33`: forest

  `34`: fox

  `35`: girl

  `36`: hamster

  `37`: house

  `38`: kangaroo

  `39`: keyboard

  `40`: lamp

  `41`: lawn_mower

  `42`: leopard

  `43`: lion

  `44`: lizard

  `45`: lobster

  `46`: man

  `47`: maple_tree

  `48`: motorcycle

  `49`: mountain

  `50`: mouse

  `51`: mushroom

  `52`: oak_tree

  `53`: orange

  `54`: orchid

  `55`: otter

  `56`: palm_tree

  `57`: pear

  `58`: pickup_truck

  `59`: pine_tree

  `60`: plain

  `61`: plate

  `62`: poppy

  `63`: porcupine

  `64`: possum

  `65`: rabbit

  `66`: raccoon

  `67`: ray

  `68`: road

  `69`: rocket

  `70`: rose

  `71`: sea

  `72`: seal

  `73`: shark

  `74`: shrew

  `75`: skunk

  `76`: skyscraper

  `77`: snail

  `78`: snake

  `79`: spider

  `80`: squirrel

  `81`: streetcar

  `82`: sunflower

  `83`: sweet_pepper

  `84`: table

  `85`: tank

  `86`: telephone

  `87`: television

  `88`: tiger

  `89`: tractor

  `90`: train

  `91`: trout

  `92`: tulip

  `93`: turtle

  `94`: wardrobe

  `95`: whale

  `96`: willow_tree

  `97`: wolf

  `98`: woman

  `99`: worm

- `coarse_label`: an `int` coarse classification label with following mapping:

  `0`: aquatic_mammals

  `1`: fish

  `2`: flowers

  `3`: food_containers

  `4`: fruit_and_vegetables

  `5`: household_electrical_devices

  `6`: household_furniture

  `7`: insects

  `8`: large_carnivores

  `9`: large_man-made_outdoor_things

  `10`: large_natural_outdoor_scenes

  `11`: large_omnivores_and_herbivores

  `12`: medium_mammals

  `13`: non-insect_invertebrates

  `14`: people

  `15`: reptiles

  `16`: small_mammals

  `17`: trees

  `18`: vehicles_1

  `19`: vehicles_2


 
### Data Splits
 
|   name   |train|test|
|----------|----:|---------:|
|cifar100|50000|     10000|
 
## Dataset Creation
 
### Curation Rationale
 
[More Information Needed]
 
### Source Data
 
#### Initial Data Collection and Normalization
 
[More Information Needed]
 
#### Who are the source language producers?
 
[More Information Needed]
 
### Annotations
 
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
 
[More Information Needed]
 
### Citation Information
 
```
@TECHREPORT{Krizhevsky09learningmultiple,
    author = {Alex Krizhevsky},
    title = {Learning multiple layers of features from tiny images},
    institution = {},
    year = {2009}
}
```

### Contributions

Thanks to [@gchhablani](https://github.com/gchablani) for adding this dataset.
