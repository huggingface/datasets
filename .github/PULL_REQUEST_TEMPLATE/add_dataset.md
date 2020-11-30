- **Name:** *name of the dataset*
- **Description:** *short description of the dataset (or link to social media or blog post)*
- **Paper:** *link to the dataset paper if available*
- **Data:** *link to the Github repository or current dataset location*
- **Motivation:** *what are some good reasons to have this dataset*

### Checkbox

- [ ] Create the dataset script `/datasets/my_dataset/my_dataset.py` using the template
- [ ] Fill the `_DESCRIPTION` and `_CITATION` variables
- [ ] Implement `_infos()`, `_split_generators()` and `_generate_examples()`
- [ ] Make sure that the `BUILDER_CONFIGS` class attribute is filled with the different configurations of the dataset and that the `BUILDER_CONFIG_CLASS` is specified if there is a custom config class.
- [ ] Generate the metadata file `dataset_infos.json` for all configurations
- [ ] Generate the dummy data `dummy_data.zip` files to have the dataset script tested and that they don't weigh too much (<50KB)
- [ ] Add the dataset card `README.md` using the template : fill the tags and the various paragraphs
- [ ] Both tests for the real data and the dummy data pass.
