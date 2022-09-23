---
annotations_creators:
- no-annotation
language:
- en
language_creators:
- found
license:
- other
multilinguality:
- monolingual
pretty_name: Amazon US Reviews
size_categories:
- 100M<n<1B
source_datasets:
- original
task_categories:
- summarization
- text-generation
- fill-mask
- text-classification
task_ids:
- text-scoring
- language-modeling
- masked-language-modeling
- sentiment-classification
- sentiment-scoring
- topic-classification
paperswithcode_id: null
dataset_info:
- config_name: Books_v1_01
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 6997552259
    num_examples: 6106719
  download_size: 2692708591
  dataset_size: 6997552259
- config_name: Watches_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 458976082
    num_examples: 960872
  download_size: 162973819
  dataset_size: 458976082
- config_name: Personal_Care_Appliances_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 49036547
    num_examples: 85981
  download_size: 17634794
  dataset_size: 49036547
- config_name: Mobile_Electronics_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 63293377
    num_examples: 104975
  download_size: 22870508
  dataset_size: 63293377
- config_name: Digital_Video_Games_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 80176851
    num_examples: 145431
  download_size: 27442648
  dataset_size: 80176851
- config_name: Digital_Software_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 58782931
    num_examples: 102084
  download_size: 18997559
  dataset_size: 58782931
- config_name: Major_Appliances_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 67642424
    num_examples: 96901
  download_size: 24359816
  dataset_size: 67642424
- config_name: Gift_Card_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 47188062
    num_examples: 149086
  download_size: 12134676
  dataset_size: 47188062
- config_name: Video_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 356264426
    num_examples: 380604
  download_size: 138929896
  dataset_size: 356264426
- config_name: Luggage_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 167354173
    num_examples: 348657
  download_size: 60320191
  dataset_size: 167354173
- config_name: Software_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 266020595
    num_examples: 341931
  download_size: 94010685
  dataset_size: 266020595
- config_name: Video_Games_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1291054668
    num_examples: 1785997
  download_size: 475199894
  dataset_size: 1291054668
- config_name: Furniture_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 405212374
    num_examples: 792113
  download_size: 148982796
  dataset_size: 405212374
- config_name: Musical_Instruments_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 518908568
    num_examples: 904765
  download_size: 193389086
  dataset_size: 518908568
- config_name: Digital_Music_Purchase_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 710546079
    num_examples: 1688884
  download_size: 253570168
  dataset_size: 710546079
- config_name: Books_v1_02
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 3387034903
    num_examples: 3105520
  download_size: 1329539135
  dataset_size: 3387034903
- config_name: Home_Entertainment_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 534333848
    num_examples: 705889
  download_size: 193168458
  dataset_size: 534333848
- config_name: Grocery_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1072289473
    num_examples: 2402458
  download_size: 401337166
  dataset_size: 1072289473
- config_name: Outdoors_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1172986088
    num_examples: 2302401
  download_size: 448963100
  dataset_size: 1172986088
- config_name: Pet_Products_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1355659812
    num_examples: 2643619
  download_size: 515815253
  dataset_size: 1355659812
- config_name: Video_DVD_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 3953234561
    num_examples: 5069140
  download_size: 1512355451
  dataset_size: 3953234561
- config_name: Apparel_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 2256558450
    num_examples: 5906333
  download_size: 648641286
  dataset_size: 2256558450
- config_name: PC_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 3982684438
    num_examples: 6908554
  download_size: 1512903923
  dataset_size: 3982684438
- config_name: Tools_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 872273119
    num_examples: 1741100
  download_size: 333782939
  dataset_size: 872273119
- config_name: Jewelry_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 703275869
    num_examples: 1767753
  download_size: 247022254
  dataset_size: 703275869
- config_name: Baby_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 956952590
    num_examples: 1752932
  download_size: 357392893
  dataset_size: 956952590
- config_name: Home_Improvement_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1329688315
    num_examples: 2634781
  download_size: 503339178
  dataset_size: 1329688315
- config_name: Camera_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1187101912
    num_examples: 1801974
  download_size: 442653086
  dataset_size: 1187101912
- config_name: Lawn_and_Garden_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1272255987
    num_examples: 2557288
  download_size: 486772662
  dataset_size: 1272255987
- config_name: Office_Products_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1370685534
    num_examples: 2642434
  download_size: 512323500
  dataset_size: 1370685534
- config_name: Electronics_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1875406721
    num_examples: 3093869
  download_size: 698828243
  dataset_size: 1875406721
- config_name: Automotive_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1520191087
    num_examples: 3514942
  download_size: 582145299
  dataset_size: 1520191087
- config_name: Digital_Video_Download_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1484214187
    num_examples: 4057147
  download_size: 506979922
  dataset_size: 1484214187
- config_name: Mobile_Apps_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1627857158
    num_examples: 5033376
  download_size: 557959415
  dataset_size: 1627857158
- config_name: Shoes_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 1781283508
    num_examples: 4366916
  download_size: 642255314
  dataset_size: 1781283508
- config_name: Toys_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 2197820069
    num_examples: 4864249
  download_size: 838451398
  dataset_size: 2197820069
- config_name: Sports_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 2241349145
    num_examples: 4850360
  download_size: 872478735
  dataset_size: 2241349145
- config_name: Kitchen_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 2453735305
    num_examples: 4880466
  download_size: 930744854
  dataset_size: 2453735305
- config_name: Beauty_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 2399292506
    num_examples: 5115666
  download_size: 914070021
  dataset_size: 2399292506
- config_name: Music_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 3900138839
    num_examples: 4751577
  download_size: 1521994296
  dataset_size: 3900138839
- config_name: Health_Personal_Care_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 2679427491
    num_examples: 5331449
  download_size: 1011180212
  dataset_size: 2679427491
- config_name: Digital_Ebook_Purchase_v1_01
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 3470453859
    num_examples: 5101693
  download_size: 1294879074
  dataset_size: 3470453859
- config_name: Home_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 2796680249
    num_examples: 6221559
  download_size: 1081002012
  dataset_size: 2796680249
- config_name: Wireless_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 4633213433
    num_examples: 9002021
  download_size: 1704713674
  dataset_size: 4633213433
- config_name: Books_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 7197687124
    num_examples: 10319090
  download_size: 2740337188
  dataset_size: 7197687124
- config_name: Digital_Ebook_Purchase_v1_00
  features:
  - name: marketplace
    dtype: string
  - name: customer_id
    dtype: string
  - name: review_id
    dtype: string
  - name: product_id
    dtype: string
  - name: product_parent
    dtype: string
  - name: product_title
    dtype: string
  - name: product_category
    dtype: string
  - name: star_rating
    dtype: int32
  - name: helpful_votes
    dtype: int32
  - name: total_votes
    dtype: int32
  - name: vine
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: verified_purchase
    dtype:
      class_label:
        names:
          0: N
          1: Y
  - name: review_headline
    dtype: string
  - name: review_body
    dtype: string
  - name: review_date
    dtype: string
  splits:
  - name: train
    num_bytes: 7302303804
    num_examples: 12520722
  download_size: 2689739299
  dataset_size: 7302303804
---

# Dataset Card for "amazon_us_reviews"

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

- **Homepage:** [https://s3.amazonaws.com/amazon-reviews-pds/readme.html](https://s3.amazonaws.com/amazon-reviews-pds/readme.html)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 30877.39 MB
- **Size of the generated dataset:** 78983.49 MB
- **Total amount of disk used:** 109860.89 MB

### Dataset Summary

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

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

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

### Data Fields

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

### Data Splits

|      name      | train  |
|----------------|-------:|
|Apparel_v1_00 | 5906333|
|Automotive_v1_00 | 3514942|
|Baby_v1_00 | 1752932|
|Beauty_v1_00 | 5115666|
|Books_v1_00 | 10319090|
|Books_v1_01 | 6106719|
|Books_v1_02 | 3105520|
|Camera_v1_00 | 1801974|
|Digital_Ebook_Purchase_v1_00 | 12520722|
|Digital_Ebook_Purchase_v1_01 | 5101693|
|Digital_Music_Purchase_v1_00 | 1688884|
|Digital_Software_v1_00 | 102084|
|Digital_Video_Download_v1_00 | 4057147|
|Digital_Video_Games_v1_00 | 145431|
|Electronics_v1_00 | 3093869|
|Furniture_v1_00 | 792113|
|Gift_Card_v1_00 | 149086|
|Grocery_v1_00 | 2402458|
|Health_Personal_Care_v1_00 | 5331449|
|Home_Entertainment_v1_00 | 705889|
|Home_Improvement_v1_00 | 2634781|
|Home_v1_00 | 6221559|
|Jewelry_v1_00 | 1767753|
|Kitchen_v1_00 | 4880466|
|Lawn_and_Garden_v1_00 | 2557288|
|Luggage_v1_00 | 348657|
|Major_Appliances_v1_00 | 96901|
|Mobile_Apps_v1_00 | 5033376|
|Mobile_Electronics_v1_00 | 104975|
|Music_v1_00 | 4751577|
|Musical_Instruments_v1_00 | 904765|
|Office_Products_v1_00 | 2642434|
|Outdoors_v1_00 | 2302401|
|PC_v1_00 | 6908554|
|Personal_Care_Appliances_v1_00 | 85981|
|Pet_Products_v1_00 | 2643619|
|Shoes_v1_00 | 4366916|
|Software_v1_00 | 341931|
|Sports_v1_00 | 4850360|
|Tools_v1_00 | 1741100|
|Toys_v1_00 | 4864249|
|Video_DVD_v1_00 | 5069140|
|Video_Games_v1_00 | 1785997|
|Video_v1_00 | 380604|
|Watches_v1_00 | 960872|
|Wireless_v1_00 | 9002021|

## Dataset Creation

### Curation Rationale

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the source language producers?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Annotations

#### Annotation process

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

#### Who are the annotators?

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Personal and Sensitive Information

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Discussion of Biases

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Other Known Limitations

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Additional Information

### Dataset Curators

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Licensing Information

https://s3.amazonaws.com/amazon-reviews-pds/LICENSE.txt

By accessing the Amazon Customer Reviews Library ("Reviews Library"), you agree that the
Reviews Library is an Amazon Service subject to the [Amazon.com Conditions of Use](https://www.amazon.com/gp/help/customer/display.html/ref=footer_cou?ie=UTF8&nodeId=508088)
and you agree to be bound by them, with the following additional conditions:

In addition to the license rights granted under the Conditions of Use,
Amazon or its content providers grant you a limited, non-exclusive, non-transferable,
non-sublicensable, revocable license to access and use the Reviews Library
for purposes of academic research.
You may not resell, republish, or make any commercial use of the Reviews Library
or its contents, including use of the Reviews Library for commercial research,
such as research related to a funding or consultancy contract, internship, or
other relationship in which the results are provided for a fee or delivered
to a for-profit organization. You may not (a) link or associate content
in the Reviews Library with any personal information (including Amazon customer accounts),
or (b) attempt to determine the identity of the author of any content in the
Reviews Library.
If you violate any of the foregoing conditions, your license to access and use the
Reviews Library will automatically terminate without prejudice to any of the
other rights or remedies Amazon may have.

### Citation Information

No citation information.

### Contributions

Thanks to [@joeddav](https://github.com/joeddav) for adding this dataset.