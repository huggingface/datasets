# Copyright 2021 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse


CUSTOM_JS_FILE = "docs/source/_static/js/custom.js"


def update_custom_js(version):
    """Update the version table in the custom.js file."""
    with open(CUSTOM_JS_FILE, encoding="utf-8", newline="\n") as f:
        lines = f.readlines()
    index = 0

    # First let's put the right version
    while not lines[index].startswith("const stableVersion ="):
        index += 1
    lines[index] = f'const stableVersion = "v{version}"\n'

    # Then update the dictionary
    while not lines[index].startswith("const versionMapping = {"):
        index += 1

    # We go until the end
    while not lines[index].startswith("}"):
        index += 1
    # We add the new version at the end
    lines[index - 1] += f'    "v{version}": "v{version}",\n'

    with open(CUSTOM_JS_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="Release version.")
    args = parser.parse_args()
    update_custom_js(args.version)
