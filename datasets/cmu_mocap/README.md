---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- other
multilinguality:
- monolingual
pretty_name: CMU MoCap
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- other
task_ids: []
paperswithcode_id: mocap
---

# Dataset Card for CMU MoCap 

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

- **Homepage:** [CMU MoCap homepage](http://mocap.cs.cmu.edu/)
- **Repository:** [More Information Needed]
- **Paper:** [More Information Needed]
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** [CMU MoCap Contact](mailto:jkh+mocap@cs.cmu.edu)

### Dataset Summary

The CMU Graphics Lab Motion Capture Database is a dataset containing motion capture recordings of people performing different actions such as walking, jumping, dancing etc. The actions have been performed by over 110 subjects. There are a total of over 2500 trials in 6 categories and 23 subcategories.

> **Note**: The dataset has subjects numbered up to 144 [here](http://mocap.cs.cmu.edu/subjects.php), but some of the subject numbers are missing, so the total number of examples is 112.

### Dataset Preprocessing

The dataset contains motions in the following formats :

- `asf-amc` : The ASF file (Acclaim Skeleton File) is a skeleton file. AMC files (Acclaim Motion Capture data) are the motion files. Most of the time a single skeleton works for many different motions and rather than storing the same skeleton in each of the motion files, thus for each subject there is one ASF file along with AMC files for each motion.

The AMC/ASF files can be parsed using [AMCParser library](https://github.com/CalciferZh/AMCParser). You can check the Usage section in this library for more information.

- `c3d`: The C3D format stores 3D coordinate information, analog data and associated information used in 3D motion data capture and subsequent analysis operations. 

You can use [py-c3d library](https://c3d.readthedocs.io/en/stable/) for reading and writing C3D binary files.

- `avi` and `mpg`: AVI (Audio Video Interleave) has been the long-standing format to save and deliver movies and other video files. An MPG file is a common video file that uses a digital video format standardized by the Moving Picture Experts Group (MPEG)

You can use a video loader library such as [decord](https://github.com/dmlc/decord) to load and process these files.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

All the categories, sub-categories and descriptions use English as their primary language.

## Dataset Structure

### Data Instances

A sample from the CMU MoCap dataset is provided below:
```
{
    'subject_id': 12, 
    'categories': ['Physical Activities & Sports', 'Locomotion', 'Locomotion', 'Locomotion'], 
    'subcategories': ['martial arts', 'walking', 'walking', 'walking'], 
    'descriptions': ['tai chi', 'walk', 'walk', 'walk'], 
    'motions': {
        'amc_files': ['~/all_asfamc/subjects/12/12_04.amc', '~/all_asfamc/subjects/12/12_01.amc', '~/all_asfamc/subjects/12/12_03.amc', '~/all_asfamc/subjects/12/12_02.amc'], 
        'skeleton_file': '~/all_asfamc/subjects/12/12.asf',
    }
}
```

### Data Fields

The following fields are common for all file formats of the dataset.

- `subject_id`: Unique ID for each subject in the MoCap dataset.
- `categories`:  A list containing the category names of all trials.
- `subcategories`: A list containing the subcategory names of all trials.
- `descriptions`: A list containing the descriptions of all trials.

The c3d, mpg and avi formats have: 
- `motions` : A list containing the path to all motion files.

The "asf/amc" config has an additional field :
- `motions`: {
        `amc_files`: A list containing the path to all motion files, 
        `skeleton_file`: path to the ASF file,
    }

    It is a dictionary containing the motion files and skeleton file.

ASF file is the skeleton file, in the ASF file a base pose is defined for the skeleton that is the starting point for the motion data. More info can be found [here](https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/ASF-AMC.html).


### Data Splits

All the data is contained in training set. 

Not all subjects were converted from the initial `asf-amc` format to the destination formats, so depending on the format, the number of examples varies:
<MARKDOWN TABLE>

These are based on the download links provided on the [CMU MoCap Website](http://mocap.cs.cmu.edu/faqs.php), it seems like all links are not provided for the mpg format.

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

From the [CMU MoCap Info](http://mocap.cs.cmu.edu/info.php) page:
> The mocap lab contains 12 Vicon infrared MX-40 cameras, each of which is capable of recording 120 Hz with images of 4 megapixel resolution. The cameras are placed around a rectangular area, of approximately 3m x 8m, in the center of the room. Only motions that take place in this rectangle can be captured. If motion of human hands is being captured, more detail is required and the cameras are moved closer to capture a smaller space with higher resolution. To capture something, small grey markers are placed on it. Humans wear a black jumpsuit and have 41 markers taped on. The Vicon cameras see the markers in infra-red. The images that the various cameras pick up are triangulated to get 3D data.
>
This 3D data can be used in two ways by you:
>
- Marker positions You can be handed a file of 3D marker positions, a .c3d . This file is relatively clean - i.e., Marker "A" should be labeled Marker "A" throughout the motion. But it is your responsibility to figure out what "A" means and how it relates to the other markers.
- Skeleton movement Data will be handed to you as either a .vsk/.v pair or .asf/.amc pair (more on that later). The former element of the pair describes the skeleton and its joints: their connections, lengths, degrees of freedom (free, ball and socket, 2 hinges, hinge, rigid), and mathematical transformations. The latter element of the pair contains the movement data. Notes: If a subject/object was captured in multiple clips, you will be handed several .v's or .amc's. Also, something like a hamburger turner, if that's what you're capturing, can have a "skeleton" - even if it's one bone long.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

From the [CMU MoCap Info](http://mocap.cs.cmu.edu/info.php) page:
> Vicon must be told what skeleton to use, in the form of a .vst, a Vicon Skeleton Template. These can be created in ViconIQ itself, under the modeling tab. The Vicon software comes with documentation on editing them. Visualized, they look like maya skeletons covered in porcupine needles. They specify the skeleton hierarchy, and what markers will be captured to help construct this skeleton. They give approximate bone lengths - the actual length, of course, will depend on the subject/object being captured.

> The markers are carefully placed to get maximal information - consider that if you had a hinge joint, 2? 3? markers would define it absolutely. Constraints between markers and joints are also specified, e.g. "the elbow belongs at the y-location of this marker", or "the wrist joint is halfway between these two markers". You get the idea. Constructing .vst's for complex objects requires careful thought and testing.

> In the lab, we have pre-tested .vst's for humans and hands. Creating .vst's for simple props is easy.

<figure>

<img src="http://mocap.cs.cmu.edu/mocap/new_skeleton_pic.jpg" alt="Skeleton Visualization" height="256" />

<figcaption>Visualization of the .vst. The balls represent markers; the thick colored segments represent bones.</figcaption>

</figure>

<figure>

<img src="http://mocap.cs.cmu.edu/mocap/new_marker_set_front.jpg" alt="Marker Set - Front View" height="256">

<figcaption>The marker set - Front View</figcaption>

</figure>

<figure>

<img src="http://mocap.cs.cmu.edu/mocap/new_marker_set_back.jpg" alt="Marker Set - Back View" height="256">

<figcaption>The marker set - Back View</figcaption>

</figure>



#### Who are the annotators?

From the [CMU MoCap Info](http://mocap.cs.cmu.edu/info.php) page:
> The Labeling

> ViconIQ requires user interaction to start off the skeleton fitting. To process a capture, a segment of motion is loaded onscreen as a point cloud of markers. The user goes through and specifies the correspondence between these markers and the markers in the .vst, e.g. "this white dot is the clavicle marker". From this data ViconIQ can fit a skeleton and determine the skeleton's limb lengths. From here on out the labeling process is automatic. ViconIQ can load up each motion clip and automatically perform a "Kinematic Fit" of the skeleton to the markers. During this time the software uses its knowledge of the skeleton to correct captured marker aberrations. The user can also fix things up by editing the joint rotation/translation graphs directly.

> The Exporting

> While this work is going on each motion clip is stored in a .trial file. When the data is clean, it is time to export useful files. A .vsk of the skeleton is exported. Keep in mind that this .vsk is unique to each person, because each person has different limb lengths. Multiple .v's are exported, one for each motion clip the person performed. Using BodyBuilder, these can be turned into asf/amc's.

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

[Needs More Information]

### Licensing Information

From the website:
> This data is free for use in research projects. You may include this data in commercially-sold products, but you may not resell this data directly, even in converted form.

### Citation Information

From the website:
> The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217.

### Contributions

Thanks to [@dnaveenr](https://github.com/dnaveenr) for adding this dataset.