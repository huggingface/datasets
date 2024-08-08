# docstyle-ignore
INSTALL_CONTENT = """
# Datasets installation
! pip install datasets transformers
# To install from source instead of the last release, comment the command above and uncomment the following one.
# ! pip install git+https://github.com/huggingface/datasets.git
"""

notebook_first_cells = [{"type": "code", "content": INSTALL_CONTENT}]
default_branch_name = "main"
version_prefix = ""
