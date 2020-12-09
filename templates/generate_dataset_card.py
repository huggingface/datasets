#!/usr/bin/env python3
from datasets import load_dataset
import random
import sys
import json
from pytablewriter import MarkdownTableWriter
from io import StringIO
from pathlib import Path
import jinja2

import sys

indent = 4


def _make_iterencode(
    markers,
    _default,
    _encoder,
    _indent,
    _floatstr,
    _key_separator,
    _item_separator,
    _sort_keys,
    _skipkeys,
    _one_shot,
    ## HACK: hand-optimized bytecode; turn globals into locals
    ValueError=ValueError,
    dict=dict,
    float=float,
    id=id,
    int=int,
    isinstance=isinstance,
    list=list,
    str=str,
    tuple=tuple,
    _intstr=int.__str__,
):

    _array_indent = None
    if isinstance(_indent, tuple):
        (_indent, _array_indent) = _indent
    else:
        _array_indent = _indent
    if _indent is not None and not isinstance(_indent, str):
        _indent = " " * _indent
    if _array_indent is not None and not isinstance(_array_indent, str):
        _array_indent = " " * _array_indent

    def _iterencode_list(lst, _current_indent_level):
        if not lst:
            yield "[]"
            return
        if markers is not None:
            markerid = id(lst)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = lst
        buf = "["
        if _array_indent is not None:
            _current_indent_level += 1
            newline_indent = "\n" + _array_indent * _current_indent_level
            separator = _item_separator + newline_indent
            buf += newline_indent
        else:
            newline_indent = None
            separator = _item_separator
        first = True
        for value in lst:
            if first:
                first = False
            else:
                buf = separator
            if isinstance(value, str):
                yield buf + _encoder(value)
            elif value is None:
                yield buf + "null"
            elif value is True:
                yield buf + "true"
            elif value is False:
                yield buf + "false"
            elif isinstance(value, int):
                # Subclasses of int/float may override __str__, but we still
                # want to encode them as integers/floats in JSON. One example
                # within the standard library is IntEnum.
                yield buf + _intstr(value)
            elif isinstance(value, float):
                # see comment above for int
                yield buf + _floatstr(value)
            else:
                yield buf
                if isinstance(value, (list, tuple)):
                    chunks = _iterencode_list(value, _current_indent_level)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                else:
                    chunks = _iterencode(value, _current_indent_level)
                yield from chunks
        if newline_indent is not None:
            _current_indent_level -= 1
            yield "\n" + _array_indent * _current_indent_level
        yield "]"
        if markers is not None:
            del markers[markerid]

    def _iterencode_dict(dct, _current_indent_level):
        if not dct:
            yield "{}"
            return
        if markers is not None:
            markerid = id(dct)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = dct
        yield "{"
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = "\n" + _indent * _current_indent_level
            item_separator = _item_separator + newline_indent
            yield newline_indent
        else:
            newline_indent = None
            item_separator = _item_separator
        first = True
        if _sort_keys:
            items = sorted(dct.items(), key=lambda kv: kv[0])
        else:
            items = dct.items()
        for key, value in items:
            if isinstance(key, str):
                pass
            # JavaScript is weakly typed for these, so it makes sense to
            # also allow them.  Many encoders seem to do something like this.
            elif isinstance(key, float):
                # see comment for int/float in _make_iterencode
                key = _floatstr(key)
            elif key is True:
                key = "true"
            elif key is False:
                key = "false"
            elif key is None:
                key = "null"
            elif isinstance(key, int):
                # see comment for int/float in _make_iterencode
                key = _intstr(key)
            elif _skipkeys:
                continue
            else:
                raise TypeError("key " + repr(key) + " is not a string")
            if first:
                first = False
            else:
                yield item_separator
            yield _encoder(key)
            yield _key_separator
            if isinstance(value, str):
                yield _encoder(value)
            elif value is None:
                yield "null"
            elif value is True:
                yield "true"
            elif value is False:
                yield "false"
            elif isinstance(value, int):
                # see comment for int/float in _make_iterencode
                yield _intstr(value)
            elif isinstance(value, float):
                # see comment for int/float in _make_iterencode
                yield _floatstr(value)
            else:
                if isinstance(value, (list, tuple)):
                    chunks = _iterencode_list(value, _current_indent_level)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                else:
                    chunks = _iterencode(value, _current_indent_level)
                yield from chunks
        if newline_indent is not None:
            _current_indent_level -= 1
            yield "\n" + _indent * _current_indent_level
        yield "}"
        if markers is not None:
            del markers[markerid]

    def _iterencode(o, _current_indent_level):
        if isinstance(o, str):
            yield _encoder(o)
        elif o is None:
            yield "null"
        elif o is True:
            yield "true"
        elif o is False:
            yield "false"
        elif isinstance(o, int):
            # see comment for int/float in _make_iterencode
            yield _intstr(o)
        elif isinstance(o, float):
            # see comment for int/float in _make_iterencode
            yield _floatstr(o)
        elif isinstance(o, (list, tuple)):
            yield from _iterencode_list(o, _current_indent_level)
        elif isinstance(o, dict):
            yield from _iterencode_dict(o, _current_indent_level)
        else:
            if markers is not None:
                markerid = id(o)
                if markerid in markers:
                    raise ValueError("Circular reference detected")
                markers[markerid] = o
            o = _default(o)
            yield from _iterencode(o, _current_indent_level)
            if markers is not None:
                del markers[markerid]

    return _iterencode


json.encoder._make_iterencode = _make_iterencode
indent = (4, None)


def pretty_json(p):
    return json.dumps(p, sort_keys=False, indent=indent, separators=[", ", ": "])


class FieldExtractor:
    def __init__(self, file_name):
        self.file_name = file_name

    def run(self):
        import tokenize
        import re

        was_class = False
        fileObj = open(self.file_name)

        classes = {}

        for toktype, tok, start, end, line in tokenize.generate_tokens(
            fileObj.readline
        ):
            # we can also use token.tok_name[toktype] instead of 'COMMENT'
            # from the token module
            if was_class:
                current_class = tok
                was_class = False
            if tok == "class":
                was_class = True
            if toktype == tokenize.COMMENT:
                if "datasets." in line:
                    line = line.strip().split("#")

                    field_info = line[0].split(":")
                    search1 = re.search("['\"](.*)['\"]", field_info[0], re.IGNORECASE)

                    type = field_info[1].strip()
                    replacements = [
                        ("datasets.features.Sequence(", "List["),
                        ('datasets.Value("string")', "string"),
                        (")", "]"),
                        (",", ""),
                    ]
                    for replacement in replacements:
                        type = type.replace(*replacement)

                    try:
                        field_name = search1.group(1)

                        if current_class not in classes:
                            classes[current_class] = {}
                        comment = line[1]
                        classes[current_class][field_name] = dict(
                            type=type, comment=comment
                        )
                    except Exception as e:
                        print(f"PROBLEM with {line}")

        return classes


class DataSetCardWriter:
    TOC = {
        "Dataset Description": ["Dataset Summary", "Supported Tasks", "Languages"],
        "Dataset Structure": ["Data Instances", "Data Fields", "Data Splits"],
        "Dataset Creation": [
            "Curation Rationale",
            "Source Data",
            "Annotations",
            "Personal and Sensitive Information",
        ],
        "Considerations for Using the Data": [
            "Social Impact of Dataset",
            "Discussion of Biases",
            "Other Known Limitations",
        ],
        "Additional Information": [
            "Dataset Curators",
            "Licensing Information",
            "Citation Information",
        ],
    }

    def __init__(self, name, config_names, output_path):
        self.name = name
        self.config_names = config_names
        self.output_path = output_path

    def get_markdown_string(self, markdown_writer):
        markdown = ""
        s = StringIO(markdown)
        s.close = lambda: None
        markdown_writer.dump(s)
        f = StringIO(s.getvalue())
        lines = f.readlines()[1:]
        ret = "".join(lines) + "\n\n"
        return ret

    def config_split_sizes_string(self, dataset, config):
        """Returns the string for the markdown table containing splits size, and a dict containing them."""
        headers = [""] + list(dataset.keys())
        values = [[config] + [dataset[key].num_rows for key in headers[1:]]]
        writer = MarkdownTableWriter(
            table_name=f"### {config}", headers=headers, value_matrix=values
        )

        data_splits_str = self.get_markdown_string(writer)

        split_sizes = {key: dataset[key].num_rows for key in list(dataset.keys())}

        return data_splits_str, split_sizes

    def aggregated_config_splits(self):
        """Try to build an aggregated markdown table with sizes for each split for each config, if all configs have the same splits."""
        first_config = list(self.configs_info.keys())[0]
        config_splits0 = list(self.configs_info[first_config].keys())

        headers = ["name"] + config_splits0
        values = []

        same_splits = True
        for k, v in self.configs_info.items():
            config_splits = list(v["split_sizes"].keys())
            if config_splits != config_splits0:
                same_splits = False
                break
            values.append([k] + [v["split_sizes"][key] for key in config_splits0])

        if same_splits:
            writer = MarkdownTableWriter(
                table_name="### Configurations", headers=headers, value_matrix=values
            )
            ret = self.get_markdown_string(writer)
            return ret
        else:
            # The splits are not the same -> no aggregated table
            return None

    def get_field_description(self, config_name, field_name):
        return None

    TOBEADDED="[TO BE ADDED]"
    def field_description(self, config_name, field_name):
        base = self.get_field_description(config_name, field_name)
        if base is None:
            return self.TOBEADDED

        base = base.strip()

        if base == "":
            return self.TOBEADDED

        return str(base)


    def run(self):
        # If configs are not given, try to guess the config names using the exception string...
        if self.config_names == None:
            try:
                _ = load_dataset(self.name)
                self.config_names = ["default"]
            except Exception as e:
                if "[" not in str(e):
                    raise
                s = str(e).split("[")[-1].split("]")[0].split(",")
                s = [e.replace("'", "").replace(" ", "") for e in s]
                self.config_names = s
                print("Guessed config list:", self.config_names)

        self.configs_info = {}
        for config_name in self.config_names:
            # Load the dataset
            dataset = load_dataset(self.name, config_name)
            # Choose a split randomly
            rnd_split = random.choice(list(dataset.keys()))
            # Get the split
            dataset_split = dataset[rnd_split]

            # Gather some information about this config
            config = {}
            self.configs_info[config_name] = config

            config["excerpt_split"] = rnd_split
            config["excerpt"] = pretty_json(dataset_split[0])

            (
                config["data_splits_str"],
                config["split_sizes"],
            ) = self.config_split_sizes_string(dataset, config_name)
            config["fields"] = {k: self.field_description(config_name, k) for k in dataset_split.features.keys()}

        # Prettyfying the config split size: check if all configs have the same splits, and if yes, build a single
        # table containing all the split sizes
        aggregated_data_splits_str = self.aggregated_config_splits()

        # Load the jinja template
        template_file = Path(__file__).parent / "README.template.md"
        template = jinja2.Template(template_file.open().read())

        header = {"Homepage": "https://github.com/microsoft/CodeXGlue"}

        # Render the template with the gathered information
        ret = template.render(
            dataset_name = str(Path(self.name).name),
            toc=self.TOC,
            header=header,
            configs=self.configs_info,
            aggregated_data_splits_str=aggregated_data_splits_str,
        )

        # Write the result
        with (self.output_path).open("w") as readme_file:
            readme_file.write(ret)


class CodeXGlueDataSetCardWriter(DataSetCardWriter):
    def __init__(self, name, config_names, output_path, code_path):
        super().__init__(name, config_names, output_path)
        self.code_path = code_path
        self.fe = FieldExtractor(self.code_path)
        field_info = self.fe.run()
        self.last_class = list(field_info.keys())[-1]
        self.last_class_info = field_info[self.last_class]


    def get_field_description(self, config_name, field_name):
        ret = self.last_class_info.get(field_name, {}).get("comment")
        return ret



for f in (Path(__file__).parent.parent).iterdir():
    if f.name.startswith("code_x_glue_"):
        name = f.name
        if "search" in name:
            continue
#        name = "code_x_glue_ct_code_to_text"
        configs = None  # ["javascript", "python", "go"]
        dataset_path = Path(f"/home/lagunas/devel/hf/datasets/datasets/{name}")
        ds = CodeXGlueDataSetCardWriter(str(dataset_path), configs, dataset_path / "README.md", dataset_path / "configs.py")
        ds.run()


# fe = FieldExtractor("code_x_glue_text_to_code.py")
# print(fe.run())
