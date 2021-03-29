# class_mapping = {
#     "Dataset Description": DatasetDescription,
# }

# key_mapping = {
#     "Dataset Desription": 'dataset_desc'
# }

# import json
import yaml
import pprint
yaml_struc = """
name: "" # Filename
text: false
subsections:
  - name: "Dataset Card for X"
    text: false
    required: true
    subsections:
      - name: "Table of Contents"
        text: true
        subsections: null # meaning it should not be checked.
      - name: "Dataset Description"
        text: false
        subsections:
          - name: "Dataset Summary"
            text: true
            subsections: null
          - name: "Supported Tasks and Leaderboards"
            text: false
            subsections: null
          - name: Languages
            text: false
            subsections: null
      - name: "Dataset Structure"
        text: false
        subsections:
          - name: "Data Instances"
            text: true
            subsections: null
          - name: "Data Fields"
            text: true
            subsections: null
          - name: "Data Splits"
            text: true
            subsections: null
      - name: "Dataset Creation"
        text: false
        subsections:
        - name: "Curation Rationale"
          text: false
          subsections: null
        - name: "Source Data"
          text: false
          subsections:
            - name: "Initial Data Collection and Normalization"
              text: false
              subsections: null
            - name: "Who are the source X producers?"
              text: false
              subsections: null
        - name: "Annotations"
          text: false
          subsections:
            - name: "Annotation process"
              text: false
              subsections: null
            - name: "Who are the annotators?"
              text: false
              subsections: null
        - name: "Personal and Sensitive Information"
          text: false
          subsections: null
      - name: "Considerations for Using the Data"
        text: false
        subsections:
          - name: "Social Impact of Dataset"
            text: false
            subsections: null
          - name: "Discussion of Biases"
            text: false
            subsections: null
          - name: "Other Known Limitations"
            text: false
            subsections: null
      - name: "Additional Information"
        text: false
        subsections:
          - name: "Dataset Curators"
            text: false
            subsections: null
          - name: "Licensing Information"
            text: false
            subsections: null
          - name: "Citation Information"
            text: true
            subsections: null
          - name: "Contributions"
            text: true
            subsections: null
"""

filler_text = ["[Needs More Information]", "[More Information Needed]", "(https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)"]


class Section:
    def __init__(self, name, level, lines=None):
        self.name = name
        self.level = level
        self.text = ""
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

    def to_dict(self):
        return {
            "name": self.name,
            "test": self.text,
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
                print("The README doesn't contain proper tags. Please ensure you add the correct YAML tags.")
                return
            super().parse(f)

    def _validate_section(self, section , structure):
        # Text validation
        if structure['text'] == True:
            if section.text.strip() == '' or section.text.strip() in filler_text:
                print(f"Expected some text for section '{section.name}'")

        if structure['subsections'] is not None:
            # If no subsections present
            if section.content == {}:
                values = [subsection['name'] for subsection in structure['subsections']]
                print(f"'{section.name}'' expected the following subsections: {values}, found `None`.")
            else:
                # Each key validation
                structure_names = [subsection['name'] for subsection in structure['subsections']]
                for idx, name in enumerate(structure_names):
                    if name not in section.content:
                        print(f"'{section.name}' is missing subsection: '{name}'.")
                    else:
                        self._validate_section(section.content[name], structure['subsections'][idx])

                for name in section.content:
                    if name not in structure_names:
                        print(f"'{section.name}' has an extra subsection: '{name}'. Skipping validation checks for this subsection.")

    def validate(self, yaml_struc):
        structure = yaml.safe_load(yaml_struc)
        num_first_level_keys = len(self.content.keys())
        if num_first_level_keys > 1:
            print(f"The README has found several first-level headings: {list(self.content.keys())}. Only one heading is expected.")
        elif num_first_level_keys < 1:
            print(f"The README has no first-level headings.")

        else:
            print(self.content.keys())
            start_key = list(self.content.keys())[0]
            if start_key.startswith("Dataset Card for"):
                self._validate_section(self.content[start_key], structure['subsections'][0])
            else:
                print("No first-level hearding starting with `Dataset Card for` found.")


if __name__ == "__main__":
    readme = ReadMe("./dummy_readme.md")
    readme.validate(yaml_struc)
