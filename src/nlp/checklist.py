from .arrow_dataset import Dataset
from checklist.test_suite import TestSuite
from typing import Callable, Any, Dict
import numpy as np

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
        example_to_dict_fn: Callable[[Any], Dict[str, Any]] = None,
        new_sample: bool = False,
        **kwargs
    ):
        self.suite = TestSuite.from_file(path)
        self.example_to_dict_fn = example_to_dict_fn
        d = self.suite.to_dict(example_to_dict_fn, new_sample=new_sample, **kwargs)
        self.dataset = Dataset.from_dict(d)
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


    def subsample(
        self,
        n: int,
        seed: bool=False,
    ):
        d = self.suite.to_dict(self.example_to_dict_fn, n=n, seed=seed, new_sample=True)
        self.dataset = Dataset.from_dict(d)
        self.fail_rate = {}


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
