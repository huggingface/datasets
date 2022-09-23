---
annotations_creators:
- expert-generated
language_creators:
- found
language:
- ady
- ang
- ar
- arn
- ast
- az
- ba
- be
- bg
- bn
- bo
- br
- ca
- ckb
- crh
- cs
- csb
- cu
- cy
- da
- de
- dsb
- el
- en
- es
- et
- eu
- fa
- fi
- fo
- fr
- frm
- fro
- frr
- fur
- fy
- ga
- gal
- gd
- gmh
- gml
- got
- grc
- gv
- hai
- he
- hi
- hu
- hy
- is
- it
- izh
- ka
- kbd
- kjh
- kk
- kl
- klr
- kmr
- kn
- krl
- kw
- la
- liv
- lld
- lt
- lud
- lv
- mk
- mt
- mwf
- nap
- nb
- nds
- nl
- nn
- nv
- oc
- olo
- osx
- pl
- ps
- pt
- qu
- ro
- ru
- sa
- sga
- sh
- sl
- sme
- sq
- sv
- swc
- syc
- te
- tg
- tk
- tr
- tt
- uk
- ur
- uz
- vec
- vep
- vot
- xcl
- xno
- yi
- zu
license:
- cc-by-sa-3.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- token-classification
- text-classification
task_ids:
- multi-class-classification
- multi-label-classification
- token-classification-other-morphology
paperswithcode_id: null
pretty_name: UniversalMorphologies
configs:
- ady
- ang
- ara
- arn
- ast
- aze
- bak
- bel
- ben
- bod
- bre
- bul
- cat
- ces
- chu
- ckb
- cor
- crh
- csb
- cym
- dan
- deu
- dsb
- ell
- eng
- est
- eus
- fao
- fas
- fin
- fra
- frm
- fro
- frr
- fry
- fur
- gal
- gla
- gle
- glv
- gmh
- gml
- got
- grc
- hai
- hbs
- heb
- hin
- hun
- hye
- isl
- ita
- izh
- kal
- kan
- kat
- kaz
- kbd
- kjh
- klr
- kmr
- krl
- lat
- lav
- lit
- liv
- lld
- lud
- mkd
- mlt
- mwf
- nap
- nav
- nds
- nld
- nno
- nob
- oci
- olo
- osx
- pol
- por
- pus
- que
- ron
- rus
- san
- sga
- slv
- sme
- spa
- sqi
- swc
- swe
- syc
- tat
- tel
- tgk
- tuk
- tur
- ukr
- urd
- uzb
- vec
- vep
- vot
- xcl
- xno
- yid
- zul
dataset_info:
- config_name: ady
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 3428235
    num_examples: 1666
  download_size: 1008487
  dataset_size: 3428235
- config_name: ang
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 6569844
    num_examples: 1867
  download_size: 1435972
  dataset_size: 6569844
- config_name: ara
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 24388295
    num_examples: 4134
  download_size: 7155824
  dataset_size: 24388295
- config_name: arn
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 124050
    num_examples: 26
  download_size: 20823
  dataset_size: 124050
- config_name: ast
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 4913008
    num_examples: 436
  download_size: 1175901
  dataset_size: 4913008
- config_name: aze
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1248687
    num_examples: 340
  download_size: 276306
  dataset_size: 1248687
- config_name: bak
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1984657
    num_examples: 1084
  download_size: 494758
  dataset_size: 1984657
- config_name: bel
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2626405
    num_examples: 1027
  download_size: 739537
  dataset_size: 2626405
- config_name: ben
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 746181
    num_examples: 136
  download_size: 251991
  dataset_size: 746181
- config_name: bod
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 880074
    num_examples: 1335
  download_size: 197523
  dataset_size: 880074
- config_name: bre
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 387583
    num_examples: 44
  download_size: 82159
  dataset_size: 387583
- config_name: bul
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 9589915
    num_examples: 2468
  download_size: 3074574
  dataset_size: 9589915
- config_name: cat
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 12988492
    num_examples: 1547
  download_size: 2902458
  dataset_size: 12988492
- config_name: ces
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 21056640
    num_examples: 5125
  download_size: 4875288
  dataset_size: 21056640
- config_name: chu
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 628237
    num_examples: 152
  download_size: 149081
  dataset_size: 628237
- config_name: ckb
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 3843267
    num_examples: 274
  download_size: 914302
  dataset_size: 3843267
- config_name: cor
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 83434
    num_examples: 9
  download_size: 17408
  dataset_size: 83434
- config_name: crh
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1154595
    num_examples: 1230
  download_size: 186325
  dataset_size: 1154595
- config_name: csb
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 82172
    num_examples: 37
  download_size: 14259
  dataset_size: 82172
- config_name: cym
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1748431
    num_examples: 183
  download_size: 374501
  dataset_size: 1748431
- config_name: dan
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 4204551
    num_examples: 3193
  download_size: 845939
  dataset_size: 4204551
- config_name: deu
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 28436466
    num_examples: 15060
  download_size: 5966618
  dataset_size: 28436466
- config_name: dsb
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2985168
    num_examples: 994
  download_size: 536096
  dataset_size: 2985168
- config_name: ell
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 34112450
    num_examples: 11906
  download_size: 11222248
  dataset_size: 34112450
- config_name: eng
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 18455909
    num_examples: 22765
  download_size: 3285554
  dataset_size: 18455909
- config_name: est
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 6125879
    num_examples: 886
  download_size: 1397385
  dataset_size: 6125879
- config_name: eus
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2444247
    num_examples: 26
  download_size: 876480
  dataset_size: 2444247
- config_name: fao
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 7117926
    num_examples: 3077
  download_size: 1450065
  dataset_size: 7117926
- config_name: fas
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 6382709
    num_examples: 273
  download_size: 2104724
  dataset_size: 6382709
- config_name: fin
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: '1'
    num_bytes: 331855860
    num_examples: 46152
  - name: '2'
    num_bytes: 81091817
    num_examples: 11491
  download_size: 109324828
  dataset_size: 412947677
- config_name: fra
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 58747699
    num_examples: 7535
  download_size: 13404983
  dataset_size: 58747699
- config_name: frm
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 6015940
    num_examples: 603
  download_size: 1441122
  dataset_size: 6015940
- config_name: fro
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 20260793
    num_examples: 1700
  download_size: 4945582
  dataset_size: 20260793
- config_name: frr
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 526898
    num_examples: 51
  download_size: 112236
  dataset_size: 526898
- config_name: fry
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 222067
    num_examples: 85
  download_size: 38227
  dataset_size: 222067
- config_name: fur
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1282374
    num_examples: 168
  download_size: 258793
  dataset_size: 1282374
- config_name: gal
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 5844604
    num_examples: 486
  download_size: 1259120
  dataset_size: 5844604
- config_name: gla
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 126847
    num_examples: 73
  download_size: 25025
  dataset_size: 126847
- config_name: gle
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 17065939
    num_examples: 7464
  download_size: 3853188
  dataset_size: 17065939
- config_name: glv
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 7523
    num_examples: 1
  download_size: 401
  dataset_size: 7523
- config_name: gmh
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 114677
    num_examples: 29
  download_size: 20851
  dataset_size: 114677
- config_name: gml
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 233831
    num_examples: 52
  download_size: 47151
  dataset_size: 233831
- config_name: got
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
  download_size: 2
  dataset_size: 0
- config_name: grc
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 6779867
    num_examples: 2431
  download_size: 2057514
  dataset_size: 6779867
- config_name: hai
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1166240
    num_examples: 41
  download_size: 329817
  dataset_size: 1166240
- config_name: hbs
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 132933961
    num_examples: 24419
  download_size: 32194142
  dataset_size: 132933961
- config_name: heb
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2211208
    num_examples: 510
  download_size: 498065
  dataset_size: 2211208
- config_name: hin
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 10083004
    num_examples: 258
  download_size: 3994359
  dataset_size: 10083004
- config_name: hun
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 83517327
    num_examples: 14892
  download_size: 19544319
  dataset_size: 83517327
- config_name: hye
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 56537127
    num_examples: 7033
  download_size: 17810316
  dataset_size: 56537127
- config_name: isl
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 12120572
    num_examples: 4775
  download_size: 2472980
  dataset_size: 12120572
- config_name: ita
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 81905203
    num_examples: 10009
  download_size: 19801423
  dataset_size: 81905203
- config_name: izh
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 170094
    num_examples: 50
  download_size: 28558
  dataset_size: 170094
- config_name: kal
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 60434
    num_examples: 23
  download_size: 9795
  dataset_size: 60434
- config_name: kan
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1052294
    num_examples: 159
  download_size: 318512
  dataset_size: 1052294
- config_name: kat
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 12532540
    num_examples: 3782
  download_size: 4678979
  dataset_size: 12532540
- config_name: kaz
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 62519
    num_examples: 26
  download_size: 14228
  dataset_size: 62519
- config_name: kbd
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 511406
    num_examples: 250
  download_size: 133788
  dataset_size: 511406
- config_name: kjh
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 193741
    num_examples: 75
  download_size: 44907
  dataset_size: 193741
- config_name: klr
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 28909688
    num_examples: 591
  download_size: 7561829
  dataset_size: 28909688
- config_name: kmr
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 35504487
    num_examples: 15083
  download_size: 8592722
  dataset_size: 35504487
- config_name: krl
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 106475
    num_examples: 20
  download_size: 19024
  dataset_size: 106475
- config_name: lat
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 81932667
    num_examples: 17214
  download_size: 19567252
  dataset_size: 81932667
- config_name: lav
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 21219584
    num_examples: 7548
  download_size: 5048680
  dataset_size: 21219584
- config_name: lit
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 5287268
    num_examples: 1458
  download_size: 1191554
  dataset_size: 5287268
- config_name: liv
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 642166
    num_examples: 203
  download_size: 141467
  dataset_size: 642166
- config_name: lld
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1240257
    num_examples: 180
  download_size: 278592
  dataset_size: 1240257
- config_name: lud
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: mikhailovskoye
    num_bytes: 11361
    num_examples: 2
  - name: new_written
    num_bytes: 35132
    num_examples: 94
  - name: southern_ludian_svjatozero
    num_bytes: 57276
    num_examples: 71
  download_size: 14697
  dataset_size: 103769
- config_name: mkd
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 27800390
    num_examples: 10313
  download_size: 8157589
  dataset_size: 27800390
- config_name: mlt
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 604577
    num_examples: 112
  download_size: 124584
  dataset_size: 604577
- config_name: mwf
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 172890
    num_examples: 29
  download_size: 25077
  dataset_size: 172890
- config_name: nap
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 293699
    num_examples: 40
  download_size: 64163
  dataset_size: 293699
- config_name: nav
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2051393
    num_examples: 674
  download_size: 523673
  dataset_size: 2051393
- config_name: nds
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
  download_size: 2
  dataset_size: 0
- config_name: nld
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 8813867
    num_examples: 4993
  download_size: 1874427
  dataset_size: 8813867
- config_name: nno
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2704566
    num_examples: 4689
  download_size: 420695
  dataset_size: 2704566
- config_name: nob
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 3359706
    num_examples: 5527
  download_size: 544432
  dataset_size: 3359706
- config_name: oci
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1327716
    num_examples: 174
  download_size: 276611
  dataset_size: 1327716
- config_name: olo
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: kotkozero
    num_bytes: 7682
    num_examples: 5
  - name: new_written
    num_bytes: 11158424
    num_examples: 15293
  - name: syamozero
    num_bytes: 6379
    num_examples: 2
  - name: vedlozero
    num_bytes: 6120
    num_examples: 1
  - name: vidlitsa
    num_bytes: 54363
    num_examples: 3
  download_size: 2130154
  dataset_size: 11232968
- config_name: osx
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 3500590
    num_examples: 863
  download_size: 759997
  dataset_size: 3500590
- config_name: pol
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 30855235
    num_examples: 10185
  download_size: 6666266
  dataset_size: 30855235
- config_name: por
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 48530106
    num_examples: 4001
  download_size: 10982524
  dataset_size: 48530106
- config_name: pus
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1176421
    num_examples: 395
  download_size: 297043
  dataset_size: 1176421
- config_name: que
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 27823298
    num_examples: 1006
  download_size: 6742890
  dataset_size: 27823298
- config_name: ron
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 13187957
    num_examples: 4405
  download_size: 2990521
  dataset_size: 13187957
- config_name: rus
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 77484460
    num_examples: 28068
  download_size: 25151401
  dataset_size: 77484460
- config_name: san
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 5500001
    num_examples: 917
  download_size: 1788739
  dataset_size: 5500001
- config_name: sga
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 190479
    num_examples: 49
  download_size: 43469
  dataset_size: 190479
- config_name: slv
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 9071547
    num_examples: 2535
  download_size: 1911039
  dataset_size: 9071547
- config_name: sme
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 9764653
    num_examples: 2103
  download_size: 2050015
  dataset_size: 9764653
- config_name: spa
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 61472202
    num_examples: 5460
  download_size: 14386131
  dataset_size: 61472202
- config_name: sqi
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 5422400
    num_examples: 589
  download_size: 1261468
  dataset_size: 5422400
- config_name: swc
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1694529
    num_examples: 100
  download_size: 414624
  dataset_size: 1694529
- config_name: swe
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 12897827
    num_examples: 10553
  download_size: 2709960
  dataset_size: 12897827
- config_name: syc
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 553392
    num_examples: 160
  download_size: 130000
  dataset_size: 553392
- config_name: tat
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1203356
    num_examples: 1283
  download_size: 194277
  dataset_size: 1203356
- config_name: tel
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 285769
    num_examples: 127
  download_size: 95069
  dataset_size: 285769
- config_name: tgk
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 25276
    num_examples: 75
  download_size: 2366
  dataset_size: 25276
- config_name: tuk
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 127712
    num_examples: 68
  download_size: 20540
  dataset_size: 127712
- config_name: tur
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 44723850
    num_examples: 3579
  download_size: 11552946
  dataset_size: 44723850
- config_name: ukr
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 3299187
    num_examples: 1493
  download_size: 870660
  dataset_size: 3299187
- config_name: urd
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2197237
    num_examples: 182
  download_size: 685613
  dataset_size: 2197237
- config_name: uzb
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 196802
    num_examples: 15
  download_size: 41921
  dataset_size: 196802
- config_name: vec
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 2892987
    num_examples: 368
  download_size: 615931
  dataset_size: 2892987
- config_name: vep
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: central_eastern
    num_bytes: 500981
    num_examples: 65
  - name: central_western
    num_bytes: 2527618
    num_examples: 111
  - name: new_written
    num_bytes: 79899484
    num_examples: 9304
  - name: northern
    num_bytes: 175242
    num_examples: 21
  - name: southern
    num_bytes: 206289
    num_examples: 17
  download_size: 20131151
  dataset_size: 83309614
- config_name: vot
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 217663
    num_examples: 55
  download_size: 37179
  dataset_size: 217663
- config_name: xcl
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 16856327
    num_examples: 4300
  download_size: 4950513
  dataset_size: 16856327
- config_name: xno
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 48938
    num_examples: 5
  download_size: 9641
  dataset_size: 48938
- config_name: yid
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 1409582
    num_examples: 803
  download_size: 429391
  dataset_size: 1409582
- config_name: zul
  features:
  - name: lemma
    dtype: string
  - name: forms
    sequence:
    - name: word
      dtype: string
    - name: Aktionsart
      sequence:
        class_label:
          names:
            0: STAT
            1: DYN
            2: TEL
            3: ATEL
            4: PCT
            5: DUR
            6: ACH
            7: ACCMP
            8: SEMEL
            9: ACTY
    - name: Animacy
      sequence:
        class_label:
          names:
            0: ANIM
            1: INAN
            2: HUM
            3: NHUM
    - name: Argument_Marking
      sequence:
        class_label:
          names:
            0: ARGNO1S
            1: ARGNO2S
            2: ARGNO3S
            3: ARGNO1P
            4: ARGNO2P
            5: ARGNO3P
            6: ARGAC1S
            7: ARGAC2S
            8: ARGAC3S
            9: ARGAC1P
            10: ARGAC2P
            11: ARGAC3P
            12: ARGAB1S
            13: ARGAB2S
            14: ARGAB3S
            15: ARGAB1P
            16: ARGAB2P
            17: ARGAB3P
            18: ARGER1S
            19: ARGER2S
            20: ARGER3S
            21: ARGER1P
            22: ARGER2P
            23: ARGER3P
            24: ARGDA1S
            25: ARGDA2S
            26: ARGDA3S
            27: ARGDA1P
            28: ARGDA2P
            29: ARGDA3P
            30: ARGBE1S
            31: ARGBE2S
            32: ARGBE3S
            33: ARGBE1P
            34: ARGBE2P
            35: ARGBE3P
    - name: Aspect
      sequence:
        class_label:
          names:
            0: IPFV
            1: PFV
            2: PRF
            3: PROG
            4: PROSP
            5: ITER
            6: HAB
    - name: Case
      sequence:
        class_label:
          names:
            0: NOM
            1: ACC
            2: ERG
            3: ABS
            4: NOMS
            5: DAT
            6: BEN
            7: PRP
            8: GEN
            9: REL
            10: PRT
            11: INS
            12: COM
            13: VOC
            14: COMPV
            15: EQTV
            16: PRIV
            17: PROPR
            18: AVR
            19: FRML
            20: TRANS
            21: BYWAY
            22: INTER
            23: AT
            24: POST
            25: IN
            26: CIRC
            27: ANTE
            28: APUD
            29: 'ON'
            30: ONHR
            31: ONVR
            32: SUB
            33: REM
            34: PROXM
            35: ESS
            36: ALL
            37: ABL
            38: APPRX
            39: TERM
    - name: Comparison
      sequence:
        class_label:
          names:
            0: CMPR
            1: SPRL
            2: AB
            3: RL
            4: EQT
    - name: Definiteness
      sequence:
        class_label:
          names:
            0: DEF
            1: INDF
            2: SPEC
            3: NSPEC
    - name: Deixis
      sequence:
        class_label:
          names:
            0: PROX
            1: MED
            2: REMT
            3: REF1
            4: REF2
            5: NOREF
            6: PHOR
            7: VIS
            8: NVIS
            9: ABV
            10: EVEN
            11: BEL
    - name: Evidentiality
      sequence:
        class_label:
          names:
            0: FH
            1: DRCT
            2: SEN
            3: VISU
            4: NVSEN
            5: AUD
            6: NFH
            7: QUOT
            8: RPRT
            9: HRSY
            10: INFER
            11: ASSUM
    - name: Finiteness
      sequence:
        class_label:
          names:
            0: FIN
            1: NFIN
    - name: Gender
      sequence:
        class_label:
          names:
            0: MASC
            1: FEM
            2: NEUT
            3: NAKH1
            4: NAKH2
            5: NAKH3
            6: NAKH4
            7: NAKH5
            8: NAKH6
            9: NAKH7
            10: NAKH8
            11: BANTU1
            12: BANTU2
            13: BANTU3
            14: BANTU4
            15: BANTU5
            16: BANTU6
            17: BANTU7
            18: BANTU8
            19: BANTU9
            20: BANTU10
            21: BANTU11
            22: BANTU12
            23: BANTU13
            24: BANTU14
            25: BANTU15
            26: BANTU16
            27: BANTU17
            28: BANTU18
            29: BANTU19
            30: BANTU20
            31: BANTU21
            32: BANTU22
            33: BANTU23
    - name: Information_Structure
      sequence:
        class_label:
          names:
            0: TOP
            1: FOC
    - name: Interrogativity
      sequence:
        class_label:
          names:
            0: DECL
            1: INT
    - name: Language_Specific
      sequence:
        class_label:
          names:
            0: LGSPEC1
            1: LGSPEC2
            2: LGSPEC3
            3: LGSPEC4
            4: LGSPEC5
            5: LGSPEC6
            6: LGSPEC7
            7: LGSPEC8
            8: LGSPEC9
            9: LGSPEC10
    - name: Mood
      sequence:
        class_label:
          names:
            0: IND
            1: SBJV
            2: REAL
            3: IRR
            4: AUPRP
            5: AUNPRP
            6: IMP
            7: COND
            8: PURP
            9: INTEN
            10: POT
            11: LKLY
            12: ADM
            13: OBLIG
            14: DEB
            15: PERM
            16: DED
            17: SIM
            18: OPT
    - name: Number
      sequence:
        class_label:
          names:
            0: SG
            1: PL
            2: GRPL
            3: DU
            4: TRI
            5: PAUC
            6: GRPAUC
            7: INVN
    - name: Part_Of_Speech
      sequence:
        class_label:
          names:
            0: N
            1: PROPN
            2: ADJ
            3: PRO
            4: CLF
            5: ART
            6: DET
            7: V
            8: ADV
            9: AUX
            10: V.PTCP
            11: V.MSDR
            12: V.CVB
            13: ADP
            14: COMP
            15: CONJ
            16: NUM
            17: PART
            18: INTJ
    - name: Person
      sequence:
        class_label:
          names:
            0: '0'
            1: '1'
            2: '2'
            3: '3'
            4: '4'
            5: INCL
            6: EXCL
            7: PRX
            8: OBV
    - name: Polarity
      sequence:
        class_label:
          names:
            0: POS
            1: NEG
    - name: Politeness
      sequence:
        class_label:
          names:
            0: INFM
            1: FORM
            2: ELEV
            3: HUMB
            4: POL
            5: AVOID
            6: LOW
            7: HIGH
            8: STELEV
            9: STSUPR
            10: LIT
            11: FOREG
            12: COL
    - name: Possession
      sequence:
        class_label:
          names:
            0: ALN
            1: NALN
            2: PSS1S
            3: PSS2S
            4: PSS2SF
            5: PSS2SM
            6: PSS2SINFM
            7: PSS2SFORM
            8: PSS3S
            9: PSS3SF
            10: PSS3SM
            11: PSS1D
            12: PSS1DI
            13: PSS1DE
            14: PSS2D
            15: PSS2DM
            16: PSS2DF
            17: PSS3D
            18: PSS3DF
            19: PSS3DM
            20: PSS1P
            21: PSS1PI
            22: PSS1PE
            23: PSS2P
            24: PSS2PF
            25: PSS2PM
            26: PSS3PF
            27: PSS3PM
    - name: Switch_Reference
      sequence:
        class_label:
          names:
            0: SS
            1: SSADV
            2: DS
            3: DSADV
            4: OR
            5: SIMMA
            6: SEQMA
            7: LOG
    - name: Tense
      sequence:
        class_label:
          names:
            0: PRS
            1: PST
            2: FUT
            3: IMMED
            4: HOD
            5: 1DAY
            6: RCT
            7: RMT
    - name: Valency
      sequence:
        class_label:
          names:
            0: IMPRS
            1: INTR
            2: TR
            3: DITR
            4: REFL
            5: RECP
            6: CAUS
            7: APPL
    - name: Voice
      sequence:
        class_label:
          names:
            0: ACT
            1: MID
            2: PASS
            3: ANTIP
            4: DIR
            5: INV
            6: AGFOC
            7: PFOC
            8: LFOC
            9: BFOC
            10: ACFOC
            11: IFOC
            12: CFOC
    - name: Other
      sequence: string
  splits:
  - name: train
    num_bytes: 7152507
    num_examples: 566
  download_size: 1581402
  dataset_size: 7152507
---

# Dataset Card for [Dataset Name]

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

- **Homepage:** [UniMorph Homepage](https://unimorph.github.io/)
- **Repository:** [List of UniMorph repositories](https://github.com/unimorph)
- **Paper:** [The Composition and Use of the Universal Morphological Feature Schema (UniMorph Schema)](https://unimorph.github.io/doc/unimorph-schema.pdf)
- **Point of Contact:** [Arya McCarthy](mailto:arya@jhu.edu)

### Dataset Summary

The Universal Morphology (UniMorph) project is a collaborative effort to improve how NLP handles complex morphology in the world’s languages.
The goal of UniMorph is to annotate morphological data in a universal schema that allows an inflected word from any language to be defined by its lexical meaning,
typically carried by the lemma, and by a rendering of its inflectional form in terms of a bundle of morphological features from our schema.
The specification of the schema is described in Sylak-Glassman (2016).

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The current version of the UniMorph dataset covers 110 languages.

## Dataset Structure

### Data Instances

Each data instance comprises of a lemma and a set of possible realizations with morphological and meaning annotations. For example:
```
{'forms': {'Aktionsart': [[], [], [], [], []],
  'Animacy': [[], [], [], [], []],
  ...
  'Finiteness': [[], [], [], [1], []],
  ...
  'Number': [[], [], [0], [], []],
  'Other': [[], [], [], [], []],
  'Part_Of_Speech': [[7], [10], [7], [7], [10]],
  ...
  'Tense': [[1], [1], [0], [], [0]],
  ...
  'word': ['ablated', 'ablated', 'ablates', 'ablate', 'ablating']},
 'lemma': 'ablate'}
```

### Data Fields

Each instance in the dataset has the following fields:
- `lemma`: the common lemma for all all_forms
- `forms`: all annotated forms for this lemma, with:
  - `word`: the full word form
  - [`category`]: a categorical variable denoting one or several tags in a category (several to represent composite tags, originally denoted with `A+B`). The full list of categories and possible tags for each can be found [here](https://github.com/unimorph/unimorph.github.io/blob/master/unimorph-schema-json/dimensions-to-features.json)


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

Thanks to [@yjernite](https://github.com/yjernite) for adding this dataset.