Beam Datasets
================

Intro
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some datasets are too big to be processed on a single machine, for example: wikipedia, wiki40b, etc.
Instead, we allow to process them using `Apache Beam <https://beam.apache.org/>`__.

Beam processing pipelines can be executed on many execution engines like Dataflow, Spark, Flink, etc.
More infos about the different runners `here <https://beam.apache.org/documentation/runners/capability-matrix/>`__.

Already processed datasets are provided
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At Hugging Face we have already run the Beam pipelines for datasets like wikipedia and wiki40b to provide already processed datasets. Therefore users can simply do run `load_dataset('wikipedia', '20200501.en')` and the already processed dataset will be downloaded.

How to run a Beam dataset processing pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to run the Beam pipeline of a dataset anyway, here are the different steps to run on Dataflow: 

- First define which dataset and config you want to process:

.. code::

    DATASET_NAME=your_dataset_name  # ex: wikipedia
    CONFIG_NAME=your_config_name    # ex: 20200501.en

- Then, define your GCP infos:

.. code::

    PROJECT=your_project
    BUCKET=your_bucket
    REGION=your_region

- Specify the python requirements:

.. code::

    echo "datasets" > /tmp/beam_requirements.txt
    echo "apache_beam" >> /tmp/beam_requirements.txt

- Finally run your pipeline:

.. code::

    python -mdatasets-cli run_beam datasets/$DATASET_NAME \
    --name $CONFIG_NAME \
    --save_infos \
    --cache_dir gs://$BUCKET/cache/datasets \
    --beam_pipeline_options=\
    "runner=DataflowRunner,project=$PROJECT,job_name=$DATASET_NAME-gen,"\
    "staging_location=gs://$BUCKET/binaries,temp_location=gs://$BUCKET/temp,"\
    "region=$REGION,requirements_file=/tmp/beam_requirements.txt"


.. note::

    you can also use the flags `num_workers` or `machine_type` to fit your needs.

Note that it also works if you change the runner to Spark, Flink, etc. instead of Dataflow or if you change the output location to S3 or HDFS instead of GCS.

How to create your own Beam dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is highly recommended to be familiar with Beam pipelines first.
Then, you can start looking at the `wikipedia.py <https://github.com/huggingface/datasets/blob/master/datasets/wikipedia/wikipedia.py>`_ script for an example.
