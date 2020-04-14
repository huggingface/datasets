<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="amazon_us_reviews" />
  <meta itemprop="description" content="Amazon Customer Reviews (a.k.a. Product Reviews) is one of Amazons iconic products. In a period of over two decades since the first review in 1995, millions of Amazon customers have contributed over a hundred million reviews to express opinions and describe their experiences regarding products on the Amazon.com website. This makes Amazon Customer Reviews a rich source of information for academic researchers in the fields of Natural Language Processing (NLP), Information Retrieval (IR), and Machine Learning (ML), amongst others. Accordingly, we are releasing this data to further research in multiple disciplines related to understanding customer product experiences. Specifically, this dataset was constructed to represent a sample of customer evaluations and opinions, variation in the perception of a product across geographical regions, and promotional intent or bias in reviews.&#10;&#10;Over 130+ million customer reviews are available to researchers as part of this release. The data is available in TSV files in the amazon-reviews-pds S3 bucket in AWS US East Region. Each line in the data files corresponds to an individual review (tab delimited, with no quote and escape characters).&#10;&#10;Each Dataset contains the following columns : &#10;  marketplace       - 2 letter country code of the marketplace where the review was written.&#10;  customer_id       - Random identifier that can be used to aggregate reviews written by a single author.&#10;  review_id         - The unique ID of the review.&#10;  product_id        - The unique Product ID the review pertains to. In the multilingual dataset the reviews&#10;                      for the same product in different countries can be grouped by the same product_id.&#10;  product_parent    - Random identifier that can be used to aggregate reviews for the same product.&#10;  product_title     - Title of the product.&#10;  product_category  - Broad product category that can be used to group reviews &#10;                      (also used to group the dataset into coherent parts).&#10;  star_rating       - The 1-5 star rating of the review.&#10;  helpful_votes     - Number of helpful votes.&#10;  total_votes       - Number of total votes the review received.&#10;  vine              - Review was written as part of the Vine program.&#10;  verified_purchase - The review is on a verified purchase.&#10;  review_headline   - The title of the review.&#10;  review_body       - The review text.&#10;  review_date       - The date the review was written.&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;amazon_us_reviews&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/amazon_us_reviews" />
  <meta itemprop="sameAs" content="https://s3.amazonaws.com/amazon-reviews-pds/readme.html" />
  <meta itemprop="citation" content="" />
</div>
# `amazon_us_reviews`

*   **Description**:

Amazon Customer Reviews (a.k.a. Product Reviews) is one of Amazons iconic
products. In a period of over two decades since the first review in 1995,
millions of Amazon customers have contributed over a hundred million reviews to
express opinions and describe their experiences regarding products on the
Amazon.com website. This makes Amazon Customer Reviews a rich source of
information for academic researchers in the fields of Natural Language
Processing (NLP), Information Retrieval (IR), and Machine Learning (ML), amongst
others. Accordingly, we are releasing this data to further research in multiple
disciplines related to understanding customer product experiences. Specifically,
this dataset was constructed to represent a sample of customer evaluations and
opinions, variation in the perception of a product across geographical regions,
and promotional intent or bias in reviews.

Over 130+ million customer reviews are available to researchers as part of this
release. The data is available in TSV files in the amazon-reviews-pds S3 bucket
in AWS US East Region. Each line in the data files corresponds to an individual
review (tab delimited, with no quote and escape characters).

Each Dataset contains the following columns : marketplace - 2 letter country
code of the marketplace where the review was written. customer_id - Random
identifier that can be used to aggregate reviews written by a single author.
review_id - The unique ID of the review. product_id - The unique Product ID the
review pertains to. In the multilingual dataset the reviews for the same product
in different countries can be grouped by the same product_id. product_parent -
Random identifier that can be used to aggregate reviews for the same product.
product_title - Title of the product. product_category - Broad product category
that can be used to group reviews (also used to group the dataset into coherent
parts). star_rating - The 1-5 star rating of the review. helpful_votes - Number
of helpful votes. total_votes - Number of total votes the review received.
vine - Review was written as part of the Vine program. verified_purchase - The
review is on a verified purchase. review_headline - The title of the review.
review_body - The review text. review_date - The date the review was written.

*   **Homepage**:
    [https://s3.amazonaws.com/amazon-reviews-pds/readme.html](https://s3.amazonaws.com/amazon-reviews-pds/readme.html)
*   **Source code**:
    [`tfds.structured.amazon_us_reviews.AmazonUSReviews`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/structured/amazon_us_reviews.py)
*   **Versions**:
    *   **`0.1.0`** (default): No release notes.
*   **Dataset size**: `Unknown size`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    No
*   **Features**:

```python
FeaturesDict({
    'data': FeaturesDict({
        'customer_id': tf.string,
        'helpful_votes': tf.int32,
        'marketplace': tf.string,
        'product_category': tf.string,
        'product_id': tf.string,
        'product_parent': tf.string,
        'product_title': tf.string,
        'review_body': tf.string,
        'review_date': tf.string,
        'review_headline': tf.string,
        'review_id': tf.string,
        'star_rating': tf.int32,
        'total_votes': tf.int32,
        'verified_purchase': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
        'vine': ClassLabel(shape=(), dtype=tf.int64, num_classes=2),
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `None`

## amazon_us_reviews/Wireless_v1_00 (default config)

*   **Config description**: A dataset consisting of reviews of Amazon
    Wireless_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `1.59 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 9,002,021

## amazon_us_reviews/Watches_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Watches_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `155.42 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 960,872

## amazon_us_reviews/Video_Games_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Video_Games_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `453.19 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,785,997

## amazon_us_reviews/Video_DVD_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Video_DVD_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `1.41 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,069,140

## amazon_us_reviews/Video_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Video_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `132.49 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 380,604

## amazon_us_reviews/Toys_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon Toys_v1_00
    products in US marketplace. Each product has its own version as specified
    with it.
*   **Download size**: `799.61 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 4,864,249

## amazon_us_reviews/Tools_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Tools_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `318.32 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,741,100

## amazon_us_reviews/Sports_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Sports_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `832.06 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 4,850,360

## amazon_us_reviews/Software_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Software_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `89.66 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 341,931

## amazon_us_reviews/Shoes_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Shoes_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `612.50 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 4,366,916

## amazon_us_reviews/Pet_Products_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Pet_Products_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `491.92 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,643,619

## amazon_us_reviews/Personal_Care_Appliances_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Personal_Care_Appliances_v1_00 products in US marketplace. Each product has
    its own version as specified with it.
*   **Download size**: `16.82 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 85,981

## amazon_us_reviews/PC_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon PC_v1_00
    products in US marketplace. Each product has its own version as specified
    with it.
*   **Download size**: `1.41 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 6,908,554

## amazon_us_reviews/Outdoors_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Outdoors_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `428.16 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,302,401

## amazon_us_reviews/Office_Products_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Office_Products_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `488.59 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,642,434

## amazon_us_reviews/Musical_Instruments_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Musical_Instruments_v1_00 products in US marketplace. Each product has its
    own version as specified with it.
*   **Download size**: `184.43 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 904,765

## amazon_us_reviews/Music_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Music_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `1.42 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 4,751,577

## amazon_us_reviews/Mobile_Electronics_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Mobile_Electronics_v1_00 products in US marketplace. Each product has its
    own version as specified with it.
*   **Download size**: `21.81 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 104,975

## amazon_us_reviews/Mobile_Apps_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Mobile_Apps_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `532.11 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,033,376

## amazon_us_reviews/Major_Appliances_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Major_Appliances_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `23.23 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 96,901

## amazon_us_reviews/Luggage_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Luggage_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `57.53 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 348,657

## amazon_us_reviews/Lawn_and_Garden_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Lawn_and_Garden_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `464.22 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,557,288

## amazon_us_reviews/Kitchen_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Kitchen_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `887.63 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 4,880,466

## amazon_us_reviews/Jewelry_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Jewelry_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `235.58 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,767,753

## amazon_us_reviews/Home_Improvement_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Home_Improvement_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `480.02 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,634,781

## amazon_us_reviews/Home_Entertainment_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Home_Entertainment_v1_00 products in US marketplace. Each product has its
    own version as specified with it.
*   **Download size**: `184.22 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 705,889

## amazon_us_reviews/Home_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon Home_v1_00
    products in US marketplace. Each product has its own version as specified
    with it.
*   **Download size**: `1.01 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 6,221,559

## amazon_us_reviews/Health_Personal_Care_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Health_Personal_Care_v1_00 products in US marketplace. Each product has its
    own version as specified with it.
*   **Download size**: `964.34 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,331,449

## amazon_us_reviews/Grocery_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Grocery_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `382.74 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 2,402,458

## amazon_us_reviews/Gift_Card_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Gift_Card_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `11.57 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 149,086

## amazon_us_reviews/Furniture_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Furniture_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `142.08 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 792,113

## amazon_us_reviews/Electronics_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Electronics_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `666.45 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 3,093,869

## amazon_us_reviews/Digital_Video_Games_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Digital_Video_Games_v1_00 products in US marketplace. Each product has its
    own version as specified with it.
*   **Download size**: `26.17 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 145,431

## amazon_us_reviews/Digital_Video_Download_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Digital_Video_Download_v1_00 products in US marketplace. Each product has
    its own version as specified with it.
*   **Download size**: `483.49 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 4,057,147

## amazon_us_reviews/Digital_Software_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Digital_Software_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `18.12 MiB`
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 102,084

## amazon_us_reviews/Digital_Music_Purchase_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Digital_Music_Purchase_v1_00 products in US marketplace. Each product has
    its own version as specified with it.
*   **Download size**: `241.82 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,688,884

## amazon_us_reviews/Digital_Ebook_Purchase_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Digital_Ebook_Purchase_v1_00 products in US marketplace. Each product has
    its own version as specified with it.
*   **Download size**: `2.51 GiB`
*   **Splits**:

Split   | Examples
:------ | ---------:
'train' | 12,520,722

## amazon_us_reviews/Camera_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Camera_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `422.15 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,801,974

## amazon_us_reviews/Books_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Books_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `2.55 GiB`
*   **Splits**:

Split   | Examples
:------ | ---------:
'train' | 10,319,090

## amazon_us_reviews/Beauty_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Beauty_v1_00 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `871.73 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,115,666

## amazon_us_reviews/Baby_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon Baby_v1_00
    products in US marketplace. Each product has its own version as specified
    with it.
*   **Download size**: `340.84 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 1,752,932

## amazon_us_reviews/Automotive_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Automotive_v1_00 products in US marketplace. Each product has its own
    version as specified with it.
*   **Download size**: `555.18 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 3,514,942

## amazon_us_reviews/Apparel_v1_00

*   **Config description**: A dataset consisting of reviews of Amazon
    Apparel_v1_00 products in US marketplace. Each product has its own version
    as specified with it.
*   **Download size**: `618.59 MiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,906,333

## amazon_us_reviews/Digital_Ebook_Purchase_v1_01

*   **Config description**: A dataset consisting of reviews of Amazon
    Digital_Ebook_Purchase_v1_01 products in US marketplace. Each product has
    its own version as specified with it.
*   **Download size**: `1.21 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 5,101,693

## amazon_us_reviews/Books_v1_01

*   **Config description**: A dataset consisting of reviews of Amazon
    Books_v1_01 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `2.51 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 6,106,719

## amazon_us_reviews/Books_v1_02

*   **Config description**: A dataset consisting of reviews of Amazon
    Books_v1_02 products in US marketplace. Each product has its own version as
    specified with it.
*   **Download size**: `1.24 GiB`
*   **Splits**:

Split   | Examples
:------ | --------:
'train' | 3,105,520
