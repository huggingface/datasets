import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import yaml


BASE_REF_URL = "https://github.com/huggingface/datasets/tree/master/src/datasets/utils"
this_url = f"{BASE_REF_URL}/{__file__}"
logger = logging.getLogger(__name__)


def load_yaml_resource(resource: str) -> Tuple[Any, str]:
    with open(resource) as f:
        content = yaml.safe_load(f)
    return content, f"{BASE_REF_URL}/resources/{resource}"


readme_structure, known_readme_structure_url = load_yaml_resource("readme_structure.yaml")
filler_text = [
    "[Needs More Information]",
    "[More Information Needed]",
    "(https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)",
]


class Section:
    def __init__(self, name, level, lines=None):
        self.name = name
        self.level = level
        self.text = ""
        self.is_empty = True
        self.content = {}
        if lines is not None:
            self.parse(lines)

    def parse(self, lines):
        current_sub_level = ""
        current_lines = []
        code_start = False
        for line in lines:
            if line.strip(" \n") == "":
                continue
            elif line.strip(" \n")[:3] == "```":
                code_start = not code_start
            elif line.split()[0] == self.level + "#" and not code_start:
                if current_sub_level != "":
                    self.content[current_sub_level] = Section(current_sub_level, self.level + "#", current_lines)
                    current_lines = []
                else:
                    if current_lines != []:
                        self.text += "".join(current_lines).strip()
                        if self.text != "" and self.text not in filler_text:
                            self.is_empty = False
                        current_lines = []

                current_sub_level = " ".join(line.split()[1:]).strip(" \n")
            else:
                current_lines.append(line)
        else:
            if current_sub_level != "":
                self.content[current_sub_level] = Section(current_sub_level, self.level + "#", current_lines)
            else:
                if current_lines != []:
                    self.text += "".join(current_lines).strip()
                    if self.text != "" and self.text not in filler_text:
                        self.is_empty = False

    def to_dict(self):
        return {
            "name": self.name,
            "text": self.text,
            "is_empty": self.is_empty,
            "subsections": [value.to_dict() for value in self.content.values()],
        }


class ReadMe(Section):  # Level 0
    def __init__(self, file_path):
        super().__init__(name=file_path, level="")
        self.yaml_tags_line_count = -2
        self.parse(file_path)

    def parse(self, file_path):
        with open(self.name) as f:
            # Skip Tags
            tag_count = 0
            for line in f:
                self.yaml_tags_line_count += 1
                if line.strip(" \n") == "---":
                    tag_count += 1

                    if tag_count == 2:
                        break
            else:
                raise ValueError(
                    "The README doesn't contain proper tags. Please ensure you add the correct YAML tags."
                )
            super().parse(f)

    def _validate_section(self, section, structure):
        # Text validation
        error_list = []
        if structure["allow_empty"] == False:
            if section.is_empty:
                error_list.append(f"Expected some text for section '{section.name}'")

        if structure["subsections"] is not None:
            # If no subsections present
            if section.content == {}:
                values = [subsection["name"] for subsection in structure["subsections"]]
                error_list.append(f"'{section.name}' expected the following subsections: {values}, found `None`.")
            else:
                # Each key validation
                structure_names = [subsection["name"] for subsection in structure["subsections"]]
                for idx, name in enumerate(structure_names):
                    if name not in section.content:
                        error_list.append(f"'{section.name}' is missing subsection: '{name}'.")
                    else:
                        error_list += self._validate_section(section.content[name], structure["subsections"][idx])

                for name in section.content:
                    if name not in structure_names:
                        error_list.append(
                            f"'{section.name}' has an extra subsection: '{name}'. Skipping validation checks for this subsection."
                        )

        return error_list

    def __str__(self):
        return str(self.to_dict())

    def validate(self, readme_structure):
        error_list = []
        num_first_level_keys = len(self.content.keys())
        if num_first_level_keys > 1:
            error_list.append(
                f"The README has found several first-level headings: {list(self.content.keys())}. Only one heading is expected."
            )
        elif num_first_level_keys < 1:
            error_list.append(f"The README has no first-level headings.")

        else:
            start_key = list(self.content.keys())[0]
            if start_key.startswith("Dataset Card for"):
                error_list += self._validate_section(self.content[start_key], readme_structure["subsections"][0])
            else:
                error_list.append("No first-level heading starting with `Dataset Card for` found.")
        return error_list


def validate_readme(file_path):
    readme = ReadMe(file_path)
    if readme.yaml_tags_line_count == 0:
        raise Warning("YAML Tags are not present in this README.")
    elif readme.yaml_tags_line_count == -1:
        raise Warning("Only the start of YAML tags present in this README.")
    error_list = readme.validate(readme_structure)
    if error_list != []:
        errors = "\n".join(list(map(lambda x: "-\t" + x, error_list)))
        error_string = "The following issues were found with the README\n" + errors
        raise ValueError(error_string)


if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(usage="Validate the content (excluding YAML tags) of a README.md file.")
    ap.add_argument("readme_filepath")
    args = ap.parse_args()
    readme_filepath = Path(args.readme_filepath)
    validate_readme(readme_filepath)
