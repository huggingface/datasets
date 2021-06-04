---
annotations_creators:
- found
language_creators:
- found
languages:
- code
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
source_datasets:
- original
task_categories:
- conditional-text-generation
task_ids:
- machine-translation
---

# Dataset Card for "code_x_glue_ct_code_to_text"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
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

### [Supported Tasks](#supported-tasks)

[More Information Needed]

### [Languages](#languages)

go, java, javascript, php, python, ruby

## [Dataset Structure](#dataset-structure)

### [Data Instances](#data-instances)

#### go

An example of 'validation' looks as follows.
```
{
    "code": "func (q *query) Close() {\n\tfor _, s := range q.matrix {\n\t\tputPointSlice(s.Points)\n\t}\n}",
    "code_tokens": ["func", "(", "q", "*", "query", ")", "Close", "(", ")", "{", "for", "_", ",", "s", ":=", "range", "q", ".", "matrix", "{", "putPointSlice", "(", "s", ".", "Points", ")", "\n", "}", "\n", "}"],
    "docstring": "// Close implements the Query interface.",
    "docstring_tokens": ["Close", "implements", "the", "Query", "interface", "."],
    "func_name": "Close",
    "id": 0,
    "language": "go",
    "original_string": "func (q *query) Close() {\n\tfor _, s := range q.matrix {\n\t\tputPointSlice(s.Points)\n\t}\n}",
    "path": "promql/engine.go",
    "repo": "prometheus/prometheus",
    "sha": "03b90b464572174a64b6ee2cb0b097eda489ba47",
    "url": "https://github.com/prometheus/prometheus/blob/03b90b464572174a64b6ee2cb0b097eda489ba47/promql/engine.go#L167-L171"
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

An example of 'train' looks as follows.
```
{
    "code": "function deleteUser(id, callback) {\n\t\torionAccount.findByUsername(id, function(err, user) {\n\t\t\tif(err) {\n\t\t\t\tcallback(err);\n\t\t\t}\n\t\t\tconst userPath = path.join(this.options.workspaceDir, id.substring(0,2));\n\t\t\tfs.access(userPath, (err) => {\n\t\t\t\tif(err) {\n\t\t\t\t\tcallback(err);\n\t\t\t\t}\n\t\t\t\t//TODO should a delete failure prevent the user delete?\n\t\t\t\treturn rimraf(userPath, (err) => {\n\t\t\t\t\tif(err) {\n\t\t\t\t\t\tcallback(err);\n\t\t\t\t\t}\n\t\t\t\t\torionAccount.remove({username: id}, callback);\n\t\t\t\t});\n\t\t\t});\n\t\t}.bind(this));\n\t}",
    "code_tokens": ["function", "deleteUser", "(", "id", ",", "callback", ")", "{", "orionAccount", ".", "findByUsername", "(", "id", ",", "function", "(", "err", ",", "user", ")", "{", "if", "(", "err", ")", "{", "callback", "(", "err", ")", ";", "}", "const", "userPath", "=", "path", ".", "join", "(", "this", ".", "options", ".", "workspaceDir", ",", "id", ".", "substring", "(", "0", ",", "2", ")", ")", ";", "fs", ".", "access", "(", "userPath", ",", "(", "err", ")", "=>", "{", "if", "(", "err", ")", "{", "callback", "(", "err", ")", ";", "}", "//TODO should a delete failure prevent the user delete?", "return", "rimraf", "(", "userPath", ",", "(", "err", ")", "=>", "{", "if", "(", "err", ")", "{", "callback", "(", "err", ")", ";", "}", "orionAccount", ".", "remove", "(", "{", "username", ":", "id", "}", ",", "callback", ")", ";", "}", ")", ";", "}", ")", ";", "}", ".", "bind", "(", "this", ")", ")", ";", "}"],
    "docstring": "Delete the user from the store with the given user ID\n@param {string} id The user identifier to delete\n@param {fn(Error: err)} callback The callback to call when complete",
    "docstring_tokens": ["Delete", "the", "user", "from", "the", "store", "with", "the", "given", "user", "ID"],
    "func_name": "deleteUser",
    "id": 0,
    "language": "javascript",
    "original_string": "function deleteUser(id, callback) {\n\t\torionAccount.findByUsername(id, function(err, user) {\n\t\t\tif(err) {\n\t\t\t\tcallback(err);\n\t\t\t}\n\t\t\tconst userPath = path.join(this.options.workspaceDir, id.substring(0,2));\n\t\t\tfs.access(userPath, (err) => {\n\t\t\t\tif(err) {\n\t\t\t\t\tcallback(err);\n\t\t\t\t}\n\t\t\t\t//TODO should a delete failure prevent the user delete?\n\t\t\t\treturn rimraf(userPath, (err) => {\n\t\t\t\t\tif(err) {\n\t\t\t\t\t\tcallback(err);\n\t\t\t\t\t}\n\t\t\t\t\torionAccount.remove({username: id}, callback);\n\t\t\t\t});\n\t\t\t});\n\t\t}.bind(this));\n\t}",
    "path": "modules/orionode/lib/metastore/mongodb/store.js",
    "repo": "eclipse/orion.client",
    "sha": "eb2583100c662b5cfc1b461a978b31d3b8555ce1",
    "url": "https://github.com/eclipse/orion.client/blob/eb2583100c662b5cfc1b461a978b31d3b8555ce1/modules/orionode/lib/metastore/mongodb/store.js#L325-L344"
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

An example of 'train' looks as follows.
```
{
    "code": "def settext(self, text, cls='current'):\n        \"\"\"Set the text for this element.\n\n        Arguments:\n            text (str): The text\n            cls (str): The class of the text, defaults to ``current`` (leave this unless you know what you are doing). There may be only one text content element of each class associated with the element.\n        \"\"\"\n        self.replace(TextContent, value=text, cls=cls)",
    "code_tokens": ["def", "settext", "(", "self", ",", "text", ",", "cls", "=", "'current'", ")", ":", "self", ".", "replace", "(", "TextContent", ",", "value", "=", "text", ",", "cls", "=", "cls", ")"],
    "docstring": "Set the text for this element.\n\n        Arguments:\n            text (str): The text\n            cls (str): The class of the text, defaults to ``current`` (leave this unless you know what you are doing). There may be only one text content element of each class associated with the element.",
    "docstring_tokens": ["Set", "the", "text", "for", "this", "element", "."],
    "func_name": "AbstractElement.settext",
    "id": 0,
    "language": "python",
    "original_string": "def settext(self, text, cls='current'):\n        \"\"\"Set the text for this element.\n\n        Arguments:\n            text (str): The text\n            cls (str): The class of the text, defaults to ``current`` (leave this unless you know what you are doing). There may be only one text content element of each class associated with the element.\n        \"\"\"\n        self.replace(TextContent, value=text, cls=cls)",
    "path": "pynlpl/formats/folia.py",
    "repo": "proycon/pynlpl",
    "sha": "7707f69a91caaa6cde037f0d0379f1d42500a68b",
    "url": "https://github.com/proycon/pynlpl/blob/7707f69a91caaa6cde037f0d0379f1d42500a68b/pynlpl/formats/folia.py#L1357-L1364"
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

## [Dataset Creation](#dataset-creation)

### [Curation Rationale](#curation-rationale)

[More Information Needed]

### [Source Data](#source-data)

[More Information Needed]

### [Annotations](#annotations)

[More Information Needed]

### [Personal and Sensitive Information](#personal-and-sensitive-information)

[More Information Needed]

## [Considerations for Using the Data](#considerations-for-using-the-data)

### [Social Impact of Dataset](#social-impact-of-dataset)

[More Information Needed]

### [Discussion of Biases](#discussion-of-biases)

[More Information Needed]

### [Other Known Limitations](#other-known-limitations)

[More Information Needed]

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

