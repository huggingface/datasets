from __future__ import absolute_import, division, print_function

import base64
import csv
import json
import os
import subprocess
import sys
import time

import numpy as np

import nlp
import nlp.features as features
from nlp.arrow_writer import ArrowWriter


ROOT = "/ssd-playpen/avmendoz/nlp"

DOWNLOAD_MINI = False
DOWNLOAD_TRAIN = False
DOWNLOAD_VAL = True


csv.field_size_limit(sys.maxsize)
FIELDNAMES = [
    "img_id",
    "img_h",
    "img_w",
    "objects_id",
    "objects_conf",
    "attrs_id",
    "attrs_conf",
    "num_boxes",
    "boxes",
    "features",
]


_MINI_URLS = [
    "https://nlp1.cs.unc.edu/data/lxmert_data/mscoco_imgfeat/val2014_obj36.zip",
    "https://raw.githubusercontent.com/airsplay/lxmert/master/data/lxmert/all_ans.json",
    "https://nlp1.cs.unc.edu/data/lxmert_data/vqa/minival.json",
]

_TEXT_DATA_TRAIN_URLS = [
    "https://nlp1.cs.unc.edu/data/lxmert_data/lxmert/mscoco_train.json",
    "https://nlp1.cs.unc.edu/data/lxmert_data/lxmert/vgnococo.json",
    "https://raw.githubusercontent.com/airsplay/lxmert/master/data/lxmert/all_ans.json",
]


_TEXT_DATA_VAL_URLS = [
    "https://nlp1.cs.unc.edu/data/lxmert_data/lxmert/mscoco_nominival.json",
    # "https://nlp1.cs.unc.edu/data/lxmert_data/lxmert/mscoco_minival.json",
    "https://raw.githubusercontent.com/airsplay/lxmert/master/data/lxmert/all_ans.json",
]


_IMG_DATA_TRAIN_URLS = [
    "https://nlp1.cs.unc.edu/data/lxmert_data/mscoco_imgfeat/train2014_obj36.zip",
    "https://nlp1.cs.unc.edu/data/lxmert_data/vg_gqa_imgfeat/vg_gqa_obj36.zip",
]

_IMG_DATA_VAL_URLS = [
    "https://nlp1.cs.unc.edu/data/lxmert_data/mscoco_imgfeat/val2014_obj36.zip",
]

if DOWNLOAD_VAL:
    urls = _IMG_DATA_VAL_URLS + _TEXT_DATA_VAL_URLS
elif DOWNLOAD_TRAIN:
    urls = _IMG_DATA_TRAIN_URLS + _TEXT_DATA_TRAIN_URLS
elif DOWNLOAD_MINI:
    urls = _MINI_URLS
else:
    exit()


class AnswerTable:
    ANS_CONVERT = {
        "a man": "man",
        "the man": "man",
        "a woman": "woman",
        "the woman": "woman",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
        "grey": "gray",
    }

    def __init__(self, dsets=None):
        self.all_ans = json.load(open(f"{ROOT}/all_ans.json"))
        if dsets is not None:
            dsets = set(dsets)
            # If the answer is used in the dsets
            self.anss = [ans["ans"] for ans in self.all_ans if len(set(ans["dsets"]) & dsets) > 0]
        else:
            self.anss = [ans["ans"] for ans in self.all_ans]
        self.ans_set = set(self.anss)

        self._id2ans_map = self.anss
        self._ans2id_map = {ans: ans_id for ans_id, ans in enumerate(self.anss)}

        assert len(self._id2ans_map) == len(self._ans2id_map)
        for ans_id, ans in enumerate(self._id2ans_map):
            assert self._ans2id_map[ans] == ans_id

    def convert_ans(self, ans):
        if len(ans) == 0:
            return ""
        ans = ans.lower()
        if ans[-1] == ".":
            ans = ans[:-1].strip()
        if ans.startswith("a "):
            ans = ans[2:].strip()
        if ans.startswith("an "):
            ans = ans[3:].strip()
        if ans.startswith("the "):
            ans = ans[4:].strip()
        if ans in self.ANS_CONVERT:
            ans = self.ANS_CONVERT[ans]
        return ans

    def ans2id(self, ans):
        return self._ans2id_map[ans]

    def id2ans(self, ans_id):
        return self._id2ans_map[ans_id]

    def ans2id_map(self):
        return self._ans2id_map.copy()

    def id2ans_map(self):
        return self._id2ans_map.copy()

    def used(self, ans):
        return ans in self.ans_set

    def all_answers(self):
        return self.anss.copy()

    @property
    def num_answers(self):
        return len(self.anss)


def load_obj_tsv(fname, topk=300):
    data = {}
    start_time = time.time()
    print("Start to load Faster-RCNN detected objects from %s" % fname)
    with open(fname) as f:
        reader = csv.DictReader(f, FIELDNAMES, delimiter="\t")
        for i, item in enumerate(reader):
            img_id = item.pop("img_id")

            for key in ["img_h", "img_w", "num_boxes"]:
                item[key] = int(item[key])

            boxes = item["num_boxes"]
            decode_config = [
                ("objects_id", (boxes,), np.int64),
                ("objects_conf", (boxes,), np.float32),
                ("attrs_id", (boxes,), np.int64),
                ("attrs_conf", (boxes,), np.float32),
                ("boxes", (boxes, 4), np.float32),
                ("features", (boxes, -1), np.float32),
            ]
            for key, shape, dtype in decode_config:
                item[key] = np.frombuffer(base64.b64decode(item[key]), dtype=dtype)
                item[key] = item[key].reshape(shape)
                item[key].setflags(write=False)

            data[img_id] = item
            if topk is not None and len(data) == topk:
                break
    elapsed_time = time.time() - start_time
    print("Loaded %d images in file %s in %d seconds." % (len(data), fname, elapsed_time))
    return data


if not os.path.exists(f"{ROOT}/"):
    os.mkdir(f"{ROOT}/")
for url in urls:
    ftype = url.split("/")[-1]
    fname = f"{ROOT}/" + ftype
    check = fname.split(".")[0]
    if os.path.exists(fname) or os.path.exists(check):
        continue
    else:
        os.mknod(fname)
        print(f"downloading:{fname}")

    command = f"wget --no-check-certificate {url} -O {fname}"
    subprocess.run(
        command, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE,
    )

for fname in filter(lambda x: x[-3:] == "zip", os.listdir(f"{ROOT}/")):
    print("unzipping and removing archives...")
    command = f"unzip {ROOT}/{fname} -d {ROOT}/{fname[:-4]}"
    process = subprocess.run(command, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE,)

    # remove zip
    command = f"rm {ROOT}/{fname}"
    process = subprocess.run(command, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE,)


if DOWNLOAD_MINI:
    split = "mini"
    with open(f"{ROOT}/minival.json", "r") as f:
        items = json.load(f)
    images = load_obj_tsv(f"{ROOT}/val2014_obj36/mscoco_imgfeat/val2014_obj36.tsv", topk=300)
elif DOWNLOAD_TRAIN:
    split = "train"
    with open(f"{ROOT}/mscoco_train.json", "r") as f:
        items = json.load(f)
    with open(f"{ROOT}/vgnococo.json", "r") as f:
        items += json.load(f)
    images = load_obj_tsv(f"{ROOT}/train2014_obj36/mscoco_imgfeat/train2014_obj36.tsv", topk=None)
    images = load_obj_tsv(f"{ROOT}/vg_gqa_obj36/vg_gqa_imgfeat/vg_gqa_obj36.tsv", topk=None)
elif DOWNLOAD_VAL:
    split = "val"
    with open(f"{ROOT}/mscoco_nominival.json", "r") as f:
        items = json.load(f)
    images = load_obj_tsv(f"{ROOT}/val2014_obj36/mscoco_imgfeat/val2014_obj36.tsv", topk=None)


# print(len(set(images.keys())), next(iter(images.keys())))
# print(len(set([i["img_id"] for i in items])),next(iter([i["img_id"] for i in items])))
# print(len(set(images.keys()).intersection(set([i["img_id"] for i in items]))))
# raise Exception
answer_table = AnswerTable()
# pre-pre process
new = {}
for j, i in enumerate(items):
    img = i.pop("img_id")
    image_data = images.get(img)
    entry = image_data
    if image_data is None:
        continue
    if split == "mini":
        i.pop("answer_type")
        i.pop("question_type")
        i.pop("question_id")
        entry = {**entry, **i}
        sent = entry["sent"]
        labels = entry["label"]
        label = list(labels.keys())
        label_conf = list(labels.values())
        label = [answer_table.convert_ans(l) for l in label]
        entry["label"] = label
        entry["label_conf"] = label_conf
        question = sent if "?" in sent else None
        sent = sent if "?" not in sent else None
        entry["question"] = question
        entry["sent"] = sent
        entry["img_id"] = img
        for k in entry:
            if k not in image_data and k != "img_id":
                entry[k] = [entry[k]]
        if img not in new:
            new[img] = entry
        else:
            cur = new[img]
            assert len(cur) == len(entry), f"{len(cur)}, {len(entry)}"
            for k in cur:
                if k not in image_data and k != "img_id":
                    temp = entry[k] + cur[k]
                    new_v = [x for x in temp if x is not None]
                    if not new_v:
                        new_v = ["<NONE>"]
                    cur[k] = new_v

            new[img] = cur
    else:
        sents = i["sentf"]
        labels = i["labelf"]
        labelk = sorted(list(labels.keys()))
        sentsk = sorted(list(sents.keys()))
        questionsf = []
        labelsf = []
        labelscf = []
        sentsf = []
        for k in labelk:
            for v in labels[k]:
                if "gqa" in k or "vqa" in k or "visual7w" in k:
                    labelsf.append(list(map(lambda x: answer_table.convert_ans(x), v.keys())))
                    labelscf.append(list(map(lambda x: x, v.values())))
        for k in sentsk:
            if "gqa" in k or "vqa" in k or "visual7w" in k:
                for s in sents[k]:
                    questionsf.append(s)
            else:
                for s in sents[k]:
                    sentsf.append(s)

        questions = questionsf
        sents = sentsf
        labels = labelsf
        assert len(questions) == len(labels), print(questions[-1], labels[-1], len(questions), len(labels))
        entry["question"] = questions if questions else ["<NONE>"]
        entry["sent"] = sents if sents else ["<NONE>"]
        entry["img_id"] = img
        entry["label"] = labels if labels else ["<NONE>"]
        entry["label_conf"] = labelscf if labelscf else ["<NONE>"]
        new[img] = entry

new = list(new.values())


"""
labels that need to be converted to pyarrow features
"""

# need to make sorting better

my_features = {
    "image": features.Array2D(dtype="float32"),
    "img_id": nlp.Value("string"),
    "boxes": features.Array2D(dtype="int32"),
    "img_h": nlp.Value("int32"),
    "img_w": nlp.Value("int32"),
    "labels": nlp.features.Array2D(dtype="string"),
    "labels_confidence": nlp.features.Array2D(dtype="float32"),
    "num_boxes": nlp.Value("int32"),
    "attrs_id": nlp.features.Sequence(nlp.ClassLabel(num_classes=400)),
    "objs_id": nlp.features.Sequence(nlp.ClassLabel(num_classes=1600)),
    "attrs_confidence": nlp.features.Sequence(nlp.Value("float32")),
    "objs_confidence": nlp.features.Sequence(nlp.Value("float32")),
    "captions": nlp.features.Sequence(nlp.Value("string")),
    "questions": nlp.features.Sequence(nlp.Value("string")),
}

my_examples = []
for i in range(len(new)):

    ex = {
        "image": new[i]["features"].astype("float32"),
        "img_id": new[i]["img_id"],
        "boxes": new[i]["boxes"],
        "img_h": new[i]["img_h"],
        "img_w": new[i]["img_w"],
        "labels": new[i]["label"],
        "labels_confidence": new[i]["label_conf"],
        "num_boxes": new[i]["num_boxes"],
        "attrs_id": new[i]["attrs_id"],
        "objs_id": new[i]["objects_id"],
        "attrs_confidence": new[i]["attrs_conf"],
        "objs_confidence": new[i]["objects_conf"],
        "captions": new[i]["sent"],
        "questions": new[i]["question"],
    }

    t = (i, ex)
    my_examples.append(t)


my_features = nlp.Features(my_features)
writer = ArrowWriter(data_type=my_features.type, path=f"{ROOT}/{split}.arrow")
for key, record in my_examples:
    example = my_features.encode_example(record)
    writer.write(example)
num_examples, num_bytes = writer.finalize()
dataset = nlp.Dataset.from_file(f"{ROOT}/{split}.arrow")
