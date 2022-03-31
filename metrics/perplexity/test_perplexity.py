"""

        device = "cuda"
        model_id = "distilbert-base-uncased"

        model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
        tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
        test = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
        encodings = tokenizer("\n\n".join(test["text"]), return_tensors="pt")
        max_length = model.config.n_positions

        nlls = []
        for i in tqdm(range(0, encodings.input_ids.size(1), stride)):
            begin_loc = max(i + stride - max_length, 0)
            end_loc = min(i + stride, encodings.input_ids.size(1))
            trg_len = end_loc - i  # may be different from stride on last loop
            input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
            target_ids = input_ids.clone()
            target_ids[:, :-trg_len] = -100

            with torch.no_grad():
                outputs = model(input_ids, labels=target_ids)
                neg_log_likelihood = outputs[0] * trg_len
                nlls.append(neg_log_likelihood)

"""

# import fixed_perplexity

# import perplexity
import datasets
from datasets import load_dataset


def main():
    print("\n\nworking...\n\n")

    # model_id='gpt2'

    print("\n\n-----STRING VERSION-----\n")
    # perp = perplexity.Perplexity()
    # perp.add_batch()
    #print("created perplexity obj, now getting results...")
    # results = perp._compute(model_id=model_id,
    #                        input_list=["lorem ipsum","happy birthday", "no way!"],
    #                        device='cuda')

    # print(results)

    # input_texts = load_dataset("wikitext", "wikitext-2-raw-v1", keep_in_memory=False, split="test")["text"][:10]
    # results2 = perp._compute(model_id=model_id,
    #                        input_list=test_dataset,
    #                        device='cuda')

    # print(results2)

    perplexity = datasets.load_metric("../perplexity")
    # perplexity_w_mask = fixed_perplexity.Perplexity() #datasets.load_metric("~/datasets/metrics/perplexity/fixed_perplexity")
    input_texts = ["lorem ipsum", "Happy Birthday!", "Bienvenue"]
    # input_texts = test_dataset
    # print(input_texts)
    results = perplexity.compute(input_texts=input_texts, model_id="gpt2", device="gpu", add_start_token=True)  # ,
    # device='gpu') #2)

    # results_w_mask = perplexity_w_mask.compute(input_texts=input_texts,
    #                                        model_id='gpt2',
    #                                        stride=256,
    #                                        device='gpu')

    print(results)
    print(round(results["perplexity"], 1))

    # print("w_mask:", results_w_mask)


if __name__ == "__main__":
    main()
