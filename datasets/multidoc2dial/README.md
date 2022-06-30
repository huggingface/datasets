---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
- expert-generated
language:
- en
license:
- apache-2.0
multilinguality:
- monolingual
pretty_name: MultiDoc2Dial
size_categories:
- 10K<n<100K
- 1K<n<10K
- n<1K
source_datasets:
- extended|doc2dial
task_categories:
- question-answering
task_ids:
- open-domain-qa
paperswithcode_id: multidoc2dial
configs:
- dialogue_domain
- document_domain
- multidoc2dial
---

# Dataset Card for MultiDoc2Dial

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

- **Homepage:** https://doc2dial.github.io/multidoc2dial/
- **Repository:** https://github.com/IBM/multidoc2dial
- **Paper:** https://arxiv.org/pdf/2109.12595.pdf
- **Leaderboard:**
- **Point of Contact:** sngfng@gmail.com

### Dataset Summary

MultiDoc2Dial is a new task and dataset on modeling goal-oriented dialogues grounded in multiple documents. 
Most previous works treat document-grounded dialogue modeling as a machine reading comprehension task based on a
single given document or passage. We aim to address more realistic scenarios where a goal-oriented information-seeking
conversation involves multiple topics, and hence is grounded on different documents. 

### Supported Tasks and Leaderboards

> Supported Task: Open domain question answering, document-grounded dialogue, passage retrieval

> Leaderboard:

### Languages

English

## Dataset Structure

### Data Instances

Sample data instance for `multidoc2dial` :
```
{
    "id": "8df07b7a98990db27c395cb1f68a962e_1", 
    "title": "Top 5 DMV Mistakes and How to Avoid Them#3_0", 
    "context": "Many DMV customers make easily avoidable mistakes that cause them significant problems, including encounters with law enforcement and impounded vehicles. Because we see customers make these mistakes over and over again , we are issuing this list of the top five DMV mistakes and how to avoid them. \n\n1. Forgetting to Update Address \nBy statute , you must report a change of address to DMV within ten days of moving. That is the case for the address associated with your license, as well as all the addresses associated with each registered vehicle, which may differ. It is not sufficient to only: write your new address on the back of your old license; tell the United States Postal Service; or inform the police officer writing you a ticket. If you fail to keep your address current , you will miss a suspension order and may be charged with operating an unregistered vehicle and/or aggravated unlicensed operation, both misdemeanors. This really happens , but the good news is this is a problem that is easily avoidable. Learn more about how to change the address on your license and registrations [1 ] \n\n2. Leaving the State Without Notifying DMV \nStates communicate with each other , so when you move to another state, be sure to tie up any loose ends regarding your New York State license or registration. That means resolving any unanswered tickets, suspensions or revocations, and surrendering your license plates to NYS when you get to your new home state. A license suspension or revocation here could mean that your new home state will not issue you a license there. Remember , it is important to notify DMV of your new address so that any possible mail correspondence can reach you. Also , turning in your plates is important to avoid an insurance lapse. \n\n3. Letting Insurance Lapse \nBecause we all pay indirectly for crashes involving uninsured motorists , New York State requires every motorist to maintain auto insurance every single day a vehicle is registered. DMV works with insurance companies to electronically monitor your insurance coverage , and we know when coverage is dropped for any reason. When that happens , we mail you an insurance inquiry letter to allow you to clear up the problem. We send 500,000 inquiry letters a year. If the inquiry letter does not resolve the problem , we must suspend the vehicle registration and , if it persists, your driver license!We suspend 300,000 registrations a year for failure to maintain insurance. If you fail to maintain an updated address with us , you won t learn that you have an insurance problem , and we will suspend your registration and license. Make sure you turn in your vehicle s license plates at DMV before you cancel your insurance policy. Insurance policies must be from a company licensed in New York State. Learn more about Insurances Lapes [2] and How to Surrender your Plates [3 ] \n\n4. Understanding how Much Traffic Points Cost \nDMV maintains a point system to track dangerous drivers. Often , motorists convicted of a traffic ticket feel they have resolved all their motoring issues with the local court, but later learn that the Driver Responsibility Assessment DRA is a separate DMV charge based on the total points they accumulate. The $300 DRA fee can be paid in $100 annual installments over three years. Motorists who fail to maintain an updated address with DMV may resolve their tickets with the court, but never receive their DRA assessment because we do not have their new address on record. Failure to pay the DRA will result in a suspended license. Learn more about About the NYS Driver Point System [4] and how to Pay Driver Responsibility Assessment [5 ] \n\n5. Not Bringing Proper Documentation to DMV Office \nAbout ten percent of customers visiting a DMV office do not bring what they need to complete their transaction, and have to come back a second time to finish their business. This can be as simple as not bringing sufficient funds to pay for a license renewal or not having the proof of auto insurance required to register a car. Better yet , don t visit a DMV office at all, and see if your transaction can be performed online, like an address change, registration renewal, license renewal, replacing a lost title, paying a DRA or scheduling a road test. Our award - winning website is recognized as one of the best in the nation. It has all the answers you need to efficiently perform any DMV transaction. Consider signing up for our MyDMV service, which offers even more benefits. Sign up or log into MyDMV [6 ] ", 
    "question": "Hello, I forgot o update my address, can you help me with that?[SEP]", 
    "da": "query_condition", 
    "answers": 
        {
          "text": ['you must report a change of address to DMV within ten days of moving. That is the case for the address associated with your license, as well as all the addresses associated with each registered vehicle, which may differ. "], 
          "answer_start": [346]
        }, 
    "utterance": "hi, you have to report any change of address to DMV within 10 days after moving. You should do this both for the address associated with your license and all the addresses associated with all your vehicles.", 
    "domain": "dmv"
}
```

Sample data instance for `document_domain` :

```
{
    "domain": "ssa",
    "doc_id": "Benefits Planner: Survivors | Planning For Your Survivors | Social Security Administration#1_0",
    "title": "Benefits Planner: Survivors | Planning For Your Survivors | Social Security Administration#1",
    "doc_text": "\n\nBenefits Planner: Survivors | Planning For Your Survivors \nAs you plan for the future , you'll want to think about what your family would need if you should die now. Social Security can help your family if you have earned enough Social Security credits through your work. You can earn up to four credits each year. In 2019 , for example , you earn one credit for each $1,360 of wages or self - employment income. When you have earned $5,440 , you have earned your four credits for the year. The number of credits needed to provide benefits for your survivors depends on your age when you die. No one needs more than 40 credits 10 years of work to be eligible for any Social Security benefit. But , the younger a person is , the fewer credits they must have for family members to receive survivors benefits. Benefits can be paid to your children and your spouse who is caring for the children even if you don't have the required number of credits. They can get benefits if you have credit for one and one - half years of work 6 credits in the three years just before your death. \n\nFor Your Widow Or Widower \nThere are about five million widows and widowers receiving monthly Social Security benefits based on their deceased spouse's earnings record. And , for many of those survivors, particularly aged women, those benefits are keeping them out of poverty. Widows and widowers can receive : reduced benefits as early as age 60 or full benefits at full retirement age or older. benefits as early as age 50 if they're disabled AND their disability started before or within seven years of your death. benefits at any age , if they have not remarried , and if they take care of your child who is under age 16 or disabled and receives benefits on your record. If applying for disability benefits on a deceased worker s record , they can speed up the application process if they complete an Adult Disability Report and have it available at the time of their appointment. We use the same definition of disability for widows and widowers as we do for workers. \n\nFor Your Surviving Divorced Spouse \nIf you have a surviving divorced spouse , they could get the same benefits as your widow or widower provided that your marriage lasted 10 years or more. Benefits paid to a surviving divorced spouse won't affect the benefit amounts your other survivors will receive based on your earnings record. If your former spouse is caring for your child who is under age 16 or disabled and gets benefits on your record , they will not have to meet the length - of - marriage rule. The child must be your natural or legally adopted child. \n\nFor Your Children \nYour unmarried children who are under 18 up to age 19 if attending elementary or secondary school full time can be eligible to receive Social Security benefits when you die. And your child can get benefits at any age if they were disabled before age 22 and remain disabled. Besides your natural children , your stepchildren, grandchildren, step grandchildren or adopted children may receive benefits under certain circumstances. For further information , view our publication. \n\nFor Your Parents \nYou must have been providing at least half of your parent s support and your parent must not be eligible to receive a retirement benefit that is higher than the benefit we could pay on your record. Generally, your parent also must not have married after your death ; however, there are some exceptions. In addition to your natural parent , your stepparent or adoptive parent may receive benefits if they became your parent before you were age 16. \n\nHow Much Would Your Survivors Receive \nHow much your family could receive in benefits depends on your average lifetime earnings. The higher your earnings were , the higher their benefits would be. We calculate a basic amount as if you had reached full retirement age at the time you die. These are examples of monthly benefit payments : Widow or widower, full retirement age or older 100 percent of your benefit amount ; Widow or widower , age 60 to full retirement age 71 to 99 percent of your basic amount ; Disabled widow or widower , age 50 through 59 71 percent ; Widow or widower , any age, caring for a child under age 16 75 percent ; A child under age 18 19 if still in elementary or secondary school or disabled 75 percent ; and Your dependent parent , age 62 or older : One surviving parent 82 percent. Two surviving parents 75 percent to each parent. Percentages for a surviving divorced spouse would be the same as above. There may also be a special lump - sum death payment. \n\nMaximum Family Amount \nThere's a limit to the amount that family members can receive each month. The limit varies , but it is generally equal to between 150 and 180 percent of the basic benefit rate. If the sum of the benefits payable to family members is greater than this limit , the benefits will be reduced proportionately. Any benefits paid to a surviving divorced spouse based on disability or age won't count toward this maximum amount. Get your online or check our Benefit Calculators for an estimate of the benefits your family could receive if you died right now. \n\nOther Things You Need To Know \nThere are limits on how much survivors may earn while they receive benefits. Benefits for a widow, widower, or surviving divorced spouse may be affected by several additional factors : If your widow, widower, or surviving divorced spouse remarries before they reach age 60 age 50 if disabled , they cannot receive benefits as a surviving spouse while they're married. If your widow, widower, or surviving divorced spouse remarries after they reach age 60 age 50 if disabled , they will continue to qualify for benefits on your Social Security record. However , if their current spouse is a Social Security beneficiary , they may want to apply for spouse's benefits on their record. If that amount is more than the widow's or widower's benefit on your record , they will receive a combination of benefits that equals the higher amount. If your widow, widower, or surviving divorced spouse receives benefits on your record , they can switch to their own retirement benefit as early as age 62. This assumes they're eligible for retirement benefits and their retirement rate is higher than their rate as a widow, widower, or surviving divorced spouse. In many cases , a widow or widower can begin receiving one benefit at a reduced rate and then, at full retirement age, switch to the other benefit at an unreduced rate. If your widow, widower, or surviving divorced spouse will also receive a pension based on work not covered by Social Security, such as government or foreign work , their Social Security benefits as a survivor may be affected. ",
    "spans": [
        {
            "id_sp": "1",
            "tag": "h2",
            "start_sp": 0,
            "end_sp": 61,
            "text_sp": "\n\nBenefits Planner: Survivors | Planning For Your Survivors \n",
            "title": "Benefits Planner: Survivors | Planning For Your Survivors",
            "parent_titles": {
                "id_sp": [],
                "text": [],
                "level": []
            },
            "id_sec": "t_0",
            "start_sec": 0,
            "text_sec": "\n\nBenefits Planner: Survivors | Planning For Your Survivors \n",
            "end_sec": 61
        },
        {
            "id_sp": "2",
            "tag": "u",
            "start_sp": 61,
            "end_sp": 90,
            "text_sp": "As you plan for the future , ",
            "title": "Benefits Planner: Survivors | Planning For Your Survivors",
            "parent_titles": {
                "id_sp": [],
                "text": [],
                "level": []
            },
            "id_sec": "1",
            "start_sec": 61,
            "text_sec": "As you plan for the future , you'll want to think about what your family would need if you should die now. Social Security can help your family if you have earned enough Social Security credits through your work. ",
            "end_sec": 274
        },
        {
            "id_sp": "3",
            "tag": "u",
            "start_sp": 90,
            "end_sp": 168,
            "text_sp": "you'll want to think about what your family would need if you should die now. ",
            "title": "Benefits Planner: Survivors | Planning For Your Survivors",
            "parent_titles": {
                "id_sp": [],
                "text": [],
                "level": []
            },
            "id_sec": "1",
            "start_sec": 61,
            "text_sec": "As you plan for the future , you'll want to think about what your family would need if you should die now. Social Security can help your family if you have earned enough Social Security credits through your work. ",
            "end_sec": 274
        }
    ],
    "doc_html_ts": "<main><section><div><h2 sent_id=\"1\" text_id=\"1\">Benefits Planner: Survivors | Planning For Your Survivors</h2></div></section><section><div><article><section><div tag_id=\"1\"><u sent_id=\"2\" tag_id=\"1\"><u sent_id=\"2\" tag_id=\"1\" text_id=\"2\">As you plan for the future ,</u><u sent_id=\"2\" tag_id=\"1\" text_id=\"3\">you 'll want to think about what your family would need if you should die now .</u></u><u sent_id=\"3\" tag_id=\"1\"><u sent_id=\"3\" tag_id=\"1\" text_id=\"4\">Social Security can help your family if you have earned enough Social Security credits through your work .</u></u></div><div tag_id=\"2\"><u sent_id=\"4\" tag_id=\"2\"><u sent_id=\"4\" tag_id=\"2\" text_id=\"5\">You can earn up to four credits each year .</u></u><u sent_id=\"5\" tag_id=\"2\"><u sent_id=\"5\" tag_id=\"2\" text_id=\"6\">In 2019 ,</u><u sent_id=\"5\" tag_id=\"2\" text_id=\"7\">for example ,</u><u sent_id=\"5\" tag_id=\"2\" text_id=\"8\">you earn one credit for each $ 1,360 of wages or self - employment income .</u></u><u sent_id=\"6\" tag_id=\"2\"><u sent_id=\"6\" tag_id=\"2\" text_id=\"9\">When you have earned $ 5,440 ,</u><u sent_id=\"6\" tag_id=\"2\" text_id=\"10\">you have earned your four credits for the year .</u></u></div><div tag_id=\"3\"><u sent_id=\"7\" tag_id=\"3\"><u sent_id=\"7\" tag_id=\"3\" text_id=\"11\">The number of credits needed to provide benefits for your survivors depends on your age when you die .</u></u><u sent_id=\"8\" tag_id=\"3\"><u sent_id=\"8\" tag_id=\"3\" text_id=\"12\">No one needs more than 40 credits 10 years of work to be eligible for any Social Security benefit .</u></u><u sent_id=\"9\" tag_id=\"3\"><u sent_id=\"9\" tag_id=\"3\" text_id=\"13\">But ,</u><u sent_id=\"9\" tag_id=\"3\" text_id=\"14\">the younger a person is ,</u><u sent_id=\"9\" tag_id=\"3\" text_id=\"15\">the fewer credits they must have for family members to receive survivors benefits .</u></u></div><div tag_id=\"4\"><u sent_id=\"10\" tag_id=\"4\"><u sent_id=\"10\" tag_id=\"4\" text_id=\"16\">Benefits can be paid to your children and your spouse who is caring for the children even if you do n't have the required number of credits .</u></u><u sent_id=\"11\" tag_id=\"4\"><u sent_id=\"11\" tag_id=\"4\" text_id=\"17\">They can get benefits if you have credit for one and one - half years of work 6 credits in the three years just before your death .</u></u></div></section><section><h3 sent_id=\"12\" text_id=\"18\">For Your Widow Or Widower</h3><div tag_id=\"5\"><u sent_id=\"13\" tag_id=\"5\"><u sent_id=\"13\" tag_id=\"5\" text_id=\"19\">There are about five million widows and widowers receiving monthly Social Security benefits based on their deceased spouse 's earnings record .</u></u><u sent_id=\"14\" tag_id=\"5\"><u sent_id=\"14\" tag_id=\"5\" text_id=\"20\">And ,</u><u sent_id=\"14\" tag_id=\"5\" text_id=\"21\">for many of those survivors , particularly aged women , those benefits are keeping them out of poverty .</u></u></div><div tag_id=\"6\"><u sent_id=\"15\" tag_id=\"6\"><u sent_id=\"15\" tag_id=\"6\" text_id=\"22\">Widows and widowers can receive :</u></u></div><ul class=\"browser-default\" tag_id=\"6\"><li tag_id=\"6\"><u sent_id=\"16\" tag_id=\"6\"><u sent_id=\"16\" tag_id=\"6\" text_id=\"23\">reduced benefits as early as age 60 or full benefits at full retirement age or older .</u></u></li><div>If widows or widowers qualify for retirement benefits on their own record, they can switch to their own retirement benefit as early as age 62.</div><li tag_id=\"6\"><u sent_id=\"17\" tag_id=\"6\"><u sent_id=\"17\" tag_id=\"6\" text_id=\"24\">benefits as early as age 50 if they 're disabled AND their disability started before or within seven years of your death .</u></u></li><div>If a widow or widower who is caring for your children receives Social Security benefits, they're still eligible if their disability starts before those payments end or within seven years after they end.</div><li tag_id=\"6\"><u sent_id=\"18\" tag_id=\"6\"><u sent_id=\"18\" tag_id=\"6\" text_id=\"25\">benefits at any age ,</u><u sent_id=\"18\" tag_id=\"6\" text_id=\"26\">if they have not remarried ,</u><u sent_id=\"18\" tag_id=\"6\" text_id=\"27\">and if they take care of your child who is under age 16 or disabled and receives benefits on your record .</u></u></li><div>If a widow or widower remarries <strong>after they reach age 60</strong> (age 50 if disabled), the remarriage will not affect their eligibility for survivors benefits.</div></ul><div>Widows, widowers, and surviving divorced spouses cannot apply online for survivors benefits. They should <a>contact Social Security</a> at <nobr><strong>1-800-772-1213</strong></nobr> (TTY <nobr><strong>1-800-325-0778</strong>) to request an appointment.</nobr></div><div tag_id=\"7\"><u sent_id=\"19\" tag_id=\"7\"><u sent_id=\"19\" tag_id=\"7\" text_id=\"28\">If applying for disability benefits on a deceased worker s record ,</u><u sent_id=\"19\" tag_id=\"7\" text_id=\"29\">they can speed up the application process if they complete an Adult Disability Report and have it available at the time of their appointment .</u></u></div><div tag_id=\"8\"><u sent_id=\"20\" tag_id=\"8\"><u sent_id=\"20\" tag_id=\"8\" text_id=\"30\">We use the same definition of disability for widows and widowers as we do for workers .</u></u></div></section><section><h3 sent_id=\"21\" text_id=\"31\">For Your Surviving Divorced Spouse</h3><div tag_id=\"9\"><u sent_id=\"22\" tag_id=\"9\"><u sent_id=\"22\" tag_id=\"9\" text_id=\"32\">If you have a surviving divorced spouse ,</u><u sent_id=\"22\" tag_id=\"9\" text_id=\"33\">they could get the same benefits as your widow or widower provided that your marriage lasted 10 years or more .</u></u></div><div>If your surviving divorced spouse qualifies for retirement benefits on their own record they can switch to their own retirement benefit as early as age 62.</div><div tag_id=\"10\"><u sent_id=\"23\" tag_id=\"10\"><u sent_id=\"23\" tag_id=\"10\" text_id=\"34\">Benefits paid to a surviving divorced spouse wo n't affect the benefit amounts your other survivors will receive based on your earnings record .</u></u></div><div>If your surviving divorced spouse remarries <strong>after they reach age 60</strong> (age 50 if disabled), the remarriage will not affect their eligibility for survivors benefits.</div><div tag_id=\"11\"><u sent_id=\"24\" tag_id=\"11\"><u sent_id=\"24\" tag_id=\"11\" text_id=\"35\">If your former spouse is caring for your child who is under age 16 or disabled and gets benefits on your record ,</u><u sent_id=\"24\" tag_id=\"11\" text_id=\"36\">they will not have to meet the length - of - marriage rule .</u></u><u sent_id=\"25\" tag_id=\"11\"><u sent_id=\"25\" tag_id=\"11\" text_id=\"37\">The child must be your natural or legally adopted child .</u></u></div><div>However, if they qualify for benefits as a surviving divorced mother or father who is caring for your child, their benefits may affect the amount of benefits your other survivors will receive based on your earnings record.</div></section><section><h3 sent_id=\"26\" text_id=\"38\">For Your Children</h3><div tag_id=\"12\"><u sent_id=\"27\" tag_id=\"12\"><u sent_id=\"27\" tag_id=\"12\" text_id=\"39\">Your unmarried children who are under 18 up to age 19 if attending elementary or secondary school full time can be eligible to receive Social Security benefits when you die .</u></u></div><div tag_id=\"13\"><u sent_id=\"28\" tag_id=\"13\"><u sent_id=\"28\" tag_id=\"13\" text_id=\"40\">And your child can get benefits at any age if they were disabled before age 22 and remain disabled .</u></u></div><div tag_id=\"14\"><u sent_id=\"29\" tag_id=\"14\"><u sent_id=\"29\" tag_id=\"14\" text_id=\"41\">Besides your natural children ,</u><u sent_id=\"29\" tag_id=\"14\" text_id=\"42\">your stepchildren , grandchildren , step grandchildren or adopted children may receive benefits under certain circumstances .</u></u><u sent_id=\"30\" tag_id=\"14\"><u sent_id=\"30\" tag_id=\"14\" text_id=\"43\">For further information ,</u><u sent_id=\"30\" tag_id=\"14\" text_id=\"44\">view our publication .</u></u></div></section><section><h3 sent_id=\"31\" text_id=\"45\">For Your Parents</h3><div tag_id=\"15\"><u sent_id=\"32\" tag_id=\"15\"><u sent_id=\"32\" tag_id=\"15\" text_id=\"46\">You must have been providing at least half of your parent s support and your parent must not be eligible to receive a retirement benefit that is higher than the benefit we could pay on your record .</u></u><u sent_id=\"33\" tag_id=\"15\"><u sent_id=\"33\" tag_id=\"15\" text_id=\"47\">Generally , your parent also must not have married after your death ;</u><u sent_id=\"33\" tag_id=\"15\" text_id=\"48\">however , there are some exceptions .</u></u></div><div tag_id=\"16\"><u sent_id=\"34\" tag_id=\"16\"><u sent_id=\"34\" tag_id=\"16\" text_id=\"49\">In addition to your natural parent ,</u><u sent_id=\"34\" tag_id=\"16\" text_id=\"50\">your stepparent or adoptive parent may receive benefits if they became your parent before you were age 16 .</u></u></div></section><section><h3 sent_id=\"35\" text_id=\"51\">How Much Would Your Survivors Receive</h3><div tag_id=\"17\"><u sent_id=\"36\" tag_id=\"17\"><u sent_id=\"36\" tag_id=\"17\" text_id=\"52\">How much your family could receive in benefits</u><u sent_id=\"36\" tag_id=\"17\" text_id=\"53\">depends on your average lifetime earnings .</u></u><u sent_id=\"37\" tag_id=\"17\"><u sent_id=\"37\" tag_id=\"17\" text_id=\"54\">The higher your earnings were ,</u><u sent_id=\"37\" tag_id=\"17\" text_id=\"55\">the higher their benefits would be .</u></u><u sent_id=\"38\" tag_id=\"17\"><u sent_id=\"38\" tag_id=\"17\" text_id=\"56\">We calculate a basic amount as if you had reached full retirement age at the time you die .</u></u></div><div>If you are already receiving reduced benefits when you die, survivors benefits are based on that amount.</div><div tag_id=\"18\"><u sent_id=\"39\" tag_id=\"18\"><u sent_id=\"39\" tag_id=\"18\" text_id=\"57\">These are examples of monthly benefit payments :</u></u></div><ul class=\"browser-default\" tag_id=\"18\"><li tag_id=\"18\"><u sent_id=\"40\" tag_id=\"18\"><u sent_id=\"40\" tag_id=\"18\" text_id=\"58\">Widow or widower , full retirement age or older 100 percent of your benefit amount ;</u></u></li><li tag_id=\"18\"><u sent_id=\"41\" tag_id=\"18\"><u sent_id=\"41\" tag_id=\"18\" text_id=\"59\">Widow or widower ,</u><u sent_id=\"41\" tag_id=\"18\" text_id=\"60\">age 60 to full retirement age 71 to 99 percent of your basic amount ;</u></u></li><li tag_id=\"18\"><u sent_id=\"42\" tag_id=\"18\"><u sent_id=\"42\" tag_id=\"18\" text_id=\"61\">Disabled widow or widower ,</u><u sent_id=\"42\" tag_id=\"18\" text_id=\"62\">age 50 through 59 71 percent ;</u></u></li><li tag_id=\"18\"><u sent_id=\"43\" tag_id=\"18\"><u sent_id=\"43\" tag_id=\"18\" text_id=\"63\">Widow or widower ,</u><u sent_id=\"43\" tag_id=\"18\" text_id=\"64\">any age , caring for a child under age 16 75 percent ;</u></u></li><li tag_id=\"18\"><u sent_id=\"44\" tag_id=\"18\"><u sent_id=\"44\" tag_id=\"18\" text_id=\"65\">A child under age 18 19 if still in elementary or secondary school or disabled 75 percent ;</u><u sent_id=\"44\" tag_id=\"18\" text_id=\"66\">and</u></u></li><li tag_id=\"18\"><div tag_id=\"18\"><u sent_id=\"48\" tag_id=\"18\"><u sent_id=\"48\" tag_id=\"18\" text_id=\"67\">Your dependent parent ,</u><u sent_id=\"48\" tag_id=\"18\" text_id=\"68\">age 62 or older :</u></u></div><ul class=\"browser-default\" tag_id=\"18\"><li tag_id=\"18\"><u sent_id=\"49\" tag_id=\"18\"><u sent_id=\"49\" tag_id=\"18\" text_id=\"69\">One surviving parent 82 percent .</u></u></li><li tag_id=\"18\"><u sent_id=\"50\" tag_id=\"18\"><u sent_id=\"50\" tag_id=\"18\" text_id=\"70\">Two surviving parents 75 percent to each parent .</u></u></li></ul></li></ul><div tag_id=\"19\"><u sent_id=\"51\" tag_id=\"19\"><u sent_id=\"51\" tag_id=\"19\" text_id=\"71\">Percentages for a surviving divorced spouse would be the same as above .</u></u></div><div tag_id=\"20\"><u sent_id=\"52\" tag_id=\"20\"><u sent_id=\"52\" tag_id=\"20\" text_id=\"72\">There may also be a special lump - sum death payment .</u></u></div><h3 sent_id=\"53\" text_id=\"73\">Maximum Family Amount</h3><div tag_id=\"21\"><u sent_id=\"54\" tag_id=\"21\"><u sent_id=\"54\" tag_id=\"21\" text_id=\"74\">There 's a limit to the amount that family members can receive each month .</u></u><u sent_id=\"55\" tag_id=\"21\"><u sent_id=\"55\" tag_id=\"21\" text_id=\"75\">The limit varies ,</u><u sent_id=\"55\" tag_id=\"21\" text_id=\"76\">but it is generally equal to between 150 and 180 percent of the basic benefit rate .</u></u></div><div tag_id=\"22\"><u sent_id=\"56\" tag_id=\"22\"><u sent_id=\"56\" tag_id=\"22\" text_id=\"77\">If the sum of the benefits payable to family members is greater than this limit ,</u><u sent_id=\"56\" tag_id=\"22\" text_id=\"78\">the benefits will be reduced proportionately .</u></u><u sent_id=\"57\" tag_id=\"22\"><u sent_id=\"57\" tag_id=\"22\" text_id=\"79\">Any benefits paid to a surviving divorced spouse based on disability or age wo n't count toward this maximum amount .</u></u></div><div tag_id=\"23\"><u sent_id=\"58\" tag_id=\"23\"><u sent_id=\"58\" tag_id=\"23\" text_id=\"80\">Get your online or check our Benefit Calculators for an estimate of the benefits your family could receive if you died right now .</u></u></div><h3 sent_id=\"59\" text_id=\"81\">Other Things You Need To Know</h3><div tag_id=\"24\"><u sent_id=\"60\" tag_id=\"24\"><u sent_id=\"60\" tag_id=\"24\" text_id=\"82\">There are limits on how much survivors may earn while they receive benefits .</u></u></div><div tag_id=\"25\"><u sent_id=\"61\" tag_id=\"25\"><u sent_id=\"61\" tag_id=\"25\" text_id=\"83\">Benefits for a widow , widower , or surviving divorced spouse may be affected by several additional factors :</u></u></div><div><a>If they remarry</a><section><div tag_id=\"26\"><u sent_id=\"62\" tag_id=\"26\"><u sent_id=\"62\" tag_id=\"26\" text_id=\"84\">If your widow , widower , or surviving divorced spouse remarries before they reach age 60 age 50 if disabled ,</u><u sent_id=\"62\" tag_id=\"26\" text_id=\"85\">they can not receive benefits as a surviving spouse while they 're married .</u></u></div><div tag_id=\"27\"><u sent_id=\"63\" tag_id=\"27\"><u sent_id=\"63\" tag_id=\"27\" text_id=\"86\">If your widow , widower , or surviving divorced spouse remarries after they reach age 60 age 50 if disabled ,</u><u sent_id=\"63\" tag_id=\"27\" text_id=\"87\">they will continue to qualify for benefits on your Social Security record .</u></u></div><div tag_id=\"28\"><u sent_id=\"64\" tag_id=\"28\"><u sent_id=\"64\" tag_id=\"28\" text_id=\"88\">However ,</u><u sent_id=\"64\" tag_id=\"28\" text_id=\"89\">if their current spouse is a Social Security beneficiary ,</u><u sent_id=\"64\" tag_id=\"28\" text_id=\"90\">they may want to apply for spouse 's benefits on their record .</u></u><u sent_id=\"65\" tag_id=\"28\"><u sent_id=\"65\" tag_id=\"28\" text_id=\"91\">If that amount is more than the widow 's or widower 's benefit on your record ,</u><u sent_id=\"65\" tag_id=\"28\" text_id=\"92\">they will receive a combination of benefits that equals the higher amount .</u></u></div></section></div><div><a>If they're eligible for retirement benefits on their own record</a><section><div tag_id=\"29\"><u sent_id=\"66\" tag_id=\"29\"><u sent_id=\"66\" tag_id=\"29\" text_id=\"93\">If your widow , widower , or surviving divorced spouse receives benefits on your record ,</u><u sent_id=\"66\" tag_id=\"29\" text_id=\"94\">they can switch to their own retirement benefit as early as age 62 .</u></u><u sent_id=\"67\" tag_id=\"29\"><u sent_id=\"67\" tag_id=\"29\" text_id=\"95\">This assumes they 're eligible for retirement benefits and their retirement rate is higher than their rate as a widow , widower , or surviving divorced spouse .</u></u></div><div tag_id=\"30\"><u sent_id=\"68\" tag_id=\"30\"><u sent_id=\"68\" tag_id=\"30\" text_id=\"96\">In many cases ,</u><u sent_id=\"68\" tag_id=\"30\" text_id=\"97\">a widow or widower can begin receiving one benefit at a reduced rate and then , at full retirement age , switch to the other benefit at an unreduced rate .</u></u></div><div><a>Full retirement age for retirement benefits</a> may not match full retirement age for survivors benefits.</div></section></div><div><a>If they will also receive a pension based on work not covered by Social Security</a><section><div tag_id=\"31\"><u sent_id=\"69\" tag_id=\"31\"><u sent_id=\"69\" tag_id=\"31\" text_id=\"98\">If your widow , widower , or surviving divorced spouse will also receive a pension based on work not covered by Social Security , such as government or foreign work ,</u><u sent_id=\"69\" tag_id=\"31\" text_id=\"99\">their Social Security benefits as a survivor may be affected .</u></u></div></section></div></section></article></div></section></main>",
    "doc_html_raw": "<main class=\"content\" id=\"content\" role=\"main\">\n\n<section>\n\n<div>\n<h2>Benefits Planner: Survivors | Planning For Your Survivors</h2>\n</div>\n</section>\n\n<section>\n\n<div>\n\n<div>\n\n\n</div>\n\n\n\n<article>\n<section>\n<p>As you plan for the future, you'll want to think about what your family would need if you should die now. Social Security can help your family if you have earned enough Social Security credits through your work.</p>\n<p><a>You can earn up to four credits each year</a>. In 2019, for example, you earn one credit for each $1,360 of wages or <a>self-employment</a> income. When you have earned $5,440, you have earned your four credits for the year.</p>\n<p>The number of credits needed to provide benefits for your survivors depends on your age when you die. No one needs more than 40 credits (10 years of work) to be eligible for any Social Security benefit. But, the younger a person is, the fewer credits they must have for family members to receive survivors benefits.</p>\n<p>Benefits can be paid to your children and your spouse who is caring for the children even if you don't have the required number of credits. They can get benefits if you have credit for one and one-half years of work (6 credits) in the three years just before your death.</p>\n</section>\n<section>\n<h3>For Your Widow Or Widower</h3>\n<p>There are about five million widows and widowers receiving monthly Social Security benefits based on their deceased spouse's earnings record. And, for many of those survivors, particularly aged women, those benefits are keeping them out of poverty. </p>\n<p>Widows and widowers can receive:</p>\n<ul class=\"browser-default\">\n<li>reduced benefits as early as age 60 or full benefits at <a>full retirement age</a> or older.</li>\n<div>\n                                If widows or widowers qualify for retirement benefits on their own record, they can switch to their own retirement benefit as early as age 62.\n                            </div>\n<li>benefits as early as age 50 if they're disabled AND their disability started before or within seven years of your death.</li>\n<div>\n                                If a widow or widower who is caring for your children receives Social Security benefits, they're still eligible if their disability starts before those payments end or within seven years after they end.\n                            </div>\n<li>benefits at any age, if they have not remarried, and if they take care of your child who is under age 16 or disabled and receives benefits on your record.</li>\n<div>\n                                If a widow or widower remarries <strong>after they reach age 60</strong> (age 50 if disabled), the remarriage will not affect their eligibility for survivors benefits.\n                            </div>\n</ul>\n<div>\n                            Widows, widowers, and surviving divorced spouses cannot apply online for survivors benefits. They should <a>contact Social Security</a> at <nobr><strong>1-800-772-1213</strong></nobr> (TTY <nobr><strong>1-800-325-0778</strong>) to request an appointment.</nobr>\n</div>\n<p>If applying for disability benefits on a deceased worker s record, they can speed up the application process if they complete an <a>Adult Disability Report</a> and have it available at the time of their appointment.</p>\n<p>We use the same <a>definition of disability</a> for widows and widowers as we do for workers.</p>\n</section>\n<section>\n<h3>For Your Surviving Divorced Spouse</h3>\n<p>If you have a surviving divorced spouse, they could get the same benefits as your widow or widower provided that your marriage lasted 10 years or more.</p>\n<div>\n                            If your surviving divorced spouse qualifies for retirement benefits on their own record they can switch to their own retirement benefit as early as age 62.\n                        </div>\n<p>Benefits paid to a surviving divorced spouse won't affect the benefit amounts your other survivors will receive based on your earnings record.</p>\n<div>\n                            If your surviving divorced spouse remarries <strong>after they reach age 60</strong> (age 50 if disabled), the remarriage will not affect their eligibility for survivors benefits.\n                        </div>\n<p>If your former spouse is caring for your child who is under age 16 or disabled and gets benefits on your record, they will not have to meet the length-of-marriage rule. The child must be your natural or legally adopted child.</p>\n<div>\n                            However, if they qualify for benefits as a surviving divorced mother or father who is caring for your child, their benefits may affect the amount of benefits your other survivors will receive based on your earnings record.\n                        </div>\n</section>\n<section>\n<h3>For Your Children</h3>\n<p>Your unmarried children who are under 18 (up to age 19 if attending elementary or secondary school full time) can be eligible to receive Social Security benefits when you die.</p>\n<p>And your child can get benefits at any age if they were disabled before age 22 and remain disabled.</p>\n<p>Besides your natural children, your stepchildren, grandchildren, step grandchildren or adopted children may receive benefits under certain circumstances. For further information, view our <a>publication</a>.</p>\n</section>\n<section>\n<h3>For Your Parents</h3>\n<p>You must have been providing at least half of your parent s support and your parent must not be eligible to receive a retirement benefit that is higher than the benefit we could pay on your record. Generally, your parent also must not have married after your death; however, there are some exceptions.</p>\n<p>In addition to your natural parent, your stepparent or adoptive parent may receive benefits if they became your parent before you were age 16.</p>\n</section>\n<section>\n<h3>How Much Would Your Survivors Receive</h3>\n<p>How much your family could receive in benefits depends on your average lifetime earnings. The higher your earnings were, the higher their benefits would be. We calculate a basic amount as if you had reached full retirement age at the time you die.</p>\n<div>\n                            If you are already receiving reduced benefits when you die, survivors benefits are based on that amount.\n                        </div>\n<p>These are examples of monthly benefit payments:</p>\n<ul class=\"browser-default\">\n<li>Widow or widower, <a>full retirement age</a> or older 100 percent of your benefit amount;</li>\n<li>Widow or widower, age 60 to <a>full retirement age</a> 71  to 99 percent of your basic amount;</li>\n<li>Disabled widow or widower, age 50 through 59 71  percent;</li>\n<li>Widow or widower, any age, caring for a child under age 16 75 percent;</li>\n<li>A child under age 18 (19 if still in elementary or secondary school) or disabled 75 percent; and</li>\n<li>Your dependent parent(s), age 62 or older:\n                                <ul class=\"browser-default\">\n<li>One surviving parent 82  percent.</li>\n<li>Two surviving parents 75 percent to each parent.</li>\n</ul>\n</li>\n</ul>\n<p>Percentages for a surviving divorced spouse would be the same as above.</p>\n<p>There may also be a <a>special lump-sum death payment</a>.</p>\n<h3>Maximum Family Amount</h3>\n<p>There's a limit to the amount that family members can receive each month. <a>The limit varies</a>, but it is generally equal to between 150 and 180 percent of the basic benefit rate.</p>\n<p>If the sum of the benefits payable to family members is greater than this limit, the benefits will be reduced proportionately. (Any benefits paid to a surviving divorced spouse based on disability or age won't count toward this maximum amount.)</p>\n<p>Get your <a></a> online or check our <a>Benefit Calculators</a> for an estimate of the benefits your family could receive if you died right now.</p>\n<h3>Other Things You Need To Know</h3>\n<p>There are <a>limits on how much survivors may earn</a> while they receive benefits.</p>\n<p>Benefits for a widow, widower, or surviving divorced spouse may be affected by several additional factors:</p>\n<div>\n<a>If they remarry</a>\n<section>\n<p>If your widow, widower, or surviving divorced spouse remarries before they reach age 60 (age 50 if disabled), they cannot receive benefits as a surviving spouse while they're married.</p>\n<p>If your widow, widower, or surviving divorced spouse remarries after they reach age 60 (age 50 if disabled), they will continue to qualify for benefits on your Social Security record.</p>\n<p>However, if their current spouse is a Social Security beneficiary, they may want to apply for spouse's benefits on their record. If that amount is more than the widow's or widower's benefit on your record, they will receive a combination of benefits that equals the higher amount.</p>\n</section>\n</div>\n<div>\n<a>If they're eligible for retirement benefits on their own record</a>\n<section>\n<p>If your widow, widower, or surviving divorced spouse receives benefits on your record, they can switch to their own retirement benefit as early as age 62. This assumes they're eligible for retirement benefits and their retirement rate is higher than their rate as a widow, widower, or surviving divorced spouse.</p>\n<p>In many cases, a widow or widower can begin receiving one benefit at a reduced rate and then, at full retirement age, switch to the other benefit at an unreduced rate.</p>\n<div>\n<a>Full retirement age for retirement benefits</a> may not match full retirement age for survivors benefits.\n                                </div>\n</section>\n</div>\n<div>\n<a>If they will also receive a pension based on work not covered by Social Security</a>\n<section>\n<p>If your widow, widower, or surviving divorced spouse will also receive a pension based on work not covered by Social Security, such as government or foreign work, <a>their Social Security benefits as a survivor may be affected</a>.</p>\n</section>\n</div>\n</section>\n</article>\n</div>\n</section>\n</main>"
}
```

Sample data instance for `dialogue_domain` :

```
{
    "dial_id": "8df07b7a98990db27c395cb1f68a962e",
    "domain": "dmv",
    "turns": [
        {
            "turn_id": 1,
            "role": "user",
            "da": "query_condition",
            "references": [
                {
                    "id_sp": "4",
                    "label": "precondition",
                    "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                }
            ],
            "utterance": "Hello, I forgot o update my address, can you help me with that?"
        },
        {
            "turn_id": 2,
            "role": "agent",
            "da": "respond_solution",
            "references": [
                {
                    "id_sp": "6",
                    "label": "solution",
                    "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                },
                {
                    "id_sp": "7",
                    "label": "solution",
                    "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                }
            ],
            "utterance": "hi, you have to report any change of address to DMV within 10 days after moving. You should do this both for the address associated with your license and all the addresses associated with all your vehicles."
        },
        {
            "turn_id": 3,
            "role": "user",
            "da": "query_solution",
            "references": [
                {
                    "id_sp": "56",
                    "label": "solution",
                    "doc_id": "Top 5 DMV Mistakes and How to Avoid Them#3_0"
                }
            ],
            "utterance": "Can I do my DMV transactions online?"
        }
    ]
}
```


### Data Fields

- `document_domain` contains the documents that are indexed by key `domain` and `doc_id` . Each document instance includes the following,
  
  - `domain`: the domain of the document;
  - `doc_id`: the ID of a document;
  - `title`: the title of the document;
  - `doc_text`: the text content of the document (without HTML markups);
  - `spans`: key-value pairs of all spans in the document, with `id_sp` as key. Each span includes the following,
    - `id_sp`: the id of a  span as noted by `text_id` in  `doc_html_ts`;
    - `start_sp`/  `end_sp`: the start/end position of the text span in `doc_text`;
    - `text_sp`: the text content of the span.
    - `id_sec`: the id of the (sub)section (e.g. `<p>`) or title (`<h2>`) that contains the span.
    - `start_sec` / `end_sec`: the start/end position of the (sub)section in `doc_text`.
    - `text_sec`: the text of the (sub)section.
    - `title`: the title of the (sub)section.
    - `parent_titles`: the parent titles of the `title`.
  - `doc_html_ts`: the document content with HTML markups and the annotated spans that are indicated by `text_id` attribute, which corresponds to `id_sp`.
  - `doc_html_raw`: the document content with HTML markups and without span annotations.
  

- `dialogue_domain`

  Each dialogue instance includes the following,

  - `dial_id`: the ID of a dialogue;
  - `domain`: the domain of the document;
  - `turns`: a list of dialogue turns. Each turn includes,
    - `turn_id`: the time order of the turn;
    - `role`: either "agent" or "user";
    - `da`: dialogue act;
    - `references`: a list of spans with `id_sp` ,  `label` and `doc_id`. `references` is empty if a turn is for indicating previous user query not answerable or irrelevant to the document. **Note** that labels "*precondition*"/"*solution*" are fuzzy annotations that indicate whether a span is for describing a conditional context or a solution.
    - `utterance`: the human-generated utterance based on the dialogue scene.


- `multidoc2dial`

  Each dialogue instance includes the following,

  - `id`: the ID of a QA instance
  - `title`: the title of the relevant document;
  - `context`: the text content of the relevant document (without HTML markups).
  - `question`: user query;
  - `da`: dialogue act;
  - `answers`: the answers that are grounded in the associated document;
    - `text`: the text content of the grounding span;
    - `answer_start`: the start position of the grounding span in the associated document (context);
  - `utterance`: the human-generated utterance based on the dialogue scene.
  - `domain`: domain of the relevant document;

### Data Splits

Training, dev and test split for default configuration `multidoc2dial`, with respectively 21451, 4201 and 5 examples,
- Training & dev split for dialogue domain, with 3474 and 661 examples,
- Training split only for document domain, with 488 examples.

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

Song Feng, Siva Sankalp Patel, Hui Wan, Sachindra Joshi

### Licensing Information

Creative Commons Attribution 3.0 Unported

### Citation Information

```bibtex
@inproceedings{feng2021multidoc2dial,
    title={MultiDoc2Dial: Modeling Dialogues Grounded in Multiple Documents},
    author={Feng, Song and Patel, Siva Sankalp and Wan, Hui and Joshi, Sachindra},
    booktitle={EMNLP},
    year={2021}
}
```

### Contributions

Thanks to [@songfeng](https://github.com/songfeng) and [@sivasankalpp](https://github.com/sivasankalpp) for adding this dataset.