---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- ar
licenses:
- gpl-2.0
multilinguality:
- monolingual
size_categories:
- n<1K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
- other-diacritics-prediction
paperswithcode_id: null
pretty_name: Tashkeela
---

# Dataset Card for Tashkeela

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

- **Homepage:** [Tashkeela](https://sourceforge.net/projects/tashkeela/)
- **Repository:** [Tashkeela](https://sourceforge.net/projects/tashkeela/)
- **Paper:** [Tashkeela: Novel corpus of Arabic vocalized texts, data for auto-diacritization systems](https://www.sciencedirect.com/science/article/pii/S2352340917300112)
- **Point of Contact:** [Taha Zerrouki](mailto:t_zerrouki@esi.dz)

### Dataset Summary

It contains 75 million of fully vocalized words mainly
97 books from classical and modern Arabic language.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The dataset is based on Arabic.

## Dataset Structure

### Data Instances

```
{'book': 'zip://Tashkeela-arabic-diacritized-text-utf8-0.3/texts.txt/msa/al-kalema.org/أشكال-التجارب-في-مَثَل-الزارع.htm.txt::https://sourceforge.net/projects/tashkeela/files/latest/download',
 'text': 'الكلمة\n\n\nصفحه اصلی\nاشترك\nالكتاب المقدس\nجميع المقالات\nالترتيب بالموضوع\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nهذا المقال على نسخة PDF\n\n\nأشكال التجارب في مَثَل الزارع\n\n\tقد رأينا في مقال " \nوسائل واشكال التجارب" الأشكال التي من الممكن أن تتخذها التجارب (وخاصة الاختبارات التي تأتي من خلال الآلام والاضطهاد وأشراك إطاعة شهوات الإنسان العتيق، الجسد)، نستطيع أيضاً أن نرى هذه الأقسام عاملة في مثال الزارع. هناك مجموعتين في مثال الزارع أنه برغم من سماعهم واستقبالهم للكلمة، إلا أنهم لم يجلبوا ثماراً. والسؤال هو لماذا؟\n\n1. التجارب في القسم الثاني من مثال الزارع\n\nفيما يخص القسم الثاني من مثال الزارع، تخبرنا عنها متى 13: 20- 21 ولوقا 8: 13 \nمتى 13: 20- 21\n"  وَالْمَزْرُوعُ عَلَى الأَمَاكِنِ الْمُحْجِرَةِ هُوَ الَّذِي يَسْمَعُ الْكَلِمَةَ، وَحَالاً يَقْبَلُهَا بِفَرَحٍ،   وَلكِنْ لَيْسَ لَهُ أَصْلٌ فِي ذَاتِهِ، بَلْ هُوَ إِلَى حِينٍ. فَإِذَا حَدَثَ ضِيقٌ أَوِ اضْطِهَادٌ مِنْ أَجْلِ الْكَلِمَةِ فَحَالاً يَعْثُرُ."\nلوقا 8: 13\n"  وَالَّذِينَ عَلَى الصَّخْرِ هُمُ الَّذِينَ مَتَى سَمِعُوا يَقْبَلُونَ الْكَلِمَةَ بِفَرَحٍ، وَهؤُلاَءِ لَيْسَ لَهُمْ أَصْلٌ، فَيُؤْمِنُونَ إِلَى حِينٍ، وَفِي وَقْتِ التَّجْرِبَةِ يَرْتَدُّونَ."\n\nكما نرى، الناس في هذا القسم سمعوا الكلمة وحالاً قبلوها بفرح! بمعنى آخر، لقد كانوا متحمسين جداً تجاه الكلمة. ثم جاءت التجارب والاختبارات في شكل ضيق واضطهاد من أجل الكلمة، أي أنه بسبب الكلمة، اضطهد هؤلاء الناس. وعندئذ توقفوا. عوضاً عن أن يحفظوا ويتمسكوا بالكلمة التي قد حدث واستقبلوها بفرح، تراجعوا وسقطوا بعيداً، إن كنت مؤمناً صغيراً مليء بالحماسة تجاه الله، وبالرغم من أنه قد يبدو أنه لا يوجد شيطان من حولك، فهذا لن يستمر إلى الأبد. فالتجارب والاختبارات آتية. ستحتاج إلى أن تحفظ وتتمسك بالإيمان وبالكلمة التي قد حدث واستقبلتها بفرح. كما تقول لنا الكلمة:\nعبرانيين 10: 35- 39\n"  فَلاَ تَطْرَحُوا ثِقَتَكُمُ الَّتِي لَهَا مُجَازَاةٌ عَظِيمَةٌ.   لأَنَّكُمْ تَحْتَاجُونَ إِلَى الصَّبْرِ، حَتَّى إِذَا صَنَعْتُمْ مَشِيئَةَ اللهِ تَنَالُونَ الْمَوْعِدَ.   لأَنَّهُ بَعْدَ قَلِيل جِدًّا «سَيَأْتِي الآتِي وَلاَ يُبْطِئُ.   أَمَّا الْبَارُّ فَبِالإِيمَانِ يَحْيَا، وَإِنِ ارْتَدَّ لاَ تُسَرُّ بِهِ نَفْسِي».   وَأَمَّا نَحْنُ فَلَسْنَا مِنَ الارْتِدَادِ لِلْهَلاَكِ، بَلْ مِنَ الإِيمَانِ لاقْتِنَاءِ النَّفْسِ."\n\nوالضيق قد يأخذ أشكالاً عديدة. رأيت أناساً يسقطون، تاركين الإيمان لأن آبائهم أو أقاربهم وأصدقائهم قد عارضوهم ورفضوهم بسبب إيمانهم. بالطبع قد يأخذ الاضطهاد أشكالاً أكثر من ذلك أيضاً، مثل أن تلقى في سجن أو أن تعذب لأجل إيمانك. قد يسبب الموت كذلك،  كما حدث مع اسطفانوس ويعقوب أخو يوحنا. وتقول الكلمة من أجلك ومن أجل كل الذين حوكموا:\nرومية 16: 19- 20\n"  لأَنَّ طَاعَتَكُمْ ذَاعَتْ إِلَى الْجَمِيعِ، فَأَفْرَحُ أَنَا بِكُمْ، وَأُرِيدُ أَنْ تَكُونُوا حُكَمَاءَ لِلْخَيْرِ وَبُسَطَاءَ لِلشَّرِّ.  وَإِلهُ السَّلاَمِ سَيَسْحَقُ الشَّيْطَانَ تَحْتَ أَرْجُلِكُمْ سَرِيعًا."\nو بطرس الأولى 5: 8- 10\n" اُصْحُوا وَاسْهَرُوا. لأَنَّ إِبْلِيسَ خَصْمَكُمْ كَأَسَدٍ زَائِرٍ، يَجُولُ مُلْتَمِسًا مَنْ يَبْتَلِعُهُ هُوَ.  فَقَاوِمُوهُ، رَاسِخِينَ فِي الإِيمَانِ، عَالِمِينَ أَنَّ نَفْسَ هذِهِ الآلاَمِ تُجْرَى عَلَى إِخْوَتِكُمُ الَّذِينَ فِي الْعَالَمِ.  وَإِلهُ كُلِّ نِعْمَةٍ الَّذِي دَعَانَا إِلَى مَجْدِهِ الأَبَدِيِّ فِي الْمَسِيحِ يَسُوعَ، بَعْدَمَا تَأَلَّمْتُمْ يَسِيرًا، هُوَ يُكَمِّلُكُمْ، وَيُثَبِّتُكُمْ، وَيُقَوِّيكُمْ، وَيُمَكِّنُكُمْ."\n\nتمسك بالإيمان حتى النهاية. ضع حياتك ووضعك بين يدي الله وكن مستعداً لمواجهة أي شيء قد يحدث، أجل وحتى السخرية والعذاب. الله معك، سيقويك وسيعينك تماماً مثلما فعل مع يسوع في بستان جسثيماني. وتماماً مثلما فعل مع بولس في السجن عندما اضطهد من قِبَل اليهود (أعمال الرسل 23: 11). وكما قال بولس  في كورنثوس الثانية 1: 7:" عَالِمِينَ أَنَّكُمْ كَمَا أَنْتُمْ شُرَكَاءُ فِي الآلاَمِ، كَذلِكَ فِي التَّعْزِيَةِ أَيْضًا." فالعزاء الآتي من الله يوازن أي سخرية أو أي عذاب قد يأتي إلينا من أي إنسان.\n\n2. التجارب في القسم الثالث من مثال الزارع\n\nبخصوص القسم الثالث من مثال الزارع، فنقرأ عنه في مرقس 4: 18- 19\n\n"  وَهؤُلاَءِ هُمُ الَّذِينَ زُرِعُوا بَيْنَ الشَّوْكِ: هؤُلاَءِ هُمُ الَّذِينَ يَسْمَعُونَ الْكَلِمَةَ،   وَهُمُومُ هذَا الْعَالَمِ وَغُرُورُ الْغِنَى وَشَهَوَاتُ سَائِرِ الأَشْيَاءِ تَدْخُلُ وَتَخْنُقُ الْكَلِمَةَ فَتَصِيرُ بِلاَ ثَمَرٍ."\nو لوقا 8: 14\n"  وَالَّذِي سَقَطَ بَيْنَ الشَّوْكِ هُمُ الَّذِينَ يَسْمَعُونَ، ثُمَّ يَذْهَبُونَ فَيَخْتَنِقُونَ مِنْ هُمُومِ الْحَيَاةِ وَغِنَاهَا وَلَذَّاتِهَا، وَلاَ يُنْضِجُونَ ثَمَرًا."\n\nهؤلاء قد سمعوا الكلمة وفهموها ولكنهم صاروا بلا ثمر، وما هو السبب؟ السبب هو لأنهم تركوا أبواب قلوبهم مفتوحة لأشواك "  وَهُمُومُ هذَا الْعَالَمِ وَغُرُورُ الْغِنَى وَشَهَوَاتُ سَائِرِ الأَشْيَاءِ" (مرقس 4: 19)، والتي تدخل فتخنق الكلمة، كما رأينا يعقوب دائماً ما يقول:\nيعقوب 1: 13- 15\n"  لاَ يَقُلْ أَحَدٌ إِذَا جُرِّبَ: «إِنِّي أُجَرَّبُ مِنْ قِبَلِ اللهِ»، لأَنَّ اللهَ غَيْرُ مُجَرَّبٍ بِالشُّرُورِ، وَهُوَ لاَ يُجَرِّبُ أَحَدًا.   وَلكِنَّ كُلَّ وَاحِدٍ يُجَرَّبُ إِذَا انْجَذَبَ وَانْخَدَعَ مِنْ شَهْوَتِهِ.   ثُمَّ الشَّهْوَةُ إِذَا حَبِلَتْ تَلِدُ خَطِيَّةً، وَالْخَطِيَّةُ إِذَا كَمَلَتْ تُنْتِجُ مَوْتًا."\nوتيموثاوس الأولى 6: 9 تقول لنا\n" وَأَمَّا الَّذِينَ يُرِيدُونَ أَنْ يَكُونُوا أَغْنِيَاءَ، فَيَسْقُطُونَ فِي تَجْرِبَةٍ وَفَخٍّ وَشَهَوَاتٍ كَثِيرَةٍ غَبِيَّةٍ وَمُضِرَّةٍ، تُغَرِّقُ النَّاسَ فِي الْعَطَبِ وَالْهَلاَكِ."\n\nيجب أن نلاحظ شيئاً هنا: أن تأثير هموم الحياة هو نفس التأثير الذي لتجارب الغنى وشهوات الأشياء الأخرى. فهموم الحياة أيضاً لا تجلب الثمار، إذاً فإن اردت أن تكون مسيحياً مثمراً، أي مسيحي حقيقي وليس فقط مسيحي اسمي، فيجب عليك أن تزيل أشواك الهموم والغنى وملذات الحياة وأن تمنعهم من العودة مرة أخرى. تحتاج إلى أن تفعل شيئاً، تحتاج إلى أن تتغير والله سيعينك في هذا إن كنت حقاً تريده. التجارب في القسم الثالث من مثال الزارع لا تأتي من خلال الاضطهاد والآلام عن طريق الشيطان. ولكن هنا تأخذ التجارب صوراً أكثر مكراً والتي مع هذا تتطلب مقاومتنا. الاهتمام بما يهتم به هذا العالم ("هموم هذا العالم")، الرغبة في الغنى  أو اشتهاء الأشياء الأخرى هي أمور خطيرة جداً. إنها أشواك يجب إزالتها. كما رأينا بولس يقول:\nرومية 13: 14\n"  بَلِ الْبَسُوا الرَّبَّ يَسُوعَ الْمَسِيحَ، وَلاَ تَصْنَعُوا تَدْبِيرًا لِلْجَسَدِ لأَجْلِ الشَّهَوَاتِ."\n\n" لاَ تَصْنَعُوا تَدْبِيرًا لِلْجَسَدِ" والتي تعني أنه يجب علينا أن لا نهتم بالجسد وشهواته. ولكن عوضاً عن ذلك ينبغي لنا أن نطعم أنفسنا بلبن الكلمة الصافي الذي ننمو بواستطه (بطرس الأولى 2: 2).\n\n\nتاسوس كيولاشوجلو'}
```

### Data Fields

- `book` (str): Book filename.
- `text` (str): Text of the book.

### Data Splits

The dataset is not split. 

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

[More Information Needed]

#### Initial Data Collection and Normalization

The Modern Standard Arabic texts crawled from the Internet.

#### Who are the source language producers?

Websites.

### Annotations

The dataset does not contain any additional annotations.

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

[GNU General Public License, version 2 (GPLv2)](https://opensource.org/licenses/GPL-2.0).

### Citation Information

The dataset was published on this [paper](https://www.sciencedirect.com/science/article/pii/S2352340917300112#!):
```
@article{zerrouki2017tashkeela,
  title={Tashkeela: Novel corpus of Arabic vocalized texts, data for auto-diacritization systems},
  author={Zerrouki, Taha and Balla, Amar},
  journal={Data in brief},
  volume={11},
  pages={147},
  year={2017},
  publisher={Elsevier}
}
```

### Contributions

Thanks to [@zaidalyafeai](https://github.com/zaidalyafeai) for adding this dataset.