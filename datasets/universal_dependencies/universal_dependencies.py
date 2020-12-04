from __future__ import absolute_import, division, print_function

import conllu

import datasets


_CITATION = """\
@misc{11234/1-3424,
title = {Universal Dependencies 2.7},
author = {Zeman, Daniel and Nivre, Joakim and Abrams, Mitchell and Ackermann, Elia and Aepli, No{\"e}mi and Aghaei, Hamid and Agi{\'c}, {\v Z}eljko and Ahmadi, Amir and Ahrenberg, Lars and Ajede, Chika Kennedy and Aleksandravi{\v c}i{\=u}t{\.e}, Gabriel{\.e} and Alfina, Ika and Antonsen, Lene and Aplonova, Katya and Aquino, Angelina and Aragon, Carolina and Aranzabe, Maria Jesus and Arnard{\'o}ttir, {\t H}{\'o}runn and Arutie, Gashaw and Arwidarasti, Jessica Naraiswari and Asahara, Masayuki and Ateyah, Luma and Atmaca, Furkan and Attia, Mohammed and Atutxa, Aitziber and Augustinus, Liesbeth and Badmaeva, Elena and Balasubramani, Keerthana and Ballesteros, Miguel and Banerjee, Esha and Bank, Sebastian and Barbu Mititelu, Verginica and Basmov, Victoria and Batchelor, Colin and Bauer, John and Bedir, Seyyit Talha and Bengoetxea, Kepa and Berk, G{\"o}zde and Berzak, Yevgeni and Bhat, Irshad Ahmad and Bhat, Riyaz Ahmad and Biagetti, Erica and Bick, Eckhard and Bielinskien{\.e}, Agn{\.e} and Bjarnad{\'o}ttir, Krist{\'{\i}}n and Blokland, Rogier and Bobicev, Victoria and Boizou, Lo{\"{\i}}c and Borges V{\"o}lker, Emanuel and B{\"o}rstell, Carl and Bosco, Cristina and Bouma, Gosse and Bowman, Sam and Boyd, Adriane and Brokait{\.e}, Kristina and Burchardt, Aljoscha and Candito, Marie and Caron, Bernard and Caron, Gauthier and Cavalcanti, Tatiana and Cebiroglu Eryigit, Gulsen and Cecchini, Flavio Massimiliano and Celano, Giuseppe G. A. and Ceplo, Slavomir and Cetin, Savas and Cetinoglu, Ozlem and Chalub, Fabricio and Chi, Ethan and Cho, Yongseok and Choi, Jinho and Chun, Jayeol and Cignarella, Alessandra T. and Cinkova, Silvie and Collomb, Aurelie and Coltekin, Cagr{\i} and Connor, Miriam and Courtin, Marine and Davidson, Elizabeth and de Marneffe, Marie-Catherine and de Paiva, Valeria and Derin, Mehmet Oguz and de Souza, Elvis and Diaz de Ilarraza, Arantza and Dickerson, Carly and Dinakaramani, Arawinda and Dione, Bamba and Dirix, Peter and Dobrovoljc, Kaja and Dozat, Timothy and Droganova, Kira and Dwivedi, Puneet and Eckhoff, Hanne and Eli, Marhaba and Elkahky, Ali and Ephrem, Binyam and Erina, Olga and Erjavec, Tomaz and Etienne, Aline and Evelyn, Wograine and Facundes, Sidney and Farkas, Rich{\'a}rd and Fernanda, Mar{\'{\i}}lia and Fernandez Alcalde, Hector and Foster, Jennifer and Freitas, Cl{\'a}udia and Fujita, Kazunori and Gajdosov{\'a}, Katar{\'{\i}}na and Galbraith, Daniel and Garcia, Marcos and G{\"a}rdenfors, Moa and Garza, Sebastian and Gerardi, Fabr{\'{\i}}cio Ferraz and Gerdes, Kim and Ginter, Filip and Goenaga, Iakes and Gojenola, Koldo and G{\"o}k{\i}rmak, Memduh and Goldberg, Yoav and G{\'o}mez Guinovart, Xavier and Gonz{\'a}lez Saavedra,
Berta and Grici{\=u}t{\.e}, Bernadeta and Grioni, Matias and Grobol, Lo{\"{\i}}c and Gr{\=u}z{\={\i}}tis, Normunds and Guillaume, Bruno and Guillot-Barbance, C{\'e}line and G{\"u}ng{\"o}r, Tunga and Habash, Nizar and Hafsteinsson, Hinrik and Haji{\v c}, Jan and Haji{\v c} jr., Jan and H{\"a}m{\"a}l{\"a}inen, Mika and H{\`a} M{\~y}, Linh and Han, Na-Rae and Hanifmuti, Muhammad Yudistira and Hardwick, Sam and Harris, Kim and Haug, Dag and Heinecke, Johannes and Hellwig, Oliver and Hennig, Felix and Hladk{\'a}, Barbora and Hlav{\'a}{\v c}ov{\'a}, Jaroslava and Hociung, Florinel and Hohle, Petter and Huber, Eva and Hwang, Jena and Ikeda, Takumi and Ingason, Anton Karl and Ion, Radu and Irimia, Elena and Ishola, {\d O}l{\'a}j{\'{\i}}d{\'e} and Jel{\'{\i}}nek, Tom{\'a}{\v s} and Johannsen, Anders and J{\'o}nsd{\'o}ttir, Hildur and J{\o}rgensen, Fredrik and Juutinen, Markus and K, Sarveswaran and Ka{\c s}{\i}kara, H{\"u}ner and Kaasen, Andre and Kabaeva, Nadezhda and Kahane, Sylvain and Kanayama, Hiroshi and Kanerva, Jenna and Katz, Boris and Kayadelen, Tolga and Kenney, Jessica and Kettnerov{\'a}, V{\'a}clava and Kirchner, Jesse and Klementieva, Elena and K{\"o}hn, Arne and K{\"o}ksal, Abdullatif and Kopacewicz, Kamil and Korkiakangas, Timo and Kotsyba, Natalia and Kovalevskait{\.e}, Jolanta and Krek, Simon and Krishnamurthy, Parameswari and Kwak, Sookyoung and Laippala, Veronika and Lam, Lucia and Lambertino, Lorenzo and Lando, Tatiana and Larasati, Septina Dian and Lavrentiev, Alexei and Lee, John and L{\^e} H{\`{\^o}}ng, Phương and Lenci, Alessandro and Lertpradit, Saran and Leung, Herman and Levina, Maria and Li, Cheuk Ying and Li, Josie and Li, Keying and Li, Yuan and Lim, {KyungTae} and Linden, Krister and Ljubesic, Nikola and Loginova, Olga and Luthfi, Andry and Luukko, Mikko and Lyashevskaya, Olga and Lynn, Teresa and Macketanz, Vivien and Makazhanov, Aibek and Mandl, Michael and Manning, Christopher and Manurung, Ruli and Maranduc, Catalina and Marcek, David and Marheinecke, Katrin and Mart{\'{\i}}nez Alonso, H{\'e}ctor and Martins, Andr{\'e} and Masek, Jan and Matsuda, Hiroshi and Matsumoto, Yuji and {McDonald}, Ryan and {McGuinness}, Sarah and Mendonca, Gustavo and Miekka, Niko and Mischenkova, Karina and Misirpashayeva, Margarita and Missil{\"a}, Anna and Mititelu, Catalin and Mitrofan, Maria and Miyao, Yusuke and Mojiri Foroushani, {AmirHossein} and Moloodi, Amirsaeid and Montemagni, Simonetta and More, Amir and Moreno Romero, Laura and Mori, Keiko Sophie and Mori, Shinsuke and Morioka, Tomohiko and Moro, Shigeki and Mortensen, Bjartur and Moskalevskyi, Bohdan and Muischnek, Kadri and Munro, Robert and Murawaki, Yugo and M{\"u}{\"u}risep, Kaili and Nainwani, Pinkey and Nakhl{\'e}, Mariam and Navarro Hor{\~n}iacek, Juan Ignacio and Nedoluzhko,
Anna and Ne{\v s}pore-B{\=e}rzkalne, Gunta and Nguy{\~{\^e}}n Th{\d i}, Lương and Nguy{\~{\^e}}n Th{\d i} Minh, Huy{\`{\^e}}n and Nikaido, Yoshihiro and Nikolaev, Vitaly and Nitisaroj, Rattima and Nourian, Alireza and Nurmi, Hanna and Ojala, Stina and Ojha, Atul Kr. and Ol{\'u}{\`o}kun, Ad{\'e}day{\d o}̀ and Omura, Mai and Onwuegbuzia, Emeka and Osenova, Petya and {\"O}stling, Robert and {\O}vrelid, Lilja and {\"O}zate{\c s}, {\c S}aziye Bet{\"u}l and {\"O}zg{\"u}r, Arzucan and {\"O}zt{\"u}rk Ba{\c s}aran, Balk{\i}z and Partanen, Niko and Pascual, Elena and Passarotti, Marco and Patejuk, Agnieszka and Paulino-Passos, Guilherme and Peljak-{\L}api{\'n}ska, Angelika and Peng, Siyao and Perez, Cenel-Augusto and Perkova, Natalia and Perrier, Guy and Petrov, Slav and Petrova, Daria and Phelan, Jason and Piitulainen, Jussi and Pirinen, Tommi A and Pitler, Emily and Plank, Barbara and Poibeau, Thierry and Ponomareva, Larisa and Popel, Martin and Pretkalnina, Lauma and Pr{\'e}vost, Sophie and Prokopidis, Prokopis and Przepi{\'o}rkowski, Adam and Puolakainen, Tiina and Pyysalo, Sampo and Qi, Peng and R{\"a}{\"a}bis, Andriela and Rademaker, Alexandre and Rama, Taraka and Ramasamy, Loganathan and Ramisch, Carlos and Rashel, Fam and Rasooli, Mohammad Sadegh and Ravishankar, Vinit and Real, Livy and Rebeja, Petru and Reddy, Siva and Rehm, Georg and Riabov, Ivan and Rie{\ss}ler, Michael and Rimkut{\.e}, Erika and Rinaldi, Larissa and Rituma, Laura and Rocha, Luisa and R{\"o}gnvaldsson, Eir{\'{\i}}kur and Romanenko, Mykhailo and Rosa, Rudolf and Roșca, Valentin and Rovati, Davide and Rudina, Olga and Rueter, Jack and R{\'u}narsson, Kristjan and Sadde, Shoval and Safari, Pegah and Sagot, Benoit and Sahala, Aleksi and Saleh, Shadi and Salomoni, Alessio and Samardzi{\'c}, Tanja and Samson, Stephanie and Sanguinetti, Manuela and S{\"a}rg,
Dage and Saul{\={\i}}te, Baiba and Sawanakunanon, Yanin and Scannell, Kevin and Scarlata, Salvatore and Schneider, Nathan and Schuster, Sebastian and Seddah, Djam{\'e} and Seeker, Wolfgang and Seraji, Mojgan and Shen, Mo and Shimada, Atsuko and Shirasu, Hiroyuki and Shohibussirri, Muh and Sichinava, Dmitry and Sigurðsson, Einar Freyr and Silveira, Aline and Silveira, Natalia and Simi, Maria and Simionescu, Radu and Simk{\'o}, Katalin and {\v S}imkov{\'a}, M{\'a}ria and Simov, Kiril and Skachedubova, Maria and Smith, Aaron and Soares-Bastos, Isabela and Spadine, Carolyn and Steingr{\'{\i}}msson, Stein{\t h}{\'o}r and Stella, Antonio and Straka, Milan and Strickland, Emmett and Strnadov{\'a}, Jana and Suhr, Alane and Sulestio, Yogi Lesmana and Sulubacak, Umut and Suzuki, Shingo and Sz{\'a}nt{\'o}, Zsolt and Taji, Dima and Takahashi, Yuta and Tamburini, Fabio and Tan, Mary Ann C. and Tanaka, Takaaki and Tella, Samson and Tellier, Isabelle and Thomas, Guillaume and Torga, Liisi and Toska, Marsida and Trosterud, Trond and Trukhina, Anna and Tsarfaty, Reut and T{\"u}rk, Utku and Tyers, Francis and Uematsu, Sumire and Untilov, Roman and Uresov{\'a}, Zdenka and Uria, Larraitz and Uszkoreit, Hans and Utka, Andrius and Vajjala, Sowmya and van Niekerk, Daniel and van Noord, Gertjan and Varga, Viktor and Villemonte de la Clergerie, Eric and Vincze, Veronika and Wakasa, Aya and Wallenberg, Joel C. and Wallin, Lars and Walsh, Abigail and Wang, Jing Xian and Washington, Jonathan North and Wendt, Maximilan and Widmer, Paul and Williams, Seyi and Wir{\'e}n, Mats and Wittern, Christian and Woldemariam, Tsegay and Wong, Tak-sum and Wr{\'o}blewska, Alina and Yako, Mary and Yamashita, Kayo and Yamazaki, Naoki and Yan, Chunxiao and Yasuoka, Koichi and Yavrumyan, Marat M. and Yu, Zhuoran and Zabokrtsk{\'y}, Zdenek and Zahra, Shorouq and Zeldes, Amir and Zhu, Hanzhi and Zhuravleva, Anna},
url = {http://hdl.handle.net/11234/1-3424},
note = {{LINDAT}/{CLARIAH}-{CZ} digital library at the Institute of Formal and Applied Linguistics ({{\'U}FAL}), Faculty of Mathematics and Physics, Charles University},
copyright = {Licence Universal Dependencies v2.7},
year = {2020} }
"""  # noqa: W605

_DESCRIPTION = """\
Universal Dependencies is a project that seeks to develop cross-linguistically consistent treebank annotation for many languages, with the goal of facilitating multilingual parser development, cross-lingual learning, and parsing research from a language typology perspective. The annotation scheme is based on (universal) Stanford dependencies (de Marneffe et al., 2006, 2008, 2014), Google universal part-of-speech tags (Petrov et al., 2012), and the Interset interlingua for morphosyntactic tagsets (Zeman, 2008).
"""

_NAMES = [
    "af_afribooms",
    "akk_pisandub",
    "akk_riao",
    "aqz_tudet",
    "sq_tsa",
    "am_att",
    "grc_perseus",
    "grc_proiel",
    "apu_ufpa",
    "ar_nyuad",
    "ar_padt",
    "ar_pud",
    "hy_armtdp",
    "aii_as",
    "bm_crb",
    "eu_bdt",
    "be_hse",
    "bho_bhtb",
    "br_keb",
    "bg_btb",
    "bxr_bdt",
    "yue_hk",
    "ca_ancora",
    "zh_cfl",
    "zh_gsd",
    "zh_gsdsimp",
    "zh_hk",
    "zh_pud",
    "ckt_hse",
    "lzh_kyoto",
    "cop_scriptorium",
    "hr_set",
    "cs_cac",
    "cs_cltt",
    "cs_fictree",
    "cs_pdt",
    "cs_pud",
    "da_ddt",
    "nl_alpino",
    "nl_lassysmall",
    "en_esl",
    "en_ewt",
    "en_gum",
    "en_gumreddit",
    "en_lines",
    "en_partut",
    "en_pronouns",
    "en_pud",
    "myv_jr",
    "et_edt",
    "et_ewt",
    "fo_farpahc",
    "fo_oft",
    "fi_ftb",
    "fi_ood",
    "fi_pud",
    "fi_tdt",
    "fr_fqb",
    "fr_ftb",
    "fr_gsd",
    "fr_partut",
    "fr_pud",
    "fr_sequoia",
    "fr_spoken",
    "gl_ctg",
    "gl_treegal",
    "de_gsd",
    "de_hdt",
    "de_lit",
    "de_pud",
    "got_proiel",
    "el_gdt",
    "he_htb",
    "qhe_hiencs",
    "hi_hdtb",
    "hi_pud",
    "hu_szeged",
    "is_icepahc",
    "is_pud",
    "id_csui",
    "id_gsd",
    "id_pud",
    "ga_idt",
    "it_isdt",
    "it_partut",
    "it_postwita",
    "it_pud",
    "it_twittiro",
    "it_vit",
    "ja_bccwj",
    "ja_gsd",
    "ja_modern",
    "ja_pud",
    "krl_kkpp",
    "kk_ktb",
    "kfm_aha",
    "koi_uh",
    "kpv_ikdp",
    "kpv_lattice",
    "ko_gsd",
    "ko_kaist",
    "ko_pud",
    "kmr_mg",
    "la_ittb",
    "la_llct",
    "la_perseus",
    "la_proiel",
    "lv_lvtb",
    "lt_alksnis",
    "lt_hse",
    "olo_kkpp",
    "mt_mudt",
    "gv_cadhan",
    "mr_ufal",
    "gun_dooley",
    "gun_thomas",
    "mdf_jr",
    "myu_tudet",
    "pcm_nsc",
    "nyq_aha",
    "sme_giella",
    "no_bokmaal",
    "no_nynorsk",
    "no_nynorsklia",
    "cu_proiel",
    "fro_srcmf",
    "orv_rnc",
    "orv_torot",
    "otk_tonqq",
    "fa_perdt",
    "fa_seraji",
    "pl_lfg",
    "pl_pdb",
    "pl_pud",
    "pt_bosque",
    "pt_gsd",
    "pt_pud",
    "ro_nonstandard",
    "ro_rrt",
    "ro_simonero",
    "ru_gsd",
    "ru_pud",
    "ru_syntagrus",
    "ru_taiga",
    "sa_ufal",
    "sa_vedic",
    "gd_arcosg",
    "sr_set",
    "sms_giellagas",
    "sk_snk",
    "sl_ssj",
    "sl_sst",
    "soj_aha",
    "ajp_madar",
    "es_ancora",
    "es_gsd",
    "es_pud",
    "swl_sslc",
    "sv_lines",
    "sv_pud",
    "sv_talbanken",
    "gsw_uzh",
    "tl_trg",
    "tl_ugnayan",
    "ta_mwtt",
    "ta_ttb",
    "te_mtg",
    "th_pud",
    "tpn_tudet",
    "qtd_sagt",
    "tr_boun",
    "tr_gb",
    "tr_imst",
    "tr_pud",
    "uk_iu",
    "hsb_ufal",
    "ur_udtb",
    "ug_udt",
    "vi_vtb",
    "wbp_ufal",
    "cy_ccg",
    "wo_wtb",
    "yo_ytb",
]

_DESCRIPTIONS = {
    "af_afribooms": "UD Afrikaans-AfriBooms is a conversion of the AfriBooms Dependency Treebank, originally annotated with a simplified PoS set and dependency relations according to a subset of the Stanford tag set. The corpus consists of public government documents.",
    "akk_pisandub": "A small set of sentences from Babylonian royal inscriptions.",
    "akk_riao": "UD_Akkadian-RIAO is a small treebank which consists of 22 277 words and 1845 sentences. This represents an intact subset of a total of 2211 sentences from the early Neo-Assyrian royal inscriptions  of the tenth and ninth centuries BCE. These royal inscriptions were extracted from Oracc (Open Richly Annotated Cuneiform Corpus; http://oracc.museum.upenn.edu/riao/), where all Neo-Assyrian royal inscriptions are lemmatized word-for-word. The language of the corpus is Standard Babylonian, with occasional Assyrianisms, whereas “Akkadian” is the umbrella term for both Assyrian and Babylonian. The treebank was manually annotated following the UD annotation guidelines.",
    "aqz_tudet": "UD_Akuntsu-TuDeT is a collection of annotated texts in Akuntsú. Together with UD_Tupinamba-TuDeT and UD_Munduruku-TuDeT, UD_Akuntsu-TuDeT is part of the TuLaR project.  The sentences are being annotated by Carolina Aragon and Fabrício Ferraz Gerardi.",
    "sq_tsa": "The UD Treebank for Standard Albanian (TSA) is a small treebank that consists of 60 sentences corresponding to 922 tokens. The data was collected from different Wikipedia entries. This treebank was created mainly manually following the Universal Dependencies guidelines. The lemmatization was performed using the lemmatizer https://bitbucket.org/timarkh/uniparser-albanian-grammar/src/master/ developed by the Albanian National Corpus team (Maria Morozova, Alexander Rusakov, Timofey Arkhangelskiy). Tagging and Morphological Analysis were semi-automated through python scripts and corrected manually, whereas Dependency relations were assigned fully manually. We encourage any initiatives to increase the size and/or improve the overall quality of the Treebank.",
    "am_att": "UD_Amharic-ATT is a manually annotated Treebanks. It is annotated for POS tag, morphological information and dependency relations. Since Amharic is a morphologically-rich, pro-drop, and languages having a feature of clitic doubling, clitics have been segmented manually.",
    "grc_perseus": "This Universal Dependencies Ancient Greek Treebank consists of an automatic conversion of a selection of passages from the Ancient Greek and Latin Dependency Treebank 2.1",
    "grc_proiel": "The Ancient Greek PROIEL treebank is based on the Ancient Greek data from the PROIEL treebank, which is maintained at the Department of Philosophy, Classics, History of Arts and Ideas at the University of Oslo. The conversion is based on the 20180408 release of the PROIEL treebank available from https://github.com/proiel/proiel-treebank/releases. The original annotators are acknowledged in the files available there. The conversion code is available in the Rubygem proiel-cli, https://github.com/proiel/proiel-cli.",
    "apu_ufpa": "The initial release contains 70 annotated sentences. This is the first treebank in a language from the Arawak family. The original interlinear glosses are included in the tree bank, and their conversion into a full UD annotation is an ongoing process. The sent_id values (e.g.: FernandaM2017:Texto-6-19) are representative of the collector, year of publication, text identifier and the number of the sentence in order from the original text.",
    "ar_nyuad": "The treebank consists of 19,738 sentences (738889 tokens), and its domain is mainly newswire. The annotation is licensed under the terms of CC BY-SA 4.0, and the original PATB can be obtained from the LDC’s official website.",
    "ar_padt": "The Arabic-PADT UD treebank is based on the Prague Arabic Dependency Treebank (PADT), created at the Charles University in Prague.",
    "ar_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "hy_armtdp": "UD_Armenian-ArmTDP is based on the ՀայՇտեմ-ArmTDP-East dataset (version 2.0), a mix of random sentences sampled from different sources and representing different genres and domains, released in several formats (local on-line newspaper and journal articles, contemporary fiction dated between 1976 and 2019). The treebank consists 2502 sentences (~53K tokens).",
    "aii_as": "The Uppsala Assyrian Treebank is a small treebank for Modern Standard Assyrian. The corpus is collected and annotated manually. The data was randomly collected from different textbooks and a short translation of The Merchant of Venice.",
    "bm_crb": "The UD Bambara treebank is a section of the Corpus Référence du Bambara annotated natively with Universal Dependencies.",
    "eu_bdt": "The Basque UD treebank is based on a automatic conversion from part of the Basque Dependency Treebank (BDT), created at the University of of the Basque Country by the IXA NLP research group. The treebank consists of 8.993 sentences (121.443 tokens) and covers mainly literary and journalistic texts.",
    "be_hse": "The Belarusian UD treebank is based on a sample of the news texts included in the Belarusian-Russian parallel subcorpus of the Russian National Corpus, online search available at: http://ruscorpora.ru/search-para-be.html.",
    "bho_bhtb": "The Bhojpuri UD Treebank (BHTB) v2.6 consists of 6,664 tokens(357 sentences). This Treebank is a part of the Universal Dependency treebank project. Initially, it was initiated by me (Atul) at Jawaharlal Nehru University, New Delhi during the doctoral research work. BHTB data contains syntactic annotation according to dependency-constituency schema, as well as morphological tags and lemmas. In this data, XPOS is annotated  according to Bureau of Indian Standards (BIS) Part Of Speech (POS) tagset.",
    "br_keb": "UD Breton-KEB is a treebank of Breton that has been manually annotated according to the Universal Dependencies guidelines. The tokenisation guidelines and morphological annotation comes from a finite-state morphological analyser of Breton released as part of the Apertium project.",
    "bg_btb": "UD_Bulgarian-BTB is based on the HPSG-based BulTreeBank, created at the Institute of Information and Communication Technologies, Bulgarian Academy of Sciences. The original consists of 215,000 tokens (over 15,000 sentences).",
    "bxr_bdt": "The UD Buryat treebank was annotated manually natively in UD and contains grammar book sentences, along with news and some fiction.",
    "yue_hk": "A Cantonese treebank (in Traditional Chinese characters) of film subtitles and of legislative proceedings of Hong Kong, parallel with the Chinese-HK treebank.",
    "ca_ancora": "Catalan data from the AnCora corpus.",
    "zh_cfl": "The Chinese-CFL UD treebank is manually annotated by Keying Li with minor manual revisions by Herman Leung and John Lee at City University of Hong Kong, based on essays written by learners of Mandarin Chinese as a foreign language. The data is in Simplified Chinese.",
    "zh_gsd": "Traditional Chinese Universal Dependencies Treebank annotated and converted by Google.",
    "zh_gsdsimp": "Simplified Chinese Universal Dependencies dataset converted from the GSD (traditional) dataset with manual corrections.",
    "zh_hk": "A Traditional Chinese treebank of film subtitles and of legislative proceedings of Hong Kong, parallel with the Cantonese-HK treebank.",
    "zh_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "ckt_hse": "This data is a manual annotation of the corpus from multimedia annotated corpus of the Chuklang project, a dialectal corpus of the Amguema variant of Chukchi.",
    "lzh_kyoto": "Classical Chinese Universal Dependencies Treebank annotated and converted by Institute for Research in Humanities, Kyoto University.",
    "cop_scriptorium": "UD Coptic contains manually annotated Sahidic Coptic texts, including Biblical texts, sermons, letters, and hagiography.",
    "hr_set": "The Croatian UD treebank is based on the extension of the SETimes-HR corpus, the hr500k corpus.",
    "cs_cac": "The UD_Czech-CAC treebank is based on the Czech Academic Corpus 2.0 (CAC; Český akademický korpus; ČAK), created at Charles University in Prague.",
    "cs_cltt": "The UD_Czech-CLTT treebank is based on the Czech Legal Text Treebank 1.0, created at Charles University in Prague.",
    "cs_fictree": "FicTree is a treebank of Czech fiction, automatically converted into the UD format. The treebank was built at Charles University in Prague.",
    "cs_pdt": "The Czech-PDT UD treebank is based on the Prague Dependency Treebank 3.0 (PDT), created at the Charles University in Prague.",
    "cs_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "da_ddt": "The Danish UD treebank is a conversion of the Danish Dependency Treebank.",
    "nl_alpino": "This corpus consists of samples from various treebanks annotated at the University of Groningen using the Alpino annotation tools and guidelines.",
    "nl_lassysmall": "This corpus contains sentences from the Wikipedia section of the Lassy Small Treebank. Universal Dependency annotation was generated automatically from the original annotation in Lassy.",
    "en_esl": "UD English-ESL / Treebank of Learner English (TLE) contains manual POS tag and dependency annotations for 5,124 English as a Second Language (ESL) sentences drawn from the Cambridge Learner Corpus First Certificate in English (FCE) dataset.",
    "en_ewt": "A Gold Standard Universal Dependencies Corpus for English, built over the source material of the English Web Treebank LDC2012T13 (https://catalog.ldc.upenn.edu/LDC2012T13).",
    "en_gum": "Universal Dependencies syntax annotations from the GUM corpus (https://corpling.uis.georgetown.edu/gum/).",
    "en_gumreddit": "Universal Dependencies syntax annotations from the Reddit portion of the GUM corpus (https://corpling.uis.georgetown.edu/gum/) ",
    "en_lines": "UD English_LinES is the English half of the LinES Parallel Treebank with the original dependency annotation first automatically converted into Universal Dependencies and then partially reviewed. Its contents cover literature, an online manual and Europarl data.",
    "en_partut": "UD_English-ParTUT is a conversion of a multilingual parallel treebank developed at the University of Turin, and consisting of a variety of text genres, including talks, legal texts and Wikipedia articles, among others.",
    "en_pronouns": "UD English-Pronouns is dataset created to make pronoun identification more accurate and with a more balanced distribution across genders. The dataset is initially targeting the Independent Genitive pronouns, 'hers', (independent) 'his', (singular) 'theirs', 'mine', and (singular) 'yours'.",
    "en_pud": "This is the English portion of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies (http://universaldependencies.org/conll17/).",
    "myv_jr": "UD Erzya is the original annotation (CoNLL-U) for texts in the Erzya language, it originally consists of a sample from a number of fiction authors writing originals in Erzya.",
    "et_edt": "UD Estonian is a converted version of the Estonian Dependency Treebank (EDT), originally annotated in the Constraint Grammar (CG) annotation scheme, and consisting of genres of fiction, newspaper texts and scientific texts. The treebank contains 30,972 trees, 437,769 tokens.",
    "et_ewt": "UD EWT treebank consists of different genres of new media. The treebank contains 4,493 trees, 56,399 tokens.",
    "fo_farpahc": "UD_Icelandic-FarPaHC is a conversion of the Faroese Parsed Historical Corpus (FarPaHC) to the Universal Dependencies scheme. The conversion was done using UDConverter.",
    "fo_oft": "This is a treebank of Faroese based on the Faroese Wikipedia.",
    "fi_ftb": "FinnTreeBank 1 consists of manually annotated grammatical examples from VISK. The UD version of FinnTreeBank 1 was converted from a native annotation model with a script and later manually revised.",
    "fi_ood": "Finnish-OOD is an external out-of-domain test set for Finnish-TDT annotated natively into UD scheme.",
    "fi_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "fi_tdt": "UD_Finnish-TDT is based on the Turku Dependency Treebank (TDT), a broad-coverage dependency treebank of general Finnish covering numerous genres. The conversion to UD was followed by extensive manual checks and corrections, and the treebank closely adheres to the UD guidelines.",
    "fr_fqb": "The corpus **UD_French-FQB** is an automatic conversion of the French QuestionBank v1, a corpus entirely made of questions.",
    "fr_ftb": "The Universal Dependency version of the French Treebank (Abeillé et al., 2003), hereafter UD_French-FTB, is a treebank of sentences from the newspaper Le Monde, initially manually annotated with morphological information and phrase-structure and then converted to the Universal Dependencies annotation scheme.",
    "fr_gsd": "The **UD_French-GSD** was converted in 2015 from the content head version of the universal dependency treebank v2.0 (https://github.com/ryanmcd/uni-dep-tb). It is updated since 2015 independently from the previous source.",
    "fr_partut": "UD_French-ParTUT is a conversion of a multilingual parallel treebank developed at the University of Turin, and consisting of a variety of text genres, including talks, legal texts and Wikipedia articles, among others.",
    "fr_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "fr_sequoia": "UD_French-Sequoia is an automatic conversion of the Sequoia Treebank corpus French Sequoia corpus.",
    "fr_spoken": "A Universal Dependencies corpus for spoken French.",
    "gl_ctg": "The Galician UD treebank is based on the automatic parsing of the Galician Technical Corpus (http://sli.uvigo.gal/CTG) created at the University of Vigo by the the TALG NLP research group.",
    "gl_treegal": "The Galician-TreeGal is a treebank for Galician developed at LyS Group (Universidade da Coruña).",
    "de_gsd": "The German UD is converted from the content head version of the universal dependency treebank v2.0 (legacy).",
    "de_hdt": "UD German-HDT is a conversion of the Hamburg Dependency Treebank, created at the University of Hamburg through manual annotation in conjunction with a standard for morphologically and syntactically annotating sentences as well as a constraint-based parser.",
    "de_lit": "This treebank aims at gathering texts of the German literary history. Currently, it hosts Fragments of the early Romanticism, i.e. aphorism-like texts mainly dealing with philosophical issues concerning art, beauty and related topics.",
    "de_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "got_proiel": "The UD Gothic treebank is based on the Gothic data from the PROIEL treebank, and consists of Wulfila's Bible translation.",
    "el_gdt": "The Greek UD treebank (UD_Greek-GDT) is derived from the Greek Dependency Treebank (http://gdt.ilsp.gr), a resource developed and maintained by researchers at the Institute for Language and Speech Processing/Athena R.C. (http://www.ilsp.gr).",
    "he_htb": "A Universal Dependencies Corpus for Hebrew.",
    "qhe_hiencs": "The Hindi-English Code-switching treebank is based on code-switching tweets of Hindi and English multilingual speakers (mostly Indian) on Twitter. The treebank is manually annotated using UD sceheme. The training and evaluations sets were seperately annotated by different annotators using UD v2 and v1 guidelines respectively. The evaluation sets are automatically converted from UD v1 to v2.",
    "hi_hdtb": "The Hindi UD treebank is based on the Hindi Dependency Treebank (HDTB), created at IIIT Hyderabad, India.",
    "hi_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "hu_szeged": "The Hungarian UD treebank is derived from the Szeged Dependency Treebank (Vincze et al. 2010).",
    "is_icepahc": "UD_Icelandic-IcePaHC is a conversion of the Icelandic Parsed Historical Corpus (IcePaHC) to the Universal Dependencies scheme. The conversion was done using UDConverter.",
    "is_pud": "Icelandic-PUD is the Icelandic part of the Parallel Universal Dependencies (PUD) treebanks.",
    "id_csui": "UD Indonesian-CSUI is a conversion from an Indonesian constituency treebank in the Penn Treebank format named Kethu that was also a conversion from a constituency treebank built by Dinakaramani et al. (2015). We named this treebank Indonesian-CSUI, since all the three versions of the treebanks were built at Faculty of Computer Science, Universitas Indonesia.",
    "id_gsd": "The Indonesian UD is converted from the content head version of the universal dependency treebank v2.0 (legacy).",
    "id_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "ga_idt": "A Universal Dependencies 4910-sentence treebank for modern Irish.",
    "it_isdt": "The Italian corpus annotated according to the UD annotation scheme was obtained by conversion from ISDT (Italian Stanford Dependency Treebank), released for the dependency parsing shared task of Evalita-2014 (Bosco et al. 2014).",
    "it_partut": "UD_Italian-ParTUT is a conversion of a multilingual parallel treebank developed at the University of Turin, and consisting of a variety of text genres, including talks, legal texts and Wikipedia articles, among others.",
    "it_postwita": "PoSTWITA-UD is a collection of Italian tweets annotated in Universal Dependencies that can be exploited for the training of NLP systems to enhance their performance on social media texts.",
    "it_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "it_twittiro": "TWITTIRÒ-UD is a collection of ironic Italian tweets annotated in Universal Dependencies. The treebank can be exploited for the training of NLP systems to enhance their performance on social media texts, and in particular, for irony detection purposes.",
    "it_vit": "The UD_Italian-VIT corpus was obtained by conversion from VIT (Venice Italian Treebank), developed at the Laboratory of Computational Linguistics of the Università Ca' Foscari in Venice (Delmonte et al. 2007; Delmonte 2009; http://rondelmo.it/resource/VIT/Browser-VIT/index.htm).",
    "ja_bccwj": "This Universal Dependencies (UD) Japanese treebank is based on the definition of UD Japanese convention described in the UD documentation. The original sentences are from `Balanced Corpus of Contemporary Written Japanese'(BCCWJ).",
    "ja_gsd": "This Universal Dependencies (UD) Japanese treebank is based on the definition of UD Japanese convention described in the UD documentation.  The original sentences are from Google UDT 2.0.",
    "ja_modern": "This Universal Dependencies (UD) Japanese treebank is based on the definition of UD Japanese convention described in the UD documentation. The original sentences are from `Corpus of Historical Japanese' (CHJ).",
    "ja_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the [CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies](http://universaldependencies.org/conll17/).",
    "krl_kkpp": "UD Karelian-KKPP is a manually annotated new corpus of Karelian made in Universal dependencies annotation scheme. The data is collected from VepKar corpora and consists of mostly modern news texts but also some stories and educational texts.",
    "kk_ktb": "The UD Kazakh treebank is a combination of text from various sources including Wikipedia, some folk tales, sentences from the UDHR, news and phrasebook sentences. Sentences IDs include partial document identifiers.",
    "kfm_aha": "The AHA Khunsari Treebank is a small treebank for contemporary Khunsari. Its corpus is collected and annotated manually. We have prepared this treebank based on interviews with Khunsari speakers.",
    "koi_uh": "This is a Komi-Permyak literary language treebank consisting of original and translated texts.",
    "kpv_ikdp": "This treebank consists of dialectal transcriptions of spoken Komi-Zyrian. The current texts are short recorded segments from different areas where the Iźva dialect of Komi language is spoken.",
    "kpv_lattice": "UD Komi-Zyrian Lattice is a treebank of written standard Komi-Zyrian.",
    "ko_gsd": "The Google Korean Universal Dependency Treebank is first converted from the Universal Dependency Treebank v2.0 (legacy), and then enhanced by Chun et al., 2018.",
    "ko_kaist": "The KAIST Korean Universal Dependency Treebank is generated by Chun et al., 2018 from the constituency trees in the KAIST Tree-Tagging Corpus.",
    "ko_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "kmr_mg": "The UD Kurmanji corpus is a corpus of Kurmanji Kurdish. It contains fiction and encyclopaedic texts in roughly equal measure. It has been annotated natively in accordance with the UD annotation scheme.",
    "la_ittb": "Latin data from the _Index Thomisticus_ Treebank. Data are taken from the _Index Thomisticus_ corpus by Roberto Busa SJ, which contains the complete work by Thomas Aquinas (1225–1274; Medieval Latin) and by 61 other authors related to Thomas.",
    "la_llct": "This Universal Dependencies version of the LLCT (Late Latin Charter Treebank) consists of an automated conversion of the LLCT2 treebank from the Latin Dependency Treebank (LDT) format into the Universal Dependencies standard.",
    "la_perseus": "This Universal Dependencies Latin Treebank consists of an automatic conversion of a selection of passages from the Ancient Greek and Latin Dependency Treebank 2.1",
    "la_proiel": "The Latin PROIEL treebank is based on the Latin data from the PROIEL treebank, and contains most of the Vulgate New Testament translations plus selections from Caesar's Gallic War, Cicero's Letters to Atticus, Palladius' Opus Agriculturae and the first book of Cicero's De officiis.",
    "lv_lvtb": "Latvian UD Treebank is based on Latvian Treebank (LVTB), being created at University of Latvia, Institute of Mathematics and Computer Science, Artificial Intelligence Laboratory.",
    "lt_alksnis": "The Lithuanian dependency treebank ALKSNIS v3.0 (Vytautas Magnus University).",
    "lt_hse": "Lithuanian treebank annotated manually (dependencies) using the Morphological Annotator by CCL, Vytautas Magnus University (http://tekstynas.vdu.lt/) and manual disambiguation. A pilot version which includes news and an essay by Tomas Venclova is available here.",
    "olo_kkpp": "UD Livvi-KKPP is a manually annotated new corpus of Livvi-Karelian made directly in the Universal dependencies annotation scheme. The data is collected from VepKar corpora and consists of mostly modern news texts but also some stories and educational texts.",
    "mt_mudt": "MUDT (Maltese Universal Dependencies Treebank) is a manually annotated treebank of Maltese, a Semitic language of Malta descended from North African Arabic with a significant amount of Italo-Romance influence. MUDT was designed as a balanced corpus with four major genres (see Splitting below) represented roughly equally.",
    "gv_cadhan": "This is the Cadhan Aonair UD treebank for Manx Gaelic, created by Kevin Scannell.",
    "mr_ufal": "UD Marathi is a manually annotated treebank consisting primarily of stories from Wikisource, and parts of an article on Wikipedia.",
    "gun_dooley": "UD Mbya_Guarani-Dooley is a corpus of narratives written in Mbyá Guaraní (Tupian) in Brazil, and collected by Robert Dooley. Due to copyright restrictions, the corpus that is distributed as part of UD only contains the annotation (tags, features, relations) while the FORM and LEMMA columns are empty.",
    "gun_thomas": "UD Mbya_Guarani-Thomas is a corpus of Mbyá Guaraní (Tupian) texts collected by Guillaume Thomas. The current version of the corpus consists of three speeches by Paulina Kerechu Núñez Romero, a Mbyá Guaraní speaker from Ytu, Caazapá Department, Paraguay.",
    "mdf_jr": "Erme Universal Dependencies annotated texts Moksha are the origin of UD_Moksha-JR with annotation (CoNLL-U) for texts in the Moksha language, it originally consists of a sample from a number of fiction authors writing originals in Moksha.",
    "myu_tudet": "UD_Munduruku-TuDeT is a collection of annotated sentences in Mundurukú. Together with UD_Akuntsu-TuDeT and UD_Tupinamba-TuDeT, UD_Munduruku-TuDeT is part of the TuLaR project.",
    "pcm_nsc": "A Universal Dependencies corpus for spoken Naija (Nigerian Pidgin).",
    "nyq_aha": "The AHA Nayini Treebank is a small treebank for contemporary Nayini. Its corpus is collected and annotated manually. We have prepared this treebank based on interviews with Nayini speakers.",
    "sme_giella": "This is a North Sámi treebank based on a manually disambiguated and function-labelled gold-standard corpus of North Sámi produced by the Giellatekno team at UiT Norgga árktalaš universitehta.",
    "no_bokmaal": "The Norwegian UD treebank is based on the Bokmål section of the Norwegian Dependency Treebank (NDT), which is a syntactic treebank of Norwegian. NDT has been automatically converted to the UD scheme by Lilja Øvrelid at the University of Oslo.",
    "no_nynorsk": "The Norwegian UD treebank is based on the Nynorsk section of the Norwegian Dependency Treebank (NDT), which is a syntactic treebank of Norwegian.  NDT has been automatically converted to the UD scheme by Lilja Øvrelid at the University of Oslo.",
    "no_nynorsklia": "This Norwegian treebank is based on the LIA treebank of transcribed spoken Norwegian dialects. The treebank has been automatically converted to the UD scheme by Lilja Øvrelid at the University of Oslo.",
    "cu_proiel": "The Old Church Slavonic (OCS) UD treebank is based on the Old Church Slavonic data from the PROIEL treebank and contains the text of the Codex Marianus New Testament translation.",
    "fro_srcmf": "UD_Old_French-SRCMF is a conversion of (part of) the SRCMF corpus (Syntactic Reference Corpus of Medieval French srcmf.org).",
    "orv_rnc": "`UD_Old_Russian-RNC` is a sample of the Middle Russian corpus (1300-1700), a part of the Russian National Corpus. The data were originally annotated according to the RNC and extended UD-Russian morphological schemas and UD 2.4 dependency schema.",
    "orv_torot": "UD_Old_Russian-TOROT is a conversion of a selection of the Old East Slavonic and Middle Russian data in the Tromsø Old Russian and OCS Treebank (TOROT), which was originally annotated in PROIEL dependency format.",
    "otk_tonqq": "`UD_Old_Turkish-Tonqq` is an Old Turkish treebank built upon Turkic script texts or sentences that are trivially convertible.",
    "fa_perdt": "The Persian Universal Dependency Treebank (PerUDT) is the result of automatic coversion of Persian Dependency Treebank (PerDT) with extensive manual corrections. Please refer to the follwoing work, if you use this data: Mohammad Sadegh Rasooli, Pegah Safari, Amirsaeid Moloodi, and Alireza Nourian. 'The Persian Dependency Treebank Made Universal'. 2020 (to appear).",
    "fa_seraji": "The Persian Universal Dependency Treebank (Persian UD) is based on Uppsala Persian Dependency Treebank (UPDT). The conversion of the UPDT to the Universal Dependencies was performed semi-automatically with extensive manual checks and corrections.",
    "pl_lfg": "The LFG Enhanced UD treebank of Polish is based on a corpus of LFG (Lexical Functional Grammar) syntactic structures generated by an LFG grammar of Polish, POLFIE, and manually disambiguated by human annotators.",
    "pl_pdb": "The Polish PDB-UD treebank is based on the Polish Dependency Bank 2.0 (PDB 2.0), created at the Institute of Computer Science, Polish Academy of Sciences in Warsaw. The PDB-UD treebank is an extended and corrected version of the Polish SZ-UD treebank (the release 1.2 to 2.3).",
    "pl_pud": "This is the Polish portion of the Parallel Universal Dependencies (PUD) treebanks, created at the Institute of Computer Science, Polish Academy of Sciences in Warsaw.Re",
    "pt_bosque": "This Universal Dependencies (UD) Portuguese treebank is based on the Constraint Grammar converted version of the Bosque, which is part of the Floresta Sintá(c)tica treebank. It contains both European (CETEMPúblico) and Brazilian (CETENFolha) variants.",
    "pt_gsd": "The Brazilian Portuguese UD is converted from the Google Universal Dependency Treebank v2.0 (legacy).",
    "pt_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "ro_nonstandard": "The Romanian Non-standard UD treebank (called UAIC-RoDia) is based on UAIC-RoDia Treebank. UAIC-RoDia = ISLRN 156-635-615-024-0",
    "ro_rrt": "The Romanian UD treebank (called RoRefTrees) (Barbu Mititelu et al., 2016) is the reference treebank in UD format for standard Romanian.",
    "ro_simonero": "SiMoNERo is a medical corpus of contemporary Romanian.",
    "ru_gsd": "Russian Universal Dependencies Treebank annotated and converted by Google.",
    "ru_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "ru_syntagrus": "Russian data from the SynTagRus corpus.",
    "ru_taiga": "Universal Dependencies treebank is based on data samples extracted from Taiga Corpus and MorphoRuEval-2017 and GramEval-2020 shared tasks collections.",
    "sa_ufal": "A small Sanskrit treebank of sentences from Pañcatantra, an ancient Indian collection of interrelated fables by Vishnu Sharma.",
    "sa_vedic": "The Treebank of Vedic Sanskrit contains 4,000 sentences with 27,000 words chosen from metrical and prose passages of the Ṛgveda (RV), the Śaunaka recension of the Atharvaveda (ŚS), the Maitrāyaṇīsaṃhitā (MS), and the Aitareya- (AB) and Śatapatha-Brāhmaṇas (ŚB). Lexical and morpho-syntactic information has been generated using a tagging software and manually validated. POS tags have been induced automatically from the morpho-sytactic information of each word.",
    "gd_arcosg": "A treebank of Scottish Gaelic based on the Annotated Reference Corpus Of Scottish Gaelic (ARCOSG).",
    "sr_set": "The Serbian UD treebank is based on the [SETimes-SR](http://hdl.handle.net/11356/1200) corpus and additional news documents from the Serbian web.",
    "sms_giellagas": "The UD Skolt Sami Giellagas treebank is based almost entirely on spoken Skolt Sami corpora.",
    "sk_snk": "The Slovak UD treebank is based on data originally annotated as part of the Slovak National Corpus, following the annotation style of the Prague Dependency Treebank.",
    "sl_ssj": "The Slovenian UD Treebank is a rule-based conversion of the ssj500k treebank, the largest collection of manually syntactically annotated data in Slovenian, originally annotated in the JOS annotation scheme.",
    "sl_sst": "The Spoken Slovenian UD Treebank (SST) is the first syntactically annotated corpus of spoken Slovenian, based on a sample of the reference GOS corpus, a collection of transcribed audio recordings of monologic, dialogic and multi-party spontaneous speech in different everyday situations.",
    "soj_aha": "The AHA Soi Treebank is a small treebank for contemporary Soi. Its corpus is collected and annotated manually. We have prepared this treebank based on interviews with Soi speakers.",
    "ajp_madar": "The South_Levantine_Arabic-MADAR treebank consists of 100 manually-annotated sentences taken from the [MADAR](https://camel.abudhabi.nyu.edu/madar/) (Multi-Arabic Dialect Applications and Resources) project. ",
    "es_ancora": "Spanish data from the AnCora corpus.",
    "es_gsd": "The Spanish UD is converted from the content head version of the universal dependency treebank v2.0 (legacy).",
    "es_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the [CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies](http://universaldependencies.org/conll17/).",
    "swl_sslc": "The Universal Dependencies treebank for Swedish Sign Language (ISO 639-3: swl) is derived from the Swedish Sign Language Corpus (SSLC) from the department of linguistics, Stockholm University.",
    "sv_lines": "UD Swedish_LinES is the Swedish half of the LinES Parallel Treebank with UD annotations. All segments are translations from English and the sources cover literary genres, online manuals and Europarl data.",
    "sv_pud": "Swedish-PUD is the Swedish part of the Parallel Universal Dependencies (PUD) treebanks.",
    "sv_talbanken": "The Swedish-Talbanken treebank is based on Talbanken, a treebank developed at Lund University in the 1970s.",
    "gsw_uzh": "_UD_Swiss_German-UZH_ is a tiny manually annotated treebank of 100 sentences in different Swiss German dialects and a variety of text genres.",
    "tl_trg": "UD_Tagalog-TRG is a UD treebank manually annotated using sentences from a grammar book.",
    "tl_ugnayan": "Ugnayan is a manually annotated Tagalog treebank currently composed of educational fiction and nonfiction text. The treebank is under development at the University of the Philippines.",
    "ta_mwtt": "MWTT - Modern Written Tamil Treebank has sentences taken primarily from a text called 'A Grammar of Modern Tamil' by Thomas Lehmann (1993). This initial release has 536 sentences of various lengths, and all of these are added as the test set.",
    "ta_ttb": "The UD Tamil treebank is based on the Tamil Dependency Treebank created at the Charles University in Prague by Loganathan Ramasamy.",
    "te_mtg": "The Telugu UD treebank is created in UD based on manual annotations of sentences from a grammar book.",
    "th_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "tpn_tudet": "UD_Tupinamba-TuDeT is a collection of annotated texts in Tupi(nambá). Together with UD_Akuntsu-TuDeT and UD_Munduruku-TuDeT, UD_Tupinamba-TuDeT is part of the TuLaR. The treebank is ongoing work and is constantly being updated.",
    "qtd_sagt": "UD Turkish-German SAGT is a Turkish-German code-switching treebank that is developed as part of the SAGT project.",
    "tr_boun": "The largest Turkish dependency treebank annotated in UD style. Created by the members of [TABILAB](http://http://tabilab.cmpe.boun.edu.tr/) from Boğaziçi University.",
    "tr_gb": "This is a treebank annotating example sentences from a comprehensive grammar book of Turkish.",
    "tr_imst": "The UD Turkish Treebank, also called the IMST-UD Treebank, is a semi-automatic conversion of the IMST Treebank (Sulubacak et al., 2016).",
    "tr_pud": "This is a part of the Parallel Universal Dependencies (PUD) treebanks created for the CoNLL 2017 shared task on Multilingual Parsing from Raw Text to Universal Dependencies.",
    "uk_iu": "Gold standard Universal Dependencies corpus for Ukrainian, developed for UD originally, by Institute for Ukrainian, NGO. [українською]",
    "hsb_ufal": "A small treebank of Upper Sorbian based mostly on Wikipedia.",
    "ur_udtb": "The Urdu Universal Dependency Treebank was automatically converted from Urdu Dependency Treebank (UDTB) which is part of an ongoing effort of creating multi-layered treebanks for Hindi and Urdu.",
    "ug_udt": "The Uyghur UD treebank is based on the Uyghur Dependency Treebank (UDT), created at the Xinjiang University in Ürümqi, China.",
    "vi_vtb": "The Vietnamese UD treebank is a conversion of the constituent treebank created in the VLSP project (https://vlsp.hpda.vn/).",
    "wbp_ufal": "A small treebank of grammatical examples in Warlpiri, taken from linguistic literature.",
    "cy_ccg": "UD Welsh-CCG (Corpws Cystrawennol y Gymraeg) is a treebank of Welsh, annotated according to the Universal Dependencies guidelines.",
    "wo_wtb": "UD_Wolof-WTB is a natively manual developed treebank for Wolof. Sentences were collected from encyclopedic, fictional, biographical, religious texts and news.",
    "yo_ytb": "Parts of the Yoruba Bible and of the Yoruba edition of Wikipedia, hand-annotated natively in Universal Dependencies.",
}
_PREFIX = "https://raw.githubusercontent.com/UniversalDependencies/"
_UD_DATASETS = {
    "af_afribooms": {
        "train": "UD_Afrikaans-AfriBooms/r2.7/af_afribooms-ud-train.conllu",
        "dev": "UD_Afrikaans-AfriBooms/r2.7/af_afribooms-ud-dev.conllu",
        "test": "UD_Afrikaans-AfriBooms/r2.7/af_afribooms-ud-test.conllu",
    },
    "akk_pisandub": {
        "test": "UD_Akkadian-PISANDUB/r2.7/akk_pisandub-ud-test.conllu",
    },
    "akk_riao": {
        "test": "UD_Akkadian-RIAO/r2.7/akk_riao-ud-test.conllu",
    },
    "aqz_tudet": {
        "test": "UD_Akuntsu-TuDeT/r2.7/aqz_tudet-ud-test.conllu",
    },
    "sq_tsa": {
        "test": "UD_Albanian-TSA/r2.7/sq_tsa-ud-test.conllu",
    },
    "am_att": {
        "test": "UD_Amharic-ATT/r2.7/am_att-ud-test.conllu",
    },
    "grc_perseus": {
        "train": "UD_Ancient_Greek-Perseus/r2.7/grc_perseus-ud-train.conllu",
        "dev": "UD_Ancient_Greek-Perseus/r2.7/grc_perseus-ud-dev.conllu",
        "test": "UD_Ancient_Greek-Perseus/r2.7/grc_perseus-ud-test.conllu",
    },
    "grc_proiel": {
        "train": "UD_Ancient_Greek-PROIEL/r2.7/grc_proiel-ud-train.conllu",
        "dev": "UD_Ancient_Greek-PROIEL/r2.7/grc_proiel-ud-dev.conllu",
        "test": "UD_Ancient_Greek-PROIEL/r2.7/grc_proiel-ud-test.conllu",
    },
    "apu_ufpa": {
        "test": "UD_Apurina-UFPA/r2.7/apu_ufpa-ud-test.conllu",
    },
    "ar_nyuad": {
        "train": "UD_Arabic-NYUAD/r2.7/ar_nyuad-ud-train.conllu",
        "dev": "UD_Arabic-NYUAD/r2.7/ar_nyuad-ud-dev.conllu",
        "test": "UD_Arabic-NYUAD/r2.7/ar_nyuad-ud-test.conllu",
    },
    "ar_padt": {
        "train": "UD_Arabic-PADT/r2.7/ar_padt-ud-train.conllu",
        "dev": "UD_Arabic-PADT/r2.7/ar_padt-ud-dev.conllu",
        "test": "UD_Arabic-PADT/r2.7/ar_padt-ud-test.conllu",
    },
    "ar_pud": {
        "test": "UD_Arabic-PUD/r2.7/ar_pud-ud-test.conllu",
    },
    "hy_armtdp": {
        "train": "UD_Armenian-ArmTDP/r2.7/hy_armtdp-ud-train.conllu",
        "dev": "UD_Armenian-ArmTDP/r2.7/hy_armtdp-ud-dev.conllu",
        "test": "UD_Armenian-ArmTDP/r2.7/hy_armtdp-ud-test.conllu",
    },
    "aii_as": {
        "test": "UD_Assyrian-AS/r2.7/aii_as-ud-test.conllu",
    },
    "bm_crb": {
        "test": "UD_Bambara-CRB/r2.7/bm_crb-ud-test.conllu",
    },
    "eu_bdt": {
        "train": "UD_Basque-BDT/r2.7/eu_bdt-ud-train.conllu",
        "dev": "UD_Basque-BDT/r2.7/eu_bdt-ud-dev.conllu",
        "test": "UD_Basque-BDT/r2.7/eu_bdt-ud-test.conllu",
    },
    "be_hse": {
        "train": "UD_Belarusian-HSE/r2.7/be_hse-ud-train.conllu",
        "dev": "UD_Belarusian-HSE/r2.7/be_hse-ud-dev.conllu",
        "test": "UD_Belarusian-HSE/r2.7/be_hse-ud-test.conllu",
    },
    "bho_bhtb": {
        "test": "UD_Bhojpuri-BHTB/r2.7/bho_bhtb-ud-test.conllu",
    },
    "br_keb": {
        "test": "UD_Breton-KEB/r2.7/br_keb-ud-test.conllu",
    },
    "bg_btb": {
        "train": "UD_Bulgarian-BTB/r2.7/bg_btb-ud-train.conllu",
        "dev": "UD_Bulgarian-BTB/r2.7/bg_btb-ud-dev.conllu",
        "test": "UD_Bulgarian-BTB/r2.7/bg_btb-ud-test.conllu",
    },
    "bxr_bdt": {
        "train": "UD_Buryat-BDT/r2.7/bxr_bdt-ud-train.conllu",
        "test": "UD_Buryat-BDT/r2.7/bxr_bdt-ud-test.conllu",
    },
    "yue_hk": {
        "test": "UD_Cantonese-HK/r2.7/yue_hk-ud-test.conllu",
    },
    "ca_ancora": {
        "train": "UD_Catalan-AnCora/r2.7/ca_ancora-ud-train.conllu",
        "dev": "UD_Catalan-AnCora/r2.7/ca_ancora-ud-dev.conllu",
        "test": "UD_Catalan-AnCora/r2.7/ca_ancora-ud-test.conllu",
    },
    "zh_cfl": {
        "test": "UD_Chinese-CFL/r2.7/zh_cfl-ud-test.conllu",
    },
    "zh_gsd": {
        "train": "UD_Chinese-GSD/r2.7/zh_gsd-ud-train.conllu",
        "dev": "UD_Chinese-GSD/r2.7/zh_gsd-ud-dev.conllu",
        "test": "UD_Chinese-GSD/r2.7/zh_gsd-ud-test.conllu",
    },
    "zh_gsdsimp": {
        "train": "UD_Chinese-GSDSimp/r2.7/zh_gsdsimp-ud-train.conllu",
        "dev": "UD_Chinese-GSDSimp/r2.7/zh_gsdsimp-ud-dev.conllu",
        "test": "UD_Chinese-GSDSimp/r2.7/zh_gsdsimp-ud-test.conllu",
    },
    "zh_hk": {
        "test": "UD_Chinese-HK/r2.7/zh_hk-ud-test.conllu",
    },
    "zh_pud": {
        "test": "UD_Chinese-PUD/r2.7/zh_pud-ud-test.conllu",
    },
    "ckt_hse": {
        "test": "UD_Chukchi-HSE/r2.7/ckt_hse-ud-test.conllu",
    },
    "lzh_kyoto": {
        "train": "UD_Classical_Chinese-Kyoto/r2.7/lzh_kyoto-ud-train.conllu",
        "dev": "UD_Classical_Chinese-Kyoto/r2.7/lzh_kyoto-ud-dev.conllu",
        "test": "UD_Classical_Chinese-Kyoto/r2.7/lzh_kyoto-ud-test.conllu",
    },
    "cop_scriptorium": {
        "train": "UD_Coptic-Scriptorium/r2.7/cop_scriptorium-ud-train.conllu",
        "dev": "UD_Coptic-Scriptorium/r2.7/cop_scriptorium-ud-dev.conllu",
        "test": "UD_Coptic-Scriptorium/r2.7/cop_scriptorium-ud-test.conllu",
    },
    "hr_set": {
        "train": "UD_Croatian-SET/r2.7/hr_set-ud-train.conllu",
        "dev": "UD_Croatian-SET/r2.7/hr_set-ud-dev.conllu",
        "test": "UD_Croatian-SET/r2.7/hr_set-ud-test.conllu",
    },
    "cs_cac": {
        "train": "UD_Czech-CAC/r2.7/cs_cac-ud-train.conllu",
        "dev": "UD_Czech-CAC/r2.7/cs_cac-ud-dev.conllu",
        "test": "UD_Czech-CAC/r2.7/cs_cac-ud-test.conllu",
    },
    "cs_cltt": {
        "train": "UD_Czech-CLTT/r2.7/cs_cltt-ud-train.conllu",
        "dev": "UD_Czech-CLTT/r2.7/cs_cltt-ud-dev.conllu",
        "test": "UD_Czech-CLTT/r2.7/cs_cltt-ud-test.conllu",
    },
    "cs_fictree": {
        "train": "UD_Czech-FicTree/r2.7/cs_fictree-ud-train.conllu",
        "dev": "UD_Czech-FicTree/r2.7/cs_fictree-ud-dev.conllu",
        "test": "UD_Czech-FicTree/r2.7/cs_fictree-ud-test.conllu",
    },
    "cs_pdt": {
        "train": [
            "UD_Czech-PDT/r2.7/cs_pdt-ud-train-l.conllu",
            "UD_Czech-PDT/r2.7/cs_pdt-ud-train-m.conllu",
            "UD_Czech-PDT/r2.7/cs_pdt-ud-train-c.conllu",
            "UD_Czech-PDT/r2.7/cs_pdt-ud-train-v.conllu",
        ],
        "dev": "UD_Czech-PDT/r2.7/cs_pdt-ud-dev.conllu",
        "test": "UD_Czech-PDT/r2.7/cs_pdt-ud-test.conllu",
    },
    "cs_pud": {
        "test": "UD_Czech-PUD/r2.7/cs_pud-ud-test.conllu",
    },
    "da_ddt": {
        "train": "UD_Danish-DDT/r2.7/da_ddt-ud-train.conllu",
        "dev": "UD_Danish-DDT/r2.7/da_ddt-ud-dev.conllu",
        "test": "UD_Danish-DDT/r2.7/da_ddt-ud-test.conllu",
    },
    "nl_alpino": {
        "train": "UD_Dutch-Alpino/r2.7/nl_alpino-ud-train.conllu",
        "dev": "UD_Dutch-Alpino/r2.7/nl_alpino-ud-dev.conllu",
        "test": "UD_Dutch-Alpino/r2.7/nl_alpino-ud-test.conllu",
    },
    "nl_lassysmall": {
        "train": "UD_Dutch-LassySmall/r2.7/nl_lassysmall-ud-train.conllu",
        "dev": "UD_Dutch-LassySmall/r2.7/nl_lassysmall-ud-dev.conllu",
        "test": "UD_Dutch-LassySmall/r2.7/nl_lassysmall-ud-test.conllu",
    },
    "en_esl": {
        "train": "UD_English-ESL/r2.7/en_esl-ud-train.conllu",
        "dev": "UD_English-ESL/r2.7/en_esl-ud-dev.conllu",
        "test": "UD_English-ESL/r2.7/en_esl-ud-test.conllu",
    },
    "en_ewt": {
        "train": "UD_English-EWT/r2.7/en_ewt-ud-train.conllu",
        "dev": "UD_English-EWT/r2.7/en_ewt-ud-dev.conllu",
        "test": "UD_English-EWT/r2.7/en_ewt-ud-test.conllu",
    },
    "en_gum": {
        "train": "UD_English-GUM/r2.7/en_gum-ud-train.conllu",
        "dev": "UD_English-GUM/r2.7/en_gum-ud-dev.conllu",
        "test": "UD_English-GUM/r2.7/en_gum-ud-test.conllu",
    },
    "en_gumreddit": {
        "train": "UD_English-GUMReddit/r2.7/en_gumreddit-ud-train.conllu",
        "dev": "UD_English-GUMReddit/r2.7/en_gumreddit-ud-dev.conllu",
        "test": "UD_English-GUMReddit/r2.7/en_gumreddit-ud-test.conllu",
    },
    "en_lines": {
        "train": "UD_English-LinES/r2.7/en_lines-ud-train.conllu",
        "dev": "UD_English-LinES/r2.7/en_lines-ud-dev.conllu",
        "test": "UD_English-LinES/r2.7/en_lines-ud-test.conllu",
    },
    "en_partut": {
        "train": "UD_English-ParTUT/r2.7/en_partut-ud-train.conllu",
        "dev": "UD_English-ParTUT/r2.7/en_partut-ud-dev.conllu",
        "test": "UD_English-ParTUT/r2.7/en_partut-ud-test.conllu",
    },
    "en_pronouns": {
        "test": "UD_English-Pronouns/r2.7/en_pronouns-ud-test.conllu",
    },
    "en_pud": {
        "test": "UD_English-PUD/r2.7/en_pud-ud-test.conllu",
    },
    "myv_jr": {
        "test": "UD_Erzya-JR/r2.7/myv_jr-ud-test.conllu",
    },
    "et_edt": {
        "train": "UD_Estonian-EDT/r2.7/et_edt-ud-train.conllu",
        "dev": "UD_Estonian-EDT/r2.7/et_edt-ud-dev.conllu",
        "test": "UD_Estonian-EDT/r2.7/et_edt-ud-test.conllu",
    },
    "et_ewt": {
        "train": "UD_Estonian-EWT/r2.7/et_ewt-ud-train.conllu",
        "dev": "UD_Estonian-EWT/r2.7/et_ewt-ud-dev.conllu",
        "test": "UD_Estonian-EWT/r2.7/et_ewt-ud-test.conllu",
    },
    "fo_farpahc": {
        "train": "UD_Faroese-FarPaHC/r2.7/fo_farpahc-ud-train.conllu",
        "dev": "UD_Faroese-FarPaHC/r2.7/fo_farpahc-ud-dev.conllu",
        "test": "UD_Faroese-FarPaHC/r2.7/fo_farpahc-ud-test.conllu",
    },
    "fo_oft": {
        "test": "UD_Faroese-OFT/r2.7/fo_oft-ud-test.conllu",
    },
    "fi_ftb": {
        "train": "UD_Finnish-FTB/r2.7/fi_ftb-ud-train.conllu",
        "dev": "UD_Finnish-FTB/r2.7/fi_ftb-ud-dev.conllu",
        "test": "UD_Finnish-FTB/r2.7/fi_ftb-ud-test.conllu",
    },
    "fi_ood": {
        "test": "UD_Finnish-OOD/r2.7/fi_ood-ud-test.conllu",
    },
    "fi_pud": {
        "test": "UD_Finnish-PUD/r2.7/fi_pud-ud-test.conllu",
    },
    "fi_tdt": {
        "train": "UD_Finnish-TDT/r2.7/fi_tdt-ud-train.conllu",
        "dev": "UD_Finnish-TDT/r2.7/fi_tdt-ud-dev.conllu",
        "test": "UD_Finnish-TDT/r2.7/fi_tdt-ud-test.conllu",
    },
    "fr_fqb": {
        "test": "UD_French-FQB/r2.7/fr_fqb-ud-test.conllu",
    },
    "fr_ftb": {
        "train": "UD_French-FTB/r2.7/fr_ftb-ud-train.conllu",
        "dev": "UD_French-FTB/r2.7/fr_ftb-ud-dev.conllu",
        "test": "UD_French-FTB/r2.7/fr_ftb-ud-test.conllu",
    },
    "fr_gsd": {
        "train": "UD_French-GSD/r2.7/fr_gsd-ud-train.conllu",
        "dev": "UD_French-GSD/r2.7/fr_gsd-ud-dev.conllu",
        "test": "UD_French-GSD/r2.7/fr_gsd-ud-test.conllu",
    },
    "fr_partut": {
        "train": "UD_French-ParTUT/r2.7/fr_partut-ud-train.conllu",
        "dev": "UD_French-ParTUT/r2.7/fr_partut-ud-dev.conllu",
        "test": "UD_French-ParTUT/r2.7/fr_partut-ud-test.conllu",
    },
    "fr_pud": {
        "test": "UD_French-PUD/r2.7/fr_pud-ud-test.conllu",
    },
    "fr_sequoia": {
        "train": "UD_French-Sequoia/r2.7/fr_sequoia-ud-train.conllu",
        "dev": "UD_French-Sequoia/r2.7/fr_sequoia-ud-dev.conllu",
        "test": "UD_French-Sequoia/r2.7/fr_sequoia-ud-test.conllu",
    },
    "fr_spoken": {
        "train": "UD_French-Spoken/r2.7/fr_spoken-ud-train.conllu",
        "dev": "UD_French-Spoken/r2.7/fr_spoken-ud-dev.conllu",
        "test": "UD_French-Spoken/r2.7/fr_spoken-ud-test.conllu",
    },
    "gl_ctg": {
        "train": "UD_Galician-CTG/r2.7/gl_ctg-ud-train.conllu",
        "dev": "UD_Galician-CTG/r2.7/gl_ctg-ud-dev.conllu",
        "test": "UD_Galician-CTG/r2.7/gl_ctg-ud-test.conllu",
    },
    "gl_treegal": {
        "train": "UD_Galician-TreeGal/r2.7/gl_treegal-ud-train.conllu",
        "test": "UD_Galician-TreeGal/r2.7/gl_treegal-ud-test.conllu",
    },
    "de_gsd": {
        "train": "UD_German-GSD/r2.7/de_gsd-ud-train.conllu",
        "dev": "UD_German-GSD/r2.7/de_gsd-ud-dev.conllu",
        "test": "UD_German-GSD/r2.7/de_gsd-ud-test.conllu",
    },
    "de_hdt": {
        "train": [
            "UD_German-HDT/r2.7/de_hdt-ud-train-a-1.conllu",
            "UD_German-HDT/r2.7/de_hdt-ud-train-a-2.conllu",
            "UD_German-HDT/r2.7/de_hdt-ud-train-b-1.conllu",
            "UD_German-HDT/r2.7/de_hdt-ud-train-b-2.conllu",
        ],
        "dev": "UD_German-HDT/r2.7/de_hdt-ud-dev.conllu",
        "test": "UD_German-HDT/r2.7/de_hdt-ud-test.conllu",
    },
    "de_lit": {
        "test": "UD_German-LIT/r2.7/de_lit-ud-test.conllu",
    },
    "de_pud": {
        "test": "UD_German-PUD/r2.7/de_pud-ud-test.conllu",
    },
    "got_proiel": {
        "train": "UD_Gothic-PROIEL/r2.7/got_proiel-ud-train.conllu",
        "dev": "UD_Gothic-PROIEL/r2.7/got_proiel-ud-dev.conllu",
        "test": "UD_Gothic-PROIEL/r2.7/got_proiel-ud-test.conllu",
    },
    "el_gdt": {
        "train": "UD_Greek-GDT/r2.7/el_gdt-ud-train.conllu",
        "dev": "UD_Greek-GDT/r2.7/el_gdt-ud-dev.conllu",
        "test": "UD_Greek-GDT/r2.7/el_gdt-ud-test.conllu",
    },
    "he_htb": {
        "train": "UD_Hebrew-HTB/r2.7/he_htb-ud-train.conllu",
        "dev": "UD_Hebrew-HTB/r2.7/he_htb-ud-dev.conllu",
        "test": "UD_Hebrew-HTB/r2.7/he_htb-ud-test.conllu",
    },
    "qhe_hiencs": {
        "train": "UD_Hindi_English-HIENCS/r2.7/qhe_hiencs-ud-train.conllu",
        "dev": "UD_Hindi_English-HIENCS/r2.7/qhe_hiencs-ud-dev.conllu",
        "test": "UD_Hindi_English-HIENCS/r2.7/qhe_hiencs-ud-test.conllu",
    },
    "hi_hdtb": {
        "train": "UD_Hindi-HDTB/r2.7/hi_hdtb-ud-train.conllu",
        "dev": "UD_Hindi-HDTB/r2.7/hi_hdtb-ud-dev.conllu",
        "test": "UD_Hindi-HDTB/r2.7/hi_hdtb-ud-test.conllu",
    },
    "hi_pud": {
        "test": "UD_Hindi-PUD/r2.7/hi_pud-ud-test.conllu",
    },
    "hu_szeged": {
        "train": "UD_Hungarian-Szeged/r2.7/hu_szeged-ud-train.conllu",
        "dev": "UD_Hungarian-Szeged/r2.7/hu_szeged-ud-dev.conllu",
        "test": "UD_Hungarian-Szeged/r2.7/hu_szeged-ud-test.conllu",
    },
    "is_icepahc": {
        "train": "UD_Icelandic-IcePaHC/r2.7/is_icepahc-ud-train.conllu",
        "dev": "UD_Icelandic-IcePaHC/r2.7/is_icepahc-ud-dev.conllu",
        "test": "UD_Icelandic-IcePaHC/r2.7/is_icepahc-ud-test.conllu",
    },
    "is_pud": {
        "test": "UD_Icelandic-PUD/r2.7/is_pud-ud-test.conllu",
    },
    "id_csui": {
        "train": "UD_Indonesian-CSUI/r2.7/id_csui-ud-train.conllu",
        "test": "UD_Indonesian-CSUI/r2.7/id_csui-ud-test.conllu",
    },
    "id_gsd": {
        "train": "UD_Indonesian-GSD/r2.7/id_gsd-ud-train.conllu",
        "dev": "UD_Indonesian-GSD/r2.7/id_gsd-ud-dev.conllu",
        "test": "UD_Indonesian-GSD/r2.7/id_gsd-ud-test.conllu",
    },
    "id_pud": {
        "test": "UD_Indonesian-PUD/r2.7/id_pud-ud-test.conllu",
    },
    "ga_idt": {
        "train": "UD_Irish-IDT/r2.7/ga_idt-ud-train.conllu",
        "dev": "UD_Irish-IDT/r2.7/ga_idt-ud-dev.conllu",
        "test": "UD_Irish-IDT/r2.7/ga_idt-ud-test.conllu",
    },
    "it_isdt": {
        "train": "UD_Italian-ISDT/r2.7/it_isdt-ud-train.conllu",
        "dev": "UD_Italian-ISDT/r2.7/it_isdt-ud-dev.conllu",
        "test": "UD_Italian-ISDT/r2.7/it_isdt-ud-test.conllu",
    },
    "it_partut": {
        "train": "UD_Italian-ParTUT/r2.7/it_partut-ud-train.conllu",
        "dev": "UD_Italian-ParTUT/r2.7/it_partut-ud-dev.conllu",
        "test": "UD_Italian-ParTUT/r2.7/it_partut-ud-test.conllu",
    },
    "it_postwita": {
        "train": "UD_Italian-PoSTWITA/r2.7/it_postwita-ud-train.conllu",
        "dev": "UD_Italian-PoSTWITA/r2.7/it_postwita-ud-dev.conllu",
        "test": "UD_Italian-PoSTWITA/r2.7/it_postwita-ud-test.conllu",
    },
    "it_pud": {
        "test": "UD_Italian-PUD/r2.7/it_pud-ud-test.conllu",
    },
    "it_twittiro": {
        "train": "UD_Italian-TWITTIRO/r2.7/it_twittiro-ud-train.conllu",
        "dev": "UD_Italian-TWITTIRO/r2.7/it_twittiro-ud-dev.conllu",
        "test": "UD_Italian-TWITTIRO/r2.7/it_twittiro-ud-test.conllu",
    },
    "it_vit": {
        "train": "UD_Italian-VIT/r2.7/it_vit-ud-train.conllu",
        "dev": "UD_Italian-VIT/r2.7/it_vit-ud-dev.conllu",
        "test": "UD_Italian-VIT/r2.7/it_vit-ud-test.conllu",
    },
    "ja_bccwj": {
        "train": "UD_Japanese-BCCWJ/r2.7/ja_bccwj-ud-train.conllu",
        "dev": "UD_Japanese-BCCWJ/r2.7/ja_bccwj-ud-dev.conllu",
        "test": "UD_Japanese-BCCWJ/r2.7/ja_bccwj-ud-test.conllu",
    },
    "ja_gsd": {
        "train": "UD_Japanese-GSD/r2.7/ja_gsd-ud-train.conllu",
        "dev": "UD_Japanese-GSD/r2.7/ja_gsd-ud-dev.conllu",
        "test": "UD_Japanese-GSD/r2.7/ja_gsd-ud-test.conllu",
    },
    "ja_modern": {
        "test": "UD_Japanese-Modern/r2.7/ja_modern-ud-test.conllu",
    },
    "ja_pud": {
        "test": "UD_Japanese-PUD/r2.7/ja_pud-ud-test.conllu",
    },
    "krl_kkpp": {
        "test": "UD_Karelian-KKPP/r2.7/krl_kkpp-ud-test.conllu",
    },
    "kk_ktb": {
        "train": "UD_Kazakh-KTB/r2.7/kk_ktb-ud-train.conllu",
        "test": "UD_Kazakh-KTB/r2.7/kk_ktb-ud-test.conllu",
    },
    "kfm_aha": {
        "test": "UD_Khunsari-AHA/r2.7/kfm_aha-ud-test.conllu",
    },
    "koi_uh": {
        "test": "UD_Komi_Permyak-UH/r2.7/koi_uh-ud-test.conllu",
    },
    "kpv_ikdp": {
        "test": "UD_Komi_Zyrian-IKDP/r2.7/kpv_ikdp-ud-test.conllu",
    },
    "kpv_lattice": {
        "test": "UD_Komi_Zyrian-Lattice/r2.7/kpv_lattice-ud-test.conllu",
    },
    "ko_gsd": {
        "train": "UD_Korean-GSD/r2.7/ko_gsd-ud-train.conllu",
        "dev": "UD_Korean-GSD/r2.7/ko_gsd-ud-dev.conllu",
        "test": "UD_Korean-GSD/r2.7/ko_gsd-ud-test.conllu",
    },
    "ko_kaist": {
        "train": "UD_Korean-Kaist/r2.7/ko_kaist-ud-train.conllu",
        "dev": "UD_Korean-Kaist/r2.7/ko_kaist-ud-dev.conllu",
        "test": "UD_Korean-Kaist/r2.7/ko_kaist-ud-test.conllu",
    },
    "ko_pud": {
        "test": "UD_Korean-PUD/r2.7/ko_pud-ud-test.conllu",
    },
    "kmr_mg": {
        "train": "UD_Kurmanji-MG/r2.7/kmr_mg-ud-train.conllu",
        "test": "UD_Kurmanji-MG/r2.7/kmr_mg-ud-test.conllu",
    },
    "la_ittb": {
        "train": "UD_Latin-ITTB/r2.7/la_ittb-ud-train.conllu",
        "dev": "UD_Latin-ITTB/r2.7/la_ittb-ud-dev.conllu",
        "test": "UD_Latin-ITTB/r2.7/la_ittb-ud-test.conllu",
    },
    "la_llct": {
        "train": "UD_Latin-LLCT/r2.7/la_llct-ud-train.conllu",
        "dev": "UD_Latin-LLCT/r2.7/la_llct-ud-dev.conllu",
        "test": "UD_Latin-LLCT/r2.7/la_llct-ud-test.conllu",
    },
    "la_perseus": {
        "train": "UD_Latin-Perseus/r2.7/la_perseus-ud-train.conllu",
        "test": "UD_Latin-Perseus/r2.7/la_perseus-ud-test.conllu",
    },
    "la_proiel": {
        "train": "UD_Latin-PROIEL/r2.7/la_proiel-ud-train.conllu",
        "dev": "UD_Latin-PROIEL/r2.7/la_proiel-ud-dev.conllu",
        "test": "UD_Latin-PROIEL/r2.7/la_proiel-ud-test.conllu",
    },
    "lv_lvtb": {
        "train": "UD_Latvian-LVTB/r2.7/lv_lvtb-ud-train.conllu",
        "dev": "UD_Latvian-LVTB/r2.7/lv_lvtb-ud-dev.conllu",
        "test": "UD_Latvian-LVTB/r2.7/lv_lvtb-ud-test.conllu",
    },
    "lt_alksnis": {
        "train": "UD_Lithuanian-ALKSNIS/r2.7/lt_alksnis-ud-train.conllu",
        "dev": "UD_Lithuanian-ALKSNIS/r2.7/lt_alksnis-ud-dev.conllu",
        "test": "UD_Lithuanian-ALKSNIS/r2.7/lt_alksnis-ud-test.conllu",
    },
    "lt_hse": {
        "train": "UD_Lithuanian-HSE/r2.7/lt_hse-ud-train.conllu",
        "dev": "UD_Lithuanian-HSE/r2.7/lt_hse-ud-train.conllu",
        "test": "UD_Lithuanian-HSE/r2.7/lt_hse-ud-train.conllu",
    },
    "olo_kkpp": {
        "train": "UD_Livvi-KKPP/r2.7/olo_kkpp-ud-train.conllu",
        "test": "UD_Livvi-KKPP/r2.7/olo_kkpp-ud-test.conllu",
    },
    "mt_mudt": {
        "train": "UD_Maltese-MUDT/r2.7/mt_mudt-ud-train.conllu",
        "dev": "UD_Maltese-MUDT/r2.7/mt_mudt-ud-dev.conllu",
        "test": "UD_Maltese-MUDT/r2.7/mt_mudt-ud-test.conllu",
    },
    "gv_cadhan": {
        "test": "UD_Manx-Cadhan/r2.7/gv_cadhan-ud-test.conllu",
    },
    "mr_ufal": {
        "train": "UD_Marathi-UFAL/r2.7/mr_ufal-ud-train.conllu",
        "dev": "UD_Marathi-UFAL/r2.7/mr_ufal-ud-dev.conllu",
        "test": "UD_Marathi-UFAL/r2.7/mr_ufal-ud-test.conllu",
    },
    "gun_dooley": {
        "test": "UD_Mbya_Guarani-Dooley/r2.7/gun_dooley-ud-test.conllu",
    },
    "gun_thomas": {
        "test": "UD_Mbya_Guarani-Thomas/r2.7/gun_thomas-ud-test.conllu",
    },
    "mdf_jr": {
        "test": "UD_Moksha-JR/r2.7/mdf_jr-ud-test.conllu",
    },
    "myu_tudet": {
        "test": "UD_Munduruku-TuDeT/r2.7/myu_tudet-ud-test.conllu",
    },
    "pcm_nsc": {
        "train": "UD_Naija-NSC/r2.7/pcm_nsc-ud-train.conllu",
        "dev": "UD_Naija-NSC/r2.7/pcm_nsc-ud-dev.conllu",
        "test": "UD_Naija-NSC/r2.7/pcm_nsc-ud-test.conllu",
    },
    "nyq_aha": {
        "test": "UD_Nayini-AHA/r2.7/nyq_aha-ud-test.conllu",
    },
    "sme_giella": {
        "train": "UD_North_Sami-Giella/r2.7/sme_giella-ud-train.conllu",
        "test": "UD_North_Sami-Giella/r2.7/sme_giella-ud-test.conllu",
    },
    "no_bokmaal": {
        "train": "UD_Norwegian-Bokmaal/r2.7/no_bokmaal-ud-train.conllu",
        "dev": "UD_Norwegian-Bokmaal/r2.7/no_bokmaal-ud-dev.conllu",
        "test": "UD_Norwegian-Bokmaal/r2.7/no_bokmaal-ud-test.conllu",
    },
    "no_nynorsk": {
        "train": "UD_Norwegian-Nynorsk/r2.7/no_nynorsk-ud-train.conllu",
        "dev": "UD_Norwegian-Nynorsk/r2.7/no_nynorsk-ud-dev.conllu",
        "test": "UD_Norwegian-Nynorsk/r2.7/no_nynorsk-ud-test.conllu",
    },
    "no_nynorsklia": {
        "train": "UD_Norwegian-NynorskLIA/r2.7/no_nynorsklia-ud-train.conllu",
        "dev": "UD_Norwegian-NynorskLIA/r2.7/no_nynorsklia-ud-dev.conllu",
        "test": "UD_Norwegian-NynorskLIA/r2.7/no_nynorsklia-ud-test.conllu",
    },
    "cu_proiel": {
        "train": "UD_Old_Church_Slavonic-PROIEL/r2.7/cu_proiel-ud-train.conllu",
        "dev": "UD_Old_Church_Slavonic-PROIEL/r2.7/cu_proiel-ud-dev.conllu",
        "test": "UD_Old_Church_Slavonic-PROIEL/r2.7/cu_proiel-ud-test.conllu",
    },
    "fro_srcmf": {
        "train": "UD_Old_French-SRCMF/r2.7/fro_srcmf-ud-train.conllu",
        "dev": "UD_Old_French-SRCMF/r2.7/fro_srcmf-ud-dev.conllu",
        "test": "UD_Old_French-SRCMF/r2.7/fro_srcmf-ud-test.conllu",
    },
    "orv_rnc": {
        "train": "UD_Old_Russian-RNC/r2.7/orv_rnc-ud-train.conllu",
        "test": "UD_Old_Russian-RNC/r2.7/orv_rnc-ud-test.conllu",
    },
    "orv_torot": {
        "train": "UD_Old_Russian-TOROT/r2.7/orv_torot-ud-train.conllu",
        "dev": "UD_Old_Russian-TOROT/r2.7/orv_torot-ud-dev.conllu",
        "test": "UD_Old_Russian-TOROT/r2.7/orv_torot-ud-test.conllu",
    },
    "otk_tonqq": {
        "test": "UD_Old_Turkish-Tonqq/r2.7/otk_tonqq-ud-test.conllu",
    },
    "fa_perdt": {
        "train": "UD_Persian-PerDT/r2.7/fa_perdt-ud-train.conllu",
        "dev": "UD_Persian-PerDT/r2.7/fa_perdt-ud-dev.conllu",
        "test": "UD_Persian-PerDT/r2.7/fa_perdt-ud-test.conllu",
    },
    "fa_seraji": {
        "train": "UD_Persian-Seraji/r2.7/fa_seraji-ud-train.conllu",
        "dev": "UD_Persian-Seraji/r2.7/fa_seraji-ud-dev.conllu",
        "test": "UD_Persian-Seraji/r2.7/fa_seraji-ud-test.conllu",
    },
    "pl_lfg": {
        "train": "UD_Polish-LFG/r2.7/pl_lfg-ud-train.conllu",
        "dev": "UD_Polish-LFG/r2.7/pl_lfg-ud-dev.conllu",
        "test": "UD_Polish-LFG/r2.7/pl_lfg-ud-test.conllu",
    },
    "pl_pdb": {
        "train": "UD_Polish-PDB/r2.7/pl_pdb-ud-train.conllu",
        "dev": "UD_Polish-PDB/r2.7/pl_pdb-ud-dev.conllu",
        "test": "UD_Polish-PDB/r2.7/pl_pdb-ud-test.conllu",
    },
    "pl_pud": {
        "test": "UD_Polish-PUD/r2.7/pl_pud-ud-test.conllu",
    },
    "pt_bosque": {
        "train": "UD_Portuguese-Bosque/r2.7/pt_bosque-ud-train.conllu",
        "dev": "UD_Portuguese-Bosque/r2.7/pt_bosque-ud-dev.conllu",
        "test": "UD_Portuguese-Bosque/r2.7/pt_bosque-ud-test.conllu",
    },
    "pt_gsd": {
        "train": "UD_Portuguese-GSD/r2.7/pt_gsd-ud-train.conllu",
        "dev": "UD_Portuguese-GSD/r2.7/pt_gsd-ud-dev.conllu",
        "test": "UD_Portuguese-GSD/r2.7/pt_gsd-ud-test.conllu",
    },
    "pt_pud": {
        "test": "UD_Portuguese-PUD/r2.7/pt_pud-ud-test.conllu",
    },
    "ro_nonstandard": {
        "train": "UD_Romanian-Nonstandard/r2.7/ro_nonstandard-ud-train.conllu",
        "dev": "UD_Romanian-Nonstandard/r2.7/ro_nonstandard-ud-dev.conllu",
        "test": "UD_Romanian-Nonstandard/r2.7/ro_nonstandard-ud-test.conllu",
    },
    "ro_rrt": {
        "train": "UD_Romanian-RRT/r2.7/ro_rrt-ud-train.conllu",
        "dev": "UD_Romanian-RRT/r2.7/ro_rrt-ud-dev.conllu",
        "test": "UD_Romanian-RRT/r2.7/ro_rrt-ud-test.conllu",
    },
    "ro_simonero": {
        "train": "UD_Romanian-SiMoNERo/r2.7/ro_simonero-ud-train.conllu",
        "dev": "UD_Romanian-SiMoNERo/r2.7/ro_simonero-ud-dev.conllu",
        "test": "UD_Romanian-SiMoNERo/r2.7/ro_simonero-ud-test.conllu",
    },
    "ru_gsd": {
        "train": "UD_Russian-GSD/r2.7/ru_gsd-ud-train.conllu",
        "dev": "UD_Russian-GSD/r2.7/ru_gsd-ud-dev.conllu",
        "test": "UD_Russian-GSD/r2.7/ru_gsd-ud-test.conllu",
    },
    "ru_pud": {
        "test": "UD_Russian-PUD/r2.7/ru_pud-ud-test.conllu",
    },
    "ru_syntagrus": {
        "train": "UD_Russian-SynTagRus/r2.7/ru_syntagrus-ud-train.conllu",
        "dev": "UD_Russian-SynTagRus/r2.7/ru_syntagrus-ud-dev.conllu",
        "test": "UD_Russian-SynTagRus/r2.7/ru_syntagrus-ud-test.conllu",
    },
    "ru_taiga": {
        "train": "UD_Russian-Taiga/r2.7/ru_taiga-ud-train.conllu",
        "dev": "UD_Russian-Taiga/r2.7/ru_taiga-ud-dev.conllu",
        "test": "UD_Russian-Taiga/r2.7/ru_taiga-ud-test.conllu",
    },
    "sa_ufal": {
        "test": "UD_Sanskrit-UFAL/r2.7/sa_ufal-ud-test.conllu",
    },
    "sa_vedic": {
        "train": "UD_Sanskrit-Vedic/r2.7/sa_vedic-ud-train.conllu",
        "test": "UD_Sanskrit-Vedic/r2.7/sa_vedic-ud-test.conllu",
    },
    "gd_arcosg": {
        "train": "UD_Scottish_Gaelic-ARCOSG/r2.7/gd_arcosg-ud-train.conllu",
        "dev": "UD_Scottish_Gaelic-ARCOSG/r2.7/gd_arcosg-ud-dev.conllu",
        "test": "UD_Scottish_Gaelic-ARCOSG/r2.7/gd_arcosg-ud-test.conllu",
    },
    "sr_set": {
        "train": "UD_Serbian-SET/r2.7/sr_set-ud-train.conllu",
        "dev": "UD_Serbian-SET/r2.7/sr_set-ud-dev.conllu",
        "test": "UD_Serbian-SET/r2.7/sr_set-ud-test.conllu",
    },
    "sms_giellagas": {
        "test": "UD_Skolt_Sami-Giellagas/r2.7/sms_giellagas-ud-test.conllu",
    },
    "sk_snk": {
        "train": "UD_Slovak-SNK/r2.7/sk_snk-ud-train.conllu",
        "dev": "UD_Slovak-SNK/r2.7/sk_snk-ud-dev.conllu",
        "test": "UD_Slovak-SNK/r2.7/sk_snk-ud-test.conllu",
    },
    "sl_ssj": {
        "train": "UD_Slovenian-SSJ/r2.7/sl_ssj-ud-train.conllu",
        "dev": "UD_Slovenian-SSJ/r2.7/sl_ssj-ud-dev.conllu",
        "test": "UD_Slovenian-SSJ/r2.7/sl_ssj-ud-test.conllu",
    },
    "sl_sst": {
        "train": "UD_Slovenian-SST/r2.7/sl_sst-ud-train.conllu",
        "test": "UD_Slovenian-SST/r2.7/sl_sst-ud-test.conllu",
    },
    "soj_aha": {
        "test": "UD_Soi-AHA/r2.7/soj_aha-ud-test.conllu",
    },
    "ajp_madar": {
        "test": "UD_South_Levantine_Arabic-MADAR/r2.7/ajp_madar-ud-test.conllu",
    },
    "es_ancora": {
        "train": "UD_Spanish-AnCora/r2.7/es_ancora-ud-train.conllu",
        "dev": "UD_Spanish-AnCora/r2.7/es_ancora-ud-dev.conllu",
        "test": "UD_Spanish-AnCora/r2.7/es_ancora-ud-test.conllu",
    },
    "es_gsd": {
        "train": "UD_Spanish-GSD/r2.7/es_gsd-ud-train.conllu",
        "dev": "UD_Spanish-GSD/r2.7/es_gsd-ud-dev.conllu",
        "test": "UD_Spanish-GSD/r2.7/es_gsd-ud-test.conllu",
    },
    "es_pud": {
        "test": "UD_Spanish-PUD/r2.7/es_pud-ud-test.conllu",
    },
    "swl_sslc": {
        "train": "UD_Swedish_Sign_Language-SSLC/r2.7/swl_sslc-ud-train.conllu",
        "dev": "UD_Swedish_Sign_Language-SSLC/r2.7/swl_sslc-ud-dev.conllu",
        "test": "UD_Swedish_Sign_Language-SSLC/r2.7/swl_sslc-ud-test.conllu",
    },
    "sv_lines": {
        "train": "UD_Swedish-LinES/r2.7/sv_lines-ud-train.conllu",
        "dev": "UD_Swedish-LinES/r2.7/sv_lines-ud-dev.conllu",
        "test": "UD_Swedish-LinES/r2.7/sv_lines-ud-test.conllu",
    },
    "sv_pud": {
        "test": "UD_Swedish-PUD/r2.7/sv_pud-ud-test.conllu",
    },
    "sv_talbanken": {
        "train": "UD_Swedish-Talbanken/r2.7/sv_talbanken-ud-train.conllu",
        "dev": "UD_Swedish-Talbanken/r2.7/sv_talbanken-ud-dev.conllu",
        "test": "UD_Swedish-Talbanken/r2.7/sv_talbanken-ud-test.conllu",
    },
    "gsw_uzh": {
        "test": "UD_Swiss_German-UZH/r2.7/gsw_uzh-ud-test.conllu",
    },
    "tl_trg": {
        "test": "UD_Tagalog-TRG/r2.7/tl_trg-ud-test.conllu",
    },
    "tl_ugnayan": {
        "test": "UD_Tagalog-Ugnayan/r2.7/tl_ugnayan-ud-test.conllu",
    },
    "ta_mwtt": {
        "test": "UD_Tamil-MWTT/r2.7/ta_mwtt-ud-test.conllu",
    },
    "ta_ttb": {
        "train": "UD_Tamil-TTB/r2.7/ta_ttb-ud-train.conllu",
        "dev": "UD_Tamil-TTB/r2.7/ta_ttb-ud-dev.conllu",
        "test": "UD_Tamil-TTB/r2.7/ta_ttb-ud-test.conllu",
    },
    "te_mtg": {
        "train": "UD_Telugu-MTG/r2.7/te_mtg-ud-train.conllu",
        "dev": "UD_Telugu-MTG/r2.7/te_mtg-ud-dev.conllu",
        "test": "UD_Telugu-MTG/r2.7/te_mtg-ud-test.conllu",
    },
    "th_pud": {
        "test": "UD_Thai-PUD/r2.7/th_pud-ud-test.conllu",
    },
    "tpn_tudet": {
        "test": "UD_Tupinamba-TuDeT/r2.7/tpn_tudet-ud-test.conllu",
    },
    "qtd_sagt": {
        "train": "UD_Turkish_German-SAGT/r2.7/qtd_sagt-ud-train.conllu",
        "dev": "UD_Turkish_German-SAGT/r2.7/qtd_sagt-ud-dev.conllu",
        "test": "UD_Turkish_German-SAGT/r2.7/qtd_sagt-ud-test.conllu",
    },
    "tr_boun": {
        "train": "UD_Turkish-BOUN/r2.7/tr_boun-ud-train.conllu",
        "dev": "UD_Turkish-BOUN/r2.7/tr_boun-ud-dev.conllu",
        "test": "UD_Turkish-BOUN/r2.7/tr_boun-ud-test.conllu",
    },
    "tr_gb": {
        "test": "UD_Turkish-GB/r2.7/tr_gb-ud-test.conllu",
    },
    "tr_imst": {
        "train": "UD_Turkish-IMST/r2.7/tr_imst-ud-train.conllu",
        "dev": "UD_Turkish-IMST/r2.7/tr_imst-ud-dev.conllu",
        "test": "UD_Turkish-IMST/r2.7/tr_imst-ud-test.conllu",
    },
    "tr_pud": {
        "test": "UD_Turkish-PUD/r2.7/tr_pud-ud-test.conllu",
    },
    "uk_iu": {
        "train": "UD_Ukrainian-IU/r2.7/uk_iu-ud-train.conllu",
        "dev": "UD_Ukrainian-IU/r2.7/uk_iu-ud-dev.conllu",
        "test": "UD_Ukrainian-IU/r2.7/uk_iu-ud-test.conllu",
    },
    "hsb_ufal": {
        "train": "UD_Upper_Sorbian-UFAL/r2.7/hsb_ufal-ud-train.conllu",
        "test": "UD_Upper_Sorbian-UFAL/r2.7/hsb_ufal-ud-test.conllu",
    },
    "ur_udtb": {
        "train": "UD_Urdu-UDTB/r2.7/ur_udtb-ud-train.conllu",
        "dev": "UD_Urdu-UDTB/r2.7/ur_udtb-ud-dev.conllu",
        "test": "UD_Urdu-UDTB/r2.7/ur_udtb-ud-test.conllu",
    },
    "ug_udt": {
        "train": "UD_Uyghur-UDT/r2.7/ug_udt-ud-train.conllu",
        "dev": "UD_Uyghur-UDT/r2.7/ug_udt-ud-dev.conllu",
        "test": "UD_Uyghur-UDT/r2.7/ug_udt-ud-test.conllu",
    },
    "vi_vtb": {
        "train": "UD_Vietnamese-VTB/r2.7/vi_vtb-ud-train.conllu",
        "dev": "UD_Vietnamese-VTB/r2.7/vi_vtb-ud-dev.conllu",
        "test": "UD_Vietnamese-VTB/r2.7/vi_vtb-ud-test.conllu",
    },
    "wbp_ufal": {
        "test": "UD_Warlpiri-UFAL/r2.7/wbp_ufal-ud-test.conllu",
    },
    "cy_ccg": {
        "train": "UD_Welsh-CCG/r2.7/cy_ccg-ud-train.conllu",
        "test": "UD_Welsh-CCG/r2.7/cy_ccg-ud-test.conllu",
    },
    "wo_wtb": {
        "train": "UD_Wolof-WTB/r2.7/wo_wtb-ud-train.conllu",
        "dev": "UD_Wolof-WTB/r2.7/wo_wtb-ud-dev.conllu",
        "test": "UD_Wolof-WTB/r2.7/wo_wtb-ud-test.conllu",
    },
    "yo_ytb": {
        "test": "UD_Yoruba-YTB/r2.7/yo_ytb-ud-test.conllu",
    },
}


class UniversaldependenciesConfig(datasets.BuilderConfig):
    """BuilderConfig for Universal dependencies"""

    def __init__(self, data_url, **kwargs):
        super(UniversaldependenciesConfig, self).__init__(version=datasets.Version("2.7.0", ""), **kwargs)

        self.data_url = data_url


class UniversalDependencies(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("2.7.0")
    BUILDER_CONFIGS = [
        UniversaldependenciesConfig(
            name=name,
            description=_DESCRIPTIONS[name],
            data_url="https://github.com/UniversalDependencies/" + _UD_DATASETS[name]["test"].split("/")[0],
        )
        for name in _NAMES
    ]
    BUILDER_CONFIG_CLASS = UniversaldependenciesConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "idx": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "lemmas": datasets.Sequence(datasets.Value("string")),
                    "upos": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "NOUN",
                                "PUNCT",
                                "ADP",
                                "NUM",
                                "SYM",
                                "SCONJ",
                                "ADJ",
                                "PART",
                                "DET",
                                "CCONJ",
                                "PROPN",
                                "PRON",
                                "X",
                                "_",
                                "ADV",
                                "INTJ",
                                "VERB",
                                "AUX",
                            ]
                        )
                    ),
                    "xpos": datasets.Sequence(datasets.Value("string")),
                    "feats": datasets.Sequence(datasets.Value("string")),
                    "head": datasets.Sequence(datasets.Value("string")),
                    "deprel": datasets.Sequence(datasets.Value("string")),
                    "deps": datasets.Sequence(datasets.Value("string")),
                    "misc": datasets.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage="https://universaldependencies.org/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {}
        for split, address in _UD_DATASETS[self.config.name].items():
            urls_to_download[split] = []
            if isinstance(address, list):
                for add in address:
                    urls_to_download[split].append(_PREFIX + add)
            else:
                urls_to_download[split].append(_PREFIX + address)

        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        splits = []

        if "train" in downloaded_files:
            splits.append(
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]})
            )

        if "dev" in downloaded_files:
            splits.append(
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}
                )
            )

        if "test" in downloaded_files:
            splits.append(
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]})
            )

        return splits

    def _generate_examples(self, filepath):
        id = 0
        for path in filepath:
            with open(path, "r", encoding="utf-8") as data_file:
                tokenlist = list(conllu.parse_incr(data_file))
                for sent in tokenlist:
                    if "sent_id" in sent.metadata:
                        idx = sent.metadata["sent_id"]
                    else:
                        idx = id

                    tokens = [token["form"] for token in sent]

                    if "text" in sent.metadata:
                        txt = sent.metadata["text"]
                    else:
                        txt = " ".join(tokens)

                    yield id, {
                        "idx": str(idx),
                        "text": txt,
                        "tokens": [token["form"] for token in sent],
                        "lemmas": [token["lemma"] for token in sent],
                        "upos": [token["upos"] for token in sent],
                        "xpos": [token["xpos"] for token in sent],
                        "feats": [str(token["feats"]) for token in sent],
                        "head": [str(token["head"]) for token in sent],
                        "deprel": [str(token["deprel"]) for token in sent],
                        "deps": [str(token["deps"]) for token in sent],
                        "misc": [str(token["misc"]) for token in sent],
                    }
                    id += 1
