"""Helper file to crawl TheLanguageArchive and create an up-to-date index of the dataset"""

import json
import re
import urllib.request

from tqdm import tqdm

base_path = "https://archive.mpi.nl"


def get_sub_pages(html):
    return [x for x in re.findall('<strong class=\"field-content\"><a href=\"(.*)\">.*</a></strong>', html)]


# Iterate over pages
next_page = "/tla/islandora/object/tla%3A1839_00_0000_0000_0004_F3D5_A"
sub_pages = []
while next_page is not None:
    with urllib.request.urlopen(base_path + next_page) as response:
        html = response.read().decode("utf-8")

        next_search = re.search('<a href=\"(.*?)\">next</a>', html)
        next_page = next_search.group(1) if next_search else None

        sub_pages += get_sub_pages(html)

# Iterate over sub pages
download_pages = []
for page in tqdm(sub_pages):
    print(base_path + page)
    with urllib.request.urlopen(base_path + page) as response:
        html = response.read().decode("utf-8")
        download_pages += get_sub_pages(html)

# Iterate over download pages
download_files = {}
for page in tqdm(download_pages):
    print(base_path + page)
    with urllib.request.urlopen(base_path + page) as response:
        html = response.read().decode("utf-8")

        files = re.findall(
            'title=\"view item\">(.*)</a></div>\n<div class=\"flat-compound-buttons\">\n<div class=\"flat-compound-download\"><a href=\"(.*)\" class=\"flat-compound-download\" title=\"download file\"></a>',
            html)
        for file in files:
            download_files[file[0]] = base_path + file[1]

f = open("data.json", "w")
json.dump(download_files, f)
f.close()
