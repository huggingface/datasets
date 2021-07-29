---
annotations_creators:
- crowdsourced
language_creators:
- crowdsourced
languages:
- en
licenses:
- cc-by-4.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- original
task_categories:
- other
- text-classification
task_ids:
- sentiment-classification
- text-classification-other-dialogue-sentiment-classification
paperswithcode_id: redial
---

# Dataset Card for ReDial (Recommendation Dialogues)

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

- **Homepage:** [ReDial Dataset](https://redialdata.github.io/website/)
- **Repository:** [ReDialData](https://github.com/ReDialData/website/tree/data)
- **Paper:** [Towards Deep Conversational Recommendations](https://proceedings.neurips.cc/paper/2018/file/800de15c79c8d840f4e78d3af937d4d4-Paper.pdf)
- **Point of Contact:** [ReDial Google Group](https://groups.google.com/forum/embed/?place=forum/redial-dataset&showpopout=true#!forum/redial-dataset)

### Dataset Summary

ReDial (Recommendation Dialogues) is an annotated dataset of dialogues, where users
recommend movies to each other. The dataset was collected by a team of researchers working at
Polytechnique Montréal, MILA – Quebec AI Institute, Microsoft Research Montréal, HEC Montreal, and Element AI.

The dataset allows research at the intersection of goal-directed dialogue systems
(such as restaurant recommendation) and free-form (also called “chit-chat”) dialogue systems.

### Supported Tasks and Leaderboards

[More Information Needed]

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

JSON-formatted example of a typical instance in the dataset.

```
{
   "movieMentions":{
      "203371":"Final Fantasy: The Spirits Within (2001)",
      "84779":"The Triplets of Belleville (2003)",
      "122159":"Mary and Max (2009)",
      "151313":"A Scanner Darkly  (2006)",
      "191602":"Waking Life (2001)",
      "165710":"The Boss Baby (2017)"
   },
   "respondentQuestions":{
      "203371":{
         "suggested":1,
         "seen":0,
         "liked":1
      },
      "84779":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "122159":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "151313":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "191602":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "165710":{
         "suggested":1,
         "seen":0,
         "liked":1
      }
   },
   "messages":[
      {
         "timeOffset":0,
         "text":"Hi there, how are you? I'm looking for movie recommendations",
         "senderWorkerId":0,
         "messageId":1021
      },
      {
         "timeOffset":15,
         "text":"I am doing okay. What kind of movies do you like?",
         "senderWorkerId":1,
         "messageId":1022
      },
      {
         "timeOffset":66,
         "text":"I like animations like @84779 and @191602",
         "senderWorkerId":0,
         "messageId":1023
      },
      {
         "timeOffset":86,
         "text":"I also enjoy @122159",
         "senderWorkerId":0,
         "messageId":1024
      },
      {
         "timeOffset":95,
         "text":"Anything artistic",
         "senderWorkerId":0,
         "messageId":1025
      },
      {
         "timeOffset":135,
         "text":"You might like @165710 that was a good movie.",
         "senderWorkerId":1,
         "messageId":1026
      },
      {
         "timeOffset":151,
         "text":"What's it about?",
         "senderWorkerId":0,
         "messageId":1027
      },
      {
         "timeOffset":207,
         "text":"It has Alec Baldwin it is about a baby that works for a company and gets adopted it is very funny",
         "senderWorkerId":1,
         "messageId":1028
      },
      {
         "timeOffset":238,
         "text":"That seems like a nice comedy",
         "senderWorkerId":0,
         "messageId":1029
      },
      {
         "timeOffset":272,
         "text":"Do you have any animated recommendations that are a bit more dramatic? Like @151313 for example",
         "senderWorkerId":0,
         "messageId":1030
      },
      {
         "timeOffset":327,
         "text":"I like comedies but I prefer films with a little more depth",
         "senderWorkerId":0,
         "messageId":1031
      },
      {
         "timeOffset":467,
         "text":"That is a tough one but I will remember something",
         "senderWorkerId":1,
         "messageId":1032
      },
      {
         "timeOffset":509,
         "text":"@203371 was a good one",
         "senderWorkerId":1,
         "messageId":1033
      },
      {
         "timeOffset":564,
         "text":"Ooh that seems cool! Thanks for the input. I'm ready to submit if you are.",
         "senderWorkerId":0,
         "messageId":1034
      },
      {
         "timeOffset":571,
         "text":"It is animated, sci fi, and has action",
         "senderWorkerId":1,
         "messageId":1035
      },
      {
         "timeOffset":579,
         "text":"Glad I could help",
         "senderWorkerId":1,
         "messageId":1036
      },
      {
         "timeOffset":581,
         "text":"Nice",
         "senderWorkerId":0,
         "messageId":1037
      },
      {
         "timeOffset":591,
         "text":"Take care, cheers!",
         "senderWorkerId":0,
         "messageId":1038
      },
      {
         "timeOffset":608,
         "text":"bye",
         "senderWorkerId":1,
         "messageId":1039
      }
   ],
   "conversationId":"391",
   "respondentWorkerId":1,
   "initiatorWorkerId":0,
   "initiatorQuestions":{
      "203371":{
         "suggested":1,
         "seen":0,
         "liked":1
      },
      "84779":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "122159":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "151313":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "191602":{
         "suggested":0,
         "seen":1,
         "liked":1
      },
      "165710":{
         "suggested":1,
         "seen":0,
         "liked":1
      }
   }
}
```

### Data Fields

The dataset is published in the “jsonl” format, i.e., as a text file where each line corresponds to a Dialogue given as a valid JSON document.

A Dialogue contains these fields:

**conversationId:** an integer
**initiatorWorkerId:** an integer identifying to the worker initiating the conversation (the recommendation seeker)
**respondentWorkerId:** an integer identifying the worker responding to the initiator (the recommender)
**messages:** a list of Message objects
**movieMentions:** a dict mapping movie IDs mentioned in this dialogue to movie names
**initiatorQuestions:** a dictionary mapping movie IDs to the labels supplied by the initiator. Each label is a bool corresponding to whether the initiator has said he saw the movie, liked it, or suggested it.
**respondentQuestions:** a dictionary mapping movie IDs to the labels supplied by the respondent. Each label is a bool corresponding to whether the initiator has said he saw the movie, liked it, or suggested it.
Each Message contains these fields:

**messageId:** a unique ID for this message
**text:** a string with the actual message. The string may contain a token starting with @ followed by an integer. This is a movie ID which can be looked up in the movieMentions field of the Dialogue object.
**timeOffset:** time since start of dialogue in seconds
**senderWorkerId:** the ID of the worker sending the message, either initiatorWorkerId or respondentWorkerId.

The labels in initiatorQuestions and respondentQuestions have the following meaning:
*suggested:* 0 if it was mentioned by the seeker, 1 if it was a suggestion from the recommender
*seen:* 0 if the seeker has not seen the movie, 1 if they have seen it, 2 if they did not say
*liked:* 0 if the seeker did not like the movie, 1 if they liked it, 2 if they did not say

### Data Splits

The dataset contains a total of 11348 dialogues, 10006 for training and model selection, and 1342 for testing.

## Dataset Creation

### Curation Rationale

The dataset allows research at the intersection of goal-directed dialogue systems (such as restaurant recommendation) and free-form (also called “chit-chat”) dialogue systems.

In the dataset, users talk about which movies they like and which ones they do not like, which ones they have seen or not etc., and labels which we ensured agree between the two participants. This allows to research how sentiment is expressed in dialogues, which differs a lot from e.g. review websites.

The dialogues and the movies they mention form a curious bi-partite graph structure, which is related to how users talk about the movie (e.g. genre information).

Ignoring label information, this dataset can also be viewed as a limited domain chit-chat dialogue dataset.

### Source Data

#### Initial Data Collection and Normalization

Describe the data collection process. Describe any criteria for data selection or filtering. List any key words or search terms used. If possible, include runtime information for the collection process.

If data was collected from other pre-existing datasets, link to source here and to their [Hugging Face version](https://huggingface.co/datasets/dataset_name).

If the data was modified or normalized after being collected (e.g. if the data is word-tokenized), describe the process and the tools used.

#### Who are the source language producers?

Here we formalize the setup of a conversation involving recommendations for the purposes of data collection. To provide some additional structure to our data (and models) we define one person in the dialogue as the recommendation seeker and the other as the recommender.

To obtain data in this form, we developed an interface and pairing mechanism mediated by Amazon Mechanical Turk (AMT).

We pair up AMT workers and give each of them a role. The movie seeker has to explain what kind of movie he/she likes, and asks for movie suggestions. The recommender tries to understand the seeker’s movie tastes, and recommends movies. All exchanges of information and recommendations are made using natural language.

We add additional instructions to improve the data quality and guide the workers to dialogue the way we expect them to. Thus we ask to use formal language and that conversations contain roughly ten messages minimum. We also require that at least four different movies are mentioned in every conversation. Finally, we also ask to converse only about movies, and notably not to mention Mechanical Turk or the task itself.

In addition, we ask that every movie mention is tagged using the ‘@’ symbol. When workers type ‘@’, the following characters are used to find matching movie names, and workers can choose a movie from that list. This allows us to detect exactly what movies are mentioned and when. We gathered entities from DBpedia that were of type http://dbpedia.org/ontology/Film to obtain a list of movies, but also allow workers to add their own movies to the list if it is not present already. We obtained the release dates from the movie titles (e.g. http://dbpedia.org/page/American_Beauty_(1999_film), or, if the movie title does not contain that information, from an additional SPARQL request. Note that the year or release date of a movie can be essential to differentiate movies with the same name, but released at different dates.

We will refer to these additional labels as movie dialogue forms. Both workers have to answer these forms even though it really concerns the seeker’s movie tastes. Ideally, the two participants would give the same answer to every form, but it is possible that their answers do not coincide (because of carelessness, or dialogue ambiguity). The movie dialogue forms therefore allow us to evaluate sub-components of an overall neural dialogue system more systematically, for example one can train and evaluate a sentiment analysis model directly using these labels. %which could produce a reward for the dialogue agent.

In each conversation, the number of movies mentioned varies, so we have different numbers of movie dialogue form answers for each conversation. The distribution of the different classes of the movie dialogue form is shown in Table 1a. The liked/disliked/did not say label is highly imbalanced. This is standard for recommendation data, since people are naturally more likely to talk about movies that they like, and the recommender’s objective is to recommend movies that the seeker is likely to like.

### Annotations

#### Annotation process

Mentioned in above sub-section.

#### Who are the annotators?

For the AMT HIT we collect data in English and chose to restrict the data collection to countries where English is the main language. The fact that we pair workers together slows down the data collection since we ask that at least two persons are online at the same time to do the task, so a good amount of workers is required to make the collection possible. Meanwhile, the task is quite demanding, and we have to select qualified workers. HIT reward and qualification requirement were decisive to get good conversation quality while still ensuring that people could get paired together. We launched preliminary HITs to find a compromise and finally set the reward to $0.50 per person for each completed conversation (so each conversation costs us $1, plus taxes), and ask that workers meet the following requirements: (1)~Approval percentage greater than 95, (2)~Number of approved HITs greater than 1000, (3)~Their location must be in United States, Canada, United Kingdom, Australia, or New Zealand.

### Personal and Sensitive Information

Workers had to confirm a consent form before every task that explains what the data is being collected for and how it is going to be used.

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

The dataset collection was funded by Google, IBM, and NSERC, with editorial support from Microsoft Research.

### Licensing Information

The data is published under the CC BY 4.0 License.

### Citation Information

```
@inproceedings{li2018conversational,
  title={Towards Deep Conversational Recommendations},
  author={Li, Raymond and Kahou, Samira Ebrahimi and Schulz, Hannes and Michalski, Vincent and Charlin, Laurent and Pal, Chris},
  booktitle={Advances in Neural Information Processing Systems 31 (NIPS 2018)},
  year={2018}
}
```

### Contributions

Thanks to [@bhavitvyamalik](https://github.com/bhavitvyamalik) for adding this dataset.