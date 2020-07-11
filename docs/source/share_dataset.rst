Sharing your dataset
=============================================

Once you've written your own dataset loading script as detailed in the :doc:`add_dataset` chapter, you may want to share it with the community for instance on the `HuggingFace Hub <https://huggingface.co/datasets>`__.

There are two possibilities to do that:
- add it as a canonical dataset by opening a Pull-Request on the `GitHub repository for 🤗nlp <https://github.com/huggingface/nlp>`__,
- directly upload it as a community provided dataset under your name or your organization namespace.

In both cases you probably wants to add testing data to your dataset so it's behavior can be tested and verified.

Adding dummy test data
----------------------------

3. **Make sure you run all of the following commands from the root of your `nlp` git clone.**. To check that your dataset works correctly and to create its `dataset_infos.json` file run the command:

::

	python nlp-cli test datasets/<your-dataset-folder> --save_infos --all_configs

4. If the command was succesful, you should now create some dummy data. Use the following command to get in-detail instructions on how to create the dummy data:

::

	python nlp-cli dummy_data datasets/<your-dataset-folder> 


5. Now test that both the real data and the dummy data work correctly using the following commands:

*For the real data*:
::

	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your-dataset-name>

	and 

*For the dummy data*:
::

	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your-dataset-name>


6. If all tests pass, your dataset works correctly. Awesome! You can now follow steps 6, 7 and 8 of the section *How to contribute to nlp?*. If you experience problems with the dummy data tests, you might want to take a look at the section *Help for dummy data tests* below.


Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command 
	::

		python nlp-cli dummy_data datasets/<your-dataset-folder> 

	and make sure you follow the exact instructions provided by the command of step 5). 

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function `_split_generations(...)` and expected by the function `_generate_examples(...)` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the repo anyways and make a remark in the description that you need help creating the dummy data.

