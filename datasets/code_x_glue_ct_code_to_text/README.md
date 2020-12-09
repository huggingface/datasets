---
annotations_creators:
- found
language_creators:
- found
languages:
- go
- java
- javascript
- ruby
- python
- php
licenses:
- other-C-UDA
multilinguality:
- other-programming-languages
size_categories:
  go:
  - 100K<n<1M
  java:
  - 100K<n<1M
  javascript:
  - 10K<n<100K
  php:
  - 100K<n<1M
  python:
  - 100K<n<1M
  ruby:
  - 10K<n<100K
source_datasets: []
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---
# Dataset Card for "code_x_glue_ct_code_to_text"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)



## [Dataset Description](#dataset-description)

 
- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Text/code-to-text

 

### [Dataset Summary](#dataset-summary)


CodeXGLUE code-to-text dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Text/code-to-text

The dataset we use comes from CodeSearchNet and we filter the dataset as the following:
- Remove examples that codes cannot be parsed into an abstract syntax tree.
- Remove examples that #tokens of documents is < 3 or >256
- Remove examples that documents contain special tokens (e.g. <img ...> or https:...)
- Remove examples that documents are not English.



### [Languages](#languages)


go, java, javascript, php, python, ruby


## [Dataset Structure](#dataset-structure)
 

### [Data Instances](#data-instances)

 

 

#### go

An example of 'test' looks as follows.
```
{
    "code": "func NewSTM(c *v3.Client, apply func(STM) error, so ...stmOption) (*v3.TxnResponse, error) {\n\topts := &stmOptions{ctx: c.Ctx()}\n\tfor _, f := range so {\n\t\tf(opts)\n\t}\n\tif len(opts.prefetch) != 0 {\n\t\tf := apply\n\t\tapply = func(s STM) error {\n\t\t\ts.Get(opts.prefetch...)\n\t\t\treturn f(s)\n\t\t}\n\t}\n\treturn runSTM(mkSTM(c, opts), apply)\n}", 
    "code_tokens": ["func", "NewSTM", "(", "c", "*", "v3", ".", "Client", ",", "apply", "func", "(", "STM", ")", "error", ",", "so", "...", "stmOption", ")", "(", "*", "v3", ".", "TxnResponse", ",", "error", ")", "{", "opts", ":=", "&", "stmOptions", "{", "ctx", ":", "c", ".", "Ctx", "(", ")", "}", "\n", "for", "_", ",", "f", ":=", "range", "so", "{", "f", "(", "opts", ")", "\n", "}", "\n", "if", "len", "(", "opts", ".", "prefetch", ")", "!=", "0", "{", "f", ":=", "apply", "\n", "apply", "=", "func", "(", "s", "STM", ")", "error", "{", "s", ".", "Get", "(", "opts", ".", "prefetch", "...", ")", "\n", "return", "f", "(", "s", ")", "\n", "}", "\n", "}", "\n", "return", "runSTM", "(", "mkSTM", "(", "c", ",", "opts", ")", ",", "apply", ")", "\n", "}"], 
    "docstring": "// NewSTM initiates a new STM instance, using serializable snapshot isolation by default.", 
    "docstring_tokens": ["NewSTM", "initiates", "a", "new", "STM", "instance", "using", "serializable", "snapshot", "isolation", "by", "default", "."], 
    "func_name": "NewSTM", 
    "id": 0, 
    "language": "go", 
    "original_string": "func NewSTM(c *v3.Client, apply func(STM) error, so ...stmOption) (*v3.TxnResponse, error) {\n\topts := &stmOptions{ctx: c.Ctx()}\n\tfor _, f := range so {\n\t\tf(opts)\n\t}\n\tif len(opts.prefetch) != 0 {\n\t\tf := apply\n\t\tapply = func(s STM) error {\n\t\t\ts.Get(opts.prefetch...)\n\t\t\treturn f(s)\n\t\t}\n\t}\n\treturn runSTM(mkSTM(c, opts), apply)\n}", 
    "path": "clientv3/concurrency/stm.go", 
    "repo": "etcd-io/etcd", 
    "sha": "616592d9ba993e3fe9798eef581316016df98906", 
    "url": "https://github.com/etcd-io/etcd/blob/616592d9ba993e3fe9798eef581316016df98906/clientv3/concurrency/stm.go#L89-L102"
}
```
 

#### java

An example of 'test' looks as follows.
```
{
    "code": "protected final void fastPathOrderedEmit(U value, boolean delayError, Disposable disposable) {\n        final Observer<? super V> observer = downstream;\n        final SimplePlainQueue<U> q = queue;\n\n        if (wip.get() == 0 && wip.compareAndSet(0, 1)) {\n            if (q.isEmpty()) {\n                accept(observer, value);\n                if (leave(-1) == 0) {\n                    return;\n                }\n            } else {\n                q.offer(value);\n            }\n        } else {\n            q.offer(value);\n            if (!enter()) {\n                return;\n            }\n        }\n        QueueDrainHelper.drainLoop(q, observer, delayError, disposable, this);\n    }", 
    "code_tokens": ["protected", "final", "void", "fastPathOrderedEmit", "(", "U", "value", ",", "boolean", "delayError", ",", "Disposable", "disposable", ")", "{", "final", "Observer", "<", "?", "super", "V", ">", "observer", "=", "downstream", ";", "final", "SimplePlainQueue", "<", "U", ">", "q", "=", "queue", ";", "if", "(", "wip", ".", "get", "(", ")", "==", "0", "&&", "wip", ".", "compareAndSet", "(", "0", ",", "1", ")", ")", "{", "if", "(", "q", ".", "isEmpty", "(", ")", ")", "{", "accept", "(", "observer", ",", "value", ")", ";", "if", "(", "leave", "(", "-", "1", ")", "==", "0", ")", "{", "return", ";", "}", "}", "else", "{", "q", ".", "offer", "(", "value", ")", ";", "}", "}", "else", "{", "q", ".", "offer", "(", "value", ")", ";", "if", "(", "!", "enter", "(", ")", ")", "{", "return", ";", "}", "}", "QueueDrainHelper", ".", "drainLoop", "(", "q", ",", "observer", ",", "delayError", ",", "disposable", ",", "this", ")", ";", "}"], 
    "docstring": "Makes sure the fast-path emits in order.\n@param value the value to emit or queue up\n@param delayError if true, errors are delayed until the source has terminated\n@param disposable the resource to dispose if the drain terminates", 
    "docstring_tokens": ["Makes", "sure", "the", "fast", "-", "path", "emits", "in", "order", "."], 
    "func_name": "QueueDrainObserver.fastPathOrderedEmit", 
    "id": 0, 
    "language": "java", 
    "original_string": "protected final void fastPathOrderedEmit(U value, boolean delayError, Disposable disposable) {\n        final Observer<? super V> observer = downstream;\n        final SimplePlainQueue<U> q = queue;\n\n        if (wip.get() == 0 && wip.compareAndSet(0, 1)) {\n            if (q.isEmpty()) {\n                accept(observer, value);\n                if (leave(-1) == 0) {\n                    return;\n                }\n            } else {\n                q.offer(value);\n            }\n        } else {\n            q.offer(value);\n            if (!enter()) {\n                return;\n            }\n        }\n        QueueDrainHelper.drainLoop(q, observer, delayError, disposable, this);\n    }", 
    "path": "src/main/java/io/reactivex/internal/observers/QueueDrainObserver.java", 
    "repo": "ReactiveX/RxJava", 
    "sha": "ac84182aa2bd866b53e01c8e3fe99683b882c60e", 
    "url": "https://github.com/ReactiveX/RxJava/blob/ac84182aa2bd866b53e01c8e3fe99683b882c60e/src/main/java/io/reactivex/internal/observers/QueueDrainObserver.java#L88-L108"
}
```
 

#### javascript

An example of 'validation' looks as follows.
```
{
    "code": "function getCounts(langs = []) {\n    return {\n        langs: langs.length,\n        modelLangs: langs.filter(({ models }) => models && !!models.length).length,\n        models: langs.map(({ models }) => (models ? models.length : 0)).reduce((a, b) => a + b, 0),\n    }\n}", 
    "code_tokens": ["function", "getCounts", "(", "langs", "=", "[", "]", ")", "{", "return", "{", "langs", ":", "langs", ".", "length", ",", "modelLangs", ":", "langs", ".", "filter", "(", "(", "{", "models", "}", ")", "=>", "models", "&&", "!", "!", "models", ".", "length", ")", ".", "length", ",", "models", ":", "langs", ".", "map", "(", "(", "{", "models", "}", ")", "=>", "(", "models", "?", "models", ".", "length", ":", "0", ")", ")", ".", "reduce", "(", "(", "a", ",", "b", ")", "=>", "a", "+", "b", ",", "0", ")", ",", "}", "}"], 
    "docstring": "Compute the overall total counts of models and languages", 
    "docstring_tokens": ["Compute", "the", "overall", "total", "counts", "of", "models", "and", "languages"], 
    "func_name": "getCounts", 
    "id": 0, 
    "language": "javascript", 
    "original_string": "function getCounts(langs = []) {\n    return {\n        langs: langs.length,\n        modelLangs: langs.filter(({ models }) => models && !!models.length).length,\n        models: langs.map(({ models }) => (models ? models.length : 0)).reduce((a, b) => a + b, 0),\n    }\n}", 
    "path": "website/src/widgets/landing.js", 
    "repo": "explosion/spaCy", 
    "sha": "a1e07f0d147e470cd4f0fd99bb62d28ddba7dd8d", 
    "url": "https://github.com/explosion/spaCy/blob/a1e07f0d147e470cd4f0fd99bb62d28ddba7dd8d/website/src/widgets/landing.js#L55-L61"
}
```
 

#### php

An example of 'validation' looks as follows.
```
{
    "code": "public static function supports(IOInterface $io, Config $config, $url, $deep = false)\n    {\n        if (!preg_match(self::URL_REGEX, $url, $match)) {\n            return false;\n        }\n\n        $scheme = !empty($match['scheme']) ? $match['scheme'] : null;\n        $guessedDomain = !empty($match['domain']) ? $match['domain'] : $match['domain2'];\n        $urlParts = explode('/', $match['parts']);\n\n        if (false === self::determineOrigin((array) $config->get('gitlab-domains'), $guessedDomain, $urlParts)) {\n            return false;\n        }\n\n        if ('https' === $scheme && !extension_loaded('openssl')) {\n            $io->writeError('Skipping GitLab driver for '.$url.' because the OpenSSL PHP extension is missing.', true, IOInterface::VERBOSE);\n\n            return false;\n        }\n\n        return true;\n    }", 
    "code_tokens": ["public", "static", "function", "supports", "(", "IOInterface", "$", "io", ",", "Config", "$", "config", ",", "$", "url", ",", "$", "deep", "=", "false", ")", "{", "if", "(", "!", "preg_match", "(", "self", "::", "URL_REGEX", ",", "$", "url", ",", "$", "match", ")", ")", "{", "return", "false", ";", "}", "$", "scheme", "=", "!", "empty", "(", "$", "match", "[", "'scheme'", "]", ")", "?", "$", "match", "[", "'scheme'", "]", ":", "null", ";", "$", "guessedDomain", "=", "!", "empty", "(", "$", "match", "[", "'domain'", "]", ")", "?", "$", "match", "[", "'domain'", "]", ":", "$", "match", "[", "'domain2'", "]", ";", "$", "urlParts", "=", "explode", "(", "'/'", ",", "$", "match", "[", "'parts'", "]", ")", ";", "if", "(", "false", "===", "self", "::", "determineOrigin", "(", "(", "array", ")", "$", "config", "->", "get", "(", "'gitlab-domains'", ")", ",", "$", "guessedDomain", ",", "$", "urlParts", ")", ")", "{", "return", "false", ";", "}", "if", "(", "'https'", "===", "$", "scheme", "&&", "!", "extension_loaded", "(", "'openssl'", ")", ")", "{", "$", "io", "->", "writeError", "(", "'Skipping GitLab driver for '", ".", "$", "url", ".", "' because the OpenSSL PHP extension is missing.'", ",", "true", ",", "IOInterface", "::", "VERBOSE", ")", ";", "return", "false", ";", "}", "return", "true", ";", "}"], 
    "docstring": "Uses the config `gitlab-domains` to see if the driver supports the url for the\nrepository given.\n\n{@inheritDoc}", 
    "docstring_tokens": ["Uses", "the", "config", "gitlab", "-", "domains", "to", "see", "if", "the", "driver", "supports", "the", "url", "for", "the", "repository", "given", "."], 
    "func_name": "GitLabDriver.supports", 
    "id": 0, 
    "language": "php", 
    "original_string": "public static function supports(IOInterface $io, Config $config, $url, $deep = false)\n    {\n        if (!preg_match(self::URL_REGEX, $url, $match)) {\n            return false;\n        }\n\n        $scheme = !empty($match['scheme']) ? $match['scheme'] : null;\n        $guessedDomain = !empty($match['domain']) ? $match['domain'] : $match['domain2'];\n        $urlParts = explode('/', $match['parts']);\n\n        if (false === self::determineOrigin((array) $config->get('gitlab-domains'), $guessedDomain, $urlParts)) {\n            return false;\n        }\n\n        if ('https' === $scheme && !extension_loaded('openssl')) {\n            $io->writeError('Skipping GitLab driver for '.$url.' because the OpenSSL PHP extension is missing.', true, IOInterface::VERBOSE);\n\n            return false;\n        }\n\n        return true;\n    }", 
    "path": "src/Composer/Repository/Vcs/GitLabDriver.php", 
    "repo": "composer/composer", 
    "sha": "5d615a16d175fcbdb67a536ef9d6fc4e8a1f6f2b", 
    "url": "https://github.com/composer/composer/blob/5d615a16d175fcbdb67a536ef9d6fc4e8a1f6f2b/src/Composer/Repository/Vcs/GitLabDriver.php#L451-L472"
}
```
 

#### python

An example of 'test' looks as follows.
```
{
    "code": "def sina_xml_to_url_list(xml_data):\n    \"\"\"str->list\n    Convert XML to URL List.\n    From Biligrab.\n    \"\"\"\n    rawurl = []\n    dom = parseString(xml_data)\n    for node in dom.getElementsByTagName('durl'):\n        url = node.getElementsByTagName('url')[0]\n        rawurl.append(url.childNodes[0].data)\n    return rawurl", 
    "code_tokens": ["def", "sina_xml_to_url_list", "(", "xml_data", ")", ":", "rawurl", "=", "[", "]", "dom", "=", "parseString", "(", "xml_data", ")", "for", "node", "in", "dom", ".", "getElementsByTagName", "(", "'durl'", ")", ":", "url", "=", "node", ".", "getElementsByTagName", "(", "'url'", ")", "[", "0", "]", "rawurl", ".", "append", "(", "url", ".", "childNodes", "[", "0", "]", ".", "data", ")", "return", "rawurl"], 
    "docstring": "str->list\n    Convert XML to URL List.\n    From Biligrab.", 
    "docstring_tokens": ["str", "-", ">", "list", "Convert", "XML", "to", "URL", "List", ".", "From", "Biligrab", "."], 
    "func_name": "sina_xml_to_url_list", 
    "id": 0, 
    "language": "python", 
    "original_string": "def sina_xml_to_url_list(xml_data):\n    \"\"\"str->list\n    Convert XML to URL List.\n    From Biligrab.\n    \"\"\"\n    rawurl = []\n    dom = parseString(xml_data)\n    for node in dom.getElementsByTagName('durl'):\n        url = node.getElementsByTagName('url')[0]\n        rawurl.append(url.childNodes[0].data)\n    return rawurl", 
    "path": "src/you_get/extractors/miomio.py", 
    "repo": "soimort/you-get", 
    "sha": "b746ac01c9f39de94cac2d56f665285b0523b974", 
    "url": "https://github.com/soimort/you-get/blob/b746ac01c9f39de94cac2d56f665285b0523b974/src/you_get/extractors/miomio.py#L41-L51"
}
```
 

#### ruby

An example of 'validation' looks as follows.
```
{
    "code": "def preparse(unparsed, args = [], opts = {})\n        case unparsed\n        when Hash  then opts.merge! unparsed\n        when Array then unparsed.each { |e| preparse(e, args, opts) }\n        else args << unparsed.to_s\n        end\n        [args, opts]\n      end", 
    "code_tokens": ["def", "preparse", "(", "unparsed", ",", "args", "=", "[", "]", ",", "opts", "=", "{", "}", ")", "case", "unparsed", "when", "Hash", "then", "opts", ".", "merge!", "unparsed", "when", "Array", "then", "unparsed", ".", "each", "{", "|", "e", "|", "preparse", "(", "e", ",", "args", ",", "opts", ")", "}", "else", "args", "<<", "unparsed", ".", "to_s", "end", "[", "args", ",", "opts", "]", "end"], 
    "docstring": "can't use flatten as it will flatten hashes", 
    "docstring_tokens": ["can", "t", "use", "flatten", "as", "it", "will", "flatten", "hashes"], 
    "func_name": "Travis.CLI.preparse", 
    "id": 0, 
    "language": "ruby", 
    "original_string": "def preparse(unparsed, args = [], opts = {})\n        case unparsed\n        when Hash  then opts.merge! unparsed\n        when Array then unparsed.each { |e| preparse(e, args, opts) }\n        else args << unparsed.to_s\n        end\n        [args, opts]\n      end", 
    "path": "lib/travis/cli.rb", 
    "repo": "travis-ci/travis.rb", 
    "sha": "6547e3ad1393f508c679236a4b0e5403d2732043", 
    "url": "https://github.com/travis-ci/travis.rb/blob/6547e3ad1393f508c679236a4b0e5403d2732043/lib/travis/cli.rb#L117-L124"
}
```
 



### [Data Fields](#data-fields)

 
In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### go, java, javascript, php, python, ruby

|   field name   |      type      |                                    description                                    |
|----------------|----------------|-----------------------------------------------------------------------------------|
|id              |int32           | Index of the sample                                                               |
|repo            |string          | repo: the owner/repo                                                              |
|path            |string          | path: the full path to the original file                                          |
|func_name       |string          | func_name: the function or method name                                            |
|original_string |string          | original_string: the raw string before tokenization or parsing                    |
|language        |string          | language: the programming language name                                           |
|code            |string          | code/function: the part of the original_string that is code                       |
|code_tokens     |Sequence[string]| code_tokens/function_tokens: tokenized version of code                            |
|docstring       |string          | docstring: the top-level comment or docstring, if it exists in the original string|
|docstring_tokens|Sequence[string]| docstring_tokens: tokenized version of docstring                                  |
|sha             |string          | sha of the file                                                                   |
|url             |string          | url of the file                                                                   |






### [Data Splits](#data-splits)

 


|   name   |train |validation|test |
|----------|-----:|---------:|----:|
|go        |167288|      7325| 8122|
|java      |164923|      5183|10955|
|javascript| 58025|      3885| 3291|
|php       |241241|     12982|14014|
|python    |251820|     13914|14918|
|ruby      | 24927|      1400| 1261|







## [Additional Information](#additional-information)
 

### [Dataset Curators](#dataset-curators)


https://github.com/microsoft, https://github.com/madlag


### [Licensing Information](#licensing-information)


Computational Use of Data Agreement (C-UDA) License.


### [Citation Information](#citation-information)


```
@article{husain2019codesearchnet,
  title={Codesearchnet challenge: Evaluating the state of semantic code search},
  author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
  journal={arXiv preprint arXiv:1909.09436},
  year={2019}
}
```




