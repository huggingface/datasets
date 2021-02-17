# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{commonvoice:2020,
  author = {Ardila, R. and Branson, M. and Davis, K. and Henretty, M. and Kohler, M. and Meyer, J. and Morais, R. and Saunders, L. and Tyers, F. M. and Weber, G.},
  title = {Common Voice: A Massively-Multilingual Speech Corpus},
  booktitle = {Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020)},
  pages = {4211--4215},
  year = 2020
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Common Voice is Mozilla's initiative to help teach machines how real people speak.
The dataset currently consists of 7,335 validated hours of speech in 60 languages, but we’re always adding more voices and languages.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://commonvoice.mozilla.org/en/datasets"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "https://github.com/common-voice/common-voice/blob/main/LICENSE"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    'first_domain': "https://mozilla-common-voice-datasets.s3.dualstack.us-west-2.amazonaws.com/cv-corpus-6.1-2020-12-11/en.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ3GQRTO3CAFSOHXG%2F20210212%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210212T082132Z&X-Amz-Expires=43200&X-Amz-Security-Token=FwoGZXIvYXdzEOr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDDBRxPQbFwld%2BrOewCKSBOR7k7VaqtnM0zucItVC0gdXyV4Uh5qtOx0vhTzhGRJ2r0mKkJ5FNL8bMe5TWtcX0IEH8HHTs28S%2BDerVhBD%2FGKfxy6J4BQCjhR0J8AoqwEYm0qRVm5b7tbWBNYetD5c8HxYGWWRppvaYxRxdnRbupfKuGpMEf3eYskfH8tAA739HbcKj44LGe4lkKsGvI1avxrxrNugcrNF%2BOccEdNInU%2F%2BVQvoFUu93oAEhJWl8dWXswDtZSCmuvfTjCbsZjphoSfTz5t0T25qXwP3PpcZTRVrYm9rQ4GGwaiva9qs0Q0nA0mC0skcMLF%2BZMxfo4wtaDfneDoPgNITqHtLyXLKeXRwIhHUzjNriniNNTp3XJyivc6qr6uNJ23IysUKfqNfQ2EiZC07VEQlVcYoSBKNHvGEIHsXfICaQ4MyHSl7dJa0CaSOAjBytNMxxhqCCLylJ%2BEgnO45VS5X12z8D3vTyyjR67hqXKDHwdTioVTlK3j%2FTXWRHDw31EbikSkhDKubD%2F2VDJLMul7cXjpCWygmJXHKG%2BNQKM09vP3pdmuVuQ1Z8an8OPMTnGKJEOsKXkrCJTOjvQVAl7z4KKlA9UW0Hp0u%2FoZnT%2Fxgi7dvqwu1Fq7%2BRQ%2BkXi3LT6lA%2B%2BJfO2HEOnlcsg1TFompSGp0dD12F3iTQNmKAuakCdunLyQRd%2Bgi2vRmwfsPyHOnRiJVbyghoEWyKLHtmIEGMir%2B01wURSgc46vtaXqBOz5Gtj4bF5wkpw6TCh%2FiHFn7Fx6igw69uJmKtpI%3D&X-Amz-Signature=573df56b8f6aa8e13b2fa26fa0763718e25f2d7a33e0be97ea5ff82680d82474&X-Amz-SignedHeaders=host"
}



_FILES = {
    "dev.tsv": "fields": {
        "client_id": "client_id",	
        "path": "path to sound file"	
        "sentence": "sentence pronounced",
        "up_votes": "upvotes by reviewers",
        "down_votes": "down votes by reviewers"	
        "age": "Age of the speaker":
        "gender" "Gender of the speaker",
        "accent": "accent of the speaker",
        "locale": "location of the speaker",
        "segment": "segment",
    }
    "invalidated.tsv": {
        "client_id": "client_id",	
        "path": "path to sound file"	
        "sentence": "sentence pronounced",
        "up_votes": "upvotes by reviewers",
        "down_votes": "down votes by reviewers"	
        "age": "Age of the speaker":
        "gender" "Gender of the speaker",
        "accent": "accent of the speaker",
        "locale": "location of the speaker",
        "segment": "segment"}
    "other.tsv": 
        {
        "client_id": "client_id",	
        "path": "path to sound file"	
        "sentence": "sentence pronounced",
        "up_votes": "upvotes by reviewers",
        "down_votes": "down votes by reviewers"	
        "age": "Age of the speaker":
        "gender" "Gender of the speaker",
        "accent": "accent of the speaker",
        "locale": "location of the speaker",
        "segment": "segment", }
    "reported.tsv": {
        {
        "sentence": "sentence",	
        "senetence_id": "sentence_id"	
        "locale": "location of the speakr",
        "reason": "reason for report"
    }
    "test.tsv": {
         {
        "client_id": "client_id",	
        "path": "path to sound file"	
        "sentence": "sentence pronounced",
        "up_votes": "upvotes by reviewers",
        "down_votes": "down votes by reviewers"	
        "age": "Age of the speaker":
        "gender" "Gender of the speaker",
        "accent": "accent of the speaker",
        "locale": "location of the speaker",
        "segment": "segment", }
    }
    "train.tsv": {
         {
        "client_id": "client_id",	
        "path": "path to sound file"	
        "sentence": "sentence pronounced",
        "up_votes": "upvotes by reviewers",
        "down_votes": "down votes by reviewers"	
        "age": "Age of the speaker":
        "gender" "Gender of the speaker",
        "accent": "accent of the speaker",
        "locale": "location of the speaker",
        "segment": "segment", }
    }
    "validated.tsv": {
         {
        "client_id": "client_id",	
        "path": "path to sound file"	
        "sentence": "sentence pronounced",
        "up_votes": "upvotes by reviewers",
        "down_votes": "down votes by reviewers"	
        "age": "Age of the speaker":
        "gender" "Gender of the speaker",
        "accent": "accent of the speaker",
        "locale": "location of the speaker",
        "segment": "segment", }
    }
}

_LANGUAGES = {
    "Abkhaz": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Arabic": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Assamese": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Breton": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Catalan": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Hakha Chin": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Czech": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Chuvash": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Welsh": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Abkhaz": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "German": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Dhivehi": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Greek": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "English": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Esperanto": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Spanish": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Estonian": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Basque": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },
    "Persian": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    },   
    "Finnish": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "French": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "Frisian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "Irish": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "Hindi": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "Sorbian, Upper": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Hungarian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "InterLinguia": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "Indonesian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Italian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Japanese": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Georgian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Kabyle": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Kyrgyz": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Luganda": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "German": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Lithuanian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Latvian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },    
    "Mongolian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Maltese": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Dutch": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14,
    "Download_Link": "https://mozilla-common-voice-datasets.s3.dualstack.us-west-2.amazonaws.com/cv-corpus-6.1-2020-12-11/nl.tar.gz?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQ3GQRTO3ND4UAQXB%2F20210217%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210217T080740Z&X-Amz-Expires=43200&X-Amz-Security-Token=FwoGZXIvYXdzEGIaDCC6ALh%2FwIK9ovvRdCKSBCs5WaSJNsZ2h0SnhpnWFv4yiAJHJTe%2BY6pBcCqadRMs0RABHeQ2n1QDACJ5V9WOqIHfMfT0AI%2Bfe6iFkTGLgRrJOMYpgV%2FmIBcXCjeb72r4ZvudMA8tprkSxZsEh53bJkIDQx1tXqfpz0yoefM0geD3461suEGhHnLIyiwffrUpRg%2BkNZN9%2FLZZXpF5F2pogieKKV533Jetkd1xlWOR%2Bem9R2bENu2RV563XX3JvbWxSYN9IHkVT1xwd4ZiOpUtX7%2F2RoluJUKw%2BUPpyml3J%2FOPPGdr7CyPLjqNxdq9ceRi8lRybty64XvNYZGt45VNTQ3pkTTz4VpUCJAGkgxq95Ve%2BOwW%2Fsc8JtblTFKrH11vej62NB7C0n7JPPS4SLKXHKW%2B7ZbybcNf3BnsAVouPdsGTMslcgkD81b9trnjyXJdOZkzdHUf2KcWVXVceEsZnMhcCZQ1cJpI7qXPEk8QrKCQcNByPLHmPIEdHpj9IrIBKDkl2qO7VX7CCB65WDt2eZRltOcNHXWVFXFktMdQOQztI1j0XSZz2iOX4jPKKaqz193VEytlAqmehNi8pePOnxkP9Z1SP7d3I6rayuBF3phmpHxw499tY3ECYYgoCnJ6QSFa3KxMjFmEpQlmjxuwEMHd4CDL2FJYGcCiIxbCcL1r8ZE3%2BbGdcu7PRsVCHX3Huh%2FqGIaF4h40FgteN6teyKCHKOebs4EGMipb9xmEMZ9ZbVopz4bkhLdMTrjKon9w624Xem0MTPqN7XY%2BB6lRgrW8rd4%3D&X-Amz-Signature=28eabdfce72a472a70b0f9e1e2c37fe1471b5ec8ed60614fbe900bfa97ae1ac8&X-Amz-SignedHeaders=host"
    },"Odia": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },'
    '"Punjabi": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },
    "Polish": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Portuguese": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Romansh Sursilvan": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Romansh Vallader": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Romanian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Russian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Kinyarwanda": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Sakha": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Slovenian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Swedish": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Tamil": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Thai": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Turkish": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Tatar": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Ukrainian": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Vietnamese": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Votic": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Chinese (China)": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Chinese (Hong Kong)": {
    "Date": "2020-12-11",
    "Size": "39 MB",
    "Version": "ab_1h_2020-12-11",
    "Validated_Hr_Total": 0.05,
    "Overall_Hr_Total": 1,
    "Number_Of_Voice": 14
    },"Chinese (Taiwan": {
        "Date": "2020-12-11",
        "Size": "39 MB",
        "Version": "ab_1h_2020-12-11",
        "Validated_Hr_Total": 0.05,
        "Overall_Hr_Total": 1,
        "Number_Of_Voice": 14
    }
}



## Languages
[Abkhaz,]


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class CommonVoice(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

      @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://commonvoice.mozilla.org/en/datasets,
    and manually download the dataset as a .tar file. Once it is completed,
    a folder will be made containing the files, validated.tsv, train.tsv, test.tsv, reported.tsv, other.tsv, invalidated.tsv, dev.tsv
    and the folder clips containing audiofiles sampled at 48khz. Each clip is around 3-4 seconds in duration with a size of around 20-50 khz"""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="first_domain", version=VERSION, description="This part of my dataset covers a first domain"),
        datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    ]

    DEFAULT_CONFIG_NAME = "first_domain"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "first_domain":  # This is the name of the configuration selected in BUILDER_CONFIGS above 
            features = datasets.Features(
                {
                    "client_id": datasets.Value("string"),
                    "path": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "up_votes": datasets.Value("int64"),
                    "down_votes": datasets.Value("int64"),
                    "age": datasets.Value("string"),
                    "gender": datasets.Value("string"),
                    "locale": datasets.Value("string"),
                    "segmet": datasets.Value("string"),

                    # These are the features of your dataset like images, labels ...
                }
            )

        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "client_id": datasets.Value("string"),
                    "path": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "up_votes": datasets.Value("int64"),
                    "down_votes": datasets.Value("int64"),
                    "age": datasets.Value("string"),
                    "gender": datasets.Value("string"),
                    "locale": datasets.Value("string"),
                    "segmet": datasets.Value("string"),

                    # These are the features of your dataset like images, labels ...
                }
            )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive 
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.tsv"),
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.DEV,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.tsv"),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATED,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "validated.tsv"),
                    "split": "validated",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.INVALIDATED,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "invalidated.tsv"),
                    "split": "invalidated",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.REPORTED,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "reported.tsv"),
                    "split": "reported",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.OTHER,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "other.tsv"),
                    "split": "other",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "first_domain":
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "answer": "" if split == "test" else data["answer"],
                    }
                else:
                    yield id_, {
                        "sentence": data["sentence"],
                        "option2": data["option2"],
                        "second_domain_answer": "" if split == "test" else data["second_domain_answer"],
                    }
