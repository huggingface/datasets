- **Name:** *name of the dataset*
- **Description:** *short description of the dataset (or link to social media or blog post)*
- **Paper:** *link to the dataset paper if available*
- **Data:** *link to the Github repository or current dataset location*
- **Motivation:** *what are some good reasons to have this dataset*

### Checkbox

- [ ] Create the dataset script `./my_dataset/my_dataset.py` using the template
- [ ] Fill the `_DESCRIPTION` and `_CITATION` variables
- [ ] Implement `_info()`, `_split_generators()` and `_generate_examples()`
- [ ] Make sure that the `BUILDER_CONFIGS` class attribute is filled with the different configurations of the dataset and that the `BUILDER_CONFIG_CLASS` is specified if there is a custom config class.
- [ ] Add the dataset card `README.md` using the template : fill the tags and the various paragraphs
- [ ] Optional - test the dataset using `datasets-cli test ./dataset_name --save_info`
