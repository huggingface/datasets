import random
from datasets import load_dataset
dataset = load_dataset('glue', 'mrpc', split='train')
dataset = dataset.map(lambda x: {'flag': random.randint(0, 1) == 1})


def _amplify(data):
    return data


dataset = dataset.filter(_amplify, batch_size=2, keep_in_memory=False, input_columns=['flag'])
