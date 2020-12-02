from __future__ import absolute_import, division, print_function

import datasets

_CITATION = """\
@misc{11234/1-3424,
 title = {Universal Dependencies 2.7},
 author = {Zeman, Daniel and Nivre, Joakim and Abrams, Mitchell and Ackermann, Elia and Aepli, No{\"e}mi and Aghaei, Hamid and Agi{\'c}, {\v Z}eljko and Ahmadi, Amir and Ahrenberg, Lars and Ajede,
 Chika Kennedy and Aleksandravi{\v c}i{\=u}t{\.e}, Gabriel{\.e} and Alfina, Ika and Antonsen, Lene and Aplonova, Katya and Aquino, Angelina and Aragon, Carolina and Aranzabe, Maria Jesus and Arnard{\'o}ttir, {\t H}{\'o}runn and Arutie, Gashaw and Arwidarasti, Jessica Naraiswari and Asahara, Masayuki and Ateyah, Luma and Atmaca, Furkan and Attia, Mohammed and Atutxa, Aitziber and Augustinus, Liesbeth and Badmaeva, Elena and Balasubramani, Keerthana and Ballesteros, Miguel and Banerjee, Esha and Bank, Sebastian and Barbu Mititelu, Verginica and Basmov, Victoria and Batchelor, Colin and Bauer, John and Bedir, Seyyit Talha and Bengoetxea, Kepa and Berk, G{\"o}zde and Berzak, Yevgeni and Bhat, Irshad Ahmad and Bhat, Riyaz Ahmad and Biagetti, Erica and Bick, Eckhard and Bielinskien{\.e}, Agn{\.e} and Bjarnad{\'o}ttir, Krist{\'{\i}}n and Blokland, Rogier and Bobicev, Victoria and Boizou, Lo{\"{\i}}c and Borges V{\"o}lker, Emanuel and B{\"o}rstell, Carl and Bosco, Cristina and Bouma, Gosse and Bowman, Sam and Boyd, Adriane and Brokait{\.e}, Kristina and Burchardt, Aljoscha and Candito, Marie and Caron, Bernard and Caron, Gauthier and Cavalcanti, Tatiana and Cebiro{\u g}lu Eryi{\u g}it, G{\"u}l{\c s}en and Cecchini, Flavio Massimiliano and Celano, Giuseppe G. A. and {\v C}{\'e}pl{\"o}, Slavom{\'{\i}}r and Cetin, Savas and {\c C}etino{\u g}lu, {\"O}zlem and Chalub, Fabricio and Chi, Ethan and Cho, Yongseok and Choi, Jinho and Chun, Jayeol and Cignarella, Alessandra T. and Cinkov{\'a}, Silvie and Collomb, Aur{\'e}lie and {\c C}{\"o}ltekin, {\c C}a{\u g}r{\i} and Connor, Miriam and Courtin, Marine and Davidson, Elizabeth and de Marneffe, Marie-Catherine and de Paiva, Valeria and Derin, Mehmet Oguz and de Souza, Elvis and Diaz de Ilarraza, Arantza and Dickerson, Carly and Dinakaramani, Arawinda and Dione, Bamba and Dirix, Peter and Dobrovoljc, Kaja and Dozat, Timothy and Droganova, Kira and Dwivedi, Puneet and Eckhoff, Hanne and Eli, Marhaba and Elkahky, Ali and Ephrem, Binyam and Erina, Olga and Erjavec, Toma{\v z} and Etienne, Aline and Evelyn, Wograine and Facundes, Sidney and Farkas, Rich{\'a}rd and Fernanda, Mar{\'{\i}}lia and Fernandez Alcalde, Hector and Foster, Jennifer and Freitas, Cl{\'a}udia and Fujita, Kazunori and Gajdo{\v s}ov{\'a}, Katar{\'{\i}}na and Galbraith, Daniel and Garcia, Marcos and G{\"a}rdenfors, Moa and Garza, Sebastian and Gerardi, Fabr{\'{\i}}cio Ferraz and Gerdes, Kim and Ginter, Filip and Goenaga, Iakes and Gojenola, Koldo and G{\"o}k{\i}rmak, Memduh and Goldberg, Yoav and G{\'o}mez Guinovart, Xavier and Gonz{\'a}lez Saavedra,
 Berta and Grici{\=u}t{\.e}, Bernadeta and Grioni, Matias and Grobol,
 Lo{\"{\i}}c and Gr{\=
u}z{\={\i}}tis, Normunds and Guillaume, Bruno and Guillot-Barbance, C{\'e}line and G{\"u}ng{\"o}r, Tunga and Habash, Nizar and Hafsteinsson, Hinrik and Haji{\v c}, Jan and Haji{\v c} jr., Jan and H{\"a}m{\"a}l{\"a}inen, Mika and H{\`a} M{\~y}, Linh and Han, Na-Rae and Hanifmuti, Muhammad Yudistira and Hardwick, Sam and Harris, Kim and Haug, Dag and Heinecke, Johannes and Hellwig, Oliver and Hennig, Felix and Hladk{\'a}, Barbora and Hlav{\'a}{\v c}ov{\'a}, Jaroslava and Hociung, Florinel and Hohle, Petter and Huber, Eva and Hwang, Jena and Ikeda, Takumi and Ingason, Anton Karl and Ion, Radu and Irimia, Elena and Ishola, {\d O}l{\'a}j{\'{\i}}d{\'e} and Jel{\'{\i}}nek, Tom{\'a}{\v s} and Johannsen, Anders and J{\'o}nsd{\'o}ttir, Hildur and J{\o}rgensen, Fredrik and Juutinen, Markus and K, Sarveswaran and Ka{\c s}{\i}kara, H{\"u}ner and Kaasen, Andre and Kabaeva, Nadezhda and Kahane, Sylvain and Kanayama, Hiroshi and Kanerva, Jenna and Katz, Boris and Kayadelen, Tolga and Kenney, Jessica and Kettnerov{\'a}, V{\'a}clava and Kirchner, Jesse and Klementieva, Elena and K{\"o}hn, Arne and K{\"o}ksal, Abdullatif and Kopacewicz, Kamil and Korkiakangas, Timo and Kotsyba, Natalia and Kovalevskait{\.e}, Jolanta and Krek, Simon and Krishnamurthy, Parameswari and Kwak, Sookyoung and Laippala, Veronika and Lam, Lucia and Lambertino, Lorenzo and Lando, Tatiana and Larasati, Septina Dian and Lavrentiev, Alexei and Lee, John and L{\^e} H{\`{\^o}}ng, Phương and Lenci, Alessandro and Lertpradit, Saran and Leung, Herman and Levina, Maria and Li, Cheuk Ying and Li, Josie and Li, Keying and Li, Yuan and Lim, {KyungTae} and Lind{\'e}n, Krister and Ljube{\v s}i{\'c}, Nikola and Loginova, Olga and Luthfi, Andry and Luukko, Mikko and Lyashevskaya, Olga and Lynn, Teresa and Macketanz, Vivien and Makazhanov, Aibek and Mandl, Michael and Manning, Christopher and Manurung, Ruli and M{\u a}r{\u a}nduc, C{\u a}t{\u a}lina and Mare{\v c}ek, David and Marheinecke, Katrin and Mart{\'{\i}}nez Alonso, H{\'e}ctor and Martins, Andr{\'e} and Ma{\v s}ek, Jan and Matsuda, Hiroshi and Matsumoto, Yuji and {McDonald}, Ryan and {McGuinness}, Sarah and Mendon{\c c}a, Gustavo and Miekka, Niko and Mischenkova, Karina and Misirpashayeva, Margarita and Missil{\"a}, Anna and Mititelu, C{\u a}t{\u a}lin and Mitrofan, Maria and Miyao, Yusuke and Mojiri Foroushani, {AmirHossein} and Moloodi, Amirsaeid and Montemagni, Simonetta and More, Amir and Moreno Romero, Laura and Mori, Keiko Sophie and Mori, Shinsuke and Morioka, Tomohiko and Moro, Shigeki and Mortensen, Bjartur and Moskalevskyi, Bohdan and Muischnek, Kadri and Munro, Robert and Murawaki, Yugo and M{\"u}{\"u}risep, Kaili and Nainwani, Pinkey and Nakhl{\'e}, Mariam and Navarro Hor{\~n}iacek, Juan Ignacio and Nedoluzhko,
 Anna and Ne{\v s}pore-B{\=e}rzkalne, Gunta and Nguy{\~{\^e}}n Th{\d i}, Lương and Nguy{\~{\^e}}n Th{\d i} Minh, Huy{\`{\^e}}n and Nikaido, Yoshihiro and Nikolaev, Vitaly and Nitisaroj, Rattima and Nourian, Alireza and Nurmi, Hanna and Ojala, Stina and Ojha, Atul Kr. and Ol{\'u}{\`o}kun, Ad{\'e}day{\d o}̀ and Omura, Mai and Onwuegbuzia, Emeka and Osenova, Petya and {\"O}stling, Robert and {\O}vrelid, Lilja and {\"O}zate{\c s}, {\c S}aziye Bet{\"u}l and {\"O}zg{\"u}r, Arzucan and {\"O}zt{\"u}rk Ba{\c s}aran, Balk{\i}z and Partanen, Niko and Pascual, Elena and Passarotti, Marco and Patejuk, Agnieszka and Paulino-Passos, Guilherme and Peljak-{\L}api{\'n}ska, Angelika and Peng, Siyao and Perez, Cenel-Augusto and Perkova, Natalia and Perrier, Guy and Petrov, Slav and Petrova, Daria and Phelan, Jason and Piitulainen, Jussi and Pirinen, Tommi A and Pitler, Emily and Plank, Barbara and Poibeau, Thierry and Ponomareva, Larisa and Popel, Martin and Pretkalni{\c n}a, Lauma and Pr{\'e}vost, Sophie and Prokopidis, Prokopis and Przepi{\'o}rkowski, Adam and Puolakainen, Tiina and Pyysalo, Sampo and Qi, Peng and R{\"a}{\"a}bis, Andriela and Rademaker, Alexandre and Rama, Taraka and Ramasamy, Loganathan and Ramisch, Carlos and Rashel, Fam and Rasooli, Mohammad Sadegh and Ravishankar, Vinit and Real, Livy and Rebeja, Petru and Reddy, Siva and Rehm, Georg and Riabov, Ivan and Rie{\ss}ler, Michael and Rimkut{\.e}, Erika and Rinaldi, Larissa and Rituma, Laura and Rocha, Luisa and R{\"o}gnvaldsson, Eir{\'{\i}}kur and Romanenko, Mykhailo and Rosa, Rudolf and Roșca, Valentin and Rovati, Davide and Rudina, Olga and Rueter, Jack and R{\'u}narsson, Kristj{\'a}n and Sadde, Shoval and Safari, Pegah and Sagot, Beno{\^{\i}}t and Sahala, Aleksi and Saleh, Shadi and Salomoni, Alessio and Samard{\v z}i{\'c}, Tanja and Samson, Stephanie and Sanguinetti, Manuela and S{\"a}rg,
 Dage and Saul{\={\i}}te, Baiba and Sawanakunanon, Yanin and Scannell, Kevin and Scarlata, Salvatore and Schneider, Nathan and Schuster, Sebastian and Seddah, Djam{\'e} and Seeker, Wolfgang and Seraji, Mojgan and Shen, Mo and Shimada, Atsuko and Shirasu, Hiroyuki and Shohibussirri, Muh and Sichinava, Dmitry and Sigurðsson, Einar Freyr and Silveira, Aline and Silveira, Natalia and Simi, Maria and Simionescu, Radu and Simk{\'o}, Katalin and {\v S}imkov{\'a}, M{\'a}ria and Simov, Kiril and Skachedubova, Maria and Smith, Aaron and Soares-Bastos, Isabela and Spadine, Carolyn and Steingr{\'{\i}}msson, Stein{\t h}{\'o}r and Stella, Antonio and Straka, Milan and Strickland, Emmett and Strnadov{\'a}, Jana and Suhr, Alane and Sulestio, Yogi Lesmana and Sulubacak, Umut and Suzuki, Shingo and Sz{\'a}nt{\'o}, Zsolt and Taji, Dima and Takahashi, Yuta and Tamburini, Fabio and Tan, Mary Ann C. and Tanaka, Takaaki and Tella, Samson and Tellier, Isabelle and Thomas, Guillaume and Torga, Liisi and Toska, Marsida and Trosterud, Trond and Trukhina, Anna and Tsarfaty, Reut and T{\"u}rk, Utku and Tyers, Francis and Uematsu, Sumire and Untilov, Roman and Ure{\v s}ov{\'a}, Zde{\v n}ka and Uria, Larraitz and Uszkoreit, Hans and Utka, Andrius and Vajjala, Sowmya and van Niekerk, Daniel and van Noord, Gertjan and Varga, Viktor and Villemonte de la Clergerie, Eric and Vincze, Veronika and Wakasa, Aya and Wallenberg, Joel C. and Wallin, Lars and Walsh, Abigail and Wang, Jing Xian and Washington, Jonathan North and Wendt, Maximilan and Widmer, Paul and Williams, Seyi and Wir{\'e}n, Mats and Wittern, Christian and Woldemariam, Tsegay and Wong, Tak-sum and Wr{\'o}blewska, Alina and Yako, Mary and Yamashita, Kayo and Yamazaki, Naoki and Yan, Chunxiao and Yasuoka, Koichi and Yavrumyan, Marat M. and Yu, Zhuoran and {\v Z}abokrtsk{\'y}, Zden{\v e}k and Zahra, Shorouq and Zeldes, Amir and Zhu, Hanzhi and Zhuravleva, Anna},
 url = {http://hdl.handle.net/11234/1-3424},
 note = {{LINDAT}/{CLARIAH}-{CZ} digital library at the Institute of Formal and Applied Linguistics ({{\'U}FAL}), Faculty of Mathematics and Physics, Charles University},
 copyright = {Licence Universal Dependencies v2.7},
 year = {2020} }
"""

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
]

_DESCRIPTION = {
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
}
_PREFIX = "https://raw.githubusercontent.com/UniversalDependencies/"
_UD_DATASETS = {
    "af_afribooms": {
        "train": "UD_Afrikaans-AfriBooms/master/af_afribooms-ud-train.conllu",
        "dev": "UD_Afrikaans-AfriBooms/master/af_afribooms-ud-dev.conllu",
        "test": "UD_Afrikaans-AfriBooms/master/af_afribooms-ud-test.conllu",
    },
    "akk_pisandub": {
        "test": "UD_Akkadian-PISANDUB/master/akk_pisandub-ud-test.conllu",
    },
    "akk_riao": {
        "test": "UD_Akkadian-RIAO/master/akk_riao-ud-test.conllu",
    },
    "aqz_tudet": {
        "test": "UD_Akuntsu-TuDeT/master/aqz_tudet-ud-test.conllu",
    },
    "sq_tsa": {
        "test": "UD_Albanian-TSA/master/sq_tsa-ud-test.conllu",
    },
    "am_att": {
        "test": "UD_Amharic-ATT/master/am_att-ud-test.conllu",
    },
    "grc_perseus": {
        "train": "UD_Ancient_Greek-Perseus/master/grc_perseus-ud-train.conllu",
        "dev": "UD_Ancient_Greek-Perseus/master/grc_perseus-ud-dev.conllu",
        "test": "UD_Ancient_Greek-Perseus/master/grc_perseus-ud-test.conllu",
    },
    "grc_proiel": {
        "train": "UD_Ancient_Greek-PROIEL/master/grc_proiel-ud-train.conllu",
        "dev": "UD_Ancient_Greek-PROIEL/master/grc_proiel-ud-dev.conllu",
        "test": "UD_Ancient_Greek-PROIEL/master/grc_proiel-ud-test.conllu",
    },
    "apu_ufpa": {
        "test": "UD_Apurina-UFPA/master/apu_ufpa-ud-test.conllu",
    },
    "ar_nyuad": {
        "train": "UD_Arabic-NYUAD/master/ar_nyuad-ud-train.conllu",
        "dev": "UD_Arabic-NYUAD/master/ar_nyuad-ud-dev.conllu",
        "test": "UD_Arabic-NYUAD/master/ar_nyuad-ud-test.conllu",
    },
    "ar_padt": {
        "train": "UD_Arabic-PADT/master/ar_padt-ud-train.conllu",
        "dev": "UD_Arabic-PADT/master/ar_padt-ud-dev.conllu",
        "test": "UD_Arabic-PADT/master/ar_padt-ud-test.conllu",
    },
    "ar_pud": {
        "test": "UD_Arabic-PUD/master/ar_pud-ud-test.conllu",
    },
    "hy_armtdp": {
        "train": "UD_Armenian-ArmTDP/master/hy_armtdp-ud-train.conllu",
        "dev": "UD_Armenian-ArmTDP/master/hy_armtdp-ud-dev.conllu",
        "test": "UD_Armenian-ArmTDP/master/hy_armtdp-ud-test.conllu",
    },
    "aii_as": {
        "test": "UD_Assyrian-AS/master/aii_as-ud-test.conllu",
    },
    "bm_crb": {
        "test": "UD_Bambara-CRB/master/bm_crb-ud-test.conllu",
    },
    "eu_bdt": {
        "train": "UD_Basque-BDT/master/eu_bdt-ud-train.conllu",
        "dev": "UD_Basque-BDT/master/eu_bdt-ud-dev.conllu",
        "test": "UD_Basque-BDT/master/eu_bdt-ud-test.conllu",
    },
    "be_hse": {
        "train": "UD_Belarusian-HSE/master/be_hse-ud-train.conllu",
        "dev": "UD_Belarusian-HSE/master/be_hse-ud-dev.conllu",
        "test": "UD_Belarusian-HSE/master/be_hse-ud-test.conllu",
    },
    "bho_bhtb": {
        "test": "UD_Bhojpuri-BHTB/master/bho_bhtb-ud-test.conllu",
    },
    "br_keb": {
        "test": "UD_Breton-KEB/master/br_keb-ud-test.conllu",
    },
    "bg_btb": {
        "train": "UD_Bulgarian-BTB/master/bg_btb-ud-train.conllu",
        "dev": "UD_Bulgarian-BTB/master/bg_btb-ud-dev.conllu",
        "test": "UD_Bulgarian-BTB/master/bg_btb-ud-test.conllu",
    },
    "bxr_bdt": {
        "train": "UD_Buryat-BDT/master/bxr_bdt-ud-train.conllu",
        "test": "UD_Buryat-BDT/master/bxr_bdt-ud-test.conllu",
    },
    "yue_hk": {
        "test": "UD_Cantonese-HK/master/yue_hk-ud-test.conllu",
    },
    "ca_ancora": {
        "train": "UD_Catalan-AnCora/master/ca_ancora-ud-train.conllu",
        "dev": "UD_Catalan-AnCora/master/ca_ancora-ud-dev.conllu",
        "test": "UD_Catalan-AnCora/master/ca_ancora-ud-test.conllu",
    },
    "zh_cfl": {
        "test": "UD_Chinese-CFL/master/zh_cfl-ud-test.conllu",
    },
    "zh_gsd": {
        "train": "UD_Chinese-GSD/master/zh_gsd-ud-train.conllu",
        "dev": "UD_Chinese-GSD/master/zh_gsd-ud-dev.conllu",
        "test": "UD_Chinese-GSD/master/zh_gsd-ud-test.conllu",
    },
    "zh_gsdsimp": {
        "train": "UD_Chinese-GSDSimp/master/zh_gsdsimp-ud-train.conllu",
        "dev": "UD_Chinese-GSDSimp/master/zh_gsdsimp-ud-dev.conllu",
        "test": "UD_Chinese-GSDSimp/master/zh_gsdsimp-ud-test.conllu",
    },
    "zh_hk": {
        "test": "UD_Chinese-HK/master/zh_hk-ud-test.conllu",
    },
    "zh_pud": {
        "test": "UD_Chinese-PUD/master/zh_pud-ud-test.conllu",
    },
    "ckt_hse": {
        "test": "UD_Chukchi-HSE/master/ckt_hse-ud-test.conllu",
    },
    "lzh_kyoto": {
        "train": "UD_Classical_Chinese-Kyoto/master/lzh_kyoto-ud-train.conllu",
        "dev": "UD_Classical_Chinese-Kyoto/master/lzh_kyoto-ud-dev.conllu",
        "test": "UD_Classical_Chinese-Kyoto/master/lzh_kyoto-ud-test.conllu",
    },
    "cop_scriptorium": {
        "train": "UD_Coptic-Scriptorium/master/cop_scriptorium-ud-train.conllu",
        "dev": "UD_Coptic-Scriptorium/master/cop_scriptorium-ud-dev.conllu",
        "test": "UD_Coptic-Scriptorium/master/cop_scriptorium-ud-test.conllu",
    },
    "hr_set": {
        "train": "UD_Croatian-SET/master/hr_set-ud-train.conllu",
        "dev": "UD_Croatian-SET/master/hr_set-ud-dev.conllu",
        "test": "UD_Croatian-SET/master/hr_set-ud-test.conllu",
    },
    "cs_cac": {
        "train": "UD_Czech-CAC/master/cs_cac-ud-train.conllu",
        "dev": "UD_Czech-CAC/master/cs_cac-ud-dev.conllu",
        "test": "UD_Czech-CAC/master/cs_cac-ud-test.conllu",
    },
    "cs_cltt": {
        "train": "UD_Czech-CLTT/master/cs_cltt-ud-train.conllu",
        "dev": "UD_Czech-CLTT/master/cs_cltt-ud-dev.conllu",
        "test": "UD_Czech-CLTT/master/cs_cltt-ud-test.conllu",
    },
    "cs_fictree": {
        "train": "UD_Czech-FicTree/master/cs_fictree-ud-train.conllu",
        "dev": "UD_Czech-FicTree/master/cs_fictree-ud-dev.conllu",
        "test": "UD_Czech-FicTree/master/cs_fictree-ud-test.conllu",
    },
    "cs_pdt": {
        "train": "UD_Czech-PDT/master/cs_pdt-ud-train.conllu",
        "dev": "UD_Czech-PDT/master/cs_pdt-ud-dev.conllu",
        "test": "UD_Czech-PDT/master/cs_pdt-ud-test.conllu",
    },
    "cs_pud": {
        "test": "UD_Czech-PUD/master/cs_pud-ud-test.conllu",
    },
    "da_ddt": {
        "train": "UD_Danish-DDT/master/da_ddt-ud-train.conllu",
        "dev": "UD_Danish-DDT/master/da_ddt-ud-dev.conllu",
        "test": "UD_Danish-DDT/master/da_ddt-ud-test.conllu",
    },
    "nl_alpino": {
        "train": "UD_Dutch-Alpino/master/nl_alpino-ud-train.conllu",
        "dev": "UD_Dutch-Alpino/master/nl_alpino-ud-dev.conllu",
        "test": "UD_Dutch-Alpino/master/nl_alpino-ud-test.conllu",
    },
    "nl_lassysmall": {
        "train": "UD_Dutch-LassySmall/master/nl_lassysmall-ud-train.conllu",
        "dev": "UD_Dutch-LassySmall/master/nl_lassysmall-ud-dev.conllu",
        "test": "UD_Dutch-LassySmall/master/nl_lassysmall-ud-test.conllu",
    },
    "en_esl": {
        "train": "UD_English-ESL/master/en_esl-ud-train.conllu",
        "dev": "UD_English-ESL/master/en_esl-ud-dev.conllu",
        "test": "UD_English-ESL/master/en_esl-ud-test.conllu",
    },
    "en_ewt": {
        "train": "UD_English-EWT/master/en_ewt-ud-train.conllu",
        "dev": "UD_English-EWT/master/en_ewt-ud-dev.conllu",
        "test": "UD_English-EWT/master/en_ewt-ud-test.conllu",
    }
}

class UniversaldependenciesConfig(datasets.BuilderConfig):
    """BuilderConfig for Universal dependencies"""

    def __init__(self, data_url, citation, url, text_features, **kwargs):
        """

        Args:
            text_features: `dict[string, string]`, map from the name of the feature
        dict for each text field to the name of the column in the tsv file
            label_column:
            label_classes
            **kwargs: keyword arguments forwarded to super.
        """
        super(UniversaldependenciesConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.text_features = text_features
        self.data_url = data_url
        self.citation = citation
        self.url = url


class Universaldependencies(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.1.0")
    BUILDER_CONFIGS = [
        UniversaldependenciesConfig(
            name=name,
            description=_DESCRIPTIONS[name.split(".")[0]],
            citation=_CITATIONS[name.split(".")[0]],
            text_features=_TEXT_FEATURES[name.split(".")[0]],
            data_url=_DATA_URLS[name.split(".")[0]],
            url=_URLS[name.split(".")[0]],
        )
        for name in _NAMES
    ]

    def _info(self):
        # info

    def _generate_examples(self, filepath):
        # parsing
