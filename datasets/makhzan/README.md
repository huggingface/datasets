---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- ur
licenses:
- other-my-license
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- sequence-modeling
task_ids:
- language-modeling
paperswithcode_id: null
---

# Dataset Card for makhzan

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

- **Homepage:** https://matnsaz.net/en/makhzan
- **Repository:** https://github.com/zeerakahmed/makhzan
- **Paper:** [More Information Needed]
- **Leaderboard:** [More Information Needed]
- **Point of Contact:** Zeerak Ahmed

### Dataset Summary

An Urdu text corpus for machine learning, natural language processing and linguistic analysis.


### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

ur

## Dataset Structure

### Data Instances

```
{
  "contains-non-urdu-languages": "No",
  "document_body":
  "
  <body>
		<section>
			<p>بنگلہ دیش کی عدالتِ عالیہ نے طلاق کے ایک مقدمے کا فیصلہ کرتے ہوئے علما کے فتووں کو غیر قانونی قرار دیا ہے۔ عدالت نے پارلیمنٹ سے یہ درخواست کی ہے کہ وہ جلد ایسا قانون وضع کرے کہ جس کے بعد فتویٰ بازی قابلِ دست اندازیِ پولیس جرم بن جائے۔ بنگلہ دیش کے علما نے اس فیصلے پر بھر پور ردِ عمل ظاہرکرتے ہوئے اس کے خلاف ملک گیر تحریک چلانے کا اعلان کیا ہے۔ اس ضمن میں علما کی ایک تنظیم ”اسلامک یونٹی الائنس“ نے متعلقہ ججوں کو مرتد یعنی دین سے منحرف اور دائرۂ اسلام سے خارج قرار دیا ہے۔</p>
			<p>فتوے کا لفظ دو موقعوں پر استعمال ہوتا ہے۔ ایک اس موقع پر جب کوئی صاحبِ علم شریعت کے کسی مئلے کے بارے میں اپنی رائے پیش کرتا ہے۔ دوسرے اس موقع پر جب کوئی عالمِ دین کسی خاص واقعے کے حوالے سے اپنا قانونی فیصلہ صادر کرتا ہے۔ ایک عرصے سے ہمارے علما کے ہاں اس دوسرے موقعِ استعمال کا غلبہ ہو گیا ہے۔ اس کا نتیجہ یہ نکلا ہے کہ اس لفظ کا رائے یا نقطۂ نظر کے مفہوم میں استعمال کم و بیش متروک ہو گیا ہے۔ چنانچہ اب فتوے کا مطلب ہی علما کی طرف سے کسی خاص مألے یا واقعے کے بارے میں حتمی فیصلے کا صدور سمجھا جاتا ہے۔ علما اسی حیثیت سے فتویٰ دیتے ہیں اور عوام الناس اسی اعتبار سے اسے قبول کرتے ہیں۔ اس صورتِ حال میں ہمارے نزدیک، چند مسائل پیدا ہوتے ہیں۔ اس سے پہلے کہ ہم مذکورہ فیصلے کے بارے میں اپنا تاثر بیان کریں، یہ ضروری معلوم ہوتا ہے کہ مختصر طور پر ان مسائل کا جائزہ لے لیا جائے۔</p>
			<p>پہلا مألہ یہ پیدا ہوتا ہے کہ قانون سازی اور شرعی فیصلوں کا اختیار ایسے لوگوں کے ہاتھ میں آجاتا ہے جو قانون کی رو سے اس کے مجاز ہی نہیں ہوتے۔ کسی میاں بیوی کے مابین طلاق کے مألے میں کیا طلاق واقع ہوئی ہے یا نہیں ہوئی؟ ان کا نکاح قائم ہے یا باطل ہو گیا ہے؟ رمضان یا عید کا چاند نظر آیا ہے یا نہیں آیا؟کوئی مسلمان اپنے کسی قول یا اقدام کی وجہ سے کہیں دائرۂ اسلام سے خارج اورنتیجۃً مسلم شہریت کے قانونی حقوق سے محروم تو نہیں ہو گیا؟ یہ اور اس نوعیت کے بہت سے دوسرے معاملات سر تا سر قانون اور عدالت سے متعلق ہوتے ہیں۔ علما کی فتویٰ سازی کے نتیجے میںیہ امور گویا حکومت اورعدلیہ کے ہاتھ سے نکل کر غیر متعلق افراد کے ہاتھوں میں آجاتے ہیں۔</p>
			<p>دوسرا مألہ یہ پیدا ہوتا ہے کہ قانون کی حاکمیت کا تصور مجروح ہوتا ہے اور لوگوں میں قانون سے روگردانی کے رجحانات کو تقویت ملتی ہے۔ اس کی وجہ یہ ہے کہ قانون اپنی روح میں نفاذ کا متقاضی ہوتا ہے۔ اگر اسے نفاذ سے محروم رکھا جائے تو اس کی حیثیت محض رائے اور نقطۂ نظر کی سی ہوتی ہے۔ غیر مجاز فرد سے صادر ہونے والا فتویٰ یا قانون حکومت کی قوتِ نافذہ سے محروم ہوتا ہے۔ اس کی خلاف ورزی پر کسی قسم کی سزا کا خوف نہیں ہوتا۔ چنانچہ فتویٰ اگر مخاطب کی پسند کے مطابق نہ ہو تو اکثر وہ اسے ماننے سے انکار کر دیتا ہے۔ اس طرح وہ فتویٰ یا قانون بے توقیر ہوتا ہے۔ ایسے ماحول میں رہنے والے شہریوں میں قانون ناپسندی کا رجحان فروغ پاتا ہے اور جیسے ہی انھیں موقع ملتا ہے وہ بے دریغ قانون کی خلاف ورزی کر ڈالتے ہیں۔</p>
			<p>تیسرامسئلہ یہ پیدا ہوتا ہے کہ اگرغیر مجاز افراد سے صادر ہونے والے فیصلوں کو نافذ کرنے کی کوشش کی جائے تو ملک میں بد نظمی اور انارکی کا شدید اندیشہ پیدا ہو جاتا ہے۔ جب غیر مجازافراد سے صادر ہونے والے قانونی فیصلوں کو حکومتی سرپرستی کے بغیر نافذ کرنے کی کوشش کی جاتی ہے تو اپنے عمل سے یہ اس بات کا اعلان ہوتا ہے کہ مرجعِ قانون و اقتدارتبدیل ہو چکا ہے۔ جب کوئی عالمِ دین مثال کے طور پر، یہ فتویٰ صادر کرتا ہے کہ سینما گھروں اور ٹی وی اسٹیشنوں کو مسمار کرنامسلمانوں کی ذمہ داری ہے، یا کسی خاص قوم کے خلاف جہاد فرض ہو چکا ہے، یا فلاں کی دی گئی طلاق واقع ہو گئی ہے اور فلاں کی نہیں ہوئی، یا فلاں شخص یا گروہ اپنا اسلامی تشخص کھو بیٹھا ہے تو وہ درحقیقت قانونی فیصلہ جاری کر رہا ہوتا ہے۔ دوسرے الفاظ میں، وہ ریاست کے اندر اپنی ایک الگ ریاست بنانے کا اعلان کر رہا ہوتا ہے۔ اس کا نتیجہ سوائے انتشار اور انارکی کے اور کچھ نہیں نکلتا۔ یہی وجہ ہے کہ جن علاقوں میں حکومت کی گرفت کمزور ہوتی ہے وہاں اس طرح کے فیصلوں کا نفاذ بھی ہو جاتا ہے اور حکومت منہ دیکھتی رہتی ہے۔</p>
			<p>چوتھا مسئلہ یہ پیدا ہوتا ہے کہ مختلف مذہبی مسالک کی وجہ سے ایک ہی معاملے میں مختلف اور متضاد فتوے منظرِ عام پر آتے ہیں۔ یہ تو ہمارے روز مرہ کی بات ہے کہ ایک ہی گروہ کو بعض علماے دین کافر قرار دیتے ہیں اور بعض مسلمان سمجھتے ہیں۔ کسی شخص کے منہ سے اگر ایک موقع پر طلاق کے الفاظ تین بار نکلتے ہیں تو بعض علما اس پر ایک طلاق کا حکم لگا کر رجوع کا حق باقی رکھتے ہیں اور بعض تین قرار دے کررجوع کو باطل قرار دیتے ہیں۔ یہ صورتِ حال ایک عام آدمی کے لیے نہایت دشواریاں پیدا کر دیتی ہے۔</p>
			<p>پانچواں مسئلہ یہ پیدا ہوتا ہے کہ حکمران اگر دین و شریعت سے کچھ خاص دلچسپی نہ رکھتے ہوں تو وہ اس صورتِ حال میں شریعت کی روشنی میں قانون سازی کی طرف متوجہ نہیں ہوتے۔ کام چل رہا ہے کے اصول پر وہ اس طریقِ قانون سازی سے سمجھوتاکیے رہتے ہیں۔ اس کا نتیجہ یہ نکلتا ہے کہ حکومتی ادارے ضروری قانون سازی کے بارے میں بے پروائی کا رویہ اختیار کرتے ہیں اور قوانین اپنے فطری ارتقا سے محروم رہتے ہیں۔</p>
			<p>چھٹا مألہ یہ پیدا ہوتا ہے کہ رائج الوقت قانون اور عدالتوں کی توہین کے امکانات پیدا ہو جاتے ہیں۔ جب کسی مسئلے میں عدالتیں اپنا فیصلہ سنائیں اور علما اسے باطل قرار دیتے ہوئے اس کے برعکس اپنا فیصلہ صادر کریں تو اس سے عدالتوں کا وقار مجروح ہوتا ہے۔ اس کا مطلب یہ ہوتا ہے کہ کوئی شہری عدلیہ کو چیلنج کرنے کے لیے کھڑا ہو گیا ہے۔</p>
			<p>ان مسائل کے تناظر میں بنگلہ دیش کی عدالتِ عالیہ کا فیصلہ ہمارے نزدیک، امت کی تاریخ میں ایک عظیم فیصلہ ہے۔ جناب جاوید احمد صاحب غامدی نے اسے بجا طور پر صدی کا بہترین فیصلہ قرار دیا ہے۔ بنگلہ دیش کی عدالت اگر علما کے فتووں اور قانونی فیصلوں پر پابندی لگانے کے بجائے، ان کے اظہارِ رائے پر پابندی عائدکرتی تو ہم اسے صدی کا بدترین فیصلہ قرار دیتے اور انھی صفحات میں بے خوفِ لومۃ و لائم اس پر نقد کر رہے ہوتے۔</p>
			<p>موجودہ زمانے میں امتِ مسلمہ کا ایک بڑا المیہ یہ ہے کہ اس کے علما اپنی اصل ذمہ داری کو ادا کرنے کے بجائے ان ذمہ داریوں کو ادا کرنے پر مصر ہیں جن کے نہ وہ مکلف ہیں اور نہ اہل ہیں۔ قرآن و سنت کی رو سے علما کی اصل ذمہ داری دعوت و تبلیغ، انذار و تبشیر اور تعلیم و تحقیق ہے۔ ان کا کام سیاست نہیں، بلکہ سیاست دانوں کو دین کی رہنمائی سے آگاہی ہے؛ ان کا کام حکومت نہیں، بلکہ حکمرانوں کی اصلاح کی کوشش ہے؛ ان کا کام جہاد و قتال نہیں، بلکہ جہادکی تعلیم اور جذبۂ جہاد کی بیداری ہے؛ اسی طرح ان کا کام قانون سازی اور فتویٰ بازی نہیں بلکہ تحقیق و اجتہاد ہے۔ گویا انھیں قرآنِ مجیدکامفہوم سمجھنے، سنتِ ثابتہ کا مدعا متعین کرنے اور قولِ پیغمبر کا منشامعلوم کرنے کے لیے تحقیق کرنی ہے اور جن امور میں قرآن و سنت خاموش ہیں ان میں اپنی عقل و بصیرت سے اجتہادی آراقائم کرنی ہیں۔ ان کی کسی تحقیق یا اجتہاد کو جب عدلیہ یا پارلیمنٹ قبول کرے گی تو وہ قانون قرار پائے گا۔ اس سے پہلے اس کی حیثیت محض ایک رائے کی ہوگی۔ اس لیے اسے اسی حیثیت سے پیش کیا جائے گا۔</p>
			<p>اس کا مطلب یہ ہے کہ کوئی حکم نہیں لگایا جائے گا، کوئی فیصلہ نہیں سنایا جائے گا، کوئی فتویٰ نہیں دیا جائے گا، بلکہ طالبِ علمانہ لب و لہجے میں محض علم و استدلال کی بنا پر اپنا نقطۂ نظر پیش کیا جائے گا۔ یہ نہیں کہا جائے گا کہ فلاں شخص کافر ہے، بلکہ اس کی اگر ضرورت پیش آئے تو یہ کہا جائے گا کہ فلاں شخص کا فلاں عقیدہ کفر ہے۔ یہ نہیں کہا جائے گا کہ فلاں آدمی دائرۂ اسلام سے خارج ہو گیا ہے، بلکہ یہ کہا جائے گا کہ فلاں آدمی کا فلاں نقطۂ نظر اسلام کے دائرے میں نہیں آتا۔ یہ نہیں کہا جائے گا فلاں آدمی مشرک ہے، بلکہ یہ کہا جائے گا فلاں نظریہ یا فلاں طرزِ عمل شرک ہے۔ یہ نہیں کہا جائے گا کہ زید کی طرف سے دی گئی ایک وقت کی تین طلاقیں واقع ہو گئی ہیں، بلکہ یہ کہا جائے گا کہ ایک وقت کی تین طلاقیں واقع ہو نی چاہییں۔</p>
			<p>حکم لگانا، فیصلہ سنانا، قانون وضع کرنا اورفتویٰ جاری کرنا درحقیقت، عدلیہ اور حکومت کا کام ہے کسی عالمِ دین یا کسی اور غیر مجاز فرد کی طرف سے اس کام کو انجام دینے کی کوشش سراسر تجاوز ہے۔ خلافتِ راشدہ کے زمانے میں اس اصول کو ہمیشہ ملحوظ رکھا گیا۔ شاہ ولی اللہ محدث دہلوی اپنی کتاب ”ازالتہ الخفا ء“ میں لکھتے ہیں:</p>
			<blockquote>
				<p>”اس زمانے تک وعظ اور فتویٰ خلیفہ کی رائے پر موقوف تھا۔ خلیفہ کے حکم کے بغیر نہ وعظ کہتے تھے اور نہ فتویٰ دیتے تھے۔ بعد میں خلیفہ کے حکم کے بغیر وعظ کہنے اور فتویٰ دینے لگے اور فتویٰ کے معاملے میں جماعت (مجلسِ شوریٰ) کے مشورہ کی جو صورت پہلے تھی وہ باقی نہ رہی——- (اس زمانے میں) جب کوئی اختلافی صورت نمودار ہوتی، خلیفہ کے سامنے معاملہ پیش کرتے، خلیفہ اہلِ علم و تقویٰ سے مشورہ کرنے کے بعد ایک رائے قائم کرتا اور وہی سب لوگوں کی رائے بن جاتی۔ حضرت عثمان کی شہادت کے بعد ہر عالم بطورِ خود فتویٰ دینے لگا اور اس طرح مسلمانوں میں اختلاف برپا ہوا۔“ (بحوالہ ”اسلامی ریاست میں فقہی اختلافات کا حل“، مولاناامین احسن اصلاحی، ص۳۲)</p>
			</blockquote>
		</section>
	</body>
  ",
  "file_id": "0001.xml",
  "metadata":
  "
  <meta>
		<title>بنگلہ دیش کی عدالت کا تاریخی فیصلہ</title>
		<author>
			<name>سید منظور الحسن</name>
			<gender>Male</gender>
		</author>
		<publication>
			<name>Mahnama Ishraq February 2001</name>
			<year>2001</year>
			<city>Lahore</city>
			<link>https://www.javedahmedghamidi.org/#!/ishraq/5adb7341b7dd1138372db999?articleId=5adb7452b7dd1138372dd6fb&amp;year=2001&amp;decade=2000</link>
			<copyright-holder>Al-Mawrid</copyright-holder>
		</publication>
		<num-words>1694</num-words>
		<contains-non-urdu-languages>No</contains-non-urdu-languages>
	</meta>
  ",
  "num-words": 1694,
  "title": "بنگلہ دیش کی عدالت کا تاریخی فیصلہ"
}
```

### Data Fields
```file_id (str)```: Document file_id corresponding to filename in repository.

```metadata(str)```: XML formatted string containing metadata on the document such as the document's title, information about the author and publication, as well as other potentially useful facts such as the number of Urdu words in the document and whether the document contains text in any other languages.

```title (str)```: Title of the document.

```num-words (int)```: Number of words in document.

```contains-non-urdu-languages (str)```: ```Yes``` if document contains words other than urdu, ```No``` otherwise.

```document_body```: XML formatted body of the document. Details below:

The document is divided into ```<section>``` elements. In general the rule is that a clear visual demarkation in the original text (such as a page break, or a horizontal rule) is used to indicate a section break. A heading does not automatically create a new section.

Each paragraph is a ```<p>``` element.

Headings are wrapped in an ```<heading>``` element.

Blockquotes are wrapped in a ```<blockquote>``` element. Blockquotes may themselves contain other elements.

Lists are wrapped in an ```<list>```. Individual items in each list are wrapped in an ```<li>``` element.

Poetic verses are wrapped in a ```<verse>``` element. Each verse is on a separate line but is not wrapped in an individual element.

Tables are wrapped in a ```<table>``` element. A table is divided into rows marked by ```<tr>``` and columns marked by ```<td>```.

Text not in the Urdu language is wrapped in an ```<annotation>``` tag (more below).

```<p>, <heading>, <li>, <td>``` and ```<annotation>``` tags are inline with the text (i.e. there is no new line character before and after the tag). Other tags have a new line after the opening and before the closing tag.

Due to the use of XML syntax, ```<```, ```>``` and ```&``` characters have been escaped as ```&lt```;, ```&gt```;, and ```&amp```; respectively. This includes the use of these characters in URLs inside metadata.

### Data Splits

All the data is in one split ```train```
## Dataset Creation

### Curation Rationale

All text in this repository has been selected for quality of language, upholding high editorial standards. Given the poor quality of most published Urdu text in digital form, this selection criteria allows the use of this text for natural language processing, and machine learning applications without the need to address fundamental quality issues in the text.

We have made efforts to ensure this text is as broadly representative as possible. Specifically we have attempted to select for as many authors as possible, and diversity in the gender of the author, as well as years and city of publication. This effort is imperfect, and we appreciate any attempts at pointing us to resources that can help diversify this text further.

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?
Makhzan has been started with generous initial donations of text from two renowned journals  Bunyad, from the Gurmani Center of Literature and Languages at the Lahore University of Management Sciences (LUMS), and Ishraq, from the Al-Mawrid Institute. This choice of sources allowed us to get a diversity of voices even in a small initial corpus, while ensuring the highest editorial standards available in published Urdu text. As a result your models can also maintain high linguistic standards.

### Annotations

#### Annotation process
Text is structured and annotated using XML syntax. The ontology of elements used is loosely based around HTML, with simplifications made when HTML's specificity is not needed, and additions made to express common occurences in this corpus that would be useful for linguistic analysis. The semantic tagging of text is editorial in nature, which is to say that another person semantically tagging the text may do so differently. Effort has been made however to ensure consistency, and to retain the original meaning of the text while making it easy to parse through linguistically different pieces of text for analysis.


Annotations have been made inline using an ```<annotation>``` element.
A language (lang) attribute is added to the ```<annotation>``` element to indicate text in other languages (such as quoted text or technical vocabulary presented in other languages and scripts). The attribute value a two-character ISO 639-1 code. So the resultant annotation for an Arabic quote for example, will be ```<annotation lang="ar"></annotation>```.
A type (type) attributed is added to indicate text that is not in a language per se but is not Urdu text. URLs for example are wrapped in an ```<annotation type="url">``` tag.


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

A few of the files do not have valid XML and cannot be loaded. This issue is tracked [here](https://github.com/zeerakahmed/makhzan/issues/28)

## Additional Information

### Dataset Curators

Zeerak Ahmed

### Licensing Information

[More Information Needed]

### Citation Information

[More Information Needed]

### Contributions

Thanks to [@arkhalid](https://github.com/arkhalid) for adding this dataset.