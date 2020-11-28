# Loading the KILT knowledge source and task data

The original KILT [release](https://github.com/facebookresearch/KILT) only provides question IDs for the TriviaQA task. Using the full dataset requires mapping those back to the TriviaQA questions, which can be done as follows: 

```python
from datasets import load_dataset

# Get the pre-processed Wikipedia knowledge source for kild
kilt_wiki = load_dataset("kilt_wikipedia")

# Get the KILT task datasets
kilt_tasks = load_dataset("kilt_tasks")

# Most tasks in KILT already have all required data, but KILT-TriviaQA
# only provides the question IDs, not the questions themselves.
# Thankfully, we can get the original TriviaQA data with:
trivia_qa = load_dataset('trivia_qa', 'unfiltered.nocontext')

# The KILT IDs can then be mapped to the TriviaQA questions with:
triviaqa_map = {}
for k in ['train', 'validation', 'test']:
    triviaqa_map = dict([(q_id, i) for i, q_id in enumerate(trivia_qa[k]['question_id'])])
    kilt_tasks[k + '_triviaqa'] = kilt_tasks[k + '_triviaqa'].filter(lambda x: x['id'] in triviaqa_map)
    kilt_tasks[k + '_triviaqa'] = kilt_tasks[k + '_triviaqa'].map(lambda x: {'input': trivia_qa[k][triviaqa_map[x['id']]]['question']})
```
