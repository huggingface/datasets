---
annotations_creators:
- found
language_creators:
- found
language:
- af
- ar
- bg
- bn
- de
- el
- en
- es
- et
- eu
- fa
- fi
- fr
- he
- hi
- hu
- id
- it
- ja
- jv
- ka
- kk
- ko
- ml
- mr
- ms
- my
- nl
- pt
- ru
- sw
- ta
- te
- th
- tl
- tr
- ur
- vi
- yo
- zh
language_bcp47:
- fa-IR
license:
- apache-2.0
- cc-by-4.0
- cc-by-2.0
- cc-by-sa-4.0
- other
- cc-by-nc-4.0
license_details: Licence Universal Dependencies v2.5
multilinguality:
- multilingual
- translation
pretty_name: XTREME
size_categories:
- n<1K
- 1K<n<10K
- 10K<n<100K
- 100K<n<1M
source_datasets:
- extended|xnli
- extended|paws-x
- extended|wikiann
- extended|xquad
- extended|mlqa
- extended|tydiqa
- extended|tatoeba
- extended|squad
task_categories:
- multiple-choice
- question-answering
- token-classification
- text-classification
- text-retrieval
- token-classification
task_ids:
- multiple-choice-qa
- extractive-qa
- open-domain-qa
- natural-language-inference
- text-classification-other-paraphrase-identification
- text-retrieval-other-parallel-sentence-retrieval
- named-entity-recognition
- part-of-speech
paperswithcode_id: xtreme
configs:
- MLQA.ar.ar
- MLQA.ar.de
- MLQA.ar.en
- MLQA.ar.es
- MLQA.ar.hi
- MLQA.ar.vi
- MLQA.ar.zh
- MLQA.de.ar
- MLQA.de.de
- MLQA.de.en
- MLQA.de.es
- MLQA.de.hi
- MLQA.de.vi
- MLQA.de.zh
- MLQA.en.ar
- MLQA.en.de
- MLQA.en.en
- MLQA.en.es
- MLQA.en.hi
- MLQA.en.vi
- MLQA.en.zh
- MLQA.es.ar
- MLQA.es.de
- MLQA.es.en
- MLQA.es.es
- MLQA.es.hi
- MLQA.es.vi
- MLQA.es.zh
- MLQA.hi.ar
- MLQA.hi.de
- MLQA.hi.en
- MLQA.hi.es
- MLQA.hi.hi
- MLQA.hi.vi
- MLQA.hi.zh
- MLQA.vi.ar
- MLQA.vi.de
- MLQA.vi.en
- MLQA.vi.es
- MLQA.vi.hi
- MLQA.vi.vi
- MLQA.vi.zh
- MLQA.zh.ar
- MLQA.zh.de
- MLQA.zh.en
- MLQA.zh.es
- MLQA.zh.hi
- MLQA.zh.vi
- MLQA.zh.zh
- PAN-X.af
- PAN-X.ar
- PAN-X.bg
- PAN-X.bn
- PAN-X.de
- PAN-X.el
- PAN-X.en
- PAN-X.es
- PAN-X.et
- PAN-X.eu
- PAN-X.fa
- PAN-X.fi
- PAN-X.fr
- PAN-X.he
- PAN-X.hi
- PAN-X.hu
- PAN-X.id
- PAN-X.it
- PAN-X.ja
- PAN-X.jv
- PAN-X.ka
- PAN-X.kk
- PAN-X.ko
- PAN-X.ml
- PAN-X.mr
- PAN-X.ms
- PAN-X.my
- PAN-X.nl
- PAN-X.pt
- PAN-X.ru
- PAN-X.sw
- PAN-X.ta
- PAN-X.te
- PAN-X.th
- PAN-X.tl
- PAN-X.tr
- PAN-X.ur
- PAN-X.vi
- PAN-X.yo
- PAN-X.zh
- PAWS-X.de
- PAWS-X.en
- PAWS-X.es
- PAWS-X.fr
- PAWS-X.ja
- PAWS-X.ko
- PAWS-X.zh
- SQuAD
- XNLI
- XQuAD
- bucc18.de
- bucc18.fr
- bucc18.ru
- bucc18.zh
- tatoeba.afr
- tatoeba.ara
- tatoeba.ben
- tatoeba.bul
- tatoeba.cmn
- tatoeba.deu
- tatoeba.ell
- tatoeba.est
- tatoeba.eus
- tatoeba.fin
- tatoeba.fra
- tatoeba.heb
- tatoeba.hin
- tatoeba.hun
- tatoeba.ind
- tatoeba.ita
- tatoeba.jav
- tatoeba.jpn
- tatoeba.kat
- tatoeba.kaz
- tatoeba.kor
- tatoeba.mal
- tatoeba.mar
- tatoeba.nld
- tatoeba.pes
- tatoeba.por
- tatoeba.rus
- tatoeba.spa
- tatoeba.swh
- tatoeba.tam
- tatoeba.tel
- tatoeba.tgl
- tatoeba.tha
- tatoeba.tur
- tatoeba.urd
- tatoeba.vie
- tydiqa
- udpos.Afrikans
- udpos.Arabic
- udpos.Basque
- udpos.Bulgarian
- udpos.Chinese
- udpos.Dutch
- udpos.English
- udpos.Estonian
- udpos.Finnish
- udpos.French
- udpos.German
- udpos.Greek
- udpos.Hebrew
- udpos.Hindi
- udpos.Hungarian
- udpos.Indonesian
- udpos.Italian
- udpos.Japanese
- udpos.Kazakh
- udpos.Korean
- udpos.Marathi
- udpos.Persian
- udpos.Portuguese
- udpos.Russian
- udpos.Spanish
- udpos.Tagalog
- udpos.Tamil
- udpos.Telugu
- udpos.Thai
- udpos.Turkish
- udpos.Urdu
- udpos.Vietnamese
- udpos.Yoruba
dataset_info:
- config_name: XNLI
  features:
  - name: language
    dtype: string
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: gold_label
    dtype: string
  splits:
  - name: test
    num_bytes: 20359500
    num_examples: 75150
  - name: validation
    num_bytes: 10049303
    num_examples: 37350
  download_size: 17865352
  dataset_size: 30408803
- config_name: tydiqa
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: train
    num_bytes: 52948607
    num_examples: 49881
  - name: validation
    num_bytes: 5006461
    num_examples: 5077
  download_size: 63621485
  dataset_size: 57955068
- config_name: SQuAD
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: train
    num_bytes: 79317110
    num_examples: 87599
  - name: validation
    num_bytes: 10472653
    num_examples: 10570
  download_size: 35142551
  dataset_size: 89789763
- config_name: PAN-X.af
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 257204
    num_examples: 1000
  - name: train
    num_bytes: 1321396
    num_examples: 5000
  - name: validation
    num_bytes: 259709
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1838309
- config_name: PAN-X.ar
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1811983
    num_examples: 10000
  - name: train
    num_bytes: 3634136
    num_examples: 20000
  - name: validation
    num_bytes: 1808303
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7254422
- config_name: PAN-X.bg
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2306158
    num_examples: 10000
  - name: train
    num_bytes: 4600773
    num_examples: 20000
  - name: validation
    num_bytes: 2310314
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9217245
- config_name: PAN-X.bn
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 159282
    num_examples: 1000
  - name: train
    num_bytes: 1568845
    num_examples: 10000
  - name: validation
    num_bytes: 159088
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1887215
- config_name: PAN-X.de
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2377639
    num_examples: 10000
  - name: train
    num_bytes: 4762352
    num_examples: 20000
  - name: validation
    num_bytes: 2381565
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9521556
- config_name: PAN-X.el
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2547594
    num_examples: 10000
  - name: train
    num_bytes: 5063176
    num_examples: 20000
  - name: validation
    num_bytes: 2533806
    num_examples: 10000
  download_size: 234008884
  dataset_size: 10144576
- config_name: PAN-X.en
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1916220
    num_examples: 10000
  - name: train
    num_bytes: 3823474
    num_examples: 20000
  - name: validation
    num_bytes: 1920069
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7659763
- config_name: PAN-X.es
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1602291
    num_examples: 10000
  - name: train
    num_bytes: 3199161
    num_examples: 20000
  - name: validation
    num_bytes: 1592525
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6393977
- config_name: PAN-X.et
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2021409
    num_examples: 10000
  - name: train
    num_bytes: 3023211
    num_examples: 15000
  - name: validation
    num_bytes: 2030160
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7074780
- config_name: PAN-X.eu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2249835
    num_examples: 10000
  - name: train
    num_bytes: 2292327
    num_examples: 10000
  - name: validation
    num_bytes: 2296335
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6838497
- config_name: PAN-X.fa
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1770284
    num_examples: 10000
  - name: train
    num_bytes: 3529354
    num_examples: 20000
  - name: validation
    num_bytes: 1782306
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7081944
- config_name: PAN-X.fi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2130665
    num_examples: 10000
  - name: train
    num_bytes: 4273793
    num_examples: 20000
  - name: validation
    num_bytes: 2131769
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8536227
- config_name: PAN-X.fr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1675785
    num_examples: 10000
  - name: train
    num_bytes: 3335424
    num_examples: 20000
  - name: validation
    num_bytes: 1664190
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6675399
- config_name: PAN-X.he
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2318756
    num_examples: 10000
  - name: train
    num_bytes: 4667100
    num_examples: 20000
  - name: validation
    num_bytes: 2332760
    num_examples: 10000
  download_size: 234008884
  dataset_size: 9318616
- config_name: PAN-X.hi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 196190
    num_examples: 1000
  - name: train
    num_bytes: 964212
    num_examples: 5000
  - name: validation
    num_bytes: 190671
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1351073
- config_name: PAN-X.hu
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2249779
    num_examples: 10000
  - name: train
    num_bytes: 4499914
    num_examples: 20000
  - name: validation
    num_bytes: 2211851
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8961544
- config_name: PAN-X.id
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1536879
    num_examples: 10000
  - name: train
    num_bytes: 3084007
    num_examples: 20000
  - name: validation
    num_bytes: 1537979
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6158865
- config_name: PAN-X.it
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1928408
    num_examples: 10000
  - name: train
    num_bytes: 3874663
    num_examples: 20000
  - name: validation
    num_bytes: 1908529
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7711600
- config_name: PAN-X.ja
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 6448960
    num_examples: 10000
  - name: train
    num_bytes: 12670401
    num_examples: 20000
  - name: validation
    num_bytes: 6323003
    num_examples: 10000
  download_size: 234008884
  dataset_size: 25442364
- config_name: PAN-X.jv
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 16917
    num_examples: 100
  - name: train
    num_bytes: 16106
    num_examples: 100
  - name: validation
    num_bytes: 14600
    num_examples: 100
  download_size: 234008884
  dataset_size: 47623
- config_name: PAN-X.ka
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2824641
    num_examples: 10000
  - name: train
    num_bytes: 2777362
    num_examples: 10000
  - name: validation
    num_bytes: 2806901
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8408904
- config_name: PAN-X.kk
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 236724
    num_examples: 1000
  - name: train
    num_bytes: 240276
    num_examples: 1000
  - name: validation
    num_bytes: 238109
    num_examples: 1000
  download_size: 234008884
  dataset_size: 715109
- config_name: PAN-X.ko
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2138294
    num_examples: 10000
  - name: train
    num_bytes: 4284733
    num_examples: 20000
  - name: validation
    num_bytes: 2138167
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8561194
- config_name: PAN-X.ml
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 276926
    num_examples: 1000
  - name: train
    num_bytes: 2865204
    num_examples: 10000
  - name: validation
    num_bytes: 290755
    num_examples: 1000
  download_size: 234008884
  dataset_size: 3432885
- config_name: PAN-X.mr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 255904
    num_examples: 1000
  - name: train
    num_bytes: 1248259
    num_examples: 5000
  - name: validation
    num_bytes: 245358
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1749521
- config_name: PAN-X.ms
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 147168
    num_examples: 1000
  - name: train
    num_bytes: 2965048
    num_examples: 20000
  - name: validation
    num_bytes: 147515
    num_examples: 1000
  download_size: 234008884
  dataset_size: 3259731
- config_name: PAN-X.my
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 37366
    num_examples: 100
  - name: train
    num_bytes: 32735
    num_examples: 100
  - name: validation
    num_bytes: 40428
    num_examples: 100
  download_size: 234008884
  dataset_size: 110529
- config_name: PAN-X.nl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2038638
    num_examples: 10000
  - name: train
    num_bytes: 4062189
    num_examples: 20000
  - name: validation
    num_bytes: 2016856
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8117683
- config_name: PAN-X.pt
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1562625
    num_examples: 10000
  - name: train
    num_bytes: 3149283
    num_examples: 20000
  - name: validation
    num_bytes: 1575141
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6287049
- config_name: PAN-X.ru
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 2074145
    num_examples: 10000
  - name: train
    num_bytes: 4121791
    num_examples: 20000
  - name: validation
    num_bytes: 2053169
    num_examples: 10000
  download_size: 234008884
  dataset_size: 8249105
- config_name: PAN-X.sw
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 140231
    num_examples: 1000
  - name: train
    num_bytes: 135911
    num_examples: 1000
  - name: validation
    num_bytes: 136368
    num_examples: 1000
  download_size: 234008884
  dataset_size: 412510
- config_name: PAN-X.ta
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 278114
    num_examples: 1000
  - name: train
    num_bytes: 4122130
    num_examples: 15000
  - name: validation
    num_bytes: 277625
    num_examples: 1000
  download_size: 234008884
  dataset_size: 4677869
- config_name: PAN-X.te
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 296963
    num_examples: 1000
  - name: train
    num_bytes: 295410
    num_examples: 1000
  - name: validation
    num_bytes: 293281
    num_examples: 1000
  download_size: 234008884
  dataset_size: 885654
- config_name: PAN-X.th
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 13586928
    num_examples: 10000
  - name: train
    num_bytes: 27133029
    num_examples: 20000
  - name: validation
    num_bytes: 13262737
    num_examples: 10000
  download_size: 234008884
  dataset_size: 53982694
- config_name: PAN-X.tl
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 117904
    num_examples: 1000
  - name: train
    num_bytes: 1168717
    num_examples: 10000
  - name: validation
    num_bytes: 114156
    num_examples: 1000
  download_size: 234008884
  dataset_size: 1400777
- config_name: PAN-X.tr
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1911503
    num_examples: 10000
  - name: train
    num_bytes: 3779170
    num_examples: 20000
  - name: validation
    num_bytes: 1915352
    num_examples: 10000
  download_size: 234008884
  dataset_size: 7606025
- config_name: PAN-X.ur
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 151922
    num_examples: 1000
  - name: train
    num_bytes: 3072276
    num_examples: 20000
  - name: validation
    num_bytes: 152148
    num_examples: 1000
  download_size: 234008884
  dataset_size: 3376346
- config_name: PAN-X.vi
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 1580216
    num_examples: 10000
  - name: train
    num_bytes: 3153227
    num_examples: 20000
  - name: validation
    num_bytes: 1565143
    num_examples: 10000
  download_size: 234008884
  dataset_size: 6298586
- config_name: PAN-X.yo
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 13533
    num_examples: 100
  - name: train
    num_bytes: 14709
    num_examples: 100
  - name: validation
    num_bytes: 13245
    num_examples: 100
  download_size: 234008884
  dataset_size: 41487
- config_name: PAN-X.zh
  features:
  - name: tokens
    sequence: string
  - name: ner_tags
    sequence:
      class_label:
        names:
          0: O
          1: B-PER
          2: I-PER
          3: B-ORG
          4: I-ORG
          5: B-LOC
          6: I-LOC
  - name: langs
    sequence: string
  splits:
  - name: test
    num_bytes: 4363172
    num_examples: 10000
  - name: train
    num_bytes: 8832051
    num_examples: 20000
  - name: validation
    num_bytes: 4491325
    num_examples: 10000
  download_size: 234008884
  dataset_size: 17686548
- config_name: MLQA.ar.ar
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 8368114
    num_examples: 5335
  - name: validation
    num_bytes: 824108
    num_examples: 517
  download_size: 75719050
  dataset_size: 9192222
- config_name: MLQA.ar.de
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 2183942
    num_examples: 1649
  - name: validation
    num_bytes: 364837
    num_examples: 207
  download_size: 75719050
  dataset_size: 2548779
- config_name: MLQA.ar.vi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 3290629
    num_examples: 2047
  - name: validation
    num_bytes: 288446
    num_examples: 163
  download_size: 75719050
  dataset_size: 3579075
- config_name: MLQA.ar.zh
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 3229872
    num_examples: 1912
  - name: validation
    num_bytes: 340049
    num_examples: 188
  download_size: 75719050
  dataset_size: 3569921
- config_name: MLQA.ar.en
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 8225662
    num_examples: 5335
  - name: validation
    num_bytes: 810089
    num_examples: 517
  download_size: 75719050
  dataset_size: 9035751
- config_name: MLQA.ar.es
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 3041378
    num_examples: 1978
  - name: validation
    num_bytes: 228180
    num_examples: 161
  download_size: 75719050
  dataset_size: 3269558
- config_name: MLQA.ar.hi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 3039396
    num_examples: 1831
  - name: validation
    num_bytes: 281770
    num_examples: 186
  download_size: 75719050
  dataset_size: 3321166
- config_name: MLQA.de.ar
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1620006
    num_examples: 1649
  - name: validation
    num_bytes: 200174
    num_examples: 207
  download_size: 75719050
  dataset_size: 1820180
- config_name: MLQA.de.de
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4366102
    num_examples: 4517
  - name: validation
    num_bytes: 488367
    num_examples: 512
  download_size: 75719050
  dataset_size: 4854469
- config_name: MLQA.de.vi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1688483
    num_examples: 1675
  - name: validation
    num_bytes: 216075
    num_examples: 182
  download_size: 75719050
  dataset_size: 1904558
- config_name: MLQA.de.zh
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1679180
    num_examples: 1621
  - name: validation
    num_bytes: 184318
    num_examples: 190
  download_size: 75719050
  dataset_size: 1863498
- config_name: MLQA.de.en
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4343144
    num_examples: 4517
  - name: validation
    num_bytes: 485894
    num_examples: 512
  download_size: 75719050
  dataset_size: 4829038
- config_name: MLQA.de.es
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1716615
    num_examples: 1776
  - name: validation
    num_bytes: 170582
    num_examples: 196
  download_size: 75719050
  dataset_size: 1887197
- config_name: MLQA.de.hi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1371074
    num_examples: 1430
  - name: validation
    num_bytes: 153871
    num_examples: 163
  download_size: 75719050
  dataset_size: 1524945
- config_name: MLQA.vi.ar
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 3205185
    num_examples: 2047
  - name: validation
    num_bytes: 230335
    num_examples: 163
  download_size: 75719050
  dataset_size: 3435520
- config_name: MLQA.vi.de
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 2227033
    num_examples: 1675
  - name: validation
    num_bytes: 277185
    num_examples: 182
  download_size: 75719050
  dataset_size: 2504218
- config_name: MLQA.vi.vi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 7922085
    num_examples: 5495
  - name: validation
    num_bytes: 726518
    num_examples: 511
  download_size: 75719050
  dataset_size: 8648603
- config_name: MLQA.vi.zh
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 2989660
    num_examples: 1943
  - name: validation
    num_bytes: 269389
    num_examples: 184
  download_size: 75719050
  dataset_size: 3259049
- config_name: MLQA.vi.en
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 7843431
    num_examples: 5495
  - name: validation
    num_bytes: 719273
    num_examples: 511
  download_size: 75719050
  dataset_size: 8562704
- config_name: MLQA.vi.es
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 2866597
    num_examples: 2018
  - name: validation
    num_bytes: 283461
    num_examples: 189
  download_size: 75719050
  dataset_size: 3150058
- config_name: MLQA.vi.hi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 2776664
    num_examples: 1947
  - name: validation
    num_bytes: 255007
    num_examples: 177
  download_size: 75719050
  dataset_size: 3031671
- config_name: MLQA.zh.ar
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1731483
    num_examples: 1912
  - name: validation
    num_bytes: 175349
    num_examples: 188
  download_size: 75719050
  dataset_size: 1906832
- config_name: MLQA.zh.de
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1390018
    num_examples: 1621
  - name: validation
    num_bytes: 174605
    num_examples: 190
  download_size: 75719050
  dataset_size: 1564623
- config_name: MLQA.zh.vi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1806186
    num_examples: 1943
  - name: validation
    num_bytes: 172934
    num_examples: 184
  download_size: 75719050
  dataset_size: 1979120
- config_name: MLQA.zh.zh
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4422350
    num_examples: 5137
  - name: validation
    num_bytes: 443810
    num_examples: 504
  download_size: 75719050
  dataset_size: 4866160
- config_name: MLQA.zh.en
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4450985
    num_examples: 5137
  - name: validation
    num_bytes: 446868
    num_examples: 504
  download_size: 75719050
  dataset_size: 4897853
- config_name: MLQA.zh.es
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1736283
    num_examples: 1947
  - name: validation
    num_bytes: 138073
    num_examples: 161
  download_size: 75719050
  dataset_size: 1874356
- config_name: MLQA.zh.hi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1578219
    num_examples: 1767
  - name: validation
    num_bytes: 184401
    num_examples: 189
  download_size: 75719050
  dataset_size: 1762620
- config_name: MLQA.en.ar
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 6739219
    num_examples: 5335
  - name: validation
    num_bytes: 630843
    num_examples: 517
  download_size: 75719050
  dataset_size: 7370062
- config_name: MLQA.en.de
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 5056722
    num_examples: 4517
  - name: validation
    num_bytes: 594936
    num_examples: 512
  download_size: 75719050
  dataset_size: 5651658
- config_name: MLQA.en.vi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 7056698
    num_examples: 5495
  - name: validation
    num_bytes: 640646
    num_examples: 511
  download_size: 75719050
  dataset_size: 7697344
- config_name: MLQA.en.zh
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 6539307
    num_examples: 5137
  - name: validation
    num_bytes: 608444
    num_examples: 504
  download_size: 75719050
  dataset_size: 7147751
- config_name: MLQA.en.en
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 14004648
    num_examples: 11590
  - name: validation
    num_bytes: 1329112
    num_examples: 1148
  download_size: 75719050
  dataset_size: 15333760
- config_name: MLQA.en.es
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 6179249
    num_examples: 5253
  - name: validation
    num_bytes: 555462
    num_examples: 500
  download_size: 75719050
  dataset_size: 6734711
- config_name: MLQA.en.hi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 6378866
    num_examples: 4918
  - name: validation
    num_bytes: 623171
    num_examples: 507
  download_size: 75719050
  dataset_size: 7002037
- config_name: MLQA.es.ar
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1740282
    num_examples: 1978
  - name: validation
    num_bytes: 148649
    num_examples: 161
  download_size: 75719050
  dataset_size: 1888931
- config_name: MLQA.es.de
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1404025
    num_examples: 1776
  - name: validation
    num_bytes: 144186
    num_examples: 196
  download_size: 75719050
  dataset_size: 1548211
- config_name: MLQA.es.vi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1747969
    num_examples: 2018
  - name: validation
    num_bytes: 176841
    num_examples: 189
  download_size: 75719050
  dataset_size: 1924810
- config_name: MLQA.es.zh
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1678451
    num_examples: 1947
  - name: validation
    num_bytes: 126646
    num_examples: 161
  download_size: 75719050
  dataset_size: 1805097
- config_name: MLQA.es.en
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4362737
    num_examples: 5253
  - name: validation
    num_bytes: 419068
    num_examples: 500
  download_size: 75719050
  dataset_size: 4781805
- config_name: MLQA.es.es
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4394333
    num_examples: 5253
  - name: validation
    num_bytes: 422071
    num_examples: 500
  download_size: 75719050
  dataset_size: 4816404
- config_name: MLQA.es.hi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 1523523
    num_examples: 1723
  - name: validation
    num_bytes: 181834
    num_examples: 187
  download_size: 75719050
  dataset_size: 1705357
- config_name: MLQA.hi.ar
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4445589
    num_examples: 1831
  - name: validation
    num_bytes: 410424
    num_examples: 186
  download_size: 75719050
  dataset_size: 4856013
- config_name: MLQA.hi.de
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 3022864
    num_examples: 1430
  - name: validation
    num_bytes: 301713
    num_examples: 163
  download_size: 75719050
  dataset_size: 3324577
- config_name: MLQA.hi.vi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4743484
    num_examples: 1947
  - name: validation
    num_bytes: 419106
    num_examples: 177
  download_size: 75719050
  dataset_size: 5162590
- config_name: MLQA.hi.zh
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 4354875
    num_examples: 1767
  - name: validation
    num_bytes: 424246
    num_examples: 189
  download_size: 75719050
  dataset_size: 4779121
- config_name: MLQA.hi.en
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 11449261
    num_examples: 4918
  - name: validation
    num_bytes: 1097857
    num_examples: 507
  download_size: 75719050
  dataset_size: 12547118
- config_name: MLQA.hi.es
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 3862229
    num_examples: 1723
  - name: validation
    num_bytes: 420402
    num_examples: 187
  download_size: 75719050
  dataset_size: 4282631
- config_name: MLQA.hi.hi
  features:
  - name: id
    dtype: string
  - name: title
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: test
    num_bytes: 11810475
    num_examples: 4918
  - name: validation
    num_bytes: 1136784
    num_examples: 507
  download_size: 75719050
  dataset_size: 12947259
- config_name: XQuAD.ar
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 1722799
    num_examples: 1190
  download_size: 1582988
  dataset_size: 1722799
- config_name: XQuAD.de
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 1283301
    num_examples: 1190
  download_size: 669810
  dataset_size: 1283301
- config_name: XQuAD.vi
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 1477239
    num_examples: 1190
  download_size: 911401
  dataset_size: 1477239
- config_name: XQuAD.zh
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 984241
    num_examples: 1190
  download_size: 808652
  dataset_size: 984241
- config_name: XQuAD.en
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 1116123
    num_examples: 1190
  download_size: 609383
  dataset_size: 1116123
- config_name: XQuAD.es
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 1273499
    num_examples: 1190
  download_size: 684322
  dataset_size: 1273499
- config_name: XQuAD.hi
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 2682975
    num_examples: 1190
  download_size: 1680538
  dataset_size: 2682975
- config_name: XQuAD.el
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 2206690
    num_examples: 1190
  download_size: 1918889
  dataset_size: 2206690
- config_name: XQuAD.ru
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 2136990
    num_examples: 1190
  download_size: 1896368
  dataset_size: 2136990
- config_name: XQuAD.th
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 2854959
    num_examples: 1190
  download_size: 1809143
  dataset_size: 2854959
- config_name: XQuAD.tr
  features:
  - name: id
    dtype: string
  - name: context
    dtype: string
  - name: question
    dtype: string
  - name: answers
    sequence:
    - name: answer_start
      dtype: int32
    - name: text
      dtype: string
  splits:
  - name: validation
    num_bytes: 1210763
    num_examples: 1190
  download_size: 729506
  dataset_size: 1210763
- config_name: bucc18.de
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: test
    num_bytes: 2325701
    num_examples: 9580
  - name: validation
    num_bytes: 248707
    num_examples: 1038
  download_size: 30719200
  dataset_size: 2574408
- config_name: bucc18.fr
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: test
    num_bytes: 2082419
    num_examples: 9086
  - name: validation
    num_bytes: 212513
    num_examples: 929
  download_size: 22706544
  dataset_size: 2294932
- config_name: bucc18.zh
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: test
    num_bytes: 415925
    num_examples: 1899
  - name: validation
    num_bytes: 55739
    num_examples: 257
  download_size: 7114794
  dataset_size: 471664
- config_name: bucc18.ru
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: test
    num_bytes: 4641678
    num_examples: 14435
  - name: validation
    num_bytes: 761347
    num_examples: 2374
  download_size: 41354312
  dataset_size: 5403025
- config_name: PAWS-X.de
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype: string
  splits:
  - name: test
    num_bytes: 510194
    num_examples: 2000
  - name: train
    num_bytes: 12451883
    num_examples: 49380
  - name: validation
    num_bytes: 500009
    num_examples: 2000
  download_size: 30282057
  dataset_size: 13462086
- config_name: PAWS-X.en
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype: string
  splits:
  - name: test
    num_bytes: 480738
    num_examples: 2000
  - name: train
    num_bytes: 11827719
    num_examples: 49175
  - name: validation
    num_bytes: 478291
    num_examples: 2000
  download_size: 30282057
  dataset_size: 12786748
- config_name: PAWS-X.es
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype: string
  splits:
  - name: test
    num_bytes: 505047
    num_examples: 2000
  - name: train
    num_bytes: 12462107
    num_examples: 49401
  - name: validation
    num_bytes: 494069
    num_examples: 1961
  download_size: 30282057
  dataset_size: 13461223
- config_name: PAWS-X.fr
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype: string
  splits:
  - name: test
    num_bytes: 521031
    num_examples: 2000
  - name: train
    num_bytes: 12948512
    num_examples: 49399
  - name: validation
    num_bytes: 516111
    num_examples: 1988
  download_size: 30282057
  dataset_size: 13985654
- config_name: PAWS-X.ja
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype: string
  splits:
  - name: test
    num_bytes: 654640
    num_examples: 2000
  - name: train
    num_bytes: 14695653
    num_examples: 49401
  - name: validation
    num_bytes: 647774
    num_examples: 2000
  download_size: 30282057
  dataset_size: 15998067
- config_name: PAWS-X.ko
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype: string
  splits:
  - name: test
    num_bytes: 547978
    num_examples: 1999
  - name: train
    num_bytes: 13542657
    num_examples: 49164
  - name: validation
    num_bytes: 540787
    num_examples: 2000
  download_size: 30282057
  dataset_size: 14631422
- config_name: PAWS-X.zh
  features:
  - name: sentence1
    dtype: string
  - name: sentence2
    dtype: string
  - name: label
    dtype: string
  splits:
  - name: test
    num_bytes: 460638
    num_examples: 2000
  - name: train
    num_bytes: 10469712
    num_examples: 49401
  - name: validation
    num_bytes: 459120
    num_examples: 2000
  download_size: 30282057
  dataset_size: 11389470
- config_name: tatoeba.afr
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 179651
    num_examples: 1000
  download_size: 59635
  dataset_size: 179651
- config_name: tatoeba.ara
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 192666
    num_examples: 1000
  download_size: 72650
  dataset_size: 192666
- config_name: tatoeba.ben
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 211719
    num_examples: 1000
  download_size: 91703
  dataset_size: 211719
- config_name: tatoeba.bul
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 222295
    num_examples: 1000
  download_size: 102279
  dataset_size: 222295
- config_name: tatoeba.deu
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 225583
    num_examples: 1000
  download_size: 105567
  dataset_size: 225583
- config_name: tatoeba.cmn
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 188947
    num_examples: 1000
  download_size: 68931
  dataset_size: 188947
- config_name: tatoeba.ell
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 198977
    num_examples: 1000
  download_size: 78961
  dataset_size: 198977
- config_name: tatoeba.est
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 179744
    num_examples: 1000
  download_size: 59728
  dataset_size: 179744
- config_name: tatoeba.eus
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 186084
    num_examples: 1000
  download_size: 66068
  dataset_size: 186084
- config_name: tatoeba.fin
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 195685
    num_examples: 1000
  download_size: 75669
  dataset_size: 195685
- config_name: tatoeba.fra
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 200034
    num_examples: 1000
  download_size: 80018
  dataset_size: 200034
- config_name: tatoeba.heb
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 203516
    num_examples: 1000
  download_size: 83500
  dataset_size: 203516
- config_name: tatoeba.hin
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 242574
    num_examples: 1000
  download_size: 122558
  dataset_size: 242574
- config_name: tatoeba.hun
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 188905
    num_examples: 1000
  download_size: 68889
  dataset_size: 188905
- config_name: tatoeba.ind
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 194860
    num_examples: 1000
  download_size: 74844
  dataset_size: 194860
- config_name: tatoeba.ita
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 185849
    num_examples: 1000
  download_size: 65833
  dataset_size: 185849
- config_name: tatoeba.jav
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 38529
    num_examples: 205
  download_size: 13913
  dataset_size: 38529
- config_name: tatoeba.jpn
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 213099
    num_examples: 1000
  download_size: 93083
  dataset_size: 213099
- config_name: tatoeba.kat
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 161696
    num_examples: 746
  download_size: 72160
  dataset_size: 161696
- config_name: tatoeba.kaz
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 116194
    num_examples: 575
  download_size: 47178
  dataset_size: 116194
- config_name: tatoeba.kor
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 199155
    num_examples: 1000
  download_size: 79139
  dataset_size: 199155
- config_name: tatoeba.mal
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 177173
    num_examples: 687
  download_size: 94717
  dataset_size: 177173
- config_name: tatoeba.mar
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 220558
    num_examples: 1000
  download_size: 100542
  dataset_size: 220558
- config_name: tatoeba.nld
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 193279
    num_examples: 1000
  download_size: 73263
  dataset_size: 193279
- config_name: tatoeba.pes
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 213735
    num_examples: 1000
  download_size: 93719
  dataset_size: 213735
- config_name: tatoeba.por
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 195201
    num_examples: 1000
  download_size: 75185
  dataset_size: 195201
- config_name: tatoeba.rus
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 212488
    num_examples: 1000
  download_size: 92472
  dataset_size: 212488
- config_name: tatoeba.spa
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 192282
    num_examples: 1000
  download_size: 72266
  dataset_size: 192282
- config_name: tatoeba.swh
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 67283
    num_examples: 390
  download_size: 20467
  dataset_size: 67283
- config_name: tatoeba.tam
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 76297
    num_examples: 307
  download_size: 39441
  dataset_size: 76297
- config_name: tatoeba.tel
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 53239
    num_examples: 234
  download_size: 25143
  dataset_size: 53239
- config_name: tatoeba.tgl
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 188154
    num_examples: 1000
  download_size: 68138
  dataset_size: 188154
- config_name: tatoeba.tha
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 128974
    num_examples: 548
  download_size: 63198
  dataset_size: 128974
- config_name: tatoeba.tur
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 191901
    num_examples: 1000
  download_size: 71885
  dataset_size: 191901
- config_name: tatoeba.urd
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 208728
    num_examples: 1000
  download_size: 88712
  dataset_size: 208728
- config_name: tatoeba.vie
  features:
  - name: source_sentence
    dtype: string
  - name: target_sentence
    dtype: string
  - name: source_lang
    dtype: string
  - name: target_lang
    dtype: string
  splits:
  - name: validation
    num_bytes: 211423
    num_examples: 1000
  download_size: 91407
  dataset_size: 211423
- config_name: udpos.Afrikaans
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 174256
    num_examples: 425
  - name: train
    num_bytes: 586382
    num_examples: 1315
  - name: validation
    num_bytes: 91302
    num_examples: 194
  download_size: 355216681
  dataset_size: 851940
- config_name: udpos.Arabic
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 973834
    num_examples: 1680
  - name: train
    num_bytes: 4453694
    num_examples: 6075
  - name: validation
    num_bytes: 593662
    num_examples: 909
  download_size: 355216681
  dataset_size: 6021190
- config_name: udpos.Basque
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 444656
    num_examples: 1799
  - name: train
    num_bytes: 1327725
    num_examples: 5396
  - name: validation
    num_bytes: 438683
    num_examples: 1798
  download_size: 355216681
  dataset_size: 2211064
- config_name: udpos.Bulgarian
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 339959
    num_examples: 1116
  - name: train
    num_bytes: 2689779
    num_examples: 8907
  - name: validation
    num_bytes: 347129
    num_examples: 1115
  download_size: 355216681
  dataset_size: 3376867
- config_name: udpos.Dutch
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 397916
    num_examples: 1471
  - name: train
    num_bytes: 4518018
    num_examples: 18051
  - name: validation
    num_bytes: 393604
    num_examples: 1394
  download_size: 355216681
  dataset_size: 5309538
- config_name: udpos.English
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1421160
    num_examples: 5440
  - name: train
    num_bytes: 6225545
    num_examples: 21253
  - name: validation
    num_bytes: 1042052
    num_examples: 3974
  download_size: 355216681
  dataset_size: 8688757
- config_name: udpos.Estonian
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1065713
    num_examples: 3760
  - name: train
    num_bytes: 6614929
    num_examples: 25749
  - name: validation
    num_bytes: 814183
    num_examples: 3125
  download_size: 355216681
  dataset_size: 8494825
- config_name: udpos.Finnish
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1025738
    num_examples: 4422
  - name: train
    num_bytes: 5613742
    num_examples: 27198
  - name: validation
    num_bytes: 656658
    num_examples: 3239
  download_size: 355216681
  dataset_size: 7296138
- config_name: udpos.French
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1731061
    num_examples: 9465
  - name: train
    num_bytes: 10118993
    num_examples: 47308
  - name: validation
    num_bytes: 1294108
    num_examples: 5979
  download_size: 355216681
  dataset_size: 13144162
- config_name: udpos.German
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 7345899
    num_examples: 22458
  - name: train
    num_bytes: 54773981
    num_examples: 166849
  - name: validation
    num_bytes: 6044862
    num_examples: 19233
  download_size: 355216681
  dataset_size: 68164742
- config_name: udpos.Greek
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1028677
    num_examples: 2809
  - name: train
    num_bytes: 8932140
    num_examples: 28152
  - name: validation
    num_bytes: 1062459
    num_examples: 2559
  download_size: 355216681
  dataset_size: 11023276
- config_name: udpos.Hebrew
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 223877
    num_examples: 491
  - name: train
    num_bytes: 2505703
    num_examples: 5241
  - name: validation
    num_bytes: 210025
    num_examples: 484
  download_size: 355216681
  dataset_size: 2939605
- config_name: udpos.Hindi
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1400237
    num_examples: 2684
  - name: train
    num_bytes: 6690274
    num_examples: 13304
  - name: validation
    num_bytes: 839714
    num_examples: 1659
  download_size: 355216681
  dataset_size: 8930225
- config_name: udpos.Hungarian
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 193740
    num_examples: 449
  - name: train
    num_bytes: 372238
    num_examples: 910
  - name: validation
    num_bytes: 215891
    num_examples: 441
  download_size: 355216681
  dataset_size: 781869
- config_name: udpos.Indonesian
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 557113
    num_examples: 1557
  - name: train
    num_bytes: 1710690
    num_examples: 4477
  - name: validation
    num_bytes: 220875
    num_examples: 559
  download_size: 355216681
  dataset_size: 2488678
- config_name: udpos.Italian
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1337881
    num_examples: 3518
  - name: train
    num_bytes: 11299329
    num_examples: 29685
  - name: validation
    num_bytes: 989008
    num_examples: 2278
  download_size: 355216681
  dataset_size: 13626218
- config_name: udpos.Japanese
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 928914
    num_examples: 2372
  - name: train
    num_bytes: 2792963
    num_examples: 7125
  - name: validation
    num_bytes: 200368
    num_examples: 511
  download_size: 355216681
  dataset_size: 3922245
- config_name: udpos.Kazakh
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 228936
    num_examples: 1047
  - name: train
    num_bytes: 11450
    num_examples: 31
  download_size: 355216681
  dataset_size: 240386
- config_name: udpos.Korean
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1162551
    num_examples: 4276
  - name: train
    num_bytes: 7341303
    num_examples: 27410
  - name: validation
    num_bytes: 782599
    num_examples: 3016
  download_size: 355216681
  dataset_size: 9286453
- config_name: udpos.Chinese
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1236063
    num_examples: 5528
  - name: train
    num_bytes: 4218915
    num_examples: 18998
  - name: validation
    num_bytes: 594460
    num_examples: 3038
  download_size: 355216681
  dataset_size: 6049438
- config_name: udpos.Marathi
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 7883
    num_examples: 47
  - name: train
    num_bytes: 59035
    num_examples: 373
  - name: validation
    num_bytes: 8509
    num_examples: 46
  download_size: 355216681
  dataset_size: 75427
- config_name: udpos.Persian
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 320695
    num_examples: 600
  - name: train
    num_bytes: 2400788
    num_examples: 4798
  - name: validation
    num_bytes: 317065
    num_examples: 599
  download_size: 355216681
  dataset_size: 3038548
- config_name: udpos.Portuguese
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1082594
    num_examples: 2681
  - name: train
    num_bytes: 7669580
    num_examples: 17992
  - name: validation
    num_bytes: 712409
    num_examples: 1770
  download_size: 355216681
  dataset_size: 9464583
- config_name: udpos.Russian
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 4236717
    num_examples: 11336
  - name: train
    num_bytes: 24230182
    num_examples: 67435
  - name: validation
    num_bytes: 3457043
    num_examples: 9960
  download_size: 355216681
  dataset_size: 31923942
- config_name: udpos.Spanish
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 1476512
    num_examples: 3147
  - name: train
    num_bytes: 13858442
    num_examples: 28492
  - name: validation
    num_bytes: 1498777
    num_examples: 3054
  download_size: 355216681
  dataset_size: 16833731
- config_name: udpos.Tagalog
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 5165
    num_examples: 55
  download_size: 355216681
  dataset_size: 5165
- config_name: udpos.Tamil
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 62378
    num_examples: 120
  - name: train
    num_bytes: 202608
    num_examples: 400
  - name: validation
    num_bytes: 40043
    num_examples: 80
  download_size: 355216681
  dataset_size: 305029
- config_name: udpos.Telugu
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 19587
    num_examples: 146
  - name: train
    num_bytes: 138061
    num_examples: 1051
  - name: validation
    num_bytes: 18002
    num_examples: 131
  download_size: 355216681
  dataset_size: 175650
- config_name: udpos.Thai
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 561348
    num_examples: 1000
  download_size: 355216681
  dataset_size: 561348
- config_name: udpos.Turkish
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 827394
    num_examples: 4785
  - name: train
    num_bytes: 704417
    num_examples: 3664
  - name: validation
    num_bytes: 186467
    num_examples: 988
  download_size: 355216681
  dataset_size: 1718278
- config_name: udpos.Urdu
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 288565
    num_examples: 535
  - name: train
    num_bytes: 2107374
    num_examples: 4043
  - name: validation
    num_bytes: 284273
    num_examples: 552
  download_size: 355216681
  dataset_size: 2680212
- config_name: udpos.Vietnamese
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 214075
    num_examples: 800
  - name: train
    num_bytes: 367347
    num_examples: 1400
  - name: validation
    num_bytes: 206200
    num_examples: 800
  download_size: 355216681
  dataset_size: 787622
- config_name: udpos.Yoruba
  features:
  - name: tokens
    sequence: string
  - name: pos_tags
    sequence:
      class_label:
        names:
          0: ADJ
          1: ADP
          2: ADV
          3: AUX
          4: CCONJ
          5: DET
          6: INTJ
          7: NOUN
          8: NUM
          9: PART
          10: PRON
          11: PROPN
          12: PUNCT
          13: SCONJ
          14: SYM
          15: VERB
          16: X
  splits:
  - name: test
    num_bytes: 44668
    num_examples: 100
  download_size: 355216681
  dataset_size: 44668
---

# Dataset Card for "xtreme"

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

- **Homepage:** [https://github.com/google-research/xtreme](https://github.com/google-research/xtreme)
- **Repository:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Paper:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Point of Contact:** [More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
- **Size of downloaded dataset files:** 15143.21 MB
- **Size of the generated dataset:** 1027.42 MB
- **Total amount of disk used:** 16170.64 MB

### Dataset Summary

The Cross-lingual Natural Language Inference (XNLI) corpus is a crowd-sourced collection of 5,000 test and
2,500 dev pairs for the MultiNLI corpus. The pairs are annotated with textual entailment and translated into
14 languages: French, Spanish, German, Greek, Bulgarian, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese,
Hindi, Swahili and Urdu. This results in 112.5k annotated pairs. Each premise can be associated with the
corresponding hypothesis in the 15 languages, summing up to more than 1.5M combinations. The corpus is made to
evaluate how to perform inference in any language (including low-resources ones like Swahili or Urdu) when only
English NLI data is available at training time. One solution is cross-lingual sentence encoding, for which XNLI
is an evaluation benchmark.
The Cross-lingual TRansfer Evaluation of Multilingual Encoders (XTREME) benchmark is a benchmark for the evaluation of
the cross-lingual generalization ability of pre-trained multilingual models. It covers 40 typologically diverse languages
(spanning 12 language families) and includes nine tasks that collectively require reasoning about different levels of
syntax and semantics. The languages in XTREME are selected to maximize language diversity, coverage in existing tasks,
and availability of training data. Among these are many under-studied languages, such as the Dravidian languages Tamil
(spoken in southern India, Sri Lanka, and Singapore), Telugu and Malayalam (spoken mainly in southern India), and the
Niger-Congo languages Swahili and Yoruba, spoken in Africa.

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

## Dataset Structure

### Data Instances

#### MLQA.ar.ar

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 8.77 MB
- **Total amount of disk used:** 80.98 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.de

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 2.43 MB
- **Total amount of disk used:** 74.64 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.en

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 8.62 MB
- **Total amount of disk used:** 80.83 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.es

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 3.12 MB
- **Total amount of disk used:** 75.33 MB

An example of 'validation' looks as follows.
```

```

#### MLQA.ar.hi

- **Size of downloaded dataset files:** 72.21 MB
- **Size of the generated dataset:** 3.17 MB
- **Total amount of disk used:** 75.38 MB

An example of 'validation' looks as follows.
```

```

### Data Fields

The data fields are the same among all splits.

#### MLQA.ar.ar
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.de
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.en
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.es
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

#### MLQA.ar.hi
- `id`: a `string` feature.
- `title`: a `string` feature.
- `context`: a `string` feature.
- `question`: a `string` feature.
- `answers`: a dictionary feature containing:
  - `answer_start`: a `int32` feature.
  - `text`: a `string` feature.

### Data Splits

|   name   |validation|test|
|----------|---------:|---:|
|MLQA.ar.ar|       517|5335|
|MLQA.ar.de|       207|1649|
|MLQA.ar.en|       517|5335|
|MLQA.ar.es|       161|1978|
|MLQA.ar.hi|       186|1831|

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

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Citation Information

```
  @InProceedings{conneau2018xnli,
  author = {Conneau, Alexis
                 and Rinott, Ruty
                 and Lample, Guillaume
                 and Williams, Adina
                 and Bowman, Samuel R.
                 and Schwenk, Holger
                 and Stoyanov, Veselin},
  title = {XNLI: Evaluating Cross-lingual Sentence Representations},
  booktitle = {Proceedings of the 2018 Conference on Empirical Methods
               in Natural Language Processing},
  year = {2018},
  publisher = {Association for Computational Linguistics},
  location = {Brussels, Belgium},
}
@article{hu2020xtreme,
      author    = {Junjie Hu and Sebastian Ruder and Aditya Siddhant and Graham Neubig and Orhan Firat and Melvin Johnson},
      title     = {XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization},
      journal   = {CoRR},
      volume    = {abs/2003.11080},
      year      = {2020},
      archivePrefix = {arXiv},
      eprint    = {2003.11080}
}

```


### Contributions

Thanks to [@thomwolf](https://github.com/thomwolf), [@jplu](https://github.com/jplu), [@lewtun](https://github.com/lewtun), [@lvwerra](https://github.com/lvwerra), [@lhoestq](https://github.com/lhoestq), [@patrickvonplaten](https://github.com/patrickvonplaten), [@mariamabarham](https://github.com/mariamabarham) for adding this dataset.