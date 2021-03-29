---
annotations_creators:
- expert-generated
- found

language_creators:
- found

languages:
- en

licenses:
- cc-by-nc-sa-4.0

multilinguality:
- monolingual

size_categories:
- 10K<n<100K

source_datasets:
- original

task_categories:
- text-classification

task_ids:
- multi-label-classification
- rationale-extraction
- legal-judgment-prediction
---

# Dataset Card for the ECtHR cases dataset

## Table of Contents
- [Dataset Card the ECtHR cases dataset](#dataset-card-for-ecthr-cases)
  - [Table of Contents](#table-of-contents)
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
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
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

- **Homepage:** http://archive.org/details/ECtHR-NAACL2021/
- **Repository:** http://archive.org/details/ECtHR-NAACL2021/
- **Paper:** https://arxiv.org/abs/2103.13084
- **Leaderboard:** TBA
- **Point of Contact:** [Ilias Chalkidis](mailto:ihalk@aueb.gr)

### Dataset Summary

The European Court of Human Rights (ECtHR) hears allegations regarding breaches in human rights provisions of the European Convention of Human Rights (ECHR) by European states. The Convention is available at https://www.echr.coe.int/Documents/Convention_ENG.pdf. 
The court rules on a subset of all ECHR articles, which are predefined (alleged) by the applicants (*plaintiffs*). 

Our dataset comprises 11k ECtHR cases and can be viewed as an enriched version of the ECtHR dataset of Chalkidis et al. (2019), which did not provide ground truth for alleged article violations (articles discussed) and rationales. The new dataset includes the following:

**Facts:** Each judgment includes a list of paragraphs that represent the facts of the case, i.e., they describe the main events that are relevant to the case, in numbered paragraphs. We hereafter call these paragraphs *facts* for simplicity. Note that the facts are presented in chronological order. Not all facts have the same impact or hold crucial information with respect to alleged article violations and the court's assessment; i.e., facts may refer to information that is trivial or otherwise irrelevant to the legally crucial allegations against *defendant* states.

**Allegedly violated articles:** Judges rule on specific accusations (allegations) made by the applicants (Harris, 2018). In ECtHR cases, the judges discuss and rule on the violation, or not, of specific articles of the Convention. The articles to be discussed (and ruled on) are put forward (as alleged article violations) by the applicants and are included in the dataset as ground truth; we identify 40 violable articles in total. The rest of the articles are procedural, i.e., the number of judges, criteria for office, election of judges, etc. In our experiments, however, the models are not aware of the allegations. They predict the Convention articles that will be discussed (the allegations) based on the case's facts, and they also produce rationales for their predictions. Models of this kind could be used by potential applicants to help them formulate future allegations (articles they could claim to have been violated), as already noted, but here we mainly use the task as a test-bed for rationale extraction.

**Violated articles:** The court decides which allegedly violated articles have indeed been violated. These decisions are also included in our dataset and could be used for full legal judgment prediction experiments (Chalkidis et al., 2019). However, they are not used in the experiments of this work.

**Silver allegation rationales:** Each decision of the ECtHR includes references to facts of the case (e.g., *"See paragraphs 2 and 4."*) and case law (e.g., *"See Draci vs. Russia (2010)"*.). We identified references to each case's facts and retrieved the corresponding paragraphs using regular expressions. These are included in the dataset as silver allegation rationales, on the grounds that the judges refer to these paragraphs when ruling on the allegations.

**Gold allegation rationales:** A legal expert with experience in ECtHR cases annotated a subset of 50 test cases to identify the relevant facts (paragraphs) of the case that support the allegations (alleged article violations). In other words, each identified fact justifies (hints) one or more alleged violations.

### Supported Tasks and Leaderboards

The dataset supports:

**Alleged violation prediction:** A multi-label text classification task where, given the facts of a ECtHR case, a model predicts which of the 40 violable ECHR articles were allegedly violated according to the applicant(s). Consult Chalkidis et al. (2021), for details.

**Violation prediction:**  A multi-label text classification task where, given the facts of a ECtHR case, a model predicts which of the allegedly violated ECHR articles were violated, as decided (ruled) by the ECtHR court. Consult Chalkidis et al. (2019), for details.

**Rationale extraction:** A model can also predict the facts of the case that most prominently support its decision with respect to a classification task. Silver rationales can be used for both classification tasks, while gold rationales are only focused on the *alleged violation prediction* task.

### Languages

All documents are written in English.

## Dataset Structure

### Data Instances

```json
{
 "case_id":  "001-59588", 
 "case_no": "29032/95",
 "title": "CASE OF FELDEK v. SLOVAKIA",
 "judgment_date": "2001-07-12",
 "facts": [
  "8.  In 1991 Mr Du\u0161an Slobodn\u00edk, a research worker in the field of literature, published an autobiography entitled Paragraph: Polar Circle. He described in it, inter alia, his conviction by a Soviet military tribunal in 1945 on the ground that he had been ordered to spy on the Soviet army after having been enrolled, in 1944 when he was 17 years old, in a military training course organised by Germans. In the book, Mr Slobodn\u00edk also wrote about his detention in Soviet gulags and his rehabilitation by the Supreme Court of the Union of the Soviet Socialist Republics in 1960. In June 1992 Mr Slobodn\u00edk became Minister for Culture and Education of the Slovak Republic.",
  "9.  On 20 July 1992 the newspaper Telegraf published a poem by the applicant. It was dated 17 July 1992 (the day when the sovereignty of the Slovak Republic was solemnly proclaimed) and entitled \u201cGood night, my beloved\u201d (\u201cDobr\u00fa noc, m\u00e1 mil\u00e1\u201d). One of its verses read as follows:\n\u201cIn Prague prisoner Havel is giving up his presidential office. In Bratislava the prosecutor rules again. And rule by one party is above the law. A member of the SS and a member of the \u0160TB [The \u0160TB (\u0160t\u00e1tna bezpe\u010dnos\u0165) was the secret police during the communist regime in Czechoslovakia] embraced each other.\u201d",
  "10.  The poem was later published in another newspaper. In separate articles, two journalists alleged that the expression \u201cmember of the SS\u201d stood for Mr Du\u0161an Slobodn\u00edk.",
  "11.  On 30 July 1992 several newspapers published a statement which the applicant had distributed to the Public Information Service (Verejn\u00e1 informa\u010dn\u00e1 slu\u017eba) the day before. It was entitled \u201cFor a better picture of Slovakia \u2013 without a minister with a fascist past\u201d (\u201cZa lep\u0161\u00ed obraz Slovenska \u2013 bez ministra s fa\u0161istickou minulos\u0165ou\u201d). It read as follows:\n\u201cThere has been a problem about how to keep a democratic character in [the Slovakian] national emancipation process, which we have tried to resolve many times. Until now, Slovakia has lost most when matters related to the Slovakian nation were in the hands of the wrong people who led us away from democratic evolution. The cost was high: for example, the combatants\u2019 lives lost in the Slovakian National Uprising [in 1944 and 1945] . \nNow, we are scared that this mistake could be made again. To say that our way to Europe is by working together and cooperating in its democratic evolution is not enough. This is a direct condition arising from international law without the fulfilment of which no one in Europe will take notice of us.\nI expressed this concern in my polemics with Mr Du\u0161an Slobodn\u00edk last year; life has finished the writing of our polemics, and my views were proved correct.\nThis year Mr Slobodn\u00edk became the Slovak Republic\u2019s Minister for Culture and Education and the next thing was that his fascist past came out in public. Mr Slobodn\u00edk managed this situation in a way that allowed the writer Ladislav M\u0148a\u010dko to prove he was a liar. But he still has not given up his ministerial post, although in any other democratic country he would have had to do so a long time ago.\nDoes Mr Slobodn\u00edk think that Slovakia is some special exception and that it is the only country having the right to revise the philosophy of the Nuremberg trials, which is binding on the post-war development of all other European countries? Or is the message of the Slovakian National Uprising not correct? ... Does Mr Me\u010diar think that having this minister in the government will help him to persuade people in Europe that his talk about the democratic intentions of his government is serious? Is it good to have Mr Slobodn\u00edk in the government when this fact will lead to the political, economic and cultural isolation of Slovakia? \nMr Slobodn\u00edk likes to use every chance to talk about improving the image of Slovakia around the world. I fully agree with him on this. He has a personal opportunity to do something in order to improve the image of Slovakia: to resign.\u201d",
  "12.  On 5 August 1992 Mr Slobodn\u00edk publicly declared that he would sue the applicant for the above statement.",
  "13.  In an interview published in the Czech daily Lidov\u00e9 noviny on 12 August 1992 the applicant stated, inter alia:\n\u201c... when I speak of the fascist past [of Mr Slobodn\u00edk], I do not characterise him, I only think that the fact that he attended a terrorist training course organised by the SS falls within the term \u2018fascist past\u2019. I consider that such a person has nothing to do in the government of a democratic State ...\u201d",
  "14.  In the context of the nomination of Mr Slobodn\u00edk to a post in the government, issues relating to his past were taken up by several Slovakian and Czech newspapers both before and after the publication of the applicant\u2019s statement. Articles concerning this subject were also published in The New York Times, on 22 July 1992, the Tribune de Gen\u00e8ve, on 18 September 1992, Izvestia on 31 August 1992, as well as by the Austrian Press Agency. The New York Times, the Tribune de Gen\u00e8ve and Izvestia later published the reaction of Mr Slobodn\u00edk to their respective articles.",
  "15.  On 9 September 1992 Mr Slobodn\u00edk sued the applicant for defamation under Article 11 et seq. of the Civil Code before the Bratislava City Court (Mestsk\u00fd s\u00fad). He later extended the action and alleged that the verses \u201cIn Bratislava the prosecutor rules again. And rule by one party is above the law. A member of the SS and a member of the \u0160TB embraced each other\u201d from the applicant\u2019s poem referred to him. He also alleged that the above-mentioned statement published in the newspapers wrongly referred to his fascist past. The plaintiff claimed that the applicant should bear the costs of publication of an apology in five newspapers and also pay him 250,000 Slovakian korunas (SKK) as compensation.",
  "16.  On 18 October 1993 the Bratislava City Court dismissed the action. It established that the plaintiff had been a member of the Hlinka Youth (Hlinkova ml\u00e1de\u017e) and that in February and March 1945 he had participated in a terrorist training course in Sekule. It observed that the Hlinka Youth had been a military corps of the Hlinka Slovakian People\u2019s Party (Hlinkova slovensk\u00e1 \u013eudov\u00e1 strana) and that under the law then in force the Slovak nation had participated in the exercise of State power through the intermediary of that party. The court pointed out that, under Article 5 of Presidential Decree no. 5/1945 of 19 May 1945, legal persons which had deliberately promoted the war waged by Germany and Hungary or had served fascist and Nazi aims were to be considered unworthy of the State\u2019s trust.",
  "17.  The City Court further established that in May 1945 a military tribunal of the Soviet army had sentenced Mr Slobodn\u00edk to fifteen years\u2019 imprisonment on the ground that he had attended the training course in Sekule and had been ordered, on 22 March 1945, to cross the front line and to spy on Soviet troops. The military tribunal\u2019s judgment further stated that Mr Slobodn\u00edk had not crossed the front line but had gone home in April 1945, when he had been arrested. The City Court also noted that the plaintiff had served the sentence in Soviet camps until his release in 1953. In 1960 the Supreme Court of the USSR had quashed the sentence and discontinued the proceedings for the lack of factual elements of an offence.",
  "18.  Before the City Court, Mr Slobodn\u00edk claimed that he had been a member of the Hlinka Youth only for a short time and that he had joined the organisation only because it had been a prerequisite for his participation in a table-tennis tournament. He further explained that he had been summoned to the training course in Sekule and that he had complied with the summons out of fear for himself and his family. Mr Slobodn\u00edk alleged that he had been excluded from the course as being unreliable after he had expressed his negative opinion about it. He had then been taken to the Hlinka Youth headquarters in Bratislava, from where he had been allowed to return home to Bansk\u00e1 Bystrica under the condition that he would report on the Soviet army. However, the City Court did not find these facts established. In particular, it did not consider as relevant evidence the description of the events contained in the plaintiff\u2019s book Paragraph: Polar Circle, which had been published earlier. In its view, the fact that the 1945 sentence had been quashed did not prove that the plaintiff had not been a member of the Hlinka Youth and that he had not attended the training course in Sekule.",
  "19.  The City Court also noted that the relevant period of Mr Slobodn\u00edk\u2019s life had been covered by the press both in Slovakia and abroad prior to the applicant\u2019s statement, and that on several occasions Mr Slobodn\u00edk himself had commented and given interviews on those issues, both in Slovakia and abroad. The court concluded that, in the statement, the applicant had expressed his opinion on the basis of information which had already been published in the press. The statement concerned a public figure who was inevitably exposed to close scrutiny and sometimes also to criticism by other members of society. By making the statement, the applicant had exercised his right to freedom of expression and he had not unjustifiably interfered with the plaintiff\u2019s personality rights.",
  "20.  Mr Slobodn\u00edk appealed to the Supreme Court (Najvy\u0161\u0161\u00ed s\u00fad), alleging that the applicant had not proved that he had a \u201cfascist past\u201d, and that the City Court had not established the meaning of that term. Mr Slobodn\u00edk argued that he had been summoned to the training course in Sekule by an order and that he had left it at the first opportunity after he had learned about its real purpose. He also explained that martial law had been in force at the material time and that people had been unlawfully executed or detained. Members of the Hlinka Youth had been incorporated in the armed forces by a presidential order and had fallen under military judicial and disciplinary rules. The plaintiff maintained that he had done nothing against his homeland or the anti-fascist allies and concluded that the applicant\u2019s statement and poem were defamatory.",
  "21.  The applicant contended, in particular, that the courts should abandon their established practice according to which the defendant has to prove the truthfulness of his statements in defamation proceedings. He maintained that the burden of proof should be shifted onto the plaintiff or shared between the parties. The applicant further argued that his statement was a value judgment based on the undisputed facts that the plaintiff had been a member of the Hlinka Youth and that he had attended a terrorist training course in Sekule. It was irrelevant to what extent the plaintiff had been involved in the activities of the Hlinka Youth or for how long he had been a member of it. What mattered was that the plaintiff had voluntarily joined the organisation and that, after his alleged exclusion from the training course in Sekule, he had undertaken, as shown by the Soviet military tribunal\u2019s judgment of 19 May 1945, to provide information on the movements of Soviet troops to the headquarters of the Hlinka Youth. The applicant therefore proposed that the appeal be dismissed.",
  "22.  On 23 March 1994 the Supreme Court reversed the first-instance judgment, ruling as follows:\n\u201c... [the applicant] has to accept that ... Du\u0161an Slobodn\u00edk will distribute, if he thinks fit, to the Press Agency of the Slovak Republic as well as to five newspapers of his choice, both in Slovakia and abroad, the following declaration to be published at [the applicant\u2019s] expense:\n  \u2018(1)  [The applicant\u2019s] statement addressed to [the Public Information Service] and published in daily newspapers on 30 July 1992 which reads: \u201c...This year Mr Slobodn\u00edk became the Slovak Republic\u2019s Minister for Culture and Education and the next thing was that his fascist past came out in public ... Does Mr Slobodn\u00edk think that Slovakia is some special exception and that it is the only country having the right to revise the philosophy of the Nuremberg trials, which is binding on the post-war development of all other European countries? ...\u201d\n  (2)  The occasional poem ... entitled \u201cGood night, my beloved\u201d in its part \u201c... In Bratislava the prosecutor rules again. And rule by one party is above the law. A member of the SS and a member of the \u0160TB embraced each other ...\u201d \n  ... represent a gross slander and disparagement of the civil honour and life, and an unjustified interference with the personality of the plaintiff Du\u0161an Slobodn\u00edk.\u2019\n...\n  (4)  [The applicant] is liable to pay SKK 200,000 to the plaintiff in respect of non-pecuniary damage. ...\u2019 \u201d",
  "23.  The applicant was also ordered to pay costs and the other party\u2019s expenses.",
  "24.  The Supreme Court noted that the plaintiff had described the relevant events in his book Paragraph: Polar Circle before the dispute concerning his past had arisen, and that no other relevant facts had been established in the course of the proceedings.",
  "25.  In the appellate court\u2019s view, the term \u201cfascist past\u201d was equivalent to the statement that a person was a fascist in the past. The court considered that the applicant himself had given a restrictive interpretation of that term in connection with the plaintiff, namely the interpretation according to the philosophy of the Nuremberg trials. This philosophy was derived from the multilateral agreement of 8 August 1945, which included also the statute of the International Military Tribunal, and which had become part of the Czechoslovakian legal order on 2 October 1947. The Supreme Court held that it was bound by the principle of individual responsibility set out in that agreement.",
  "26.  The Supreme Court further studied all available documents and evidence used during the Nuremberg trials relating to Slovakia. It found no reference in those documents to the Hlinka Youth in connection with fascist organisations. It established that the propagation or implementation of fascist theories had not been inherent in the statutory rules and regulations governing the Hlinka Youth. If some persons had abused the Christian principles on which the organisation had been built, this had contravened the rules then in force. Such persons and, as the case might be, those who had let themselves be abused for criminal purposes, were individually responsible. However, such was not the case of the plaintiff. The Supreme Court accepted the latter\u2019s argument that he had learned about the character of the training course in Sekule only after he had started attending it.",
  "27.  The appellate court found irrelevant the reference, in the first-instance court\u2019s judgment, to Presidential Decree no. 5/1945 of 19 May 1945 as that decree had only concerned property, in that it had placed under national administration the property of persons whom the State had considered unreliable.",
  "28.  The Supreme Court recalled that, at the relevant time, criminal and moral liability had been governed by Order no. 33 on the punishment of fascist criminals, occupants, traitors and collaborators and on the establishment of the people\u2019s judiciary adopted by the Slovakian National Council on 15 May 1945 and also by Presidential Decree no. 16/1945 of 19 June 1945 on the punishment of Nazi criminals, traitors and their assistants and on extra-ordinary people\u2019s courts. These rules were partly based on the principle of collective liability, but they did not mention the Hlinka Youth.",
  "29.  As regards the poem by the applicant, the Supreme Court noted that it was dated 17 July 1992, that is, the day on which the sovereignty of the Slovak Republic had been proclaimed from the balcony of the Slovakian National Council, where Mr Slobodn\u00edk had also been present. Shortly afterwards, the applicant had written his statement concerning Mr Slobodn\u00edk\u2019s past and two journalists had interpreted the poem as a description of the scene during the proclamation. They had alleged that by \u201cmember of the SS\u201d the applicant had meant to designate Mr Slobodn\u00edk. The court therefore concluded that the applicant had infringed the plaintiff\u2019s personality rights by his poem as well as by his statement of 29 July 1992.",
  "30.  The applicant\u2019s request that the burden of proof in the case should be shifted onto the plaintiff or at least shared between the parties was not accepted as it had no basis in domestic law and practice. The Supreme Court concluded that the applicant had not proved that Mr Slobodn\u00edk had been a fascist in the past, holding that the latter had joined the Hlinka Youth because he had wanted to participate in sports activities and had not been motivated by fascist sympathies. As to the training course in Sekule, it found that Mr Slobodn\u00edk had not completed it, and it was irrelevant whether he had been excluded or had left it on his own initiative. The only relevant fact was that the plaintiff\u2019s past could not be considered fascist from that point of view.",
  "31.  The applicant filed an appeal on points of law alleging, inter alia, a violation of his rights under Article 10 of the Convention. He claimed that the Supreme Court should have concluded from the relevant provisions of Presidential Decree no. 5/1945 that the Hlinka Youth was a fascist organisation and that, in accordance with the relevant provisions of the Slovakian National Council\u2019s Orders nos. 1/1944 and 4/1944, participation in any activity within the Hlinka Youth was to be considered as participation in an unlawful fascist organisation. He further complained that the Supreme Court had not established with sufficient certainty whether the plaintiff had actually been excluded from the training course in Sekule, and whether he had undertaken to carry out terrorist activities or not.",
  "32.  On 25 May 1995 a different Chamber of the Supreme Court sitting as a court of cassation upheld the part of the appeal judgment of 23 March 1994 according to which the plaintiff was entitled to arrange for publication of the text set out in it and concerning the applicant\u2019s statement of 29 July 1992. As for the remainder, the court of cassation quashed both the first and second-instance judgments and sent the case back to the Bratislava City Court.",
  "33.  The court of cassation did not share the applicant\u2019s view that the plaintiff should be required to prove that the applicant\u2019s allegations were untrue. It further held that a person could be considered as having a fascist past only if he or she had propagated or practised fascism in an active manner. Mere membership of an organisation and participation in a terrorist training course which had not been followed by any practical actions could not be characterised as a fascist past.",
  "34.  As the applicant had failed to prove that the plaintiff had a fascist past within the above meaning, the court found that his statement had infringed without justification the plaintiff\u2019s personality rights. In the judgment, the court admitted that Slovakian law characterised the Hlinka Youth as a fascist organisation. It recalled, however, that the relevant legal rules, including those relied on by the applicant, applied to natural persons only where justified by their specific actions. Applying those rules to all members of such organisations without considering their actual deeds would entail the recognition of their collective guilt. It recalled that children over the age of 6 had been admitted to the Hlinka Youth.",
  "35.  The court considered that the applicant\u2019s argument according to which his statement was a value judgment could only have been accepted if the applicant had expressly referred, in that statement, to the particular facts on which such a value judgment was based. The court stated, inter alia:\n\u201cIndicating that the plaintiff has had a fascist past is not a value judgment based on an analysis of facts, but an allegation (statement) made without any concurrent justification of factual circumstances from which a conclusion can be inferred by the person making the judgment. It could have been a value judgment if the statement [of the applicant] had been accompanied by reference to the [plaintiff\u2019s] membership of the Hlinka Youth and his participation in the training course, namely, to the activities which the person making the judgment considers to constitute a fascist past. Only such a statement, based on circumstantial facts used by the person making the judgment, would be a value judgment the truthfulness of which would not require any proof. Only such an interpretation will guarantee a balance between the freedom of expression and the right to the protection of [a person\u2019s] reputation within the meaning of Article 10 of the Convention.\u201d",
  "36.  The court then found the restriction on the applicant\u2019s freedom of expression compatible with the requirements of Article 10 \u00a7 2 of the Convention as it was necessary for the protection of the plaintiff\u2019s reputation in accordance with Articles 11 et seq. of the Civil Code.",
  "37.  As to the poem, the court of cassation quashed both the first and second-instance judgments for lack of evidence and held that in further proceedings the plaintiff would have to prove that the applicant had referred to him in the poem. It also quashed the part of the appeal concerning compensation for non-pecuniary damage and costs since their award depended on an assessment of both the interferences complained of by the plaintiff.",
  "38.  On 15 April 1996 the Bratislava City Court reached a new decision on the remainder of the case. It stayed the proceedings as far as the poem was concerned on the ground that the plaintiff had withdrawn that part of the action.",
  "39.  The City Court further dismissed the claim in respect of non-pecuniary damage as it did not find it established that the applicant\u2019s statement had considerably diminished the plaintiff\u2019s dignity and position in society within the meaning of Article 13 \u00a7 2 of the Civil Code. In its view, the plaintiff had failed to show that the considerable publicity concerning his person had arisen as a result of the applicant\u2019s statement and not, as the case might be, as a consequence of newspaper articles and the plaintiff\u2019s book published prior to the applicant\u2019s statement.",
  "40.  Having considered to what extent the parties had been successful in the proceedings, the City Court ordered the plaintiff to pay SKK 56,780 to the applicant in reimbursement of the relevant part of the latter\u2019s costs. The applicant and the plaintiff were further ordered to pay respectively SKK 875 and 2,625 in reimbursement of the costs paid in advance by the court.",
  "41.  On 25 November 1998 the Supreme Court upheld the decision of the Bratislava City Court to discontinue the proceedings in respect of the poem and to dismiss the plaintiff\u2019s claim for non-pecuniary damage. The Supreme Court held that neither party was entitled to have the costs reimbursed. It further ordered each party to pay half of the costs paid in advance by the State, namely SKK 1,750. Mr Slobodn\u00edk filed an appeal on points of law. The proceedings are pending."
 ],
 "allegedly_violated_articles": ["14", "10", "9", "36"], 
 "violated_articles": ["10"],
 "silver_rationales": [27],
 "gold_rationales": []
}
```

### Data Fields

`case_id`: The official ID of the case in the HUDOC database.\
`case_no`: The number (ID) of the original application.\
`title`: The title of the case in the form of applicant vs. defendant.\
`facts`: The paragraphs (facts) of the case.\
`allegedly_violated_articles`: The ECHR articles under discussion (*Allegedly violated articles*).\
`violated_articles`: The list of allegedly violated ECHR articles that found to be violated by the court (judges).\
`silver_rationales`: Indices of the paragraphs (facts) that are present in the court's assessment.\
`gold_rationales`: Indices of the paragraphs (facts) that support alleged violations, according to a legal expert.

### Data Splits

| Split         | No of ECtHR cases                         | Silver rationales ratio | Avg. allegations / case |
| ------------------- | ------------------------------------  |  --- | --- |
| Train | 9,000 | 24% | 1.8 |
|Development | 1,000 | 30% | 1.7 |
|Test | 1,000 | 31% | 1.7 |

## Dataset Creation

### Curation Rationale

The dataset was curated by Chalkidis et al. (2021).\
The annotations for the gold rationales are available thanks to Dimitris Tsarapatsanis (Lecturer, York Law School).

### Source Data

#### Initial Data Collection and Normalization

The original data are available at HUDOC database (https://hudoc.echr.coe.int/eng) in an unprocessed format. The data were downloaded and all information was extracted from the HTML files and several JSON metadata files.

#### Who are the source language producers?

[More Information Needed]

### Annotations

#### Annotation process

* The original documents are available in HTML format at HUDOC database (https://hudoc.echr.coe.int/eng), except the gold rationales. The metadata are provided by additional JSON files, produced by REST services.
* The annotations for the gold rationales are available thanks to Dimitris Tsarapatsanis (Lecturer, York Law School).


#### Who are the annotators?

Dimitris Tsarapatsanis (Lecturer, York Law School).

### Personal and Sensitive Information

Privacy statement / Protection of personal data from HUDOC (https://www.echr.coe.int/Pages/home.aspx?p=privacy)

```
The Court complies with the Council of Europe's policy on protection of personal data, in so far as this is consistent with exercising its functions under the European Convention on Human Rights.

The Council of Europe is committed to respect for private life. Its policy on protection of personal data is founded on the Secretary General’s Regulation of 17 April 1989 outlining a data protection system for personal data files in the Council of Europe. 

Most pages of the Council of Europe site require no personal information except in certain cases to allow requests for on-line services to be met. In such cases, the information is processed in accordance with the Confidentiality policy described below.
```

## Considerations for Using the Data

### Social Impact of the Dataset

The publication of this dataset complies with the ECtHR data policy (https://www.echr.coe.int/Pages/home.aspx?p=privacy).

By no means do we aim to build a `robot' lawyer or judge, and we acknowledge the possible harmful impact (Angwin et al., 2016, Dressel et al., 2018) of irresponsible deployment. 
Instead, we aim to support fair and explainable AI-assisted judicial decision making and empirical legal studies. 

For example, automated services can help applicants (plaintiffs) identify alleged violations that are supported by the facts of a case. They can help judges identify more quickly facts that support the alleged violations, contributing towards more informed judicial decision making (Zhong et al., 2020). They can also help legal experts identify previous cases related to particular allegations, helping analyze case law (Katz et al., 2012).  

Also, consider ongoing critical research on responsible AI (Elish et al., 2021) that aims to provide explainable and fair  systems to support human experts.

### Discussion of Biases

Consider the work of Chalkidis et al. (2019) for the identification of demographic bias by models.

### Other Known Limitations

N/A

## Additional Information

### Dataset Curators

Ilias Chalkidis and Dimitris Tsarapatsanis

### Licensing Information

**CC BY-NC-SA (Creative Commons / Attribution-NonCommercial-ShareAlike)**

Read  more: https://creativecommons.org/licenses/by-nc-sa/4.0/.

### Citation Information

*Ilias Chalkidis, Manos Fergadiotis, Dimitrios Tsarapatsanis, Nikolaos Aletras, Ion Androutsopoulos and Prodromos Malakasiotis. Paragraph-level Rationale Extraction through Regularization: A case study on European Court of Human Rights Cases.* 
*Proceedings of the Annual Conference of the North American Chapter of the Association for Computational Linguistics (NAACL 2021). Mexico City, Mexico. 2021.*

```
@InProceedings{chalkidis-et-al-2021-ecthr,
    title = "Paragraph-level Rationale Extraction through Regularization: A case study on European Court of Human Rights Cases",
    author = "Chalkidis, Ilias and Fergadiotis, Manos and Tsarapatsanis, Dimitrios and Aletras, Nikolaos and Androutsopoulos, Ion and Malakasiotis, Prodromos",
    booktitle = "Proceedings of the Annual Conference of the North American Chapter of the Association for Computational Linguistics",
    year = "2021",
    address = "Mexico City, Mexico",
    publisher = "Association for Computational Linguistics"
}
```

*Ilias Chalkidis, Ion Androutsopoulos and Nikolaos Aletras. Neural Legal Judgment Prediction in English.*
*Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL 2019). Florence, Italy. 2019.*

```
@InProceedings{chalkidis-etal-2019-neural,
    title = "Neural Legal Judgment Prediction in {E}nglish",
    author = "Chalkidis, Ilias  and Androutsopoulos, Ion  and Aletras, Nikolaos",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1424",
    doi = "10.18653/v1/P19-1424",
    pages = "4317--4323"
}
```

### Contributions

Thanks to [@iliaschalkidis](https://github.com/iliaschalkidis) for adding this dataset.
