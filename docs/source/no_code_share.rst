Upload a dataset to the Hub
===========================

In the last section of the tutorials, you will learn how to upload a dataset to the Hugging Face Hub. 🤗 Datasets aims to provide the largest collection of datasets that anyone can use to train their models. We welcome all dataset contributions from the NLP community, and we have made it very simple for you to add a dataset that anyone can use. Even if you don't have a lot of developer experience, you can still contribute!

Start by creating a Hugging Face Hub account at `hf.co <https://huggingface.co/join>`_ if you don't have one yet.

Create a repository
-------------------

A repository hosts all your dataset files, including the revision history, which makes it possible to store more than one version of a dataset.

Click on your profile and select **New Dataset** to create a new dataset repository. Give your dataset a name, and select whether this is a public or private dataset. A public dataset is visible to anyone, whereas a private dataset can only be viewed by you or members of your organization.

.. image:: /imgs/create_repo.png
   :align: center

Upload your files
-----------------

1. Once you have created a repository, navigate to the **Files and versions** tab to add a file. Select **Add file** to upload your dataset files.

.. image:: /imgs/upload_files.png
   :align: center

2. Drag and drop your dataset files here, and add a brief descriptive commit message.

.. image:: /imgs/commit_files.png
   :align: center

3. Once you have uploaded your dataset files, they are now stored in your dataset repository!

.. image:: /imgs/files_stored.png
   :align: center

Create a Dataset card
---------------------

The last step is to create a Dataset card. The Dataset card is very important for helping users understand how to use your dataset responsibly.

1. Click on the **Create Dataset card** to create a Dataset card.

.. image:: /imgs/dataset_card.png
   :align: center

2. Get a quick start with our Dataset card `template <https://raw.githubusercontent.com/huggingface/datasets/master/templates/README.md>`_ to help you fill out all the relevant fields to the best of your ability. 

3. The Dataset card uses structured tags to help users discover your dataset on the Hub. Use the `online card creator <https://huggingface.co/datasets/tagging/>`_ to help you generate the appropriate tags.

4. Copy and paste the generated tags at the top of your dataset card, and commit your changes!

.. image:: /imgs/card_tags.png
   :align: center 

For a detailed example of what a good Dataset card should look like, take a look at the `CNN DailyMail Dataset card <https://huggingface.co/datasets/cnn_dailymail>`_.

What's next?
------------

Congratulations, you have completed your first set 🤗 Datasets tutorials!

Over the course of these tutorials, you learned the basic steps of using 🤗 Datasets. You loaded a dataset from the Hub, and learned how to access the information stored inside the dataset. Next, you tokenized the dataset into sequences of integers, and formatted it so you can use it with PyTorch or TensorFlow. Then you loaded a metric to evaluate your models predictions. Finally, you uploaded a dataset to the Hub without writing a single line of code! This is all you need to get started with 🤗 Datasets! 

Now that you have a solid grasp of what 🤗 Datasets can do, you can begin formulating your own questions about how you can use it with your dataset. Please take a look at our :doc:`How-to guides <./how_to>` for more practical help on solving common use-cases, or read our :doc:`Conceptual guides <./about_arrow>` to deepen your understanding about 🤗 Datasets.