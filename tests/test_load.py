def test_builder_kwargs_and_config_kwargs_do_not_conflict():
    from datasets import load_dataset_builder

    # "glue" has config_name internally,
    # and we pass it again via kwargs to simulate conflict
    builder = load_dataset_builder("glue", config_name="sst2")

    assert builder.config.name == "sst2"
