# Beam Datasets

## Intro

Some datasets ar too big to be processed on a single machine, for example: wikipedia, wiki40b, etc.
Instead, we allow to process them using [Apache Beam](https://beam.apache.org/).

Beam processing pipelines can be executed on many execution engines like Dataflow, Spark, Flink, etc.
More infos about the different runners [here](https://beam.apache.org/documentation/runners/capability-matrix/).

## Already processed datasets are provided

At Hugging Face we have already run the Beam pipelines for datasets like wikipedia and wiki40b to provide already processed datasets. Therefore users can simply do run `load_dataset('wikipedia', '20200501.en')` and the already processed dataset will be downloaded.

## How to generate a Beam dataset

If you want to run the Beam pipeline of a dataset anyway, here are the different steps to run on Dataflow:

- First define which dataset and config you want to process:

    ```
    DATASET_NAME=your_dataset_name  # ex: wikipedia
    CONFIG_NAME=your_config_name    # ex: 20200501.en
    ```
- Then, define your GCP infos:

    ```
    PROJECT=your_project
    BUCKET=your_bucket
    REGION=your_region
    ```
- Specify the python requirements:

    ```
    echo "nlp" > /tmp/beam_requirements.txt
    echo "apache_beam" >> /tmp/beam_requirements.txt
    ```
- Finally run your pipeline:

    ```
    python -m nlp-cli run_beam datasets/$DATASET_NAME \
    --name $CONFIG_NAME \
    --save_infos \
    --cache_dir gs://$BUCKET/cache/datasets \
    --beam_pipeline_options=\
    "runner=DataflowRunner,project=$PROJECT,job_name=$DATASET_NAME-gen,"\
    "staging_location=gs://$BUCKET/binaries,temp_location=gs://$BUCKET/temp,"\
    "region=$REGION,requirements_file=/tmp/beam_requirements.txt"
    ```

Tips: you can also use the flags `num_workers` or `machine_type` to fit your needs.
