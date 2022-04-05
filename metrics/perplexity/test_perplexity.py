import datasets
from datasets import load_dataset


def main():
    print("\n\n\n------------  WIKITEXT:  ------------")
    input_texts = load_dataset("wikitext", "wikitext-2-raw-v1", keep_in_memory=False, split="test")["text"][:50]
    print("input len with empty strings:", len(input_texts))
    input_texts = [s for s in input_texts if s!='']
    print("input len without empty strings:", len(input_texts))

    perplexity = datasets.load_metric("../perplexity")
    
    results_w_start = perplexity.compute(input_texts=input_texts, model_id="gpt2", device="gpu", add_start_token=True)
    print("\n\nRES W START:", results_w_start)

    results_no_start = perplexity.compute(input_texts=input_texts, model_id="gpt2", device="gpu", add_start_token=False)
    print("\n\nRES NO START:", results_no_start)


    
    print("\n\n\n------------  SMALL SNIPPETS:  ------------")
    input_texts = ["lorem ipsum", "Happy Birthday!", "Bienvenue"]
    print(input_texts)

    results_w_start = perplexity.compute(input_texts=input_texts, model_id="gpt2", device="gpu", add_start_token=True)
    print("\n\nRES W START:", results_w_start)

    results_no_start = perplexity.compute(input_texts=input_texts, model_id="gpt2", device="gpu", add_start_token=False)
    print("\n\nRES NO START:", results_no_start)



if __name__ == "__main__":
    main()
