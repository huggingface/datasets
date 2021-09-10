annotations_creators:
- crowdsourced
- expert-generated
language_creators:
- crowdsourced
- expert-generated
languages:
- en-US
licenses:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Mostly Basic Python Problems
size_categories:
- unknown
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- conditional-text-generation-other-code-generation

# Dataset Card for Mostly Basic Python Problems (mbpp)

## Dataset Description
- **Repository: https://github.com/google-research/google-research/tree/master/mbpp**
- **Paper: [Program Synthesis with Large Language Models](https://arxiv.org/abs/2108.07732)**

### Dataset Summary
The benchmark consists of around 1,000 crowd-sourced Python programming problems, designed to be solvable by entry level programmers, covering programming fundamentals, standard library functionality, and so on. Each problem consists of a task description, code solution and 3 automated test cases. As described in the paper, a subset of the data has been hand-verified by us. 

Released [here](https://github.com/google-research/google-research/tree/master/mbpp) as part of [Program Synthesis with Large Language Models, Austin et. al., 2021](https://arxiv.org/abs/2108.07732).

### Languages
English - Python code

## Data Structure

```python
dataset_full = load_dataset("mbpp")
DatasetDict({
    test: Dataset({
        features: ['task_id', 'text', 'code', 'test_list', 'test_setup_code', 'challenge_test_list'],
        num_rows: 974
    })
})

dataset_sanitized = load_dataset("mbpp", "sanitized")
DatasetDict({
    test: Dataset({
        features: ['source_file', 'task_id', 'prompt', 'code', 'test_imports', 'test_list'],
        num_rows: 427
    })
})
```

### Data Instances

#### mbpp - full
```
{
    'task_id': 1,
    'text': 'Write a function to find the minimum cost path to reach (m, n) from (0, 0) for the given cost matrix cost[][] and a position (m, n) in cost[][].',
    'code': 'R = 3\r\nC = 3\r\ndef min_cost(cost, m, n): \r\n\ttc = [[0 for x in range(C)] for x in range(R)] \r\n\ttc[0][0] = cost[0][0] \r\n\tfor i in range(1, m+1): \r\n\t\ttc[i][0] = tc[i-1][0] + cost[i][0] \r\n\tfor j in range(1, n+1): \r\n\t\ttc[0][j] = tc[0][j-1] + cost[0][j] \r\n\tfor i in range(1, m+1): \r\n\t\tfor j in range(1, n+1): \r\n\t\t\ttc[i][j] = min(tc[i-1][j-1], tc[i-1][j], tc[i][j-1]) + cost[i][j] \r\n\treturn tc[m][n]',
    'test_list': [
        'assert min_cost([[1, 2, 3], [4, 8, 2], [1, 5, 3]], 2, 2) == 8',
        'assert min_cost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) == 12',
        'assert min_cost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) == 16'],
    'test_setup_code': '',
    'challenge_test_list': []
}
```
#### mbpp - sanitized
```
{
    'source_file': 'Benchmark Questions Verification V2.ipynb',
    'task_id': 2,
    'prompt': 'Write a function to find the shared elements from the given two lists.',
    'code': 'def similar_elements(test_tup1, test_tup2):\n  res = tuple(set(test_tup1) & set(test_tup2))\n  return (res) ',
    'test_imports': [],
    'test_list': [
        'assert set(similar_elements((3, 4, 5, 6),(5, 7, 4, 10))) == set((4, 5))',
        'assert set(similar_elements((1, 2, 3, 4),(5, 4, 3, 7))) == set((3, 4))',
        'assert set(similar_elements((11, 12, 14, 13),(17, 15, 14, 13))) == set((13, 14))'
        ]
}
```

### Data Splits
There are two version of the dataset (full and sanitized) which only one split each (test).

## Dataset Creation
See section 2.1 of original [paper](https://arxiv.org/abs/2108.07732).

## Considerations of Using the Data

### Security Considerations
Make sure you execute generated Python code in a safe environment when evauating against this dataset as generated code could be harmful.