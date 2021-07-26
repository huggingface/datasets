Beam Datasets
=============

Some datasets are too large to be processed on a single machine. Instead, you can process them with `Apache Beam <https://beam.apache.org/>`_, a library for parallel data processing. The processing pipeline is executed on a distributed processing backend such as `Apache Flink <https://flink.apache.org/>`_, `Apache Spark <https://spark.apache.org/>`_, and `Google Cloud Dataflow <https://cloud.google.com/dataflow>`_.

At Hugging Face, we have already created Beam pipelines for some of the larger datasets like `wikipedia <https://huggingface.co/datasets/wikipedia>`_, and `wiki40b <https://huggingface.co/datasets/wiki40b>`_. You can load these normally with :func:`datasets.Datasets.load_dataset`. But if you want to run your own Beam pipeline with Dataflow, here is how:

1. Specify the dataset and configuration you want to process:

   .. code::

        DATASET_NAME=your_dataset_name  # ex: wikipedia
        CONFIG_NAME=your_config_name    # ex: 20200501.en

2. Input your Google Cloud Platform information:

   .. code::

        PROJECT=your_project
        BUCKET=your_bucket
        REGION=your_region

3. Specify your Python requirements:

   .. code::

        echo "datasets" > /tmp/beam_requirements.txt
        echo "apache_beam" >> /tmp/beam_requirements.txt

4. Run the pipeline:

   .. code::

        datasets-cli run_beam datasets/$DATASET_NAME \
        --name $CONFIG_NAME \
        --save_infos \
        --cache_dir gs://$BUCKET/cache/datasets \
        --beam_pipeline_options=\
        "runner=DataflowRunner,project=$PROJECT,job_name=$DATASET_NAME-gen,"\
        "staging_location=gs://$BUCKET/binaries,temp_location=gs://$BUCKET/temp,"\
        "region=$REGION,requirements_file=/tmp/beam_requirements.txt"

.. tip::

    Adjust the parameters here if you want to change the runner (Flink or Spark), output location (S3 bucket or HDFS), and the number of workers.