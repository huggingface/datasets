# Copyright 2021 The HuggingFace Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import unittest

from cer import CER


cer = CER()


class TestCER(unittest.TestCase):
    def test_cer_case_senstive(self):
        refs = ["White House"]
        preds = ["white house"]
        # S = 2, D = 0, I = 0, N = 11, CER = 2 / 11
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.1818181818) < 1e-6)

    def test_cer_whitespace(self):
        refs = ["were wolf"]
        preds = ["werewolf"]
        # S = 0, D = 0, I = 1, N = 9, CER = 1 / 9
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.1111111) < 1e-6)

        refs = ["werewolf"]
        preds = ["weae     wolf"]
        # S = 1, D = 1, I = 0, N = 8, CER = 0.25
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.25) < 1e-6)

        # consecutive whitespaces case 1
        refs = ["were wolf"]
        preds = ["were               wolf"]
        # S = 0, D = 0, I = 0, N = 9, CER = 0
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.0) < 1e-6)

        # consecutive whitespaces case 2
        refs = ["were   wolf"]
        preds = ["were               wolf"]
        # S = 0, D = 0, I = 0, N = 9, CER = 0
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.0) < 1e-6)

    def test_cer_sub(self):
        refs = ["werewolf"]
        preds = ["weaewolf"]
        # S = 1, D = 0, I = 0, N = 8, CER = 0.125
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.125) < 1e-6)

    def test_cer_del(self):
        refs = ["werewolf"]
        preds = ["wereawolf"]
        # S = 0, D = 1, I = 0, N = 8, CER = 0.125
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.125) < 1e-6)

    def test_cer_insert(self):
        refs = ["werewolf"]
        preds = ["wereolf"]
        # S = 0, D = 0, I = 1, N = 8, CER = 0.125
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.125) < 1e-6)

    def test_cer_equal(self):
        refs = ["werewolf"]
        char_error_rate = cer.compute(predictions=refs, references=refs)
        self.assertEqual(char_error_rate, 0.0)

    def test_cer_list_of_seqs(self):
        refs = ["werewolf", "I am your father"]
        char_error_rate = cer.compute(predictions=refs, references=refs)
        self.assertEqual(char_error_rate, 0.0)

        refs = ["werewolf", "I am your father", "doge"]
        preds = ["werxwolf", "I       am your father", "doge"]
        # S = 1, D = 0, I = 0, N = 28, CER = 1 / 28
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.03571428) < 1e-6)

    def test_correlated_sentences(self):
        refs = ["My hovercraft", "is full of eels"]
        preds = ["My hovercraft is full", " of eels"]
        # S = 0, D = 0, I = 2, N = 28, CER = 2 / 28
        # whitespace at the front of " of eels" will be strip during preporcessing
        # so need to insert 2 whitespaces
        char_error_rate = cer.compute(predictions=preds, references=refs, concatenate_texts=True)
        self.assertTrue(abs(char_error_rate - 0.071428) < 1e-6)

    def test_cer_unicode(self):
        refs = ["我能吞下玻璃而不伤身体"]
        preds = [" 能吞虾玻璃而 不霜身体啦"]
        # S = 3, D = 2, I = 0, N = 11, CER = 5 / 11
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.4545454545) < 1e-6)

        refs = ["我能吞下玻璃", "而不伤身体"]
        preds = ["我    能 吞 下 玻 璃", "而不伤身体"]
        # S = 0, D = 5, I = 0, N = 11, CER = 5 / 11
        char_error_rate = cer.compute(predictions=preds, references=refs)
        self.assertTrue(abs(char_error_rate - 0.454545454545) < 1e-6)

        refs = ["我能吞下玻璃而不伤身体"]
        char_error_rate = cer.compute(predictions=refs, references=refs)
        self.assertFalse(char_error_rate, 0.0)

    def test_cer_empty(self):
        refs = [""]
        preds = ["Hypothesis"]
        with self.assertRaises(ValueError):
            cer.compute(predictions=preds, references=refs)


if __name__ == "__main__":
    unittest.main()
