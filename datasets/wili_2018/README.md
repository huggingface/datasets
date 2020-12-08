Please refer to the WiLI paper for details about the dataset.
If you want to report problems of the WiLI dataset, please send an email to
info@martin-thoma.de or leave a comment at http://martin-thoma.com/wili

Errata are listed on http://martin-thoma.com/wili.


## Contents

* `x_train.txt`: 175000 lines of text. Each line belongs to one language.
* `y_train.txt`: 175000 lines. Each line denots the language of the same line
                 in `x_train.txt`
* `x_test.txt`: See `x_train.txt`
* `y_test.txt`: See `y_train.txt`
* `urls.txt`: A list of permanent URLs to all pages used for paragraph extraction
* `labels.csv`: A header line plus one line per language
* `README.txt`: This file


## Changelog

* 07.01.2017, WiLI-2018: Various fixes in data extraction, e.g. better filtering
                         for math and literature content.
* 10.09.2017, WiLI-2017: Initial upload
                         https://doi.org/10.5281/zenodo.841984
