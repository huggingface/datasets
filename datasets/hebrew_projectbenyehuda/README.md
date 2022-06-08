---
annotations_creators:
- expert-generated
language_creators:
- found
languages:
- he
licenses:
- mit
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- language-modeling
- masked-language-modeling
paperswithcode_id: null
pretty_name: Hebrew Projectbenyehuda
---

# Dataset Card for Hebrew Projectbenyehuda

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

- **Homepage:** https://github.com/projectbenyehuda/public_domain_dump
- **Repository:** https://github.com/projectbenyehuda/public_domain_dump
- **Paper:** 
- **Leaderboard:**
- **Point of Contact:** 

### Dataset Summary

This repository contains a dump of thousands of public domain works in Hebrew, from Project Ben-Yehuda, in plaintext UTF-8 files, with and without diacritics (nikkud), and in HTML files. The pseudocatalogue.csv file is a list of titles, authors, genres, and file paths, to help you process the dump.

The Releases tab contains a downloadable ZIP archive of the full release. The git repo can be used to track individual file changes, or for incremenetal updates. In the ZIPs, each format (plaintext, plaintext stripped of diacritics, and HTML) has a ZIP file containing one directory per author, with all the author's works under that directory.

To request changes or improvements to this dump, file an issue against this repository.

All these works are in the public domain, so you are free to make any use of them, and do not need to ask for permission.

If you would like to give credit, please credit "Project Ben-Yehuda volunteers", and include a link to the site. We'd also love to hear about the uses you've made of this dump, as it encourages us to keep producing the dump. E-mail us with a brief description (and links, if/as appropriate) of your re-use, at editor@benyehuda.org.

There are 10078 files, 3181136 lines

Data Annotation: 

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

Hebrew

## Dataset Structure

### Data Instances

Sample:
```
{
  'id': 10,
  'url': 'https://raw.githubusercontent.com/projectbenyehuda/public_domain_dump/master/txt/p23/m10.txt',
  'title': 'חצי-נחמה',
  'authors': 'אחד העם',
  'translators': '',
  'original_language': '',
  'genre': 'מאמרים ומסות',
  'source_edition': '',
  'text': '\n\n\n\t\n\tחצי-נחמה\n\t\n\n\n\n1\n\nבין כל הצרות שנתחדשו עלינו בעת האחרונה תעשׂה ביחוד רושם מעציב בלב כל איש ישׂראל התחדשות ‘עלילת־הדם’. העלילה הנתעבה הזאת, בכל יָשנה, היתה ותהיה תמיד בעינינו כחדשה, ומימי הבינים ועד עתה תצטין בפעולתה החזקה על רוח עמנו, לא רק במקום המעשׂה, כי אם גם בארצות רחוקות שהגיעה אליהן השמועה.\n\nאמרתי: ‘על רוח עמנו’, כי אמנם רואה אני מקור החזיון הזה לא בסבּות חיצוניות, כי אם עמוק ברוח העם. בימי הבינים, שהיה כלל ישׂראל במקרים כאלה רגיל לחשוב עצמו כעומד במשפט ביחד עם אותם האומללים שעלה עליהם הגורל להיות כפּרותו, – יש מקום אמנם לראות בזה רק תוצאת הסכנה הגשמית הגדולה להכלל כולו, שהיתה כרוכה אז באמת בעקב כל עלילה כזו. גם לפני חמשים שנה, בימי מנוחה ושלוה, שעוררה עלילת דמשׂק רעש גדול כל־כך בארצות המערב, עדיין יש מקום לאמר, כי היתה בזה, להפך, יד הקנאה הגדולה לכבודם וזכויותיהם ששׂררה אז בלבות אחינו המערביים, אשר זה מעט יצאו מעבדות לחרות. אך בימינו אלה הרי מצד אחד אין הסכנה הגשמית גדולה עוד הרבה, ביחוד לקהלות רחוקות, ומצד אחר כבר הורגלנו לשמוע חרפתנו בקור רוח וקנאת כבודנו לא תאכלנו עוד, ואם בכל זאת גם עתה עודנו מתעוררים ומתנודדים בחזקה לשמע ‘עלילת־דם’, ורגש הכלל יתפרץ החוצה מכל עברים להשליך מעליו את החלאה הזאת, – אות הוא, כי לא הפחד ולא הכבוד החיצוני הם המניעים לזה, כי אם רוח העם הוא המרגיש פה את קלונו והוא זה המתעורר והמעורר; כי אעפ"י שבכל יתר הדברים כבר הביאונו צרותינו לאותו המצב שעליו אמר הנשׂיא החכם בימי קדם: ‘אין בשׂר המת מרגיש באיזמל’, – הנה פה אין ‘האיזמל’ חותך את ‘הבשׂר’ בלבד, כי אם עד הנפש יגע…\n\nאבל – ‘אין רע בלא טוב’, כלומר, בלא לקח טוב. גם הרע הגדול הזה שאנו עסוקים בו אינו ריק מלקח טוב, ואנחנו, אשר לא אדונים אנחנו לגורלנו וגם את הטוב גם את הרע נקבל מן החוץ שלא בטובתנו, ראוי לנו לבקש ברעותינו תמיד את התועלת הלמודית הצפונה בהן, והיתה לנו זאת, לפחות, חצי נחמה.\n\n\n\nאחד הכוחות היותר גדולים בחיי החברה הוא – ‘ההסכמה הכללית’. היו ימים שגם הפלוסופים ראו בהסכמה זו מופת נאמן על הדבר המוסכם ונתנו לה מקום בתוך שאר מופתיהם על מציאות האלהות. עתה אמנם יודעים הפלוסופים , שאין שקר ואין אולת אשר לא תוכל לבוא עליו ‘ההסכמה הכללית’, אם אך תנאי החיים נאותים לזה. אבל רק הפלוסופים יודעים זאת, ובעיני ההמון עוד גם עתה אין אַבטוֹריטט גדול מן ‘ההסכמה’: אם ‘כל העולם’ מאמינים שהדבר כן, בודאי כן הוא; ואם אני איני מבינו, אחרים מבינים; ואם אני רואה כעין סתירה לו, הרי ‘הכל’ רואים גם כן ואעפ"כ מאמינים, וכי חכם אני מכל העולם? – זה הוא בקירוב מהלך הרעיונות של האיש הפשוט, בדעת או בלי דעת ברורה, ומתוך כך הוא מסכים גם מצדו ונעשׂה בעצמו חלק מן ‘ההסכמה’.\n\nוכל־כך גדול כוח ‘ההסכמה’, עד שעל הרוב לא יוכל האדם למַלט נפשו מפעולתה גם כשהוא עצמו הוא ‘הדבר המוסכם’. אם ‘כל העולם’ אומרים על פלוני שגדול הוא בחכמה או ביראה, שיש בו מדה פלונית, טובה או רעה, – סופו להסכים לזה גם בעצמו, אע"פ שמתחלה לא מצא בנפשו אותו היתרון או החסרון שאחרים מיחסים לו. ולא זו בלבד אלא שההסכמה הזאת מצד ‘המוסכם’ עצמו פועלת מעט מעט על תכונת רוחו עד שמקרבתו באמת (או, לפחות, מולידה בו נטיה להתקרב) אל המצב ההוא שרואה בו ‘כל העולם’. על כן יזהירו הפדגוגים בצדק, לבלתי עורר את הילדים על מגרעותיהם המוסריות בראשית התפתחותן, וכל שכּן לבלתי יחס להם מגרעות שאין בהם, כי על ידי זה אפשר שנחזק בלבם את הראשונות ונוליד בם נטיה להאחרונות.\n\nואולם, הדבר מובן, כי ‘כל העולם’ אינו אחד לכל אחד. האדם רואה ‘עולמו’ רק באותה החברה שהוא חושב עצמו לחלק ממנה ורואה באישיה אנשים הקרובים לו מאיזה צד; אבל אין אדם חושב למאומה הסכמת אנשים שרוחם זרה לו לגמרי, שאינו מרגיש בנפשו שום יחס פנימי בינו ובינם. ככה אין האוֹרתוֹדוֹכּסים והמשׂכילים שלנו שׂמים לב כלל אלו להסכמתם של אלו, אף בדברים שאינם נוגעים לאמונה ודת, ושׂחקם ולעגם של אלו על אלו אינו עושׂה שום רושם בלבם של שניהם, לפי שכּל אחת משתי הכּתּות רואה את חברתה כאלו אינה. ואולם כשתנאי החיים מכריחים את בני הכתות השונות להמצא במשׂא ומתן תמידי זה עם זה והם מתרגלים לראות זה בזה קודם כל את האדם, – אז יתרחב ‘עולמם’ והשקפותיהם סובלות שנויים רבים על פי הסכמת ‘העולם’ במובנו החדש.\n\n\n\nלפיכך, בדורות שעברו, כשהיו אבותינו מאמינים בפשטו של ‘אתה בחרתנו’, לא היתה החרפּה שחרפום האומות פועלת כלל על טוהר נפשם פנימה. הם ידעו את ערכם ולא התפעלו עד מה מן ‘ההסכמה הכללית’ אשר מחוץ להם, בהיות כל חברת ‘המסכימים’ נחשבת בעיניהם למין מיוחד של בריות זרות להם ושונות מהם שנוי עצמי, בלי כל יחס וכל דמיון בינם ובינן. אז היה היהודי יכול לשמוע במנוחת לב כל המגרעות המוסריות והחטאים המעשׂיים שטפלה עליו הסכמת העמים, מבלי להרגיש בנפשו שום בושה או שפלוּת פנימית. כי מה לו ולמחשבות ‘הנכרים’ עליו ועל ערכּוֹ? לוּ רק יתנו לו לישב בשלוה! – אבל בדור הזה אין הדבר כן, עתה ‘עולמנו’ נתרחב הרבה, וההסכמה האירופּית פועלת עלינו בחזקה בכל ענפי החיים. ולפי שאין אנו מוציאים עוד את ‘הכל’ מן הכלל, לכן נתפעל בעל כרחנו ממה ש’הכל\' מוציאים אותנו מן הכלל, סופר אחד רוסי שאל באלו הימים בתמימוּת: אחר שכל העולם שׂונאים את היהודים, וכי אפשר לאמור, שכל העולם חייבים והיהודים זכאים? – ושאלה כזו מתגנבת עתה גם אל לב רבים מאחינו: וכי אפשר לאמור, שכל אותן התכונות הנשחתות והמעשׂים הרעים שכל העולם מיחס ליהודים אינם אלא ‘בדותא’?\n\nוהספק הזה, מכיון שנתעורר, מוצא לו מחיה בנקל באותם ההיקשים המוטעים ‘מן הפרט אל הכלל’ הרגילים מאד אצל המון בני האדם. הספור הידוע על דבר נוסע אחד, שבא לאחת הערים ונזדמן לאכסניא שהיה בה משרת כבד־פה, וכתב בפנקסו: בעיר פלונית משרתי האכסניות הם כבדי־פה, – הספור הזה מצייר בצורה של התוּל דרכי־ההגיון של ההמון ברוב משפטיו הכלליים. כל החזיונות הנראים באיזה דבר פרטי רגיל ההמון ליחס אל הכלל שהדבר ההוא מתחשב עליו לפי שמו התמידי, מבלי להתבונן, כי ‘פרט’ אחד יוכל להתחשב על ‘כללים’ רבים ביחד, כלומר, להיות שוּתף בתכוּנה אחת עם פרטיו של כלל אחד ובתכונה אחרת עם פרטיו של כלל אחר, בעוד שהשם הנקרא עליו מציין רק את התיחסותו לאחד הכללים באחד מצדדיו, לא בכולם. – על משפטים ממין זה תוכל להשען, וגם תשען באמת, ההסכמה הכללית ביחוסה אלינו: פלוני ופלוני הם יהודים לפי שמם ורמאים לפי תכוּנתם; שמע מינה, שהיהודים הם לפי תכונתם רמאים. ההגיון האמתי ישיב אמנם על זה, כי אף אם היו באמת כל היהודים בדורנו רמאים, אין מזה עוד ראיה, שהיהודים הם רמאים, כלומר, שתכוּנת הרמאוּת הנמצאת בכל יהודי נמצאת בו מצד התיחסותו אל הכלל ‘יהודים’ ולא מצד איזה כלל אחר (למשל, כלל ‘סוחרים’), שגם אליו מתיחס היהודי בתור פרט, ביחד עם אחרים אשר דבר אין להם עם הכלל ‘יהודים’. וכדי לברר הדבר, צריך לבדוֹק תחלה אותם ‘האחרים’ המשתתפים יחד עם היהודים בכללים אחרים. ורק אחר שנמצא על ידי בדיקה זו, שאין תכוּנת הרמאוּת מצויה בשום ‘כלל’ אחר המשותף ליהודים ולאחרים, – רק אז תהיה לנו צדקה לחרוץ משפט, כי היהדות היא אֵם הרמאוּת. – אבל, כאמור, אין דרכם של בני אדם להעמיק בהגיון, ואין אנו יכולים לדרוש כזאת גם מהמון בני עמנו. הם שומעים את המשפט החרוץ של ההסכמה הכללית ורואים עם זה, שרבים בקרבּנוּ כך הם באמת כמו שאומרת ההסכמה, ובזה די להם, והרי הם מתחילים להסכים גם בעצמם. וככה עוברות ‘תכוּנות היהודים’ כמטבע כשרה מיד ליד, מן ההסכמה החיצונית של העמים אל ההסכמה הפנימית בקרב עמנו, רק עם ההבדל הזה, שהעמים מונים את תכוּנותינו הרעות אחת לאחת בקול ענוֹת גבוּרה ולעג השאננים, ואנחנו עונים אחריהם מלה במלה בקול דממה דקה והצטדקות חלושה; הם ממשילים אותנו לכלי חרס, שאין לו תקנה אלא שבירה, ואנחנו ממשילים עצמנו לכלי מתכת, שאפשר לו בהגעלה ולבּוּן…\n\nהמצב הזה, אם יאריך ימים, יוכל לגרום לנו נזק מוסרי גדול. אין דבר מסוכּן לגוי ולאדם כהודאה על חטאים שאין בו. מי שחטא באמת, הרי שערי תשובה לא ננעלו, וברצונו הטוב יכול להסיר חלאתו מעליו. אבל מי שאחרים הביאוהו לחשוֹד עצמו במה שאין בו, איך יוכל להטהר בעיני עצמו? מצד אחד מאמין הוא לדברי האומרים לו: טול קורה מבין עיניך, ומצד אחר מרגיש הוא, שאינו יכול לטול את הקורה מבין עיניו, אחר שאינה באמת אלא בדמיון, והרי הוא במצב אותם המונומַנים הידועים, שמאיזו סבּה באו לידי אמונה, כי משׂא כבד תלוי להם בחוטמם מבלי שיוכלו להסירו. ולא עוד אלא שלפעמים תביא אמונה זו את האיש הפרטי להשתתף באותה המדה המגוּנה שלפי אמונתו היא קנין הכלל כולו, אעפ“י שהוא עצמו מצד פרטיותו אינו נוטה כלל לזה. אין ספק, למשל, כי בקרב העם שיצאו מתוכו אנשים כהרמב”ם נמצאים גם עתה בעלי דעה מיושבת ואוהבי סדר ושיטה בכל דבר, והם, בקחתם חלק בעבודת הצבּוּר, היו יכולים לתת בה את רוחם ולפעול גם על יתר העובדים. אבל מה נעשׂה, וכל גזרה ‘ההסכמה’, ששׂנאת הסדרים היא תכוּנה יהודית, וכבר הסכמנו גם אנחנו להסכמה זו (אעפ"י שעוד לא נתברר, אם התכוּנה הזאת, המצויה באמת בחלק גדול מעמנו, מתיחסת אל הכלל ‘יהודים’, או אולי – מה שיותר מתקבל על הלב – אל הכלל ‘חניכי־החדר’). ועל כן תרפינה ידי אוהבי הסדר, בהאמינם, כי אין עצה ואין תבונה נגד תכוּנת העם. ואם פטריוטים הם, יעקרו גם מלבם את האהבה לסדרים, המתנגדת לרוח עמם, ויעשׂו גם הם את מעשׂיהם כראוי ליהודים אמתיים…\n\n\n\nצריך איפוא לבקש איזה אמצעי, איך להוציא את עצמנו מתחת השפעת ‘ההסכמה הכללית’ בנוגע לתכוּנות ישׂראל וערכו המוסרי, כדי שלא נהיה בזויים בעיני עצמנו ולא נחשוב, שבאמת גרועים אנחנו מכל בני האדם תחת השמש, וכדי שלא נבוא עי"ז להיות ברבות הימים בפועל מה שאין אנו עתה אלא בדמיון.\n\nואת האמצעי הזה נותנת לנו ‘ההסכמה הכללית’ עצמה על ידי עלילת־הדם. העלילה הזאת היא היחידה בין כל רעותיה אשר בה לא תוכל ההסכמה להביא גם אותנו לידי ספק, אם באמת ‘כל העולם חייבים ואנחנו זכאים’, בהיותה מיוסדת כולה על שקר מוחלט ואין לה משען באיזה היקש מוטעה ‘מן הפרט על הכלל’. כל איש ישׂראל שנתחנך בתוך עמו יודע בבירור גמור, שאין בתוך כלל ישׂראל אף פרט אחד האוכל דם אדם לשם שמים. ואת הידיעה הברורה הזאת משגיאת ‘ההסכמה הכללית’, המתחדשת בלבנו מזמן לזמן על ידי התחדשות עלילת־הדם, צריכים אנו לשמור תמיד בזכרוננו, והיא תעזור לנו לעקור מלבנו את הנטיה להכּנע מפני האַבטוֹריטט של ‘כל העולם’ גם ביתר הדברים. יאמר כל העולם מה שיאמר על דבר פחיתוּת ערכּנוּ המוסרי, – אנחנו יודעים, כי ‘ההסכמה’ הזאת נשענת רק על הגיון המוני, בלי כל יסוד מדעי אמתּי. כי מי בא בסוד עמקי רוחנו וראה את ‘היהודי’ כמו שהוא מצד עצמו? מי שקל זה לעומת זה יהודים ושאינם יהודים הדומים אלו לאלו בכל יתר ‘הכללים’: סוחרים לעומת סוחרים, נרדפים לעומת נרדפים, רעבים לעומת רעבים וכו\'. – מי שקל כל אלה במאזני החכמה האמתּית ומצא את הכף מַכרעת לאחד הצדדים?\n\n‘וכי אפשר שכּל העולם חייבים והיהודים זכאים?’\n\nאפשר ואפשר, ועלילת־הדם תוכיח. פה הרי היהודים זכאים וטהורים כמלאכי השרת: יהודי ודם! היש שני הפכים גדולים מאלו? – ואף על פי כן…\n\n\n\nה\' תשרי תרנ"ג\n\n\n\n\n\n\nנדפס ב‘המליץ’ י“ד תשרי תרנ”ג. \xa0↩\n\n\n\n\n\n\n\n\n\n\nאת הטקסט לעיל הפיקו מתנדבי פרויקט בן־יהודה באינטרנט.  הוא זמין תמיד בכתובת הבאה:https://benyehuda.org/read/10'
}
```

### Data Fields

- `authors` 
- `genre` 
- `id`
- `original_language` 
- `source_edition` 
- `text` 
- `title`
- `translators` 
- `url` 

### Data Splits

|        | train | 
|--------|------:|
| corpus | 10078 |

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

Researchers.

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

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Citation Information

```
@article{,
  author = {},
  title = {Public domain texts from Project Ben-Yehuda},
  journal = {},
  url = {https://github.com/projectbenyehuda/public_domain_dump},
  year = {2020},
}
```

### Contributions

Thanks to [@imvladikon](https://github.com/imvladikon) for adding this dataset.
