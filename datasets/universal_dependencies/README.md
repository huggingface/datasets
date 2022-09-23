---
annotations_creators:
- expert-generated
language_creators:
- crowdsourced
language:
- af
- aii
- ajp
- akk
- am
- apu
- aqz
- ar
- be
- bg
- bho
- bm
- br
- bxr
- ca
- ckt
- cop
- cs
- cu
- cy
- da
- de
- el
- en
- es
- et
- eu
- fa
- fi
- fo
- fr
- fro
- ga
- gd
- gl
- got
- grc
- gsw
- gun
- gv
- he
- hi
- hr
- hsb
- hu
- hy
- id
- is
- it
- ja
- kfm
- kk
- kmr
- ko
- koi
- kpv
- krl
- la
- lt
- lv
- lzh
- mdf
- mr
- mt
- myu
- myv
- nl
- 'no'
- nyq
- olo
- orv
- otk
- pcm
- pl
- pt
- ro
- ru
- sa
- sk
- sl
- sme
- sms
- soj
- sq
- sr
- sv
- swl
- ta
- te
- th
- tl
- tpn
- tr
- ug
- uk
- ur
- vi
- wbp
- wo
- yo
- yue
- zh
license:
- unknown
multilinguality:
- multilingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- token-classification
task_ids:
- parsing
- token-classification-other-constituency-parsing
- token-classification-other-dependency-parsing
paperswithcode_id: universal-dependencies
pretty_name: Universal Dependencies Treebank
configs:
- af_afribooms
- aii_as
- ajp_madar
- akk_pisandub
- akk_riao
- am_att
- apu_ufpa
- aqz_tudet
- ar_nyuad
- ar_padt
- ar_pud
- be_hse
- bg_btb
- bho_bhtb
- bm_crb
- br_keb
- bxr_bdt
- ca_ancora
- ckt_hse
- cop_scriptorium
- cs_cac
- cs_cltt
- cs_fictree
- cs_pdt
- cs_pud
- cu_proiel
- cy_ccg
- da_ddt
- de_gsd
- de_hdt
- de_lit
- de_pud
- el_gdt
- en_esl
- en_ewt
- en_gum
- en_gumreddit
- en_lines
- en_partut
- en_pronouns
- en_pud
- es_ancora
- es_gsd
- es_pud
- et_edt
- et_ewt
- eu_bdt
- fa_perdt
- fa_seraji
- fi_ftb
- fi_ood
- fi_pud
- fi_tdt
- fo_farpahc
- fo_oft
- fr_fqb
- fr_ftb
- fr_gsd
- fr_partut
- fr_pud
- fr_sequoia
- fr_spoken
- fro_srcmf
- ga_idt
- gd_arcosg
- gl_ctg
- gl_treegal
- got_proiel
- grc_perseus
- grc_proiel
- gsw_uzh
- gun_dooley
- gun_thomas
- gv_cadhan
- he_htb
- hi_hdtb
- hi_pud
- hr_set
- hsb_ufal
- hu_szeged
- hy_armtdp
- id_csui
- id_gsd
- id_pud
- is_icepahc
- is_pud
- it_isdt
- it_partut
- it_postwita
- it_pud
- it_twittiro
- it_vit
- ja_bccwj
- ja_gsd
- ja_modern
- ja_pud
- kfm_aha
- kk_ktb
- kmr_mg
- ko_gsd
- ko_kaist
- ko_pud
- koi_uh
- kpv_ikdp
- kpv_lattice
- krl_kkpp
- la_ittb
- la_llct
- la_perseus
- la_proiel
- lt_alksnis
- lt_hse
- lv_lvtb
- lzh_kyoto
- mdf_jr
- mr_ufal
- mt_mudt
- myu_tudet
- myv_jr
- nl_alpino
- nl_lassysmall
- no_bokmaal
- no_nynorsk
- no_nynorsklia
- nyq_aha
- olo_kkpp
- orv_rnc
- orv_torot
- otk_tonqq
- pcm_nsc
- pl_lfg
- pl_pdb
- pl_pud
- pt_bosque
- pt_gsd
- pt_pud
- qhe_hiencs
- qtd_sagt
- ro_nonstandard
- ro_rrt
- ro_simonero
- ru_gsd
- ru_pud
- ru_syntagrus
- ru_taiga
- sa_ufal
- sa_vedic
- sk_snk
- sl_ssj
- sl_sst
- sme_giella
- sms_giellagas
- soj_aha
- sq_tsa
- sr_set
- sv_lines
- sv_pud
- sv_talbanken
- swl_sslc
- ta_mwtt
- ta_ttb
- te_mtg
- th_pud
- tl_trg
- tl_ugnayan
- tpn_tudet
- tr_boun
- tr_gb
- tr_imst
- tr_pud
- ug_udt
- uk_iu
- ur_udtb
- vi_vtb
- wbp_ufal
- wo_wtb
- yo_ytb
- yue_hk
- zh_cfl
- zh_gsd
- zh_gsdsimp
- zh_hk
- zh_pud
dataset_info:
- config_name: af_afribooms
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1050299
    num_examples: 425
  - name: train
    num_bytes: 3523113
    num_examples: 1315
  - name: validation
    num_bytes: 547285
    num_examples: 194
  download_size: 3088237
  dataset_size: 5120697
- config_name: akk_pisandub
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 153470
    num_examples: 101
  download_size: 101789
  dataset_size: 153470
- config_name: akk_riao
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3374577
    num_examples: 1804
  download_size: 2022357
  dataset_size: 3374577
- config_name: aqz_tudet
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 8286
    num_examples: 24
  download_size: 5683
  dataset_size: 8286
- config_name: sq_tsa
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 116034
    num_examples: 60
  download_size: 68875
  dataset_size: 116034
- config_name: am_att
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1554859
    num_examples: 1074
  download_size: 1019607
  dataset_size: 1554859
- config_name: grc_perseus
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3004502
    num_examples: 1306
  - name: train
    num_bytes: 22611612
    num_examples: 11476
  - name: validation
    num_bytes: 3152233
    num_examples: 1137
  download_size: 18898313
  dataset_size: 28768347
- config_name: grc_proiel
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2192289
    num_examples: 1047
  - name: train
    num_bytes: 30938089
    num_examples: 15014
  - name: validation
    num_bytes: 2264551
    num_examples: 1019
  download_size: 23715831
  dataset_size: 35394929
- config_name: apu_ufpa
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 75578
    num_examples: 76
  download_size: 69565
  dataset_size: 75578
- config_name: ar_nyuad
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 9880240
    num_examples: 1963
  - name: train
    num_bytes: 79064476
    num_examples: 15789
  - name: validation
    num_bytes: 9859912
    num_examples: 1986
  download_size: 58583673
  dataset_size: 98804628
- config_name: ar_padt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 7428063
    num_examples: 680
  - name: train
    num_bytes: 58537298
    num_examples: 6075
  - name: validation
    num_bytes: 7787253
    num_examples: 909
  download_size: 51208169
  dataset_size: 73752614
- config_name: ar_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2816625
    num_examples: 1000
  download_size: 2084082
  dataset_size: 2816625
- config_name: hy_armtdp
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 947287
    num_examples: 278
  - name: train
    num_bytes: 7697891
    num_examples: 1975
  - name: validation
    num_bytes: 988849
    num_examples: 249
  download_size: 6886567
  dataset_size: 9634027
- config_name: aii_as
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 52540
    num_examples: 57
  download_size: 32639
  dataset_size: 52540
- config_name: bm_crb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1502886
    num_examples: 1026
  download_size: 892924
  dataset_size: 1502886
- config_name: eu_bdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2734601
    num_examples: 1799
  - name: train
    num_bytes: 8199861
    num_examples: 5396
  - name: validation
    num_bytes: 2701073
    num_examples: 1798
  download_size: 8213576
  dataset_size: 13635535
- config_name: be_hse
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1818113
    num_examples: 889
  - name: train
    num_bytes: 34880663
    num_examples: 21555
  - name: validation
    num_bytes: 1745668
    num_examples: 1090
  download_size: 26433402
  dataset_size: 38444444
- config_name: bho_bhtb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 947740
    num_examples: 357
  download_size: 614159
  dataset_size: 947740
- config_name: br_keb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1026257
    num_examples: 888
  download_size: 679680
  dataset_size: 1026257
- config_name: bg_btb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2344136
    num_examples: 1116
  - name: train
    num_bytes: 18545312
    num_examples: 8907
  - name: validation
    num_bytes: 2393174
    num_examples: 1115
  download_size: 14910603
  dataset_size: 23282622
- config_name: bxr_bdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1116630
    num_examples: 908
  - name: train
    num_bytes: 17364
    num_examples: 19
  download_size: 726053
  dataset_size: 1133994
- config_name: yue_hk
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1242850
    num_examples: 1004
  download_size: 710060
  dataset_size: 1242850
- config_name: ca_ancora
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 6441038
    num_examples: 1846
  - name: train
    num_bytes: 46502842
    num_examples: 13123
  - name: validation
    num_bytes: 6282364
    num_examples: 1709
  download_size: 35924146
  dataset_size: 59226244
- config_name: zh_cfl
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 660584
    num_examples: 451
  download_size: 384725
  dataset_size: 660584
- config_name: zh_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1130467
    num_examples: 500
  - name: train
    num_bytes: 9268661
    num_examples: 3997
  - name: validation
    num_bytes: 1188371
    num_examples: 500
  download_size: 6828367
  dataset_size: 11587499
- config_name: zh_gsdsimp
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1130459
    num_examples: 500
  - name: train
    num_bytes: 9268663
    num_examples: 3997
  - name: validation
    num_bytes: 1188383
    num_examples: 500
  download_size: 6828419
  dataset_size: 11587505
- config_name: zh_hk
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 880193
    num_examples: 1004
  download_size: 494447
  dataset_size: 880193
- config_name: zh_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2425817
    num_examples: 1000
  download_size: 1606982
  dataset_size: 2425817
- config_name: ckt_hse
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 808669
    num_examples: 1004
  download_size: 771943
  dataset_size: 808669
- config_name: lzh_kyoto
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3155207
    num_examples: 4469
  - name: train
    num_bytes: 26615708
    num_examples: 38669
  - name: validation
    num_bytes: 3770507
    num_examples: 5296
  download_size: 22658287
  dataset_size: 33541422
- config_name: cop_scriptorium
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1487709
    num_examples: 403
  - name: train
    num_bytes: 3944468
    num_examples: 1089
  - name: validation
    num_bytes: 1566786
    num_examples: 381
  download_size: 4502996
  dataset_size: 6998963
- config_name: hr_set
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3035797
    num_examples: 1136
  - name: train
    num_bytes: 19104315
    num_examples: 6914
  - name: validation
    num_bytes: 2787184
    num_examples: 960
  download_size: 15103034
  dataset_size: 24927296
- config_name: cs_cac
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1878841
    num_examples: 628
  - name: train
    num_bytes: 81527862
    num_examples: 23478
  - name: validation
    num_bytes: 1898678
    num_examples: 603
  download_size: 55990235
  dataset_size: 85305381
- config_name: cs_cltt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 646103
    num_examples: 136
  - name: train
    num_bytes: 4277239
    num_examples: 860
  - name: validation
    num_bytes: 752253
    num_examples: 129
  download_size: 3745656
  dataset_size: 5675595
- config_name: cs_fictree
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2679930
    num_examples: 1291
  - name: train
    num_bytes: 21490020
    num_examples: 10160
  - name: validation
    num_bytes: 2677727
    num_examples: 1309
  download_size: 17464342
  dataset_size: 26847677
- config_name: cs_pdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 29817339
    num_examples: 10148
  - name: train
    num_bytes: 201356662
    num_examples: 68495
  - name: validation
    num_bytes: 27366981
    num_examples: 9270
  download_size: 171506068
  dataset_size: 258540982
- config_name: cs_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3195818
    num_examples: 1000
  download_size: 2231853
  dataset_size: 3195818
- config_name: da_ddt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1082651
    num_examples: 565
  - name: train
    num_bytes: 8689809
    num_examples: 4383
  - name: validation
    num_bytes: 1117939
    num_examples: 564
  download_size: 6425281
  dataset_size: 10890399
- config_name: nl_alpino
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1354908
    num_examples: 596
  - name: train
    num_bytes: 22503950
    num_examples: 12264
  - name: validation
    num_bytes: 1411253
    num_examples: 718
  download_size: 16858557
  dataset_size: 25270111
- config_name: nl_lassysmall
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1391136
    num_examples: 875
  - name: train
    num_bytes: 9001614
    num_examples: 5787
  - name: validation
    num_bytes: 1361552
    num_examples: 676
  download_size: 8034396
  dataset_size: 11754302
- config_name: en_esl
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 651829
    num_examples: 500
  - name: train
    num_bytes: 5335977
    num_examples: 4124
  - name: validation
    num_bytes: 648562
    num_examples: 500
  download_size: 3351548
  dataset_size: 6636368
- config_name: en_ewt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2820398
    num_examples: 2077
  - name: train
    num_bytes: 22755753
    num_examples: 12543
  - name: validation
    num_bytes: 2829889
    num_examples: 2002
  download_size: 16893922
  dataset_size: 28406040
- config_name: en_gum
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1743317
    num_examples: 890
  - name: train
    num_bytes: 8999554
    num_examples: 4287
  - name: validation
    num_bytes: 1704949
    num_examples: 784
  download_size: 7702761
  dataset_size: 12447820
- config_name: en_gumreddit
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 374707
    num_examples: 158
  - name: train
    num_bytes: 1365930
    num_examples: 587
  - name: validation
    num_bytes: 317546
    num_examples: 150
  download_size: 1195979
  dataset_size: 2058183
- config_name: en_lines
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1766797
    num_examples: 1035
  - name: train
    num_bytes: 5728898
    num_examples: 3176
  - name: validation
    num_bytes: 1911762
    num_examples: 1032
  download_size: 5522254
  dataset_size: 9407457
- config_name: en_partut
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 326834
    num_examples: 153
  - name: train
    num_bytes: 4133445
    num_examples: 1781
  - name: validation
    num_bytes: 265039
    num_examples: 156
  download_size: 2720286
  dataset_size: 4725318
- config_name: en_pronouns
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 207364
    num_examples: 285
  download_size: 147181
  dataset_size: 207364
- config_name: en_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2282027
    num_examples: 1000
  download_size: 1340563
  dataset_size: 2282027
- config_name: myv_jr
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2763297
    num_examples: 1690
  download_size: 1945981
  dataset_size: 2763297
- config_name: et_edt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 5994421
    num_examples: 3214
  - name: train
    num_bytes: 42901059
    num_examples: 24633
  - name: validation
    num_bytes: 5551620
    num_examples: 3125
  download_size: 32393618
  dataset_size: 54447100
- config_name: et_ewt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1600116
    num_examples: 913
  - name: train
    num_bytes: 4199896
    num_examples: 2837
  - name: validation
    num_bytes: 1089459
    num_examples: 743
  download_size: 4044147
  dataset_size: 6889471
- config_name: fo_farpahc
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 798245
    num_examples: 301
  - name: train
    num_bytes: 2114958
    num_examples: 1020
  - name: validation
    num_bytes: 809707
    num_examples: 300
  download_size: 2186706
  dataset_size: 3722910
- config_name: fo_oft
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1220792
    num_examples: 1208
  download_size: 802681
  dataset_size: 1220792
- config_name: fi_ftb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2144908
    num_examples: 1867
  - name: train
    num_bytes: 16800109
    num_examples: 14981
  - name: validation
    num_bytes: 2074201
    num_examples: 1875
  download_size: 13132466
  dataset_size: 21019218
- config_name: fi_ood
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2366923
    num_examples: 2122
  download_size: 1480506
  dataset_size: 2366923
- config_name: fi_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2086421
    num_examples: 1000
  download_size: 1411514
  dataset_size: 2086421
- config_name: fi_tdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2855263
    num_examples: 1555
  - name: train
    num_bytes: 22065448
    num_examples: 12217
  - name: validation
    num_bytes: 2483303
    num_examples: 1364
  download_size: 16692242
  dataset_size: 27404014
- config_name: fr_fqb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2674644
    num_examples: 2289
  download_size: 1556235
  dataset_size: 2674644
- config_name: fr_ftb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 7583038
    num_examples: 2541
  - name: train
    num_bytes: 44714315
    num_examples: 14759
  - name: validation
    num_bytes: 3929428
    num_examples: 1235
  download_size: 30926802
  dataset_size: 56226781
- config_name: fr_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1086926
    num_examples: 416
  - name: train
    num_bytes: 38329902
    num_examples: 14449
  - name: validation
    num_bytes: 3861548
    num_examples: 1476
  download_size: 25492044
  dataset_size: 43278376
- config_name: fr_partut
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 288829
    num_examples: 110
  - name: train
    num_bytes: 2620477
    num_examples: 803
  - name: validation
    num_bytes: 205839
    num_examples: 107
  download_size: 1817897
  dataset_size: 3115145
- config_name: fr_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2660405
    num_examples: 1000
  download_size: 1685033
  dataset_size: 2660405
- config_name: fr_sequoia
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1067676
    num_examples: 456
  - name: train
    num_bytes: 5370647
    num_examples: 2231
  - name: validation
    num_bytes: 1065411
    num_examples: 412
  download_size: 4415282
  dataset_size: 7503734
- config_name: fr_spoken
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1078438
    num_examples: 730
  - name: train
    num_bytes: 1625626
    num_examples: 1167
  - name: validation
    num_bytes: 1091750
    num_examples: 909
  download_size: 2483341
  dataset_size: 3795814
- config_name: gl_ctg
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3053764
    num_examples: 861
  - name: train
    num_bytes: 8157432
    num_examples: 2272
  - name: validation
    num_bytes: 3057483
    num_examples: 860
  download_size: 8230649
  dataset_size: 14268679
- config_name: gl_treegal
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1174023
    num_examples: 400
  - name: train
    num_bytes: 1804389
    num_examples: 600
  download_size: 1741471
  dataset_size: 2978412
- config_name: de_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2000117
    num_examples: 977
  - name: train
    num_bytes: 32297384
    num_examples: 13814
  - name: validation
    num_bytes: 1504189
    num_examples: 799
  download_size: 21507364
  dataset_size: 35801690
- config_name: de_hdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 39519143
    num_examples: 18459
  - name: train
    num_bytes: 334214761
    num_examples: 153035
  - name: validation
    num_bytes: 39099013
    num_examples: 18434
  download_size: 249243037
  dataset_size: 412832917
- config_name: de_lit
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3327891
    num_examples: 1922
  download_size: 2060988
  dataset_size: 3327891
- config_name: de_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2684407
    num_examples: 1000
  download_size: 1731875
  dataset_size: 2684407
- config_name: got_proiel
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1518642
    num_examples: 1029
  - name: train
    num_bytes: 5175361
    num_examples: 3387
  - name: validation
    num_bytes: 1498101
    num_examples: 985
  download_size: 5225655
  dataset_size: 8192104
- config_name: el_gdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1521094
    num_examples: 456
  - name: train
    num_bytes: 6028077
    num_examples: 1662
  - name: validation
    num_bytes: 1492610
    num_examples: 403
  download_size: 5788161
  dataset_size: 9041781
- config_name: he_htb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1550465
    num_examples: 491
  - name: train
    num_bytes: 17324640
    num_examples: 5241
  - name: validation
    num_bytes: 1440985
    num_examples: 484
  download_size: 12054025
  dataset_size: 20316090
- config_name: qhe_hiencs
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 236291
    num_examples: 225
  - name: train
    num_bytes: 1510145
    num_examples: 1448
  - name: validation
    num_bytes: 244129
    num_examples: 225
  download_size: 914584
  dataset_size: 1990565
- config_name: hi_hdtb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 7786343
    num_examples: 1684
  - name: train
    num_bytes: 61893814
    num_examples: 13304
  - name: validation
    num_bytes: 7748544
    num_examples: 1659
  download_size: 51589681
  dataset_size: 77428701
- config_name: hi_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3384789
    num_examples: 1000
  download_size: 2303495
  dataset_size: 3384789
- config_name: hu_szeged
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1419130
    num_examples: 449
  - name: train
    num_bytes: 2822934
    num_examples: 910
  - name: validation
    num_bytes: 1584932
    num_examples: 441
  download_size: 3687905
  dataset_size: 5826996
- config_name: is_icepahc
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 19039838
    num_examples: 5157
  - name: train
    num_bytes: 97197159
    num_examples: 34007
  - name: validation
    num_bytes: 18931295
    num_examples: 4865
  download_size: 85106126
  dataset_size: 135168292
- config_name: is_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2304432
    num_examples: 1000
  download_size: 1525635
  dataset_size: 2304432
- config_name: id_csui
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 888832
    num_examples: 374
  - name: train
    num_bytes: 1611334
    num_examples: 656
  download_size: 1448601
  dataset_size: 2500166
- config_name: id_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1417208
    num_examples: 557
  - name: train
    num_bytes: 11728948
    num_examples: 4477
  - name: validation
    num_bytes: 1513894
    num_examples: 559
  download_size: 9487349
  dataset_size: 14660050
- config_name: id_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1768596
    num_examples: 1000
  download_size: 1149692
  dataset_size: 1768596
- config_name: ga_idt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1109028
    num_examples: 454
  - name: train
    num_bytes: 10327215
    num_examples: 4005
  - name: validation
    num_bytes: 1057313
    num_examples: 451
  download_size: 7417728
  dataset_size: 12493556
- config_name: it_isdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1267932
    num_examples: 482
  - name: train
    num_bytes: 33510781
    num_examples: 13121
  - name: validation
    num_bytes: 1439348
    num_examples: 564
  download_size: 20998527
  dataset_size: 36218061
- config_name: it_partut
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 413752
    num_examples: 153
  - name: train
    num_bytes: 5428686
    num_examples: 1781
  - name: validation
    num_bytes: 335085
    num_examples: 156
  download_size: 3582155
  dataset_size: 6177523
- config_name: it_postwita
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1344079
    num_examples: 674
  - name: train
    num_bytes: 10523322
    num_examples: 5368
  - name: validation
    num_bytes: 1299818
    num_examples: 671
  download_size: 7611319
  dataset_size: 13167219
- config_name: it_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2612838
    num_examples: 1000
  download_size: 1641073
  dataset_size: 2612838
- config_name: it_twittiro
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 316211
    num_examples: 142
  - name: train
    num_bytes: 2536429
    num_examples: 1138
  - name: validation
    num_bytes: 323504
    num_examples: 144
  download_size: 1894686
  dataset_size: 3176144
- config_name: it_vit
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2870355
    num_examples: 1067
  - name: train
    num_bytes: 24536095
    num_examples: 8277
  - name: validation
    num_bytes: 3144507
    num_examples: 743
  download_size: 17605311
  dataset_size: 30550957
- config_name: ja_bccwj
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 21904413
    num_examples: 7871
  - name: train
    num_bytes: 119164443
    num_examples: 40740
  - name: validation
    num_bytes: 23390188
    num_examples: 8417
  download_size: 87340125
  dataset_size: 164459044
- config_name: ja_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2858141
    num_examples: 543
  - name: train
    num_bytes: 36905139
    num_examples: 7027
  - name: validation
    num_bytes: 2662999
    num_examples: 501
  download_size: 30397358
  dataset_size: 42426279
- config_name: ja_modern
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3062149
    num_examples: 822
  download_size: 2163988
  dataset_size: 3062149
- config_name: ja_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 6322307
    num_examples: 1000
  download_size: 4661525
  dataset_size: 6322307
- config_name: krl_kkpp
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 370378
    num_examples: 228
  download_size: 226103
  dataset_size: 370378
- config_name: kk_ktb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1263246
    num_examples: 1047
  - name: train
    num_bytes: 64737
    num_examples: 31
  download_size: 849300
  dataset_size: 1327983
- config_name: kfm_aha
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 8464
    num_examples: 10
  download_size: 6290
  dataset_size: 8464
- config_name: koi_uh
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 117629
    num_examples: 81
  download_size: 91509
  dataset_size: 117629
- config_name: kpv_ikdp
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 182189
    num_examples: 132
  download_size: 121684
  dataset_size: 182189
- config_name: kpv_lattice
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 685683
    num_examples: 435
  download_size: 467085
  dataset_size: 685683
- config_name: ko_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1129555
    num_examples: 989
  - name: train
    num_bytes: 5480313
    num_examples: 4400
  - name: validation
    num_bytes: 1156603
    num_examples: 950
  download_size: 4882238
  dataset_size: 7766471
- config_name: ko_kaist
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2792215
    num_examples: 2287
  - name: train
    num_bytes: 29037654
    num_examples: 23010
  - name: validation
    num_bytes: 2511880
    num_examples: 2066
  download_size: 21855177
  dataset_size: 34341749
- config_name: ko_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2511856
    num_examples: 1000
  download_size: 2024810
  dataset_size: 2511856
- config_name: kmr_mg
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1248564
    num_examples: 734
  - name: train
    num_bytes: 30374
    num_examples: 20
  download_size: 765158
  dataset_size: 1278938
- config_name: la_ittb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 4221459
    num_examples: 2101
  - name: train
    num_bytes: 54306304
    num_examples: 22775
  - name: validation
    num_bytes: 4236222
    num_examples: 2101
  download_size: 40247546
  dataset_size: 62763985
- config_name: la_llct
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3352500
    num_examples: 884
  - name: train
    num_bytes: 26885433
    num_examples: 7289
  - name: validation
    num_bytes: 3363915
    num_examples: 850
  download_size: 21975884
  dataset_size: 33601848
- config_name: la_perseus
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1575350
    num_examples: 939
  - name: train
    num_bytes: 2542043
    num_examples: 1334
  download_size: 2573703
  dataset_size: 4117393
- config_name: la_proiel
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2029828
    num_examples: 1260
  - name: train
    num_bytes: 24956038
    num_examples: 15917
  - name: validation
    num_bytes: 2020476
    num_examples: 1234
  download_size: 18434442
  dataset_size: 29006342
- config_name: lv_lvtb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 4565919
    num_examples: 1823
  - name: train
    num_bytes: 29167529
    num_examples: 10156
  - name: validation
    num_bytes: 4501172
    num_examples: 1664
  download_size: 25227301
  dataset_size: 38234620
- config_name: lt_alksnis
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1648521
    num_examples: 684
  - name: train
    num_bytes: 7272501
    num_examples: 2341
  - name: validation
    num_bytes: 1763901
    num_examples: 617
  download_size: 7008248
  dataset_size: 10684923
- config_name: lt_hse
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 433214
    num_examples: 153
  - name: train
    num_bytes: 433214
    num_examples: 153
  - name: validation
    num_bytes: 433214
    num_examples: 153
  download_size: 265619
  dataset_size: 1299642
- config_name: olo_kkpp
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 175355
    num_examples: 106
  - name: train
    num_bytes: 18096
    num_examples: 19
  download_size: 121837
  dataset_size: 193451
- config_name: mt_mudt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 892629
    num_examples: 518
  - name: train
    num_bytes: 1858001
    num_examples: 1123
  - name: validation
    num_bytes: 826004
    num_examples: 433
  download_size: 2011753
  dataset_size: 3576634
- config_name: gv_cadhan
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 483042
    num_examples: 291
  download_size: 287206
  dataset_size: 483042
- config_name: mr_ufal
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 56582
    num_examples: 47
  - name: train
    num_bytes: 420345
    num_examples: 373
  - name: validation
    num_bytes: 60791
    num_examples: 46
  download_size: 339354
  dataset_size: 537718
- config_name: gun_dooley
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1037858
    num_examples: 1046
  download_size: 571571
  dataset_size: 1037858
- config_name: gun_thomas
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 143111
    num_examples: 98
  download_size: 92963
  dataset_size: 143111
- config_name: mdf_jr
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 234147
    num_examples: 167
  download_size: 162330
  dataset_size: 234147
- config_name: myu_tudet
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 26202
    num_examples: 62
  download_size: 20315
  dataset_size: 26202
- config_name: pcm_nsc
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2063685
    num_examples: 972
  - name: train
    num_bytes: 16079391
    num_examples: 7279
  - name: validation
    num_bytes: 2099571
    num_examples: 991
  download_size: 14907410
  dataset_size: 20242647
- config_name: nyq_aha
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 8723
    num_examples: 10
  download_size: 6387
  dataset_size: 8723
- config_name: sme_giella
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1142396
    num_examples: 865
  - name: train
    num_bytes: 1987666
    num_examples: 2257
  download_size: 1862302
  dataset_size: 3130062
- config_name: no_bokmaal
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3151638
    num_examples: 1939
  - name: train
    num_bytes: 25647647
    num_examples: 15696
  - name: validation
    num_bytes: 3828310
    num_examples: 2409
  download_size: 19177350
  dataset_size: 32627595
- config_name: no_nynorsk
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2601676
    num_examples: 1511
  - name: train
    num_bytes: 25630539
    num_examples: 14174
  - name: validation
    num_bytes: 3277649
    num_examples: 1890
  download_size: 18532495
  dataset_size: 31509864
- config_name: no_nynorsklia
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 999943
    num_examples: 957
  - name: train
    num_bytes: 3500907
    num_examples: 3412
  - name: validation
    num_bytes: 1003845
    num_examples: 881
  download_size: 3349676
  dataset_size: 5504695
- config_name: cu_proiel
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1648459
    num_examples: 1141
  - name: train
    num_bytes: 6106144
    num_examples: 4124
  - name: validation
    num_bytes: 1639912
    num_examples: 1073
  download_size: 6239839
  dataset_size: 9394515
- config_name: fro_srcmf
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1535923
    num_examples: 1927
  - name: train
    num_bytes: 11959859
    num_examples: 13909
  - name: validation
    num_bytes: 1526574
    num_examples: 1842
  download_size: 9043098
  dataset_size: 15022356
- config_name: orv_rnc
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2552216
    num_examples: 637
  - name: train
    num_bytes: 1527306
    num_examples: 320
  download_size: 2627398
  dataset_size: 4079522
- config_name: orv_torot
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2347934
    num_examples: 1756
  - name: train
    num_bytes: 18077991
    num_examples: 13336
  - name: validation
    num_bytes: 2408313
    num_examples: 1852
  download_size: 15296362
  dataset_size: 22834238
- config_name: otk_tonqq
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 22829
    num_examples: 18
  download_size: 14389
  dataset_size: 22829
- config_name: fa_perdt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2600303
    num_examples: 1455
  - name: train
    num_bytes: 48654947
    num_examples: 26196
  - name: validation
    num_bytes: 2687750
    num_examples: 1456
  download_size: 33606395
  dataset_size: 53943000
- config_name: fa_seraji
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1675134
    num_examples: 600
  - name: train
    num_bytes: 12627691
    num_examples: 4798
  - name: validation
    num_bytes: 1634327
    num_examples: 599
  download_size: 9890107
  dataset_size: 15937152
- config_name: pl_lfg
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2100915
    num_examples: 1727
  - name: train
    num_bytes: 16810910
    num_examples: 13774
  - name: validation
    num_bytes: 2093712
    num_examples: 1745
  download_size: 14865541
  dataset_size: 21005537
- config_name: pl_pdb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 5322608
    num_examples: 2215
  - name: train
    num_bytes: 44652289
    num_examples: 17722
  - name: validation
    num_bytes: 5494883
    num_examples: 2215
  download_size: 36340919
  dataset_size: 55469780
- config_name: pl_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2943603
    num_examples: 1000
  download_size: 1943983
  dataset_size: 2943603
- config_name: pt_bosque
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1131511
    num_examples: 476
  - name: train
    num_bytes: 22808617
    num_examples: 8328
  - name: validation
    num_bytes: 1201577
    num_examples: 560
  download_size: 15201503
  dataset_size: 25141705
- config_name: pt_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2732063
    num_examples: 1204
  - name: train
    num_bytes: 22208385
    num_examples: 9664
  - name: validation
    num_bytes: 2805628
    num_examples: 1210
  download_size: 15300844
  dataset_size: 27746076
- config_name: pt_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2431942
    num_examples: 1000
  download_size: 1516883
  dataset_size: 2431942
- config_name: ro_nonstandard
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3017162
    num_examples: 1052
  - name: train
    num_bytes: 74489083
    num_examples: 24121
  - name: validation
    num_bytes: 2663152
    num_examples: 1052
  download_size: 50345748
  dataset_size: 80169397
- config_name: ro_rrt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2092520
    num_examples: 729
  - name: train
    num_bytes: 23695399
    num_examples: 8043
  - name: validation
    num_bytes: 2190973
    num_examples: 752
  download_size: 17187956
  dataset_size: 27978892
- config_name: ro_simonero
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1940787
    num_examples: 491
  - name: train
    num_bytes: 15390734
    num_examples: 3747
  - name: validation
    num_bytes: 1926639
    num_examples: 443
  download_size: 11409378
  dataset_size: 19258160
- config_name: ru_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1597603
    num_examples: 601
  - name: train
    num_bytes: 10504099
    num_examples: 3850
  - name: validation
    num_bytes: 1635884
    num_examples: 579
  download_size: 8830986
  dataset_size: 13737586
- config_name: ru_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2695958
    num_examples: 1000
  download_size: 1869304
  dataset_size: 2695958
- config_name: ru_syntagrus
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 16880203
    num_examples: 6491
  - name: train
    num_bytes: 126305584
    num_examples: 48814
  - name: validation
    num_bytes: 17043673
    num_examples: 6584
  download_size: 102745164
  dataset_size: 160229460
- config_name: ru_taiga
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1314084
    num_examples: 881
  - name: train
    num_bytes: 5802733
    num_examples: 3138
  - name: validation
    num_bytes: 1382140
    num_examples: 945
  download_size: 5491427
  dataset_size: 8498957
- config_name: sa_ufal
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 431697
    num_examples: 230
  download_size: 424675
  dataset_size: 431697
- config_name: sa_vedic
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1209605
    num_examples: 1473
  - name: train
    num_bytes: 2179608
    num_examples: 2524
  download_size: 2041583
  dataset_size: 3389213
- config_name: gd_arcosg
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1034788
    num_examples: 538
  - name: train
    num_bytes: 3952356
    num_examples: 1990
  - name: validation
    num_bytes: 1038211
    num_examples: 645
  download_size: 3474087
  dataset_size: 6025355
- config_name: sr_set
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1432672
    num_examples: 520
  - name: train
    num_bytes: 9309552
    num_examples: 3328
  - name: validation
    num_bytes: 1503953
    num_examples: 536
  download_size: 7414381
  dataset_size: 12246177
- config_name: sms_giellagas
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 174744
    num_examples: 104
  download_size: 116491
  dataset_size: 174744
- config_name: sk_snk
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1943012
    num_examples: 1061
  - name: train
    num_bytes: 12017312
    num_examples: 8483
  - name: validation
    num_bytes: 1863926
    num_examples: 1060
  download_size: 10013420
  dataset_size: 15824250
- config_name: sl_ssj
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2083062
    num_examples: 788
  - name: train
    num_bytes: 16713639
    num_examples: 6478
  - name: validation
    num_bytes: 2070847
    num_examples: 734
  download_size: 12455962
  dataset_size: 20867548
- config_name: sl_sst
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1493885
    num_examples: 1110
  - name: train
    num_bytes: 2903675
    num_examples: 2078
  download_size: 2655777
  dataset_size: 4397560
- config_name: soj_aha
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 6218
    num_examples: 8
  download_size: 4577
  dataset_size: 6218
- config_name: ajp_madar
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 71956
    num_examples: 100
  download_size: 43174
  dataset_size: 71956
- config_name: es_ancora
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 5928986
    num_examples: 1721
  - name: train
    num_bytes: 50101327
    num_examples: 14305
  - name: validation
    num_bytes: 5883940
    num_examples: 1654
  download_size: 37668083
  dataset_size: 61914253
- config_name: es_gsd
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1253720
    num_examples: 426
  - name: train
    num_bytes: 39582074
    num_examples: 14187
  - name: validation
    num_bytes: 3834443
    num_examples: 1400
  download_size: 26073760
  dataset_size: 44670237
- config_name: es_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2595946
    num_examples: 1000
  download_size: 1628475
  dataset_size: 2595946
- config_name: swl_sslc
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 24542
    num_examples: 34
  - name: train
    num_bytes: 57443
    num_examples: 87
  - name: validation
    num_bytes: 59002
    num_examples: 82
  download_size: 81699
  dataset_size: 140987
- config_name: sv_lines
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2070626
    num_examples: 1035
  - name: train
    num_bytes: 6731662
    num_examples: 3176
  - name: validation
    num_bytes: 2239951
    num_examples: 1032
  download_size: 7245283
  dataset_size: 11042239
- config_name: sv_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2554725
    num_examples: 1000
  download_size: 1722516
  dataset_size: 2554725
- config_name: sv_talbanken
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2835742
    num_examples: 1219
  - name: train
    num_bytes: 9287256
    num_examples: 4303
  - name: validation
    num_bytes: 1361535
    num_examples: 504
  download_size: 8476012
  dataset_size: 13484533
- config_name: gsw_uzh
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 111357
    num_examples: 100
  download_size: 59675
  dataset_size: 111357
- config_name: tl_trg
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 86696
    num_examples: 128
  download_size: 61344
  dataset_size: 86696
- config_name: tl_ugnayan
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 90863
    num_examples: 94
  download_size: 55207
  dataset_size: 90863
- config_name: ta_mwtt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 522349
    num_examples: 534
  download_size: 414263
  dataset_size: 522349
- config_name: ta_ttb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 478941
    num_examples: 120
  - name: train
    num_bytes: 1538780
    num_examples: 400
  - name: validation
    num_bytes: 305206
    num_examples: 80
  download_size: 1753448
  dataset_size: 2322927
- config_name: te_mtg
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 99757
    num_examples: 146
  - name: train
    num_bytes: 703512
    num_examples: 1051
  - name: validation
    num_bytes: 91547
    num_examples: 131
  download_size: 643764
  dataset_size: 894816
- config_name: th_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2341697
    num_examples: 1000
  download_size: 1606517
  dataset_size: 2341697
- config_name: tpn_tudet
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 8089
    num_examples: 8
  download_size: 5447
  dataset_size: 8089
- config_name: qtd_sagt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1710777
    num_examples: 805
  - name: train
    num_bytes: 583697
    num_examples: 285
  - name: validation
    num_bytes: 1564765
    num_examples: 801
  download_size: 2299611
  dataset_size: 3859239
- config_name: tr_boun
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1580727
    num_examples: 979
  - name: train
    num_bytes: 12827173
    num_examples: 7803
  - name: validation
    num_bytes: 1577760
    num_examples: 979
  download_size: 9742035
  dataset_size: 15985660
- config_name: tr_gb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2146729
    num_examples: 2880
  download_size: 1474083
  dataset_size: 2146729
- config_name: tr_imst
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1347524
    num_examples: 983
  - name: train
    num_bytes: 5063905
    num_examples: 3664
  - name: validation
    num_bytes: 1342351
    num_examples: 988
  download_size: 4711018
  dataset_size: 7753780
- config_name: tr_pud
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2021772
    num_examples: 1000
  download_size: 1359487
  dataset_size: 2021772
- config_name: uk_iu
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 3561164
    num_examples: 892
  - name: train
    num_bytes: 18886802
    num_examples: 5496
  - name: validation
    num_bytes: 2592721
    num_examples: 672
  download_size: 17344586
  dataset_size: 25040687
- config_name: hsb_ufal
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1246592
    num_examples: 623
  - name: train
    num_bytes: 54257
    num_examples: 23
  download_size: 781067
  dataset_size: 1300849
- config_name: ur_udtb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 2702596
    num_examples: 535
  - name: train
    num_bytes: 19808745
    num_examples: 4043
  - name: validation
    num_bytes: 2652349
    num_examples: 552
  download_size: 15901007
  dataset_size: 25163690
- config_name: ug_udt
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1371993
    num_examples: 900
  - name: train
    num_bytes: 2570856
    num_examples: 1656
  - name: validation
    num_bytes: 1406032
    num_examples: 900
  download_size: 3455092
  dataset_size: 5348881
- config_name: vi_vtb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 987207
    num_examples: 800
  - name: train
    num_bytes: 1689772
    num_examples: 1400
  - name: validation
    num_bytes: 948019
    num_examples: 800
  download_size: 2055529
  dataset_size: 3624998
- config_name: wbp_ufal
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 48533
    num_examples: 55
  download_size: 38326
  dataset_size: 48533
- config_name: cy_ccg
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1779002
    num_examples: 953
  - name: train
    num_bytes: 1629465
    num_examples: 704
  download_size: 1984759
  dataset_size: 3408467
- config_name: wo_wtb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 1227124
    num_examples: 470
  - name: train
    num_bytes: 2781883
    num_examples: 1188
  - name: validation
    num_bytes: 1204839
    num_examples: 449
  download_size: 3042699
  dataset_size: 5213846
- config_name: yo_ytb
  features:
  - name: idx
    dtype: string
  - name: text
    dtype: string
  - name: tokens
    sequence: string
  - name: lemmas
    sequence: string
  - name: upos
    sequence:
      class_label:
        names:
          0: NOUN
          1: PUNCT
          2: ADP
          3: NUM
          4: SYM
          5: SCONJ
          6: ADJ
          7: PART
          8: DET
          9: CCONJ
          10: PROPN
          11: PRON
          12: X
          13: _
          14: ADV
          15: INTJ
          16: VERB
          17: AUX
  - name: xpos
    sequence: string
  - name: feats
    sequence: string
  - name: head
    sequence: string
  - name: deprel
    sequence: string
  - name: deps
    sequence: string
  - name: misc
    sequence: string
  splits:
  - name: test
    num_bytes: 905766
    num_examples: 318
  download_size: 567955
  dataset_size: 905766
---

# Dataset Card for Universal Dependencies Treebank

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

- **Homepage:** [Universal Dependencies](https://universaldependencies.org/)
- **Repository:**
- **Paper:**
- **Leaderboard:**
- **Point of Contact:**

### Dataset Summary

[More Information Needed]

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

[More Information Needed]

## Dataset Structure

### Data Instances

[More Information Needed]

### Data Fields

[More Information Needed]

### Data Splits

[More Information Needed]

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

[More Information Needed]
### Contributions

Thanks to [@patrickvonplaten](https://github.com/patrickvonplaten), [@jplu](https://github.com/jplu) for adding this dataset.