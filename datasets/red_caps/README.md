---
annotations_creators:
- found
language_creators:
- found
language:
- en
license:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10M<n<100M
source_datasets:
- original
task_categories:
- image-to-text
task_ids:
- image-captioning
paperswithcode_id: redcaps
pretty_name: RedCaps
---

# Dataset Card for RedCaps

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Dataset Preprocessing](#dataset-preprocessing)
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

- **Homepage:** [RedCaps homepage](https://redcaps.xyz/)
- **Repository:** [RedCaps repository](https://github.com/redcaps-dataset/redcaps-downloader)
- **Paper:** [RedCaps: web-curated image-text data created by the people, for the people](https://arxiv.org/abs/2111.11431)
- **Leaderboard:**
- **Point of Contact:** [Karan Desai](mailto:kdexd@umich.edu)

### Dataset Summary

RedCaps is a large-scale dataset of 12M image-text pairs collected from Reddit.
Images and captions from Reddit depict and describe a wide variety of objects and scenes.
The data is collected from a manually curated set of subreddits (350 total),
which give coarse image labels and allow steering of the dataset composition
without labeling individual instances. RedCaps data is created *by the people, for the people* – it contains everyday things that users like to share on social media, for example hobbies (r/crafts) and pets (r/shiba). Captions often contain specific and
fine-grained descriptions (northern cardinal, taj mahal). Subreddit names provide relevant image
labels (r/shiba) even when captions may not (mlem!), and sometimes may group many visually
unrelated images through a common semantic meaning (r/perfectfit).

### Dataset Preprocessing

This dataset doesn't download the images locally by default. Instead, it exposes URLs to the images. To fetch the images, use the following code:

```python
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import io
import urllib

import PIL.Image

from datasets import load_dataset
from datasets.utils.file_utils import get_datasets_user_agent


USER_AGENT = get_datasets_user_agent()


def fetch_single_image(image_url, timeout=None, retries=0):
    for _ in range(retries + 1):
        try:
            request = urllib.request.Request(
                image_url,
                data=None,
                headers={"user-agent": USER_AGENT},
            )
            with urllib.request.urlopen(request, timeout=timeout) as req:
                image = PIL.Image.open(io.BytesIO(req.read()))
            break
        except Exception:
            image = None
    return image


def fetch_images(batch, num_threads, timeout=None, retries=0):
    fetch_single_image_with_args = partial(fetch_single_image, timeout=timeout, retries=retries)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        batch["image"] = list(executor.map(fetch_single_image_with_args, batch["image_url"]))
    return batch


num_threads = 20
dset = load_dataset("red_caps", "rabbits_2017")
dset = dset.map(fetch_images, batched=True, batch_size=100, fn_kwargs={"num_threads": num_threads})
```

Some image links point to more than one image. You can process and downloaded those as follows:

```python
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import io
import os
import re
import urllib

import PIL.Image

import datasets
from datasets import load_dataset
from datasets.utils.file_utils import get_datasets_user_agent


USER_AGENT = get_datasets_user_agent()


def fetch_single_image(image_url, timeout=None, retries=0):
    for _ in range(retries + 1):
        try:
            request = urllib.request.Request(
                image_url,
                data=None,
                headers={"user-agent": USER_AGENT},
            )
            with urllib.request.urlopen(request, timeout=timeout) as req:
                image = PIL.Image.open(io.BytesIO(req.read()))
            break
        except Exception:
            image = None
    return image


def fetch_images(batch, num_threads, timeout=None, retries=0):
    fetch_single_image_with_args = partial(fetch_single_image, timeout=timeout, retries=retries)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        batch["image"] = list(executor.map(lambda image_urls: [fetch_single_image_with_args(image_url) for image_url in image_urls], batch["image_url"]))
    return batch


def process_image_urls(batch):
    processed_batch_image_urls = []
    for image_url in batch["image_url"]:
        processed_example_image_urls = []
        image_url_splits = re.findall(r"http\S+", image_url)
        for image_url_split in image_url_splits:
            if "imgur" in image_url_split and "," in image_url_split:
                for image_url_part in image_url_split.split(","):
                    if not image_url_part:
                        continue
                    image_url_part = image_url_part.strip()
                    root, ext = os.path.splitext(image_url_part)
                    if not root.startswith("http"):
                      root = "http://i.imgur.com/" + root
                    root = root.split("#")[0]
                    if not ext:
                      ext = ".jpg"
                    ext = re.split(r"[?%]", ext)[0]
                    image_url_part = root + ext
                    processed_example_image_urls.append(image_url_part)
            else:
                processed_example_image_urls.append(image_url_split)
        processed_batch_image_urls.append(processed_example_image_urls)
    batch["image_url"] = processed_batch_image_urls
    return batch


dset = load_dataset("red_caps", "rabbits_2017")
dset = dset.map(process_image_urls, batched=True, num_proc=4)
features = dset["train"].features.copy()
features["image"] = datasets.Sequence(datasets.Image())
num_threads = 20
dset = dset.map(fetch_images, batched=True, batch_size=100, features=features, fn_kwargs={"num_threads": num_threads})
```

Note that in the above code, we use the `datasets.Sequence` feature to represent a list of images for the multi-image links.

### Supported Tasks and Leaderboards

From the paper:
> We have used our dataset to train deep neural networks that perform image captioning, and
that learn transferable visual representations for a variety of downstream visual recognition tasks
(image classification, object detection, instance segmentation).

> We anticipate that the dataset could be used for a variety of vision-and-language (V&L) tasks,
such as image or text retrieval or text-to-image synthesis.

### Languages

All of the subreddits in RedCaps use English as their primary language.

## Dataset Structure

### Data Instances

Each instance in RedCaps represents a single Reddit image post:

```
{
  'image_id': 'bpzj7r',
  'author': 'djasz1',
  'image_url': 'https://i.redd.it/ho0wntksivy21.jpg',
  'raw_caption': 'Found on a friend’s property in the Keys FL. She is now happily living in my house.',
  'caption': 'found on a friend's property in the keys fl. she is now happily living in my house.', 'subreddit': 3,
  'score': 72,
  'created_utc': datetime.datetime(2019, 5, 18, 1, 36, 41),
  'permalink': '/r/airplants/comments/bpzj7r/found_on_a_friends_property_in_the_keys_fl_she_is/', 'crosspost_parents': None
}
```

### Data Fields

- `image_id`: Unique alphanumeric ID of the image post (assigned by Reddit).
- `author`: Reddit username of the image post author.
- `image_url`: Static URL for downloading the image associated with the post.
- `raw_caption`: Textual description of the image, written by the post author.
- `caption`: Cleaned version of "raw_caption" by us (see Q35).
- `subreddit`: Name of subreddit where the post was submitted.
- `score`: Net upvotes (discounting downvotes) received by the image post. This field is equal to `None` if the image post is a crosspost.
- `created_utc`: Integer time epoch (in UTC) when the post was submitted to Reddit.
- `permalink`: Partial URL of the Reddit post (https://reddit.com/<permalink>).
- `crosspost_parents`: List of parent posts. This field is optional.


### Data Splits

All the data is contained in training set. The training set has nearly 12M (12,011,111) instances. 

From the paper:
> We intend our dataset to be primarily used for pre-training with one or more specific downstream task(s) in mind. Hence, all instances in our dataset would be used for training while
the validation split is derived from downstream task(s). If users require a validation split, we
recommend sampling it such that it follows the same subreddit distribution as entire dataset.

## Dataset Creation

### Curation Rationale

From the paper:
> Large datasets of image-text pairs are widely used for pre-training generic representations
that transfer to a variety of downstream vision and vision-and-language tasks. Existing public
datasets of this kind were curated from search engine results (SBU Captions [1]) or HTML
alt-text from arbitrary web pages (Conceptual Captions [2, 31]). They performed complex
data filtering to deal with noisy web data. Due to aggressive filtering, their data collection is
inefficient and diversity is artificially supressed. We argue that the quality of data depends on
its source, and the human intent behind its creation. In this work, we explore Reddit – a social
media platform, for curating high quality data. We introduce RedCaps – a large dataset of
12M image-text pairs from Reddit. While we expect the use-cases of RedCaps to be similar to
existing datasets, we discuss how Reddit as a data source leads to fast and lightweight collection,
better data quality, lets us easily steer the data distribution, and facilitates ethically responsible data curation.

### Source Data

#### Initial Data Collection and Normalization

From the paper:
> **Data Collection Pipeline**
Reddit’s uniform structure allows us to parallelize data collection as independent tasks – each task
involves collecting posts submitted to a single subreddit in one year. Our collection pipeline has three steps: (1) subreddit selection, (2) image post filtering, and (3) caption cleaning.
**Step 1**. Subreddit selection: We collect data from a manually curated set of subreddits. Subreddits
have their own rules, community norms, and moderators so curating subreddits allows us to steer the
dataset’s composition without annotating individual instances. We select subreddits with a high volume of images posts, where images tend to be photographs (rather than memes, drawings, screenshots,
etc) and post titles tend to describe image content (rather than making jokes, political commentary,
etc). We do not select any NSFW, banned, or quarantined subreddits. We want to minimize the
number of people that appear in RedCaps, so we omit subreddits whose primary purpose is to share or
comment on images of people (such as celebrity pics or user selfies). We choose subreddits focused on
general photography (r/pics, r/itookapicture), animals (r/axolotls, r/birdsofprey, r/dachshund),
plants (r/roses, r/succulents), objects (r/classiccars, r/trains, r/mechanicalkeyboards), food
(r/steak, r/macarons), scenery (r/cityporn1
, r/desertporn), or activities (r/carpentry, r/kayaking).
In total we collect data from 350 subreddits; the full list can be found in Appendix A.
**Step 2**. Image post filtering: We use Pushshift [41] and Reddit [42, 43] APIs to download all image
posts submitted to our selected subreddits from 2008–2020. Posts are collected at least six months
after their creation to let upvotes stabilize. We only collect posts with images hosted on three domains:
Reddit (i.redd.it), Imgur (i.imgur.com), and Flickr (staticflickr.com). Some image posts contain
multiple images (gallery posts) – in this case we only collect the first image and associate it with
the caption. We discard posts with < 2 upvotes to avoid unappealing content, and we discard posts
marked NSFW (by their authors or subreddit moderators) to avoid pornographic or disturbing content.
**Step 3**. Caption cleaning: We expect Reddit post titles to be less noisy than other large-scale
sources of image captions such as alt-text [2, 31], so we apply minimal text cleaning. We lowercase
captions and use ftfy [44] to remove character accents, emojis, and non-latin characters, following
[29, 35, 36]. Then we apply simple pattern matching to discard all sub-strings enclosed in brackets
((.*), [.*]). These sub-strings usually give non-semantic information: original content tags [oc],
image resolutions (800x600 px), camera specs (shot with iPhone), self-promotion [Instagram:
@user], and other references (link in comments). Finally, like [31] we replace social media
handles (words starting with ‘@’) with a [USR] token to protect user privacy and reduce redundancy.
Due to such filtering, ≈12K (0.1%) captions in our dataset are empty strings. We do not discard them,
as subreddit names alone provide meaningful supervision. Unlike CC-3M or CC-12M that discard
captions without nouns or that don’t overlap image tags, we do not discard any instances in this step.
Through this pipeline, we collect 13.4M instances from 350 subreddits. Our collection pipeline is
less resource-intensive than existing datasets – we do not require webpage crawlers, search engines,
or large databases of indexed webpages. RedCaps is easily extensible in the future by selecting more
subreddits and collecting posts from future years. Next, we perform additional filtering to mitigate
user privacy risks and harmful stereotypes in RedCaps, resulting in final size of 12M instances.

#### Who are the source language producers?

Reddit is the singular data source for RedCaps.

### Annotations

#### Annotation process

The dataset is built using fully automatic data collection pipeline which doesn't require any human annotators.

#### Who are the annotators?

The annotation process doesn't require any human annotators.

### Personal and Sensitive Information

From the paper:
> **Does the dataset relate to people?**
The dataset pertains to people in that people wrote the captions and posted images to Reddit
that we curate in RedCaps. We made specific design choices while curating RedCaps to avoid
large quantities of images containing people:
(a) We collect data from manually curated subreddits in which most contain primarily pertains
to animals, objects, places, or activities. We exclude all subreddits whose primary purpose
is to share and describe images of people (such as celebrity photos or user selfies).
(b) We use an off-the-shelf face detector to find and remove images with potential presence of
human faces. We manually checked 50K random images in RedCaps (Q16) and found 79
images with identifiable human faces – the entire dataset may have ≈19K (0.15%) images
with identifiable people. Refer Section 2.2 in the main paper.

> **Is it possible to identify one or more natural persons, either directly or indirectly (i.e., in
combination with other data) from the dataset?** 
Yes, all instances in RedCaps include Reddit usernames of their post authors. This could be
used to look up the Reddit user profile, and some Reddit users may have identifying information
in their profiles. Some images may contain human faces which could be identified by
appearance. However, note that all this information is already public on Reddit, and searching it
in RedCaps is no easier than searching directly on Reddit.

> **Were the individuals in question notified about the data collection?**
No. Reddit users are anonymous by default, and are not required to share their personal contact
information (email, phone numbers, etc.). Hence, the only way to notify the authors of RedCaps
image posts is by sending them private messages on Reddit. This is practically difficult to do
manually, and will be classified as spam and blocked by Reddit if attempted to programmatically
send a templated message to millions of users.

> **Did the individuals in question consent to the collection and use of their data?**
Users did not explicitly consent to the use of their data in our dataset. However, by uploading
their data on Reddit, they consent that it would appear on the Reddit plaform and will be
accessible via the official Reddit API (which we use to collect RedCaps).

> **If consent was obtained, were the consenting individuals provided with a mechanism to
revoke their consent in the future or for certain uses?**
Users have full control over the presence of their data in our dataset. If users wish to revoke
their consent, they can delete the underlying Reddit post – it will be automatically removed
dfrom RedCaps since we distributed images as URLs. Moreover, we provide an opt-out request
form on our dataset website for anybody to request removal of an individual instance if it is
potentially harmful (e.g. NSFW, violates privacy, harmful stereotypes, etc.).

## Considerations for Using the Data

### Social Impact of Dataset

From the paper:
> **Has an analysis of the potential impact of the dataset and its use on data subjects (e.g.,
a data protection impact analysis) been conducted?**
No.

### Discussion of Biases

From the paper:
> **Harmful Stereotypes**: Another concern with
Reddit data is that images or language may represent harmful stereotypes about gender, race, or other
characteristics of people [48, 49, 51]. We select only non-NSFW subreddits with active moderation
for collecting data. This stands in contrast to less curated uses of Reddit data, such as GPT-2 [35]
whose training data includes at least 63K documents from banned or quarantined subreddits which
may contain toxic language [53]. We attempt to further reduce harmful stereotypes in two ways:
>  * **NSFW images**: We use the InceptionV3 [54] model from [55] to filter images detected as porn or hentai with confidence ≥ 0.9. Similar to face filtering, we estimated precision of our filtering and estimated amount of missed detections, shown in Table 1. The model detects 87K images with low
precision (∼1%) – most detections are non-NSFW images with pink and beige hues.
>  * **Potentially derogatory language**: We filter instances whose captions contain words or phrases from a common blocklist [56]. It is important to note that such coarse filtering might suppress language from marginalized groups reclaiming slurs [51]; however, as RedCaps is not intended to describe people, we believe this is a pragmatic tradeoff to avoid propagating harmful labels.

> **Reddit demographics**: Reddit’s user demographics are not representative of the population at large.
Compared to US adults, Reddit users skew male (69% vs 49%), young (58% 18-29 years old vs
22%), college educated (36% vs 28%), and politically liberal (41% vs 25%) [57]. Reddit users
are predominantly white (63%) [57], and 49% of desktop traffic to Reddit comes from the United
States [58]. All of the subreddits in RedCaps use English as their primary language. Taken together,
these demographic biases likely also bias the types of objects and places that appear in images on
Reddit, and the language used to describe these images. We do not offer explicit countermeasures to
these biases, but users of RedCaps should keep in mind that size doesn’t guarantee diversity [51].
Subtler issues may also exist, such as imbalanced representation of demographic groups [59] or
gender bias in object co-occurrence [60] or language [61]. These are hard to control in internet
data, so we release RedCaps with explicit instructions on suitable use-cases; specifically requesting models not be trained to identify people, or make decisions that impact people. We document these instructions and other terms-of-use in a datasheet [45], provided in Appendix G.

> **Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety?**
The scale of RedCaps means that we are unable to verify the contents of all images and
captions. However we have tried to minimize the possibility that RedCaps contains data that
might be offensive, insulting, threatening, or might cause anxiety via the following mitigations:
(a) We manually curate the set of subreddits from which to collect data; we only chose
subreddits that are not marked NSFW and which generally contain non-offensive content.
(b) Within our curated subreddits, we did not include any posts marked NSFW.
(c) We removed all instances whose captions contained any of the 400 potentially offensive
words or phrases. Refer Section 2.2 in the main paper.
(d) We remove all instances whose images were flagged NSFW by an off-the-shelf detector.
We manually checked 50K random images in RedCaps and found one image containing
nudity (exposed buttocks; no identifiable face). Refer Section 2.2 in the main paper

> **Does the dataset identify any subpopulations (e.g., by age, gender)?**
RedCaps does not explicitly identify any subpopulations. Since some images contain people
and captions are free-form natural language written by Reddit users, it is possible that some
captions may identify people appearing in individual images as part of a subpopulation.

> **Were any ethical review processes conducted (e.g., by an institutional review board)?**
We did not conduct a formal ethical review process via institutional review boards. However,
as described in Section 2.2 of the main paper and Q16 we employed several filtering mechanisms
to try and remove instances that could be problematic.

### Other Known Limitations

From the paper:
> **Are there any errors, sources of noise, or redundancies in the dataset?**
RedCaps is noisy by design since image-text pairs on the internet are noisy and unstructured.
Some instances may also have duplicate images and captions – Reddit users may have shared
the same image post in multiple subreddits. Such redundancies constitute a very small fraction
of the dataset, and should have almost no effect in training large-scale models.

> **Does the dataset contain data that might be considered confidential (e.g., data that is
protected by legal privilege or by doctor-patient confidentiality, data that includes the
content of individuals non-public communications)?**
No, the subreddits included in RedCaps do not cover topics that may be considered confidential. All posts were publicly shared on Reddit prior to inclusion in RedCaps.

## Additional Information

### Dataset Curators

From the paper:
> Four researchers at the University of Michigan (affiliated as of 2021) have created RedCaps:
Karan Desai, Gaurav Kaul, Zubin Aysola, and Justin Johnson.

### Licensing Information

The image metadata is licensed under CC-BY 4.0 license. Additionally, uses of this dataset are subject to Reddit API terms (https://www.reddit.com/wiki/
api-terms) and users must comply with Reddit User Agreeement, Content Policy,
and Privacy Policy – all accessible at https://www.redditinc.com/policies.

From the paper:
> RedCaps should only be used for non-commercial research. RedCaps should not be used for any tasks that involve identifying features related to people (facial recognition, gender, age, ethnicity identification, etc.) or make decisions that impact people (mortgages, job applications, criminal sentences; or moderation decisions about user-uploaded data that could result in bans from a website). Any commercial and for-profit uses of RedCaps are restricted – it should not be used to train models that will be deployed in production systems as part of a product offered by businesses or government agencies.


### Citation Information

```bibtex
@misc{desai2021redcaps,
      title={RedCaps: web-curated image-text data created by the people, for the people},
      author={Karan Desai and Gaurav Kaul and Zubin Aysola and Justin Johnson},
      year={2021},
      eprint={2111.11431},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

### Contributions

Thanks to [@mariosasko](https://github.com/mariosasko) for adding this dataset.
