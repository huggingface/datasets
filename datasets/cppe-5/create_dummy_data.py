import json

train = r"C:\Users\Mario\Downloads\dataset.tar\dataset\annotations\train.json" #[:8]
test = r"C:\Users\Mario\Downloads\dataset.tar\dataset\annotations\test.json" #[:13]

import os
import copy
p = r"C:\Users\Mario\Desktop\projects\datasets\datasets\cppe-5\dummy\1.0.0\dummy_data\dataset\dataset\annotations"

with open(train, encoding="utf-8") as f:
    train_data = json.load(f)
    train_data["annotations"] = train_data["annotations"][:13]
    train_data["images"] = train_data["images"][:2]
    with open(os.path.join(p, "train.json"), "w", encoding="utf-8") as f:
        json.dump(train_data, f)

with open(test, encoding="utf-8") as f:
    test_data = json.load(f)
    test_data["annotations"] = test_data["annotations"][:8]
    test_data["images"] = test_data["images"][:2]
    with open(os.path.join(p, "test.json"), "w", encoding="utf-8") as f:
        json.dump(test_data, f)
