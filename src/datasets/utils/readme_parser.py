# class_mapping = {
#     "Dataset Description": DatasetDescription,
# }

# key_mapping = {
#     "Dataset Desription": 'dataset_desc'
# }
import json


class Section:
    def __init__(self, name, level, lines=None):
        self.name = name
        self.level = level
        self.attributes = ""
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
                        self.attributes += "".join(current_lines).strip()
                        current_lines = []

                current_sub_level = " ".join(line.split()[1:]).strip(" \n")
            else:
                current_lines.append(line)
        else:
            if current_sub_level != "":
                self.content[current_sub_level] = Section(current_sub_level, self.level + "#", current_lines)
            else:
                if current_lines != []:
                    self.attributes += "".join(current_lines).strip()

    def to_dict(self):
        return {
            "name": self.name,
            "attributes": self.attributes,
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
            super().parse(f)


if __name__ == "__main__":
    readme = ReadMe("./datasets/fashion_mnist/README.md")
    # print(readme.attributes)
    json_obj = json.dumps(readme.to_dict(), indent=4)
    print(json_obj)
