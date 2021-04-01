# class_mapping = {
#     "Dataset Description": DatasetDescription,
# }

# key_mapping = {
#     "Dataset Desription": 'dataset_desc'
# }

import pprint

# import json
import yaml


yaml_struc = """
name: "" # Filename
allow_empty: false
subsections:
  - name: "Dataset Card for X"
    allow_empty: true
    subsections:
      - name: "Table of Contents"
        allow_empty: false
        subsections: null # meaning it should not be checked.
      - name: "Dataset Description"
        allow_empty: false
        subsections:
          - name: "Dataset Summary"
            allow_empty: false
            subsections: null
          - name: "Supported Tasks and Leaderboards"
            allow_empty: true
            subsections: null
          - name: Languages
            allow_empty: true
            subsections: null
      - name: "Dataset Structure"
        allow_empty: true
        subsections:
          - name: "Data Instances"
            allow_empty: false
            subsections: null
          - name: "Data Fields"
            allow_empty: false
            subsections: null
          - name: "Data Splits"
            allow_empty: false
            subsections: null
      - name: "Dataset Creation"
        allow_empty: true
        subsections:
        - name: "Curation Rationale"
          allow_empty: true
          subsections: null
        - name: "Source Data"
          allow_empty: true
          subsections:
            - name: "Initial Data Collection and Normalization"
              allow_empty: true
              subsections: null
            - name: "Who are the source X producers?"
              allow_empty: true
              subsections: null
        - name: "Annotations"
          allow_empty: true
          subsections:
            - name: "Annotation process"
              allow_empty: true
              subsections: null
            - name: "Who are the annotators?"
              allow_empty: true
              subsections: null
        - name: "Personal and Sensitive Information"
          allow_empty: true
          subsections: null
      - name: "Considerations for Using the Data"
        allow_empty: true
        subsections:
          - name: "Social Impact of Dataset"
            allow_empty: true
            subsections: null
          - name: "Discussion of Biases"
            allow_empty: true
            subsections: null
          - name: "Other Known Limitations"
            allow_empty: true
            subsections: null
      - name: "Additional Information"
        allow_empty: true
        subsections:
          - name: "Dataset Curators"
            allow_empty: true
            subsections: null
          - name: "Licensing Information"
            allow_empty: true
            subsections: null
          - name: "Citation Information"
            allow_empty: false
            subsections: null
          - name: "Contributions"
            allow_empty: false
            subsections: null
"""

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
        self.parse(file_path)

    def parse(self, file_path):
        with open(self.name) as f:
            # Skip Tags
            tag_count = 0
            for line in f:
                if line.strip(" \n") == "---":
                    tag_count += 1
                    if tag_count == 2:
                        break
            else:
                raise ValueError("The README doesn't contain proper tags. Please ensure you add the correct YAML tags.")
            super().parse(f)

    def _validate_section(self, section, structure):
        # Text validation
        error_list = []
        if structure["allow_empty"] == False:
            if section.is_empty:
                print(section.text)
                error_list.append(f"Expected some text for section '{section.name}'")

        if structure["subsections"] is not None:
            # If no subsections present
            if section.content == {}:
                values = [subsection["name"] for subsection in structure["subsections"]]
                error_list.append(f"'{section.name}'' expected the following subsections: {values}, found `None`.")
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

    def validate(self, yaml_struc):
        error_list = []
        structure = yaml.safe_load(yaml_struc)
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
                error_list += self._validate_section(self.content[start_key], structure["subsections"][0])
            else:
                error_list.append("No first-level heading starting with `Dataset Card for` found.")
        return error_list


if __name__ == "__main__":
    readme = ReadMe("./dummy_readme.md")
    error_list = readme.validate(yaml_struc)
    if error_list != []:
        errors = "\n".join(list(map(lambda x: "-\t" + x, error_list)))
        error_string = "The following issues were found with the README\n" + errors
        raise ValueError(error_string)
