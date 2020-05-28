import json
import nlp

_CITATION = """\
@inproceedings{fb_kilt,
  author    = {Fabio Petroni and
               Angela Fan and
               Sebastian Riedel},
  title     = {{KILT:} Knowledge Intensive Language Tasks},
  booktitle = {ArXiv},
  year      = {2020},
}
"""

_DESCRIPTION = """\
Wiki-KILT Wikipedia pre-processed for KILT/ELI5
"""


class WikiKILTConfig(nlp.BuilderConfig):
    """BuilderConfig for WikiKILT."""

    def __init__(self, **kwargs):
        """BuilderConfig for WikiKILT.
    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        super(WikiKILTConfig, self).__init__(**kwargs)


class WikiKILT(nlp.GeneratorBasedBuilder):
    """Wiki-KILT: Wikipedia for Knowledge Intensive Language Tasks."""

    _DATA_URL = (
        "http://dl.fbaipublicfiles.com/KILT/kilt_knowledgesource.json"
    )
    
    name = "wiki_kilt"
    BUILDER_CONFIGS = [
        WikiKILTConfig(name="wikipedia_kilt", version=nlp.Version("1.0.0"), description="Wikipedia pre-processed for KILT tasks"),
    ]

    def _info(self):
        return nlp.DatasetInfo(
                description=_DESCRIPTION,
                features=nlp.Features({
                        "title": nlp.Value("string"),
                        "kilt_id": nlp.Value("string"),
                        "paragraphs":
                                nlp.features.Sequence({
                                        "paragraph": nlp.Value("string"),
                                }),
                        "anchors":
                                nlp.features.Sequence({
                                        "text": nlp.Value("string"),
                                        "href": nlp.Value("string"),
                                        "paragraph_id": nlp.Value("int32"),
                                        "start": nlp.Value("int32"),
                                        "end": nlp.Value("int32"),
                                }),
                }),
                supervised_keys=None,
                homepage="https://facebookresearch.github.io/KILT",
                citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download_and_extract(self._DATA_URL)
        return [
                nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        gen_kwargs={"kilt_file": downloaded_file}),
        ]

    def _generate_examples(self, kilt_file):
        """This function returns the examples in the raw (text) form."""
        f = open(kilt_file)
        for line in f:
            example = json.loads(line.strip())
            id_ = 'kilt_' + example['_id']
            title = example['wikipedia_title']
            paragraphs = [par for par in example['text']]
            anchor_text =[a['text'] for a in example['anchors']]
            anchor_href = [a['href'] for a in example['anchors']]
            anchor_pid = [a['paragraph_id'] for a in example['anchors']]
            anchor_start = [a['start'] for a in example['anchors']]
            anchor_end = [a['end'] for a in example['anchors']]
            res_dct = {
                "title": title,
                "kilt_id": id_,
                "paragraphs": {"paragraph": paragraphs},
                "anchors": {
                    "text": anchor_text,
                    "href": anchor_href,
                    "paragraph_id": anchor_pid,
                    "start": anchor_start,
                    "end": anchor_end,
                },
            }
            yield id_, res_dct
        f.close()

