---
annotations_creators:
- found
language_creators:
- found
languages:
- en
licenses:
- unknown
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- text-classification
task_ids:
- topic-classification
---

# Dataset Card for `prachathai67k`

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

- **Homepage:** https://github.com/PyThaiNLP/prachathai-67k
- **Repository:** https://github.com/PyThaiNLP/prachathai-67k
- **Paper:**
- **Leaderboard:**
- **Point of Contact:** https://github.com/PyThaiNLP/

### Dataset Summary

`prachathai-67k`: News Article Corpus and Multi-label Text Classificdation from Prachathai.com

The `prachathai-67k` dataset was scraped from the news site [Prachathai](prachathai.com). We filtered out those articles with less than 500 characters of body text, mostly images and cartoons. It contains 67,889 articles wtih 12 curated tags from August 24, 2004 to November 15, 2018. The dataset was originally scraped by [@lukkiddd](https://github.com/lukkiddd) and cleaned by [@cstorm125](https://github.com/cstorm125). Download the dataset [here](https://www.dropbox.com/s/fsxepdka4l2pr45/prachathai-67k.zip?dl=1). You can also see preliminary exploration in [exploration.ipynb](https://github.com/PyThaiNLP/prachathai-67k/blob/master/exploration.ipynb).

This dataset is a part of [pyThaiNLP](https://github.com/PyThaiNLP/) Thai text [classification-benchmarks](https://github.com/PyThaiNLP/classification-benchmarks). For the benchmark, we selected the following tags with substantial volume that resemble **classifying types of articles**:

* `การเมือง` - politics
* `สิทธิมนุษยชน` - human_rights
* `คุณภาพชีวิต` - quality_of_life
* `ต่างประเทศ` - international
* `สังคม` - social
* `สิ่งแวดล้อม` - environment
* `เศรษฐกิจ` - economics
* `วัฒนธรรม` - culture
* `แรงงาน` - labor
* `ความมั่นคง` - national_security
* `ไอซีที` - ict
* `การศึกษา` - education

### Supported Tasks and Leaderboards

multi-label text classification, language modeling

### Languages

Thai

## Dataset Structure

### Data Instances

{'body_text': '17 พ.ย. 2558 Blognone [1] รายงานว่า กลุ่มแฮคเกอร์ Anonymous ประกาศสงครามไซเบอร์กับกลุ่มหัวรุนแรงหลังจากกลุ่ม IS ออกมาประกาศว่าเป็นผู้อยู่เบื้องหลังการโจมตีกรุงปารีสในคืนวันศุกร์ที่ผ่านมา\n\n\nภาพในคลิปใน YouTube โฆษกของกลุ่มแฮคเกอร์สวมหน้ากากที่เป็นสัญลักษณ์ของกลุ่มได้ออกมาอ่านแถลงเป็นภาษาฝรั่งเศส มีใจความว่า จากการโจมตีของกลุ่ม IS ในกรุงปารีส กลุ่ม Anonymous ทั่วโลกจะตามล่ากลุ่ม IS เหมือนที่เคยทำตอนที่มีการโจมตีสำนักพิมพ์ Charlie Hebdo และครั้งนี้จะเป็นปฏิบัติการโจมตีครั้งใหญ่ที่สุดของกลุ่ม Anonymous เลย นอกจากนี้กลุ่ม Anonymous ยังแสดงความเสียใจต่อครอบครัวผู้สูญเสียในเหตุการณ์ครั้งนี้\nกลุ่ม Anonymous เคยประกาศสงครามกับกลุ่ม IS หลังจากการโจมตีสำนักพิมพ์ Charlie Hebdo ที่ฝรั่งเศสเมื่อต้นปีที่ผ่านมา ซึ่งครั้งนั้นกลุ่ม Anonymous อ้างว่าได้ระงับบัญชีผู้ใช้งานที่เกี่ยวข้องกับ IS ไปหลายพันบัญชี (อ่านรายละเอียดเพิ่มเติม จากBlognone ที่\xa0\xa0กลุ่มแฮคเกอร์ Anonymous ประกาศสงครามไซเบอร์ขอกวาดล้างพวก ISIS [2])', 'culture': 0, 'date': '2015-11-17 18:14', 'economics': 0, 'education': 0, 'environment': 0, 'human_rights': 0, 'ict': 1, 'international': 1, 'labor': 0, 'national_security': 0, 'politics': 0, 'quality_of_life': 0, 'social': 0, 'title': 'แฮคเกอร์ Anonymous ลั่นทำสงครามไซเบอร์ครั้งใหญ่สุดกับกลุ่ม IS', 'url': 'https://prachatai.com/print/62490'}
{'body_text': 'แถลงการณ์\n\n\xa0\n\nองค์การนักศึกษามหาวิทยาลัยธรรมศาสตร์\n\n\xa0\n\nมหาวิทยาลัยธรรมศาสตร์ก่อตั้งขึ้นภายใต้แนวคิดการให้การศึกษากับประชาชนเพื่อสนับสนุนการปกครองระบอบประชาธิปไตย อีกทั้งยังเป็นสถาบันหนึ่งที่อยู่เคียงข้างประชาชนมาโดยตลอด\n\n\xa0\n\nสถานการณ์สังคมไทยปัจจุบันได้เกิดความขัดแย้งทางการเมือง ทางแนวคิด จนลุกลามเป็นวิกฤตการณ์อันหาทางออกได้ยากยิ่ง องค์กรนักศึกษามหาวิทยาลัยธรรมศาสตร์ขอร้องเรียนและเสนอแนะต่อทุกฝ่าย โดยยึดหลักแนวทางตามรัฐธรรมนูญแห่งราชอาณาจักรไทย พ.ศ. ๒๕๕๐ อันเป็นกฎหมายสูงสุดในการจัดการปกครองรัฐ ที่มีผลบังคับใช้อยู่ในปัจจุบันซึ่งผ่านการประชามติจากปวงชนชาวไทยเมื่อวันที่ ๑๙ สิงหาคม พ.ศ. ๒๕๕๐ แล้วดังต่อนี้\n\n\xa0\n\n๑.การชุมชมโดยสงบและปราศจากอาวุธย่อมได้รับการคุ้มครองตามรัฐธรรมนูญ แต่หากการชุมนุมและเคลื่อนไหวของกลุ่มใดๆ มีการละเมิดสิทธิและเสรีภาพของผู้อื่นหรือก่อให้เกิดความเสียหายต่อชีวิตและทรัพย์สินของบุคคลและส่วนรวมนั้น ไม่สามารถกระทำได้ การใช้ความรุนแรง การกระทำอุกอาจต่างๆ ทั้งต่อบุคคลและทรัพย์สิน การยั่วยุ ปลุกระดมเพื่อหวังผลในการปะทะต่อสู้ จึงควรได้รับการกล่าวโทษ\n\n\xa0\n\nดังนั้นทั้งกลุ่มพันธมิตรประชาชนเพื่อประชาธิปไตย (พธม.) และกลุ่มแนวร่วมประชาธิปไตยไม่เอาเผด็จการแห่งชาติ (นปช.) จึงควรยอมรับกระบวนการตามกฎหมาย และหากถูกกล่าวหาไม่ว่ากรณีใดๆ ก็ควรพิสูจน์ความบริสุทธิ์โดยใช้กระบวนการยุติธรรม และหากจะยังชุมนุมต่อไปก็ยังคงทำได้ภายใต้บทบัญญัติแห่งกฎหมาย\n\n\xa0\n\nองค์กรนักศึกษามหาวิทยาลัยธรรมศาสตร์ จึงร้องขอให้หน่วยงานต่างๆ ที่เกี่ยวข้องดำเนินการตามกระบวนการทางกฎหมายกับการกระทำที่ผิดบทบัญญัติแห่งกฎหมายที่ทุกฝ่ายได้กระทำไป\n\n\xa0\n\n๒.นายสมัคร สุนทรเวช นายกรัฐมนตรี ไม่มีความเหมาะสมในการบริหารราชการแผ่นดินขาดหลักธรรมาภิบาล แต่ทั้งนี้นายสมัคร สุนทรเวช ยังคงยืนยันและกล่าวอ้างความชอบธรรมตามระบอบประชาธิปไตยภายใต้รัฐธรรมนูญ โดยไม่คำนึงถึงกระแสเรียกร้องใดๆ อันส่งผลให้ความขัดแย้งทางสังคมยิ่งบานปลายจนกลายเป็นวิกฤตการณ์เช่นปัจจุบัน ซึ่งก่อให้เกิดความเสียหายต่อประเทศแนวโน้มจะคลี่คลาย\n\n\xa0\n\nองค์การนักศึกษามหาวิทยาลัยธรรมศาสตร์ จึงเห็นว่า ควรใช้สิทธิตามรัฐธรรมนูญแห่งราชอาณาจักรไทย พุทธศักราช ๒๕๕๐ มาตรา ๑๖๔ โดยการเข้าชื่อเพื่อร้องต่อประธานวุฒิสภาเพื่อให้มีมติตามมาตรา ๒๗๔ ให้ถอดถอนนายสมัคร สุนทรเวช ออกจากตำแหน่งนายกรัฐมนตรีตามมาตรา ๒๗๐ ณ ลานโพ มหาวิทยาลัยธรรมศาสตร์ ท่าพระจันทร์ อาคารเรียนรวมสังคมศาสตร์ อาคารปิยชาติ และตึกกิจกรรมนักศึกษา มหาวิทยาลัยธรรมศาสตร์ ศูนย์รังสิต\n\n\xa0\n\n\xa0\n\nด้วยความสมานฉันท์\n\nองค์การนักศึกษามหาวิทยาลัยธรรมศาสตร์', 'culture': 0, 'date': '2008-09-06 03:36', 'economics': 0, 'education': 0, 'environment': 0, 'human_rights': 0, 'ict': 0, 'international': 0, 'labor': 0, 'national_security': 0, 'politics': 1, 'quality_of_life': 0, 'social': 0, 'title': 'แถลงการณ์ อมธ.แนะใช้สิทธิ ตาม รธน.เข้าชื่อร้องต่อประธานวุฒิสภาถอดถอน "สมัคร" จากตำแหน่งนายกฯ', 'url': 'https://prachatai.com/print/18038'}

### Data Fields

- `url`: url of the article
- `date`: date the article was published
- `title`: title of the article
- `body_text`: body text of the article
- `politics`: 1 if sample has this tag else 0
- `human_rights`: 1 if sample has this tag else 0
- `quality_of_life`: 1 if sample has this tag else 0
- `international`: 1 if sample has this tag else 0
- `social`: 1 if sample has this tag else 0
- `environment`: 1 if sample has this tag else 0
- `economics`: 1 if sample has this tag else 0
- `culture`: 1 if sample has this tag else 0
- `labor`: 1 if sample has this tag else 0
- `national_security`: 1 if sample has this tag else 0
- `ict`: 1 if sample has this tag else 0
- `education`: 1 if sample has this tag else 0

### Data Splits

|                   | train | valid  | test |
|-------------------|-------|--------|------|
| # articles        | 54379 | 6721   | 6789 |
| politics          | 31401 | 3852   | 3842 |
| human_rights      | 12061 | 1458   | 1511 |
| quality_of_life   | 9037  | 1144   | 1127 |
| international     | 6432  | 828    | 834  |
| social            | 6321  | 782    | 789  |
| environment       | 6157  | 764    | 772  |
| economics         | 3994  | 487    | 519  |
| culture           | 3279  | 388    | 398  |
| labor             | 2905  | 375    | 350  |
| national_security | 2865  | 339    | 338  |
| ict               | 2326  | 285    | 292  |
| education         | 2093  | 248    | 255  |

## Dataset Creation

### Curation Rationale

The data was scraped from the news site [Prachathai](prachathai.com) from August 24, 2004 to November 15, 2018. The initial intention was to use the dataset as a benchmark for Thai text classification. Due to the size of the dataset, it can also be used for language modeling.

### Source Data

#### Initial Data Collection and Normalization

67,889 articles wtih 51,797 tags were scraped from the news site [Prachathai](prachathai.com) from August 24, 2004 to November 15, 2018. We filtered out those articles with less than 500 characters of body text, mostly images and cartoons.

#### Who are the source language producers?

Prachathai.com

### Annotations

#### Annotation process

Tags are annotated for the news website Prachathai.com

#### Who are the annotators?

We assume that the reporters who wrote the articles or other Prachathai staff gave each article its tags.

### Personal and Sensitive Information

We do not expect any personal and sensitive information to be present since all data are public news articles.

## Considerations for Using the Data

### Social Impact of Dataset

- classification benchmark for multi-label Thai text classification

### Discussion of Biases

Prachathai.com is a left-leaning, human-right-focused news site, and thus unusual news labels such as human rights and quality of life. The news articles are expected to be left-leaning in contents.

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

PyThaiNLP

### Licensing Information

CC-BY-NC

### Citation Information

@misc{prachathai67k,
  author = {cstorm125, lukkiddd },
  title = {prachathai67k},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished={\\url{https://github.com/PyThaiNLP/prachathai-67k}},
}
