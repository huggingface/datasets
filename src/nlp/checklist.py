import os
from checklist.test_suite import TestSuite
from typing import Callable, Any, Dict
import numpy as np
from .load import load_dataset, prepare_module, import_main_class
from nlp.utils.download_manager import DownloadManager
from nlp.utils.file_utils import DownloadConfig

def aggr_testcases(dataset):
    nd = {'data': [], 'test_name': [], 'test_case': []}
    case_index = {}
    for e in dataset:
        key = (e['test_name'], e['test_case'])
        if key not in case_index:
            i = len(nd['data'])
            nd['data'].append([])
            nd['test_name'].append(e['test_name'])
            nd['test_case'].append(e['test_case'])
            case_index[key] = i
        i = case_index[key]
        cl_keys = set(['test_case', 'test_name', 'example_idx'])
        d = {x:v for x, v in e.items() if x not in cl_keys}
        nd['data'][i].append(d)
    return Dataset.from_dict(nd)


class CheckListSuite(object):
    def __init__(
        self,
        path: str,
        **kwargs
    ):
        self.dataset = load_dataset(path, **kwargs)['test']
        download_config = kwargs.get('download_config')
        module_path, hash = prepare_module(path, download_config=download_config, dataset=True)
        builder_cls = import_main_class(module_path, dataset=True)
        builder_instance = builder_cls(
            hash=hash,
            **kwargs,
            )
        if download_config is None:
            download_config = DownloadConfig()
            download_config.cache_dir = os.path.join(builder_instance._cache_dir_root, "downloads")
        dl_manager = DownloadManager(
            dataset_name=builder_instance.name, download_config=download_config, data_dir=builder_instance.config.data_dir
        )
        suite_file = os.path.join(dl_manager.download_and_extract(builder_instance.config.url), builder_instance.config.suite_name)
        self.suite = TestSuite.from_file(suite_file)
        self.fail_rate = {}

    def get_test(
        self,
        test_name: str,
        aggregate_testcases: bool=False,
    ) -> 'Dataset':
        d = self.dataset.filter(lambda x:x['test_name'] == test_name)
        if aggregate_testcases:
            d = aggr_testcases(d)
        return d



    def compute(
        self,
        prediction_key,
        confidence_key=None,
    ):
        preds = self.dataset[prediction_key]
        confs = self.dataset[confidence_key] if confidence_key is not None else np.ones(len(preds))
        if type(confs[0]) == list:
            confs = [np.array(x) for x in confs]
        self.suite.run_from_preds_confs(preds, confs, overwrite=True)
        def update_fails(e):
            test_name = e['test_name']
            if self.suite.tests[test_name].run_idxs is None:
                test_case = e['test_case']
            else:
                test_case = np.where(self.suite.tests[test_name].run_idxs == e['test_case'])[0][0]
            d = self.suite.tests[test_name].results.expect_results[test_case]
            if d is None or d[e['example_idx']] is None:
                fail = -1
            else:
                fail = d[e['example_idx']] <= 0
            if 'fail' not in e:
                e['fail'] = {}
            e['fail'][prediction_key] = int(fail)
            return e
        self.dataset = self.dataset.map(update_fails)
        self.fail_rate[prediction_key] = {}
        for t in self.suite.tests:
            try:
                self.fail_rate[prediction_key][t] = self.suite.tests[t].get_stats().fail_rate
            except:
                self.fail_rate[prediction_key][t] = -1

    def summary(
        self,
        **kwargs
    ):
        self.suite.summary(**kwargs)
