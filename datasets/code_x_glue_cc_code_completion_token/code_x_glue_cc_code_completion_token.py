import os
import os.path
from typing import List

import datasets

from .common import Child
from .generated_definitions import DEFINITIONS


_DESCRIPTION = """Predict next code token given context of previous tokens. Models are evaluated by token level accuracy.
Code completion is a one of the most widely used features in software development through IDEs. An effective code completion tool could improve software developers' productivity. We provide code completion evaluation tasks in two granularities -- token level and line level. Here we introduce token level code completion. Token level task is analogous to language modeling. Models should have be able to predict the next token in arbitary types.
"""

_CITATION = """@article{raychev2016probabilistic,
    title={Probabilistic Model for Code with Decision Trees},
    author={Raychev, Veselin and Bielik, Pavol and Vechev, Martin},
    journal={ACM SIGPLAN Notices},
    pages={731--747},
    year={2016},
    publisher={ACM New York, NY, USA}
}
@inproceedings{allamanis2013mining,
    title={Mining Source Code Repositories at Massive Scale using Language Modeling},
    author={Allamanis, Miltiadis and Sutton, Charles},
    booktitle={2013 10th Working Conference on Mining Software Repositories (MSR)},
    pages={207--216},
    year={2013},
    organization={IEEE}
}"""


class CodeXGlueCcCodeCompletionTokenImpl(Child):
    _DESCRIPTION = _DESCRIPTION
    _CITATION = _CITATION


class CodeXGlueCcCodeCompletionTokenJavaImpl(CodeXGlueCcCodeCompletionTokenImpl):
    SPLITS = {
        "training": datasets.Split.TRAIN,
        "validation": datasets.Split.VALIDATION,
        "test": datasets.Split.TEST,
    }

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "code": datasets.features.Sequence(datasets.Value("string")),  # Code Tokens
    }

    def generate_urls(self, split_name):
        language = self.info["parameters"]["language"]
        if language != "java":
            raise RuntimeError(f"Unknown language {language}: should be java.")

        yield "data", f"https://zenodo.org/record/3628665/files/java_{split_name}_pre"

    def _generate_examples(self, split_name, file_paths):
        with open(file_paths["data"], encoding="utf-8") as f:
            for idx, line in enumerate(f):
                new_data = []
                for token in line.strip().split():
                    if len(token) > 100:
                        continue
                    new_data.append(token)
                entry = dict(id=idx, code=new_data)
                yield idx, entry


class CodeXGlueCcCodeCompletionTokenPythonImpl(CodeXGlueCcCodeCompletionTokenImpl):
    SPLITS = {"train": datasets.Split.TRAIN, "test": datasets.Split.TEST}

    _FEATURES = {
        "id": datasets.Value("int32"),  # Index of the sample
        "path": datasets.Value("string"),  # Original path in the dataset
        "code": datasets.features.Sequence(datasets.Value("string")),  # Code Tokens
    }

    PYTHON_FILE_MAPPING = dict(train="python100k_train.txt", test="python50k_eval.txt")

    def generate_urls(self, split_name):
        language = self.info["parameters"]["language"]
        if language != "python":
            raise RuntimeError(f"Unknown language {language}")

        yield "data", "http://files.srl.inf.ethz.ch/data/py150_files.tar.gz"

    def process_string(self, token):
        # Copyright (c) Microsoft Corporation.
        # Licensed under the MIT License.
        import re

        str_quote_options = ["'''", '"""', "'", '"']
        start_quote = ""
        end_quote = ""
        qualifier_regex = r"^[a-z]+"
        qualifier_match = re.search(qualifier_regex, token)
        # string qualifiers like 'r' for regex, 'f' for formatted string, 'b' for bytes, 'u' for unicode, etc (or combination of them)
        qualifier = "" if not qualifier_match else qualifier_match[0]
        # token string without qualifiers
        token_string = re.sub(qualifier_regex, "", token)
        # string literal without quotes
        str_lit = token_string
        for q in str_quote_options:
            if token_string.startswith(q):
                start_quote = q
                str_lit = str_lit[len(q) :]
                if token_string.endswith(q):
                    end_quote = q
                    str_lit = str_lit[: -len(q)]
                break
        if start_quote in str_quote_options[:2]:
            return ""
        return (
            f"{qualifier}{start_quote}{str_lit}{end_quote}"
            if len(str_lit) < 15
            and "\n" not in str_lit
            and "</s>" not in str_lit
            and "<s>" not in str_lit
            and "<pad>" not in str_lit
            and "<EOL>" not in str_lit
            else f"{qualifier}{start_quote}{end_quote}"
        )

    def py_tokenize(self, base_dir, file_name):
        # Copyright (c) Microsoft Corporation.
        # Licensed under the MIT License.
        from io import BytesIO
        from tokenize import COMMENT, ENCODING, ENDMARKER, INDENT, NEWLINE, NL, NUMBER, STRING, tokenize

        file_paths = open(os.path.join(base_dir, file_name), encoding="utf-8").readlines()
        for ct, path in enumerate(file_paths):
            try:
                code = open(os.path.join(base_dir, path.strip()), encoding="utf-8").read()
                token_gen = tokenize(BytesIO(bytes(code, "utf8")).readline)
                out_tokens = []
                prev_eol = False
                for toknum, tokval, _, _, _ in token_gen:
                    tokval = " ".join(tokval.split())
                    if len(tokval) > 100:
                        continue
                    if toknum == STRING:
                        add_token = self.process_string(tokval)
                        if len(add_token) > 0:
                            out_tokens.append(add_token)
                            prev_eol = False
                    elif toknum == NUMBER:
                        if len(tokval) < 50:
                            out_tokens.append(tokval)
                            prev_eol = False
                    elif toknum in [NEWLINE, NL]:
                        if not prev_eol:
                            out_tokens.append("<EOL>")
                            prev_eol = True
                    elif toknum in [COMMENT, INDENT, ENCODING, ENDMARKER] or len(tokval) == 0:
                        continue
                    else:
                        out_tokens.append(tokval)
                        prev_eol = False
                if out_tokens[0] == "<EOL>":
                    out_tokens = out_tokens[1:]
                if out_tokens[-1] == "<EOL>":
                    out_tokens = out_tokens[:-1]
            except Exception:
                out_tokens = []
            out_tokens = ["<s>"] + out_tokens + ["</s>"]
            yield path, out_tokens

    def _generate_examples(self, split_name, file_paths):
        base_dir = file_paths["data"]
        filename = self.PYTHON_FILE_MAPPING[split_name]

        data_dir = os.path.join(base_dir, "data")
        if not os.path.exists(data_dir):
            import gzip
            import tarfile

            gzip_filename = os.path.join(base_dir, "data.tar.gz")
            with gzip.open(gzip_filename, "rb") as gzip_file:
                t = tarfile.TarFile(fileobj=gzip_file)
                t.extractall(path=base_dir)

        idx = 0
        for entry in self.py_tokenize(base_dir=base_dir, file_name=filename):
            path, out_tokens = entry
            path = path[len("data/") :]
            yield idx, dict(id=idx, path=path, code=out_tokens)
            idx += 1


CLASS_MAPPING = {
    "CodeXGlueCcCodeCompletionTokenJava": CodeXGlueCcCodeCompletionTokenJavaImpl,
    "CodeXGlueCcCodeCompletionTokenPython": CodeXGlueCcCodeCompletionTokenPythonImpl,
}


class CodeXGlueCcCodeCompletionToken(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = datasets.BuilderConfig
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name=name, description=info["description"]) for name, info in DEFINITIONS.items()
    ]

    def _info(self):
        name = self.config.name
        info = DEFINITIONS[name]
        if info["class_name"] in CLASS_MAPPING:
            self.child = CLASS_MAPPING[info["class_name"]](info)
        else:
            raise RuntimeError(f"Unknown python class for dataset configuration {name}")
        ret = self.child._info()
        return ret

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        return self.child._split_generators(dl_manager=dl_manager)

    def _generate_examples(self, split_name, file_paths):
        return self.child._generate_examples(split_name, file_paths)
