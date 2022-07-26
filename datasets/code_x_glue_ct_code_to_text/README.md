---
annotations_creators:
- found
language_creators:
- found
language:
- code
- en
license:
- c-uda
multilinguality:
- other-programming-languages
size_categories:
- 100K<n<1M
- 10K<n<100K
source_datasets:
- original
task_categories:
- translation
task_ids:
- translation-other-code-to-text
pretty_name: CodeXGlueCtCodeToText
configs:
- go
- java
- javascript
- php
- python
- ruby
---
# Dataset Card for "code_x_glue_ct_code_to_text"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits-sample-size)
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
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Text/code-to-text

### Dataset Summary

CodeXGLUE code-to-text dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Text/code-to-text

The dataset we use comes from CodeSearchNet and we filter the dataset as the following:
- Remove examples that codes cannot be parsed into an abstract syntax tree.
- Remove examples that #tokens of documents is < 3 or >256
- Remove examples that documents contain special tokens (e.g. <img ...> or https:...)
- Remove examples that documents are not English.

### Supported Tasks and Leaderboards

- `machine-translation`: The dataset can be used to train a model for automatically generating **English** docstrings for code.

### Languages

- Go **programming** language
- Java **programming** language
- Javascript **programming** language
- PHP **programming** language
- Python **programming** language
- Ruby **programming** language
- English **natural** language

## Dataset Structure

### Data Instances

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

An example of 'test' looks as follows.
```
{
    "code": "function createInstance(defaultConfig) {\n  var context = new Axios(defaultConfig);\n  var instance = bind(Axios.prototype.request, context);\n\n  // Copy axios.prototype to instance\n  utils.extend(instance, Axios.prototype, context);\n\n  // Copy context to instance\n  utils.extend(instance, context);\n\n  return instance;\n}", 
    "code_tokens": ["function", "createInstance", "(", "defaultConfig", ")", "{", "var", "context", "=", "new", "Axios", "(", "defaultConfig", ")", ";", "var", "instance", "=", "bind", "(", "Axios", ".", "prototype", ".", "request", ",", "context", ")", ";", "// Copy axios.prototype to instance", "utils", ".", "extend", "(", "instance", ",", "Axios", ".", "prototype", ",", "context", ")", ";", "// Copy context to instance", "utils", ".", "extend", "(", "instance", ",", "context", ")", ";", "return", "instance", ";", "}"], 
    "docstring": "Create an instance of Axios\n\n@param {Object} defaultConfig The default config for the instance\n@return {Axios} A new instance of Axios", 
    "docstring_tokens": ["Create", "an", "instance", "of", "Axios"], 
    "func_name": "createInstance", 
    "id": 0, 
    "language": "javascript", 
    "original_string": "function createInstance(defaultConfig) {\n  var context = new Axios(defaultConfig);\n  var instance = bind(Axios.prototype.request, context);\n\n  // Copy axios.prototype to instance\n  utils.extend(instance, Axios.prototype, context);\n\n  // Copy context to instance\n  utils.extend(instance, context);\n\n  return instance;\n}", 
    "path": "lib/axios.js", 
    "repo": "axios/axios", 
    "sha": "92d231387fe2092f8736bc1746d4caa766b675f5", 
    "url": "https://github.com/axios/axios/blob/92d231387fe2092f8736bc1746d4caa766b675f5/lib/axios.js#L15-L26"
}
```

#### php

An example of 'train' looks as follows.
```
{
    "code": "public static function build($serviceAddress, $restConfigPath, array $config = [])\n    {\n        $config += [\n            'httpHandler'  => null,\n        ];\n        list($baseUri, $port) = self::normalizeServiceAddress($serviceAddress);\n        $requestBuilder = new RequestBuilder(\"$baseUri:$port\", $restConfigPath);\n        $httpHandler = $config['httpHandler'] ?: self::buildHttpHandlerAsync();\n        return new RestTransport($requestBuilder, $httpHandler);\n    }", 
    "code_tokens": ["public", "static", "function", "build", "(", "$", "serviceAddress", ",", "$", "restConfigPath", ",", "array", "$", "config", "=", "[", "]", ")", "{", "$", "config", "+=", "[", "'httpHandler'", "=>", "null", ",", "]", ";", "list", "(", "$", "baseUri", ",", "$", "port", ")", "=", "self", "::", "normalizeServiceAddress", "(", "$", "serviceAddress", ")", ";", "$", "requestBuilder", "=", "new", "RequestBuilder", "(", "\"$baseUri:$port\"", ",", "$", "restConfigPath", ")", ";", "$", "httpHandler", "=", "$", "config", "[", "'httpHandler'", "]", "?", ":", "self", "::", "buildHttpHandlerAsync", "(", ")", ";", "return", "new", "RestTransport", "(", "$", "requestBuilder", ",", "$", "httpHandler", ")", ";", "}"], 
    "docstring": "Builds a RestTransport.\n\n@param string $serviceAddress\nThe address of the API remote host, for example \"example.googleapis.com\".\n@param string $restConfigPath\nPath to rest config file.\n@param array $config {\nConfig options used to construct the gRPC transport.\n\n@type callable $httpHandler A handler used to deliver PSR-7 requests.\n}\n@return RestTransport\n@throws ValidationException", 
    "docstring_tokens": ["Builds", "a", "RestTransport", "."], 
    "func_name": "RestTransport.build", 
    "id": 0, 
    "language": "php", 
    "original_string": "public static function build($serviceAddress, $restConfigPath, array $config = [])\n    {\n        $config += [\n            'httpHandler'  => null,\n        ];\n        list($baseUri, $port) = self::normalizeServiceAddress($serviceAddress);\n        $requestBuilder = new RequestBuilder(\"$baseUri:$port\", $restConfigPath);\n        $httpHandler = $config['httpHandler'] ?: self::buildHttpHandlerAsync();\n        return new RestTransport($requestBuilder, $httpHandler);\n    }", 
    "path": "src/Transport/RestTransport.php", 
    "repo": "googleapis/gax-php", 
    "sha": "48387fb818c6882296710a2302a0aa973b99afb2", 
    "url": "https://github.com/googleapis/gax-php/blob/48387fb818c6882296710a2302a0aa973b99afb2/src/Transport/RestTransport.php#L85-L94"
}
```

#### python

An example of 'validation' looks as follows.
```
{
    "code": "def save_act(self, path=None):\n        \"\"\"Save model to a pickle located at `path`\"\"\"\n        if path is None:\n            path = os.path.join(logger.get_dir(), \"model.pkl\")\n\n        with tempfile.TemporaryDirectory() as td:\n            save_variables(os.path.join(td, \"model\"))\n            arc_name = os.path.join(td, \"packed.zip\")\n            with zipfile.ZipFile(arc_name, 'w') as zipf:\n                for root, dirs, files in os.walk(td):\n                    for fname in files:\n                        file_path = os.path.join(root, fname)\n                        if file_path != arc_name:\n                            zipf.write(file_path, os.path.relpath(file_path, td))\n            with open(arc_name, \"rb\") as f:\n                model_data = f.read()\n        with open(path, \"wb\") as f:\n            cloudpickle.dump((model_data, self._act_params), f)", 
    "code_tokens": ["def", "save_act", "(", "self", ",", "path", "=", "None", ")", ":", "if", "path", "is", "None", ":", "path", "=", "os", ".", "path", ".", "join", "(", "logger", ".", "get_dir", "(", ")", ",", "\"model.pkl\"", ")", "with", "tempfile", ".", "TemporaryDirectory", "(", ")", "as", "td", ":", "save_variables", "(", "os", ".", "path", ".", "join", "(", "td", ",", "\"model\"", ")", ")", "arc_name", "=", "os", ".", "path", ".", "join", "(", "td", ",", "\"packed.zip\"", ")", "with", "zipfile", ".", "ZipFile", "(", "arc_name", ",", "'w'", ")", "as", "zipf", ":", "for", "root", ",", "dirs", ",", "files", "in", "os", ".", "walk", "(", "td", ")", ":", "for", "fname", "in", "files", ":", "file_path", "=", "os", ".", "path", ".", "join", "(", "root", ",", "fname", ")", "if", "file_path", "!=", "arc_name", ":", "zipf", ".", "write", "(", "file_path", ",", "os", ".", "path", ".", "relpath", "(", "file_path", ",", "td", ")", ")", "with", "open", "(", "arc_name", ",", "\"rb\"", ")", "as", "f", ":", "model_data", "=", "f", ".", "read", "(", ")", "with", "open", "(", "path", ",", "\"wb\"", ")", "as", "f", ":", "cloudpickle", ".", "dump", "(", "(", "model_data", ",", "self", ".", "_act_params", ")", ",", "f", ")"], 
    "docstring": "Save model to a pickle located at `path`", 
    "docstring_tokens": ["Save", "model", "to", "a", "pickle", "located", "at", "path"], 
    "func_name": "ActWrapper.save_act", 
    "id": 0, 
    "language": "python", 
    "original_string": "def save_act(self, path=None):\n        \"\"\"Save model to a pickle located at `path`\"\"\"\n        if path is None:\n            path = os.path.join(logger.get_dir(), \"model.pkl\")\n\n        with tempfile.TemporaryDirectory() as td:\n            save_variables(os.path.join(td, \"model\"))\n            arc_name = os.path.join(td, \"packed.zip\")\n            with zipfile.ZipFile(arc_name, 'w') as zipf:\n                for root, dirs, files in os.walk(td):\n                    for fname in files:\n                        file_path = os.path.join(root, fname)\n                        if file_path != arc_name:\n                            zipf.write(file_path, os.path.relpath(file_path, td))\n            with open(arc_name, \"rb\") as f:\n                model_data = f.read()\n        with open(path, \"wb\") as f:\n            cloudpickle.dump((model_data, self._act_params), f)", 
    "path": "baselines/deepq/deepq.py", 
    "repo": "openai/baselines", 
    "sha": "3301089b48c42b87b396e246ea3f56fa4bfc9678", 
    "url": "https://github.com/openai/baselines/blob/3301089b48c42b87b396e246ea3f56fa4bfc9678/baselines/deepq/deepq.py#L55-L72"
}
```

#### ruby

An example of 'train' looks as follows.
```
{
    "code": "def render_body(context, options)\n      if options.key?(:partial)\n        [render_partial(context, options)]\n      else\n        StreamingTemplateRenderer.new(@lookup_context).render(context, options)\n      end\n    end", 
    "code_tokens": ["def", "render_body", "(", "context", ",", "options", ")", "if", "options", ".", "key?", "(", ":partial", ")", "[", "render_partial", "(", "context", ",", "options", ")", "]", "else", "StreamingTemplateRenderer", ".", "new", "(", "@lookup_context", ")", ".", "render", "(", "context", ",", "options", ")", "end", "end"], 
    "docstring": "Render but returns a valid Rack body. If fibers are defined, we return\n a streaming body that renders the template piece by piece.\n\n Note that partials are not supported to be rendered with streaming,\n so in such cases, we just wrap them in an array.", 
    "docstring_tokens": ["Render", "but", "returns", "a", "valid", "Rack", "body", ".", "If", "fibers", "are", "defined", "we", "return", "a", "streaming", "body", "that", "renders", "the", "template", "piece", "by", "piece", "."], 
    "func_name": "ActionView.Renderer.render_body", 
    "id": 0, 
    "language": "ruby", 
    "original_string": "def render_body(context, options)\n      if options.key?(:partial)\n        [render_partial(context, options)]\n      else\n        StreamingTemplateRenderer.new(@lookup_context).render(context, options)\n      end\n    end", 
    "path": "actionview/lib/action_view/renderer/renderer.rb", 
    "repo": "rails/rails", 
    "sha": "85a8bc644be69908f05740a5886ec19cd3679df5", 
    "url": "https://github.com/rails/rails/blob/85a8bc644be69908f05740a5886ec19cd3679df5/actionview/lib/action_view/renderer/renderer.rb#L38-L44"
}
```

### Data Fields

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

### Data Splits

|   name   |train |validation|test |
|----------|-----:|---------:|----:|
|go        |167288|      7325| 8122|
|java      |164923|      5183|10955|
|javascript| 58025|      3885| 3291|
|php       |241241|     12982|14014|
|python    |251820|     13914|14918|
|ruby      | 24927|      1400| 1261|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

Data from CodeSearchNet Challenge dataset.
[More Information Needed]

#### Who are the source language producers?

Software Engineering developers.

### Annotations

#### Annotation process

[More Information Needed]

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

https://github.com/microsoft, https://github.com/madlag

### Licensing Information

Computational Use of Data Agreement (C-UDA) License.

### Citation Information

```
@article{husain2019codesearchnet,
  title={Codesearchnet challenge: Evaluating the state of semantic code search},
  author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
  journal={arXiv preprint arXiv:1909.09436},
  year={2019}
}
```

### Contributions

Thanks to @madlag (and partly also @ncoop57) for adding this dataset.
