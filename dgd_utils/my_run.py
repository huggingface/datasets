import json
import os
from collections import defaultdict

from datasets import load_dataset


def btag(tag, text):
    text = text.replace("\n", "\t")
    return "<{}> {}".format(tag, text)


def load_sharc_bart(split, out_path=None):
    dataset = load_dataset("sharc", split=split)
    source = []
    target = []
    if out_path and not os.path.exists(out_path):
        os.makedirs(out_path)
    for ex in dataset:
        contexts = [
            btag("snippet", ex["snippet"]),
            btag("scenario", ex["scenario"]),
            btag("question", ex["question"]),
        ]
        if not ex["history"]:
            continue
        while len(ex["history"]) > 0:
            turn = ex["history"].pop()
            source.append("\t".join(contexts))
            target.append(turn["follow_up_question"])
            contexts.extend([btag("agent", turn["follow_up_question"]), btag("user", turn["follow_up_answer"])])
        source.append("\t".join(contexts))
        target.append(ex["answer"])
        break
    with open(os.path.join(out_path, "{}.source".format(split)), "w") as fp:
        fp.write("\n".join(source))
        fp.close()
    with open(os.path.join(out_path, "{}.target".format(split)), "w") as fp:
        fp.write("\n".join(target))
        fp.close()


def load_doqa_bart(split, out_path=None):
    dataset = load_dataset("doqa", name="cooking", split=split)
    source = []
    target = []
    if out_path and not os.path.exists(out_path):
        os.makedirs(out_path)
    contexts = []
    dial_id_pre = None
    for ex in dataset:
        if not ex["answers"]:
            continue
        dial_id, q_id = ex["id"].split("#")
        question_context = btag("user", ex["question"])
        answer_context = btag("agent", ex["answers"]["text"][0])
        if ex["followup"] != "y" or dial_id != dial_id_pre:
            contexts = [
                btag("title", ex["title"]),
                btag("context", ex["context"]),
                btag("background", ex["background"]),
            ]
        source.append("\t".join(contexts + [question_context]))
        target.append(ex["answers"]["text"][0])
        if ex["followup"] == "y":
            contexts.extend([question_context, answer_context])
        dial_id_pre = dial_id
        # break
    with open(os.path.join(out_path, "{}.source".format(split)), "w") as fp:
        fp.write("\n".join(source))
        fp.close()
    with open(os.path.join(out_path, "{}.target".format(split)), "w") as fp:
        fp.write("\n".join(target))
        fp.close()


def load_doc2dial_bart(split, out_path=None):
    dataset = load_dataset(
        "/Users/songfeng/work/projects/hf_datasets/datasets/doc2dial/", name="doc2dial_rc", split=split
    )
    source = []
    target = []
    if out_path and not os.path.exists(out_path):
        os.makedirs(out_path)
    contexts = []
    dial_id_pre = None
    for ex in dataset:
        if ex["is_impossible"]:
            continue
        dial_id, turn_id = ex["id"].split("_")
        user_context = btag("user", ex["question"])
        da_context = btag("da", ex["answers"]["da"][0])
        agent_context = btag("agent", ex["answers"]["utterance"][0])
        agent_utterance = ex["answers"]["utterance"][0]
        if dial_id_pre != dial_id:
            contexts = [
                btag("title", ex["title"]),
                btag("doc_context", ex["doc_context"]),
            ]
        dial_id_pre = dial_id
        source.append("\t".join(contexts + [user_context, da_context]))
        target.append(agent_utterance)
        contexts.extend([user_context, agent_context])
    with open(os.path.join(out_path, "{}.source".format(split)), "w") as fp:
        fp.write("\n".join(source))
        fp.close()
    with open(os.path.join(out_path, "{}.target".format(split)), "w") as fp:
        fp.write("\n".join(target))
        fp.close()


if __name__ == "__main__":
    # load_doqa_bart("train", "~/work/projects/data/my_bart_doqa/")
    # load_sharc_bart("train", "~/work/projects/data/my_bart_sharc/")
    load_doc2dial_bart("validation", "my_bart_doc2dial/")
