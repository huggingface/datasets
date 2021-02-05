---
---

# Dataset Card for "amazon_us_reviews"

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

- **Homepage:** [https://s3.amazonaws.com/amazon-reviews-pds/readme.html](https://s3.amazonaws.com/amazon-reviews-pds/readme.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 30877.39 MB
- **Size of the generated dataset:** 78983.49 MB
- **Total amount of disk used:** 109860.89 MB

### [Dataset Summary](#dataset-summary)

Amazon Customer Reviews (a.k.a. Product Reviews) is one of Amazons iconic products. In a period of over two decades since the first review in 1995, millions of Amazon customers have contributed over a hundred million reviews to express opinions and describe their experiences regarding products on the Amazon.com website. This makes Amazon Customer Reviews a rich source of information for academic researchers in the fields of Natural Language Processing (NLP), Information Retrieval (IR), and Machine Learning (ML), amongst others. Accordingly, we are releasing this data to further research in multiple disciplines related to understanding customer product experiences. Specifically, this dataset was constructed to represent a sample of customer evaluations and opinions, variation in the perception of a product across geographical regions, and promotional intent or bias in reviews.
Over 130+ million customer reviews are available to researchers as part of this release. The data is available in TSV files in the amazon-reviews-pds S3 bucket in AWS US East Region. Each line in the data files corresponds to an individual review (tab delimited, with no quote and escape characters).
Each Dataset contains the following columns :
    marketplace       - 2 letter country code of the marketplace where the review was written.
    customer_id       - Random identifier that can be used to aggregate reviews written by a single author.
    review_id         - The unique ID of the review.
    product_id        - The unique Product ID the review pertains to. In the multilingual dataset the reviews
                        for the same product in different countries can be grouped by the same product_id.
    product_parent    - Random identifier that can be used to aggregate reviews for the same product.
    product_title     - Title of the product.
    product_category  - Broad product category that can be used to group reviews
                        (also used to group the dataset into coherent parts).
    star_rating       - The 1-5 star rating of the review.
    helpful_votes     - Number of helpful votes.
    total_votes       - Number of total votes the review received.
    vine              - Review was written as part of the Vine program.
    verified_purchase - The review is on a verified purchase.
    review_headline   - The title of the review.
    review_body       - The review text.
    review_date       - The date the review was written.

### [Supported Tasks](#supported-tasks)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### [Languages](#languages)

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## [Dataset Structure](#dataset-structure)

We show detailed information for up to 5 configurations of the dataset.

### [Data Instances](#data-instances)

#### Apparel_v1_00

- **Size of downloaded dataset files:** 618.59 MB
- **Size of the generated dataset:** 2149.93 MB
- **Total amount of disk used:** 2768.52 MB

An example of 'train' looks as follows.
```
{
    "customer_id": "45223824",
    "helpful_votes": 0,
    "marketplace": "US",
    "product_category": "Apparel",
    "product_id": "B016PUU3VO",
    "product_parent": "893588059",
    "product_title": "Fruit of the Loom Boys' A-Shirt (Pack of 4)",
    "review_body": "I ordered the same size as I ordered last time, and these shirts were much larger than the previous order. They were also about 6 inches longer. It was like they sent men's shirts instead of boys' shirts. I'll be returning these...",
    "review_date": "2015-01-01",
    "review_headline": "Sizes not correct, too big overall and WAY too long",
    "review_id": "R1N3Z13931J3O9",
    "star_rating": 2,
    "total_votes": 0,
    "verified_purchase": 1,
    "vine": 0
}
```

#### Automotive_v1_00

- **Size of downloaded dataset files:** 555.18 MB
- **Size of the generated dataset:** 1448.52 MB
- **Total amount of disk used:** 2003.70 MB

An example of 'train' looks as follows.
```
{
    "customer_id": "16825098",
    "helpful_votes": 0,
    "marketplace": "US",
    "product_category": "Automotive",
    "product_id": "B000E4PCGE",
    "product_parent": "694793259",
    "product_title": "00-03 NISSAN SENTRA MIRROR RH (PASSENGER SIDE), Power, Non-Heated (2000 00 2001 01 2002 02 2003 03) NS35ER 963015M000",
    "review_body": "Product was as described, new and a great look. Only bad thing is that one of the screws was stripped so I couldn't tighten all three.",
    "review_date": "2015-08-31",
    "review_headline": "new and a great look. Only bad thing is that one of ...",
    "review_id": "R2RUIDUMDKG7P",
    "star_rating": 3,
    "total_votes": 0,
    "verified_purchase": 1,
    "vine": 0
}
```

#### Baby_v1_00

- **Size of downloaded dataset files:** 340.84 MB
- **Size of the generated dataset:** 912.00 MB
- **Total amount of disk used:** 1252.84 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "customer_id": "23299101",
    "helpful_votes": 2,
    "marketplace": "US",
    "product_category": "Baby",
    "product_id": "B00SN6F9NG",
    "product_parent": "3470998",
    "product_title": "Rhoost Nail Clipper for Baby - Ergonomically Designed and Easy to Use Baby Nail Clipper, Natural Wooden Bamboo - Baby Health and Personal Care Kits",
    "review_body": "\"This is an absolute MUST item to have!  I was scared to death to clip my baby's nails.  I tried other baby nail clippers and th...",
    "review_date": "2015-08-31",
    "review_headline": "If fits so comfortably in my hand and I feel like I have ...",
    "review_id": "R2DRL5NRODVQ3Z",
    "star_rating": 5,
    "total_votes": 2,
    "verified_purchase": 1,
    "vine": 0
}
```

#### Beauty_v1_00

- **Size of downloaded dataset files:** 871.73 MB
- **Size of the generated dataset:** 2286.33 MB
- **Total amount of disk used:** 3158.06 MB

An example of 'train' looks as follows.
```
{
    "customer_id": "24655453",
    "helpful_votes": 1,
    "marketplace": "US",
    "product_category": "Beauty",
    "product_id": "B00SAQ9DZY",
    "product_parent": "292127037",
    "product_title": "12 New, High Quality, Amber 2 ml (5/8 Dram) Glass Bottles, with Orifice Reducer and Black Cap.",
    "review_body": "These are great for small mixtures for EO's, especially for traveling.  I only gave this 4 stars because of the orifice reducer.  The hole is so small it is hard to get the oil out.  Just needs to be slightly bigger.",
    "review_date": "2015-08-31",
    "review_headline": "Good Product",
    "review_id": "R2A30ALEGLMCGN",
    "star_rating": 4,
    "total_votes": 1,
    "verified_purchase": 1,
    "vine": 0
}
```

#### Books_v1_00

- **Size of downloaded dataset files:** 2613.39 MB
- **Size of the generated dataset:** 6860.60 MB
- **Total amount of disk used:** 9473.99 MB

An example of 'train' looks as follows.
```
This example was too long and was cropped:

{
    "customer_id": "49735028",
    "helpful_votes": 0,
    "marketplace": "US",
    "product_category": "Books",
    "product_id": "0664254969",
    "product_parent": "248307276",
    "product_title": "Presbyterian Creeds: A Guide to the Book of Confessions",
    "review_body": "\"The Presbyterian Book of Confessions contains multiple Creeds for use by the denomination. This guidebook helps he lay person t...",
    "review_date": "2015-08-31",
    "review_headline": "The Presbyterian Book of Confessions contains multiple Creeds for use ...",
    "review_id": "R2G519UREHRO8M",
    "star_rating": 3,
    "total_votes": 1,
    "verified_purchase": 1,
    "vine": 0
}
```

### [Data Fields](#data-fields)

The data fields are the same among all splits.

#### Apparel_v1_00
- `marketplace`: a `string` feature.
- `customer_id`: a `string` feature.
- `review_id`: a `string` feature.
- `product_id`: a `string` feature.
- `product_parent`: a `string` feature.
- `product_title`: a `string` feature.
- `product_category`: a `string` feature.
- `star_rating`: a `int32` feature.
- `helpful_votes`: a `int32` feature.
- `total_votes`: a `int32` feature.
- `vine`: a classification label, with possible values including `Y` (0), `N` (1).
- `verified_purchase`: a classification label, with possible values including `Y` (0), `N` (1).
- `review_headline`: a `string` feature.
- `review_body`: a `string` feature.
- `review_date`: a `string` feature.

#### Automotive_v1_00
- `marketplace`: a `string` feature.
- `customer_id`: a `string` feature.
- `review_id`: a `string` feature.
- `product_id`: a `string` feature.
- `product_parent`: a `string` feature.
- `product_title`: a `string` feature.
- `product_category`: a `string` feature.
- `star_rating`: a `int32` feature.
- `helpful_votes`: a `int32` feature.
- `total_votes`: a `int32` feature.
- `vine`: a classification label, with possible values including `Y` (0), `N` (1).
- `verified_purchase`: a classification label, with possible values including `Y` (0), `N` (1).
- `review_headline`: a `string` feature.
- `review_body`: a `string` feature.
- `review_date`: a `string` feature.

#### Baby_v1_00
- `marketplace`: a `string` feature.
- `customer_id`: a `string` feature.
- `review_id`: a `string` feature.
- `product_id`: a `string` feature.
- `product_parent`: a `string` feature.
- `product_title`: a `string` feature.
- `product_category`: a `string` feature.
- `star_rating`: a `int32` feature.
- `helpful_votes`: a `int32` feature.
- `total_votes`: a `int32` feature.
- `vine`: a classification label, with possible values including `Y` (0), `N` (1).
- `verified_purchase`: a classification label, with possible values including `Y` (0), `N` (1).
- `review_headline`: a `string` feature.
- `review_body`: a `string` feature.
- `review_date`: a `string` feature.

#### Beauty_v1_00
- `marketplace`: a `string` feature.
- `customer_id`: a `string` feature.
- `review_id`: a `string` feature.
- `product_id`: a `string` feature.
- `product_parent`: a `string` feature.
- `product_title`: a `string` feature.
- `product_category`: a `string` feature.
- `star_rating`: a `int32` feature.
- `helpful_votes`: a `int32` feature.
- `total_votes`: a `int32` feature.
- `vine`: a classification label, with possible values including `Y` (0), `N` (1).
- `verified_purchase`: a classification label, with possible values including `Y` (0), `N` (1).
- `review_headline`: a `string` feature.
- `review_body`: a `string` feature.
- `review_date`: a `string` feature.

#### Books_v1_00
- `marketplace`: a `string` feature.
- `customer_id`: a `string` feature.
- `review_id`: a `string` feature.
- `product_id`: a `string` feature.
- `product_parent`: a `string` feature.
- `product_title`: a `string` feature.
- `product_category`: a `string` feature.
- `star_rating`: a `int32` feature.
- `helpful_votes`: a `int32` feature.
- `total_votes`: a `int32` feature.
- `vine`: a classification label, with possible values including `Y` (0), `N` (1).
- `verified_purchase`: a classification label, with possible values including `Y` (0), `N` (1).
- `review_headline`: a `string` feature.
- `review_body`: a `string` feature.
- `review_date`: a `string` feature.

### [Data Splits Sample Size](#data-splits-sample-size)

|      name      | train  |
|----------------|-------:|
|Apparel_v1_00   | 5906333|
|Automotive_v1_00| 3514942|
|Baby_v1_00      | 1752932|
|Beauty_v1_00    | 5115666|
|Books_v1_00     |10319090|

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

```


### Contributions

Thanks to [@joeddav](https://github.com/joeddav) for adding this dataset.