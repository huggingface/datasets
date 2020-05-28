#!/usr/bin/env python3

import nlp

ds = nlp.load_dataset("squad", split="validation[:10%]")

def remove_under_idx_5(example, idx):
    print(idx)
    return idx < 5


result = ds.filter(remove_under_idx_5, with_indices=True, load_from_cache_file=False)

import ipdb
ipdb.set_trace()


