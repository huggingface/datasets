# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import nlp
import os
import logging

from transformers import BertTokenizerFast

logging.basicConfig(level=logging.INFO)

tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')

d = nlp.load('squad', split='validation[:10%]')


# %%
def convert_to_features(example_batch):
    # Tokenize contexts and questions (as pairs of inputs) - keep offset mappings for evaluation
    input_pairs = list(zip(example_batch['context'], example_batch['question']))
    encodings = tokenizer.batch_encode_plus(input_pairs, pad_to_max_length=True, return_offsets_mapping=True)

    # Compute start and end tokens for labels
    start_positions, end_positions = [], []
    for i, answer in enumerate(example_batch['answers']):
        first_char = answer['answer_start'][0]
        last_char = first_char + len(answer['text'][0]) - 1
        start_positions.append(encodings.char_to_token(i, first_char))
        end_positions.append(encodings.char_to_token(i, last_char))

    encodings.update({'start_positions': start_positions, 'end_positions': end_positions})
    return encodings

# %%
d = d.map(convert_to_features, batched=True)
print(d[0])

# %%
d.set_format(return_type='numpy', filter_columns=['input_ids', 'start_positions', 'end_positions'] + tokenizer.model_input_names)
print(d[:2])

# %%
import torch
dataloader = torch.utils.data.DataLoader(d, batch_size=3)
print(next(iter(dataloader)))
