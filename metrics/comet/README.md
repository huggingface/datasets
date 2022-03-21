# Metric Card for COMET

## Metric description

Crosslingual Optimized Metric for Evaluation of Translation (COMET) is an open-source framework used to train Machine Translation metrics that achieve high levels of correlation with different types of human judgments. 


## How to use 

COMET takes 3 lists of strings as input: `sources` (a list of source sentences), `predictions` (a list of candidate translations) and `references` (a list of reference translations). 

```python
from datasets import load_metric
comet_metric = load_metric('comet')
source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
hypothesis = ["The fire could be stopped", "Schools and kindergartens were open"]
reference = ["They were able to control the fire.", "Schools and kindergartens opened"]
comet_score = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)
```
It also has several optional arguments:

`cuda`: a boolean -- if set to `True`, COMET will run using GPU; else, it will run using CPU. The default value is `True`.

`show_progress`a boolean -- if set to `True`, progress updates will be printed out. The default value is `False`.

`model`: the COMET model to be used. Will default to `wmt-large-da-estimator-1719`. Alternate models that can be chosen include `wmt20-comet-da`, `wmt20-comet-qe-da`, `wmt21-comet-mqm`, `wmt21-cometinho-da`, `wmt21-comet-qe-mqm` and `emnlp20-comet-rank`. 

More information about model characteristics can be found on the [COMET website](https://unbabel.github.io/COMET/html/models.html).

## Output values

The COMET metric outputs two lists:

`samples`: a list of dictionaries with `src`, `mt`, `ref` and `score`

`scores`: a list of COMET scores for each of the input sentences, ranging from 0-1.


### Values from popular papers
The [original COMET paper](https://arxiv.org/pdf/2009.09025.pdf) reported average COMET scores ranging from 0.4 to 0.6, depending on the language pairs used for evaluating translation models. They also illustrate that COMET correlates well with human judgements compared to other metrics such as [BLEU](https://huggingface.co/metrics/bleu) and [CHRF](https://huggingface.co/metrics/chrf). 

## Examples 

Full match:

```python
from datasets import load_metric
comet_metric = load_metric('comet') 
source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
hypothesis = ["They were able to control the fire.", "Schools and kindergartens opened"]
reference = ["They were able to control the fire.", "Schools and kindergartens opened"]
results = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)
print([round(v, 1) for v in results["scores"]])
[1.0, 1.0]
```

Partial match: 

```python
from datasets import load_metric
comet_metric = load_metric('comet') 
source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
hypothesis = ["The fire could be stopped", "Schools and kindergartens were open"]
reference = ["They were able to control the fire", "Schools and kindergartens opened"]
results = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)
print([round(v, 2) for v in results["scores"]])
[0.19, 0.92]
```

No match: 

```python
from datasets import load_metric
comet_metric = load_metric('comet') 
source = ["Dem Feuer konnte Einhalt geboten werden", "Schulen und Kindergärten wurden eröffnet."]
hypothesis = ["The girl went for a walk", "The boy was sleeping"]
reference = ["They were able to control the fire", "Schools and kindergartens opened"]
results = comet_metric.compute(predictions=hypothesis, references=reference, sources=source)
print([round(v, 2) for v in results["scores"]])
[0.00, 0.00]
```

## Limitations and bias

The models provided for calculating the COMET metric are built on top of XLM-R and cover the following languages:

Afrikaans, Albanian, Amharic, Arabic, Armenian, Assamese, Azerbaijani, Basque, Belarusian, Bengali, Bengali Romanized, Bosnian, Breton, Bulgarian, Burmese, Burmese, Catalan, Chinese (Simplified), Chinese (Traditional), Croatian, Czech, Danish, Dutch, English, Esperanto, Estonian, Filipino, Finnish, French, Galician, Georgian, German, Greek, Gujarati, Hausa, Hebrew, Hindi, Hindi Romanized, Hungarian, Icelandic, Indonesian, Irish, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Kurdish (Kurmanji), Kyrgyz, Lao, Latin, Latvian, Lithuanian, Macedonian, Malagasy, Malay, Malayalam, Marathi, Mongolian, Nepali, Norwegian, Oriya, Oromo, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Sanskri, Scottish, Gaelic, Serbian, Sindhi, Sinhala, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tamil, Tamil Romanized, Telugu, Telugu Romanized, Thai, Turkish, Ukrainian, Urdu, Urdu Romanized, Uyghur, Uzbek, Vietnamese, Welsh, Western, Frisian, Xhosa, Yiddish.

Thus, results for language pairs containing uncovered languages are unreliable, as per the [COMET website](https://github.com/Unbabel/COMET)

Also, calculating the COMET metric involves downloading the model from which features are obtained -- the default model, `wmt20-comet-da`, takes over 1.79GB of storage space and downloading it can take a significant amount of time depending on the speed of your internet connection. If this is an issue, choose a smaller model; for instance `wmt21-cometinho-da` is 344MB.

## Citation

```bibtex
@inproceedings{rei-EtAl:2020:WMT,
   author    = {Rei, Ricardo  and  Stewart, Craig  and  Farinha, Ana C  and  Lavie, Alon},
   title     = {Unbabel's Participation in the WMT20 Metrics Shared Task},
   booktitle      = {Proceedings of the Fifth Conference on Machine Translation},
   month          = {November},
   year           = {2020},
   address        = {Online},
   publisher      = {Association for Computational Linguistics},
   pages     = {909--918},
}
```
```bibtex
@inproceedings{rei-etal-2020-comet,
   title = "{COMET}: A Neural Framework for {MT} Evaluation",
   author = "Rei, Ricardo  and
      Stewart, Craig  and
      Farinha, Ana C  and
      Lavie, Alon",
   booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
   month = nov,
   year = "2020",
   address = "Online",
   publisher = "Association for Computational Linguistics",
   url = "https://www.aclweb.org/anthology/2020.emnlp-main.213",
   pages = "2685--2702",

```
    
## Further References 

- [COMET website](https://unbabel.github.io/COMET/html/index.html)
- [Hugging Face Tasks - Machine Translation](https://huggingface.co/tasks/translation)
