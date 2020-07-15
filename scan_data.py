from nlp import prepare_module, DownloadConfig, import_main_class, hf_api
import tempfile
import os


def scan_for_nested_unnecessary_dict(dataset_name):

    def load_builder_class(dataset_name):
        module_path = prepare_module(dataset_name, download_config=DownloadConfig(force_download=True))
        return import_main_class(module_path)

    def load_configs(dataset_name):
        builder_cls = load_builder_class(dataset_name)
        if len(builder_cls.BUILDER_CONFIGS) == 0:
            return [None]
        return builder_cls.BUILDER_CONFIGS

    def scan_features_for_nested_dict(features):
        is_sequence = False
        if hasattr(features, "_type"):
            if features._type != 'Sequence':
                return False
            else:
                is_sequence = True
                features = features.feature

        if isinstance(features, list):
            for value in features:
                if scan_features_for_nested_dict(value):
                    return True
            return False

        elif isinstance(features, dict):
            for key, value in features.items():
                if is_sequence and len(features.keys()) == 1 and hasattr(features[key], "_type") and features[key]._type != "Sequence":
                    return True
                if scan_features_for_nested_dict(value):
                    return True
            return False
        elif hasattr(features, "_type"):
            return False
        else:
            raise ValueError(f"{features} should be either a list, a dict or a feature")
    if dataset_name not in  ['csv', 'json', 'pandas'] :
        configs = load_configs(dataset_name)

        for config in configs:
            with tempfile.TemporaryDirectory() as processed_temp_dir:
                # create config and dataset
                dataset_builder_cls = load_builder_class(dataset_name)
                name = config.name if config is not None else None
                dataset_builder = dataset_builder_cls(name=name, cache_dir=processed_temp_dir)

            is_nested_dict_in_dataset = scan_features_for_nested_dict(dataset_builder._info().features)
            if is_nested_dict_in_dataset:
                print(f"{dataset_name} with {name} needs refactoring")


if __name__ == "__main__":
    datasets = sorted(os.listdir('/home/mariama/PycharmProjects/nlp/datasets'))
    for name in datasets:
        if name != 'search_qa':
            print(name)
            scan_for_nested_unnecessary_dict(name) 
            print('=='*100)