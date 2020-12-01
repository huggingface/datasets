"""Helper file to crawl The Public DGS Corpus and create an up-to-date index of the dataset"""

import json
import re
import urllib.request


corpus_path = "https://www.sign-lang.uni-hamburg.de/meinedgs/"

index_data = {}

with urllib.request.urlopen(corpus_path + "ling/start-name_en.html") as response:
    html = response.read().decode("utf-8")

    trs = re.findall('<tr id="(.*?)">([\s\S]*?)</tr>', html)
    for tr_id, tr in trs:
        tds = re.findall("(?:(<td />)|<td.*?>([\s\S]*?)</)", tr)
        td_links = [re.findall('href="(.*?)"', td[1]) for td in tds]
        links = [corpus_path + links[0][3:] if len(links) > 0 else None for links in td_links]
        assert len(links) == 13

        index_data[tr_id] = {
            "transcript": links[0],
            "format": links[2],
            "ilex": links[4],
            "eaf": links[5],
            "video_a": links[6],
            "video_b": links[7],
            "video_c": links[8],
            "srt": links[9],
            "cmdi": links[11],
            "openpose": links[12],
        }

        if index_data[tr_id]["openpose"] is not None:
            assert index_data[tr_id]["openpose"].endswith(".json.gz")


# with open("/home/nlp/amit/WWW/datasets/dgs.json", "w") as f:
with open("data.json", "w") as f:
    json.dump(index_data, f)
