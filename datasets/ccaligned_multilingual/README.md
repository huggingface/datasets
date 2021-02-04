---
annotations_creators: []
language_creators:
- found
languages: []
licenses:
- unknown
multilinguality:
- translation
size_categories:
- unknown
source_datasets: []
task_categories:
- other
task_ids:
- other-other-translation
---

# Dataset Card for ccaligned_multilingual

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

- **Homepage:** http://www.statmt.org/cc-aligned/
- **Repository:** [Needs More Information]
- **Paper:** https://www.aclweb.org/anthology/2020.emnlp-main.480.pdf
- **Leaderboard:** [Needs More Information]
- **Point of Contact:** [Needs More Information]

### Dataset Summary

CCAligned consists of parallel or comparable web-document pairs in 137 languages aligned with English. These web-document pairs were constructed by performing language identification on raw web-documents, and ensuring corresponding language codes were corresponding in the URLs of web documents. This pattern matching approach yielded more than 100 million aligned documents paired with English. Recognizing that each English document was often aligned to mulitple documents in different target language, we can join on English documents to obtain aligned documents that directly pair two non-English documents (e.g., Arabic-French). This corpus was created from 68 Commoncrawl Snapshots

### Supported Tasks and Leaderboards

[Needs More Information]

### Languages

The text in the dataset is in (137) multiple languages aligned with english.

## Dataset Structure

### Data Instances

An instance of `documents` type:

```
{'Domain': 'cjtaisangha.com', 'Source_Content': 'Activities|Search|Search|Home|News|News for education|Our Club|B.A. Students|PGD Students|M.A. Students|M.Phil Studensts|Ph.D. Students|List of CJ Students|Dhamma|MP3|MP-4|Activities|CJTS.Members|E-Books|Ceylon Journey News|SGS Libaray|book list|English|Thai|Shan|Myanmar|Download|Gallery|Contact us|Donate|Links|Skip to content|Home|News|News for education|Our Club|B.A. Students|PGD Students|M.A. Students|M.Phil Studensts|Ph.D. Students|List of CJ Students|Dhamma|MP3|MP-4|Activities|CJTS.Members|E-Books|Ceylon Journey News|SGS Libaray|book list|English|Thai|Shan|Myanmar|Download|Gallery|Contact us|Donate|Links|Activities|Sorry, this entry is only available in Shan.|(Shan) သွၵ်ႈႁႃ|Search for:|Search|English:|English|Shan|Buddha|Calender|December 2019|M|T|W|T|F|S|S|« Sep|1|2 3 4 5 6 7 8|9 10 11 12 13 14 15|16 17 18 19 20 21 22|23 24 25 26 27 28 29|30 31|Cjtaisangha’s facebook|(Shan) ပပ်ႉၸဝ်ႈၶူး Dr. မႁေႃသထႃလင်ၵႃရႃၽိဝမ်သ|(Shan)|Recent Posts|(Shan) ႁၢင်ႈၽၢင်မၢႆတွင်း ႁပ်ႉၸုမ်ႈၶူး M.A & P.G.D တီႈၸၼ်ႉၸွမ် ၵေႇလၼိယ လႄႈ ပၢင်ႁူပ်ႉထူပ်းလုၵ်ႈႁဵၼ်းသင်ႇၶတႆး မိူင်းသီႇႁူဝ်ႇ|(Shan) ပွင်ႇလႅင်းထိုင် ၽူႈႁၵ်ႉလိၵ်ႈလၢႆးပၢႆပႄႇႁဝ်းၶဝ်တင်းသဵင်ႈတီႈၶႃႈ ဢမ်ႇပေႃးႁိုင်ပေႃးၼၢၼ်း ဢၼ်တေပဵၼ်ပပ်ႉမၢႆတွင်း ပီၵွၼ်းၶမ်း (50) ပီတဵမ်|(Shan) ယွၼ်းမူႇလိၵ်ႈၶၢဝ်းတၢင်းသီႇႁူဝ်ႇ မၢႆ-21 ၊ ပီ – 2019 ထိုင် ၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉႁဝ်းၶဝ်တင်းသဵင်ႈ|(Shan) လုၵ်ႈႁဵၼ်းသင်ႇၶတႆး လႆႈၸုမ်ႈ M.A တီႈၸၼ်ႉၸွမ် Buddhist & Pāli Unversity မိူင်းသီႇရိလင်းၵႃ၊ သီႇၸဝ်ႈ|Congraduration to you all|Recent Commens|Resent Ports|September 2019|August 2019|June 2019|February 2019|December 2018|November 2018|October 2018|September 2018|August 2018|July 2018|May 2018|April 2018|March 2018|December 2017|November 2017|October 2017|September 2017|August 2017|July 2017|June 2017|May 2017|(Shan) မူႇၵေႃ|Activities|Local News|News|Uncategorized|World News|Meta|Log in|Entries RSS|Comments RSS|WordPress.org|Visiter|Copyright 2015 © 2017 Cjtaisangha.com |Makutarama Temple 42/15 Reservoir Road, Dematagoda, Colombo 09, Sri Lanka Tel: 009 411 2662488 Email: Lankajourney@yahoo.co.uk |Ribosome by GalussoThemes.com|Powered by WordPress|', 'Source_URL': 'http://www.cjtaisangha.com/en/activities/', 'Target_Content': 'ၵၢၼ်တူင်ႉၼိုင်|Search|Search|ၼႃႈႁူဝ်ႁႅၵ်ႈ|ၶၢဝ်ႇၵူႈလွင်ႈ|ၶၢဝ်ႇလွင်ႈၵၢၼ်ႁဵၼ်း|ၽႂ်ပဵၼ်ၽႂ်ၼႂ်းႁဝ်းႁႃး|လုၵ်ႈႁဵၼ်းၸၼ်ႉ BA|လုၵ်ႈႁဵၼ်းၸၼ်ႉ PGD|လုၵ်ႈႁဵၼ်းၸၼ်ႉ MA|လုၵ်ႈႁဵၼ်းၸၼ်ႉ M.Phil|လုၵ်ႈႁဵၼ်းၸၼ်ႉ PhD|သဵၼ်ႈမၢႆလုၵ်ႈႁဵၼ်းၵူႈပီပီ|ထမ်ႇမ|MP3|MP-4|ၵၢၼ်တူင်ႉၼိုင်|ၸုမ်းၽူႈပွင်ၵၢၼ်|ႁွင်ႈပပ်ႉလိၵ်ႈ|ၶၢဝ်းတၢင်းသီႇႁူဝ်ႇ|ႁူင်းတူၺ်းလိၵ်ႈ SGS|သဵၼ်ႈမၢႆပပ်ႉ|ဢင်းၵိတ်ႉ|ၽၢႆႇထႆး|ၽၢႆႇတႆး|ၽၢႆႇမၢၼ်ႈ|တႃႇလုတ်ႇလူင်း|ၶႅပ်းႁၢင်ႈ|တီႈၵပ်းသိုပ်ႇ|ၵပ်းသိုပ်ႇလူႇတၢၼ်း|လိင်ႉ|Skip to content|ၼႃႈႁူဝ်ႁႅၵ်ႈ|ၶၢဝ်ႇၵူႈလွင်ႈ|ၶၢဝ်ႇလွင်ႈၵၢၼ်ႁဵၼ်း|ၽႂ်ပဵၼ်ၽႂ်ၼႂ်းႁဝ်းႁႃး|လုၵ်ႈႁဵၼ်းၸၼ်ႉ BA|လုၵ်ႈႁဵၼ်းၸၼ်ႉ PGD|လုၵ်ႈႁဵၼ်းၸၼ်ႉ MA|လုၵ်ႈႁဵၼ်းၸၼ်ႉ M.Phil|လုၵ်ႈႁဵၼ်းၸၼ်ႉ PhD|သဵၼ်ႈမၢႆလုၵ်ႈႁဵၼ်းၵူႈပီပီ|ထမ်ႇမ|MP3|MP-4|ၵၢၼ်တူင်ႉၼိုင်|ၸုမ်းၽူႈပွင်ၵၢၼ်|ႁွင်ႈပပ်ႉလိၵ်ႈ|ၶၢဝ်းတၢင်းသီႇႁူဝ်ႇ|ႁူင်းတူၺ်းလိၵ်ႈ SGS|သဵၼ်ႈမၢႆပပ်ႉ|ဢင်းၵိတ်ႉ|ၽၢႆႇထႆး|ၽၢႆႇတႆး|ၽၢႆႇမၢၼ်ႈ|တႃႇလုတ်ႇလူင်း|ၶႅပ်းႁၢင်ႈ|တီႈၵပ်းသိုပ်ႇ|ၵပ်းသိုပ်ႇလူႇတၢၼ်း|လိင်ႉ|ၵၢၼ်တူင်ႉၼိုင်|မိူဝ်ႈဝၼ်းထိ 19-20 May 2018 ၼၼ်ႉ ၸဝ်ႈသြႃႇဝိၸယႃၽိပႃလ ပူင်သွၼ်ပၼ် ၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉ ဢၼ်မႃးႁဵၼ်းလိၵ်ႈ တီႈမိူင်းသီႇႁူဝ်ႇၼႆႉ၊ ၼင်ႇႁိုဝ် မိူဝ်းၼႃႈထႃႈပၢႆမႃး ပေႃႈတေမီးလွင်ႈ ယုမ်ႇတူဝ်ယုမ်ႇၸႂ်သေဢမ်ႇၵႃး ၼင်ႇႁိုဝ်ပေႃးတေ မီးလွင်ႈတူဝ်ႈတၼ်းလီ တွၼ်ႈတႃႇႁဵၼ်းလႆႈထိုင်ၸၼ်ႉသုင်သုင်ၼႆၼၼ်ႉလႄႈ ၸဝ်ႈသြႃႇဝိၸယႃၽိပႃလ ၸင်ႇလႆႈမီးၸႂ် မဵတ်ႉတႃႇယႂ်ႇၼိူဝ် ၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉပေႃးတေမီးလွင်ႈတၢင်းႁူႉတၢင်းႁၼ် ၼိူဝ်လိၵ်ႈလၢႆးပၢႆပႄႇၼႆသေ ပူင်သွၼ်ပၼ် လွၵ်းလၢႆးတႅမ်ႈလိၵ်ႈ M.Phil တီႈဝတ်ႉမၵုတႃႇရႃႇမ၊ ႁွင်ႈတူၺ်းလိၵ်ႈ ၸဝ်ႈၵၢင်းသိူဝ် ၵႂႃႇၼႆယူႇယဝ်ႉ။|တေလႆႈႁဵတ်းႁိုဝ် ဝႆႉဝၢင်းတူၼ်ႈထႅဝ်၊ တေလႆႈႁဵတ်းႁိုဝ်ၶပ်ႉလိၵ်ႈမႅၼ်ႈမႅၼ်ႈၸွမ်းပိူင်၊ တေလႆႈႁဵတ်းႁိုဝ်သႂ်ႇ Footnote , တေႁဵတ်းႁိုဝ် သႂ်ႇၽိုၼ်ဢိင် တႄႇၵႂႃႇၸိူဝ်းၼႆႉ တေလႆႈဝႃႈ ပၼ်တၢင်းႁူႉႁၼ် တၢင်းၼမ်တၢင်းလၢႆယူႇ။ ပဵၼ်ဢၼ်လီမၢႆ လီတွင်းဝႆႉတႄႉတႄႉယူႇယဝ်ႉ။|ၶၢဝ်းတၢင်းသီႇႁူဝ်ႇ|မိူဝ်ႈဝၼ်းထိ 12.04.2018 ၸဝ်ႈသြႃႇဝိၸယႃၽိပႃလ ဢွၼ်ႁူဝ် ၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉ လုၵ်ႈႁဵၼ်းသင်ႇၶတႆး ၊ မိူင်းသီႇႁူဝ်ႇ ၶပ်ႉပပ်ႉလိၵ်ႈ၊ ႁူင်းတူၺ်းလိၵ်ႈ ၸဝ်ႈၵၢင်းသိူဝ် ၶၢဝ်းတၢင်းတႄႇၶပ်ႉပပ်ႉလိၵ်ႈ တႄႇဝၼ်းထိ 10 – 20. 04 . 2018 ၼႆယူႇယဝ်ႉ။|ၸိူဝ်းပဵၼ်ၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉ ၸိူဝ်းမီးၶၢဝ်းယၢမ်းတူဝ်ႈတၼ်းၸိူဝ်းၼၼ်ႉ လႄႈ မၢင်ၸိူဝ်းၵေႃႈ တတ်းဢဝ်ၶၢဝ်းယၢမ်း ၼႂ်းၵႄႈဢမ်ႇတၼ်းၼၼ်ႉသေ မႃးၸွႆႈမႃးထႅမ် မိူၼ်ၼင်ႇဝႃႈ ႁူမ်ႈၵၼ်ၵိၼ်ၸင်ႇဝၢၼ် ႁူမ်ႈၵၼ်ႁၢမ်ၸင်ႇမဝ် ၼႆၼၼ်ႉ ယဝ်ႉ။ တွၼ်ႈတႃႇၼိုင်ႈပီၼိုင်ႈပီၼႆႉ ဢၼ်ပဵၼ်ပပ်ႉလိၵ်ႈ ဢင်းၵိတ်ႉ၊ တႆး ၊ ထႆး၊ မၢၼ်ႈ တႄႇၵႂႃႇၸိူဝ်းၼႆႉၵေႃႈ တိူဝ်းၼမ် မႃးတိၵ်းꧦ ၵူႈပီပီလႄႈ လႆႈ Update ပၼ်သဵၼ်ႈမၢႆမၼ်ႈယူႇ ၵူႈပီပီၼႆယဝ်ႉ။ ဢၼ်ၼမ်လိူဝ်ၼႆႉတႄႉ တေပဵၼ်ဢင်းၵိတ်ႉ ယဝ်ႉၶႃႈ၊ ယွၼ်ႉပိူဝ်ႈဝႃႈ ဢင်းၵိတ်ႉၼႆႉ ပဵၼ်လၵ်းထၢၼ် ၵၢၼ်ႁဵၼ်း တွၼ်ႈတႃႇ လုၵ်ႈႁဵၼ်းသင်ႇၶတႆး ၸိူဝ်းဢၼ်မႃး ၶိုၼ်ႈႁဵၼ်း လဵပ်ႈႁဵၼ်း ပႆၸွမ်းၶၢဝ်းတၢင်းသီႇႁူဝ်ႇၼႆႉ|ၼႆလႄႈ ၸဝ်ႈၶူးလူင် Prof. Dr. ၶမ်းမၢႆ ထမ်မသႃမိ ၸင်ႇဢွၼ်ႁူဝ်တႄႇတင်ႈ မႃးပၼ်ႁဝ်းၶႃႈ ၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉ ႁႂ်ႈပေႃးလႆႈတူၺ်းလႆႈ တွင်းလႆႈ ႁႃႈလႆႈၶေႃႈမုၼ်း ၵဵဝ်ႇလူၺ်ႈၵၢၼ်ႁဵၼ်း၊ ဢၼ်ပဵၼ် တၢင်းၸွႆႈထႅမ်လွင်ႈၵၢၼ်ႁဵၼ်းလႆႈ ငၢႆႈငၢႆႈၼႆၼၼ်ႉယူႇယဝ်ႉ၊ ၼႆလႄႈ ၸိူဝ်းပဵၼ်လုၵ်ႈၼွင်ႉၸဝ်ႈၶူးလူင်ၵေႃႈ ၸင်ႇလႆႈသိုပ်ႇ ထိင်းသိမ်း၊ သိုပ်ႇႁဵၼ်းၵၢၼ်ၵႂႃႇ ပၢၼ်သိုပ်ႇပၢၼ်ယူႇၶႃႈယဝ်ႉ။|မိူဝ်ႈဝၼ်းထိ 08.06.2017 ပၢင်ႁူပ်ႉထူပ်း ၸုမ်းဝႆႈၽြႃး ဢၼ်ၸဝ်ႈၶူး မုၼိဝရ (လၢႆးၶႃႈ) လႄႈ ၸဝ်ႈၶူး ၺႃၼဝရ (ၵျွၵ်းမႄး) ဢွၼ်ႁူဝ် တၵ်ႉၵႃသထႃး ဝဵင်းၵျွၵ်းမႄး၊ ဝဵင်းလၢႆးၶႃႈ လႄႈ သင်ႇၶတႆး မိူင်းသီႇႁူဝ်ႇ။|ယိူင်းၸူးလူႇတၢၼ်းပၼ် ၶိင်းသူၺ်ႇၵျွင်းဢၢႆႈၽူင်း ၼိုင်ႈလိူၼ်တဵမ် (AD. 1943-2017)|(ၽူႈဢၼ်လူႇတၢၼ်းယႂ်ႇလူင် ၼႂ်းၽႃႇသႃႇ၊ သႃႇသၼႃႇ၊ လႄႈ ၼႃႈယၵ ၵေႃလိၵ်ႈလၢႆးလႄႈ ၽင်ႈ|ငႄႈတႆး ဝဵင်းလိူဝ်ႇ) ဢၼ်သဵင်ႈၵႂႃႇ တဵမ်ၼိုင်ႈလိူၼ်သေ ၼၢႆးသူၺ်ႇၵျွင်းဢီႇသၢဝ် လႄႈ|လုၵ်ႈလၢၼ်တင်းသဵင်ႈ (မူႇၸေႈ၊ လႃႈသဵဝ်ႈ၊ တႃႈလိူဝ်ႇ၊ တႃႈၵုင်ႈ) လူႇတၢၼ်းၵၢပ်ႈသွမ်းဢေႃႈ။ (10/06/2017)|သွၵ်ႈႁႃ|Search for:|Search|ၽႃႇသႃႇတႆး:|English|Shan|ၿုၻ်ꩪၸဝ်ႈ|ပၵ်းယဵမ်ႈဝၼ်း|December 2019|M|T|W|T|F|S|S|« Sep|1|2 3 4 5 6 7 8|9 10 11 12 13 14 15|16 17 18 19 20 21 22|23 24 25 26 27 28 29|30 31|ၾဵတ်ႉၶၢဝ်းတၢင်းသီႇႁူဝ်ႇ|ပပ်ႉၸဝ်ႈၶူး Dr. မႁေႃသထႃလင်ၵႃရႃၽိဝမ်သ|ၶၢဝ်ႇမိူဝ်ႈလဵဝ်|ႁၢင်ႈၽၢင်မၢႆတွင်း ႁပ်ႉၸုမ်ႈၶူး M.A & P.G.D တီႈၸၼ်ႉၸွမ် ၵေႇလၼိယ လႄႈ ပၢင်ႁူပ်ႉထူပ်းလုၵ်ႈႁဵၼ်းသင်ႇၶတႆး မိူင်းသီႇႁူဝ်ႇ|ပွင်ႇလႅင်းထိုင် ၽူႈႁၵ်ႉလိၵ်ႈလၢႆးပၢႆပႄႇႁဝ်းၶဝ်တင်းသဵင်ႈတီႈၶႃႈ ဢမ်ႇပေႃးႁိုင်ပေႃးၼၢၼ်း ဢၼ်တေပဵၼ်ပပ်ႉမၢႆတွင်း ပီၵွၼ်းၶမ်း (50) ပီတဵမ်|ယွၼ်းမူႇလိၵ်ႈၶၢဝ်းတၢင်းသီႇႁူဝ်ႇ မၢႆ-21 ၊ ပီ – 2019 ထိုင် ၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉႁဝ်းၶဝ်တင်းသဵင်ႈ|လုၵ်ႈႁဵၼ်းသင်ႇၶတႆး လႆႈၸုမ်ႈ M.A တီႈၸၼ်ႉၸွမ် Buddhist & Pāli Unversity မိူင်းသီႇရိလင်းၵႃ၊ သီႇၸဝ်ႈ|သဵၼ်ႈမၢႆၸဝ်ႈပီႈၸဝ်ႈၼွင်ႉ ၸိူဝ်းဢွင်ႇပူၼ်ႉၸၼ်ႉလိၵ်ႈၼႂ်းပီ 2018|ၶေႃႈပၼ်တၢင်းၶႆႈၸႂ်|ႁွင်ႈၶၢဝ်ႇ|September 2019|August 2019|June 2019|February 2019|December 2018|November 2018|October 2018|September 2018|August 2018|July 2018|May 2018|April 2018|March 2018|December 2017|November 2017|October 2017|September 2017|August 2017|July 2017|June 2017|May 2017|မူႇၵေႃ|ၵၢၼ်တူင်ႉၼိုင်|ၶၢဝ်ႇၼႂ်းမိူင်း|News|Uncategorized|ၶၢဝ်ႇၼွၵ်ႈမိူင်း|Meta|Log in|Entries RSS|Comments RSS|WordPress.org|တူဝ်ၼပ်ႉၵူၼ်းမႃးယဵမ်ႈ|Copyright 2015 © 2017 Cjtaisangha.com |Makutarama Temple 42/15 Reservoir Road, Dematagoda, Colombo 09, Sri Lanka Tel: 009 411 2662488 Email: Lankajourney@yahoo.co.uk |Ribosome by GalussoThemes.com|Powered by WordPress|\n', 'Target_URL': 'http://www.cjtaisangha.com/activities/'}
```

An instance of `sentences` type:

```
{'LASER_similarity': 1.2734256982803345, 'Source_Sentence': '>>> PhD Students in 2018', 'Target_Sentence': '>>> လုၵ်ႈႁဵၼ်းၸၼ်ႉ Ph.D ၼႂ်းပီ 2018', 'from_english': True}
```

### Data Fields

For `documents` type:

- `Domain`: a `string` feature containing the domain.
- `Source_URL`: a `string` feature containing the source URL.
- `Source_Content`: a `string` feature containing the content on Source_URL.
- `Target_URL`: a `string` feature containing the target URL.
- `Target_Content`: a `string` feature containing the content on Target_URL.

For `sentences` type:

- `Source_Sentence`: a `string` feature containig the source sentence.
- `Target_Sentence`: a `string` feature containing the target sentence.
- `LASER_similarity`: a `float32` feature representing the LASER similarity score.
- `from_english`: a `bool` feature representing whether the source sentence is in English.


### Data Splits

[Needs More Information]

## Dataset Creation

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

[Needs More Information]

### Citation Information

@inproceedings{elkishky_ccaligned_2020,
 author = {El-Kishky, Ahmed and Chaudhary, Vishrav and Guzm{\'a}n, Francisco and Koehn, Philipp},
 booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP 2020)},
 month = {November},
 title = {{CCAligned}: A Massive Collection of Cross-lingual Web-Document Pairs},
 year = {2020}
 address = "Online",
 publisher = "Association for Computational Linguistics",
 url = "https://www.aclweb.org/anthology/2020.emnlp-main.480",
 doi = "10.18653/v1/2020.emnlp-main.480",
 pages = "5960--5969"
}