from datasets import load_dataset

data = load_dataset('./datasets/interpress_news_category_tr_lite', '270k_10class', split="train")

print(data[0])