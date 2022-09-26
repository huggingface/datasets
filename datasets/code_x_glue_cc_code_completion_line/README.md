---
annotations_creators:
- found
language_creators:
- found
language:
- code
license:
- c-uda
multilinguality:
- monolingual
size_categories:
- 1K<n<10K
- n<1K
source_datasets:
- original
task_categories:
- text-generation
- fill-mask
task_ids:
- slot-filling
pretty_name: CodeXGlueCcCodeCompletionLine
configs:
- go
- java
- javascript
- php
- python
- ruby
---
# Dataset Card for "code_x_glue_cc_code_completion_line"

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

- **Homepage:** https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/CodeCompletion-line

### Dataset Summary

CodeXGLUE CodeCompletion-line dataset, available at https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/CodeCompletion-line

Complete the unfinished line given previous context. Models are evaluated by exact match and edit similarity.
We propose line completion task to test model's ability to autocomplete a line. Majority code completion systems behave well in token level completion, but fail in completing an unfinished line like a method call with specific parameters, a function signature, a loop condition, a variable definition and so on. When a software develop finish one or more tokens of the current line, the line level completion model is expected to generate the entire line of syntactically correct code.
Line level code completion task shares the train/dev dataset with token level completion. After training a model on CodeCompletion-token, you could directly use it to test on line-level completion.

### Supported Tasks and Leaderboards

- `slot-filling`: The dataset can be used to train a model for completing entire code lines.

### Languages

- Java **programming** language
- Python **programming** language

## Dataset Structure

### Data Instances

#### java

An example of 'train' looks as follows.
```
{
    "gt": "", 
    "id": 0, 
    "input": "<s> package org . rubypeople . rdt . internal . ui . rubyeditor ; import java . util . Iterator ; import org . eclipse . core . resources . IMarker ; import org . eclipse . ui . texteditor . MarkerAnnotation ; import org . eclipse . ui . texteditor . MarkerUtilities ; import org . rubypeople . rdt . core . IRubyElement ; import org . rubypeople . rdt . core . IRubyModelMarker ; import org . rubypeople . rdt . core . IRubyScript ; import org . rubypeople . rdt . core . RubyCore ; public class RubyMarkerAnnotation extends MarkerAnnotation implements IRubyAnnotation { public static final String RUBY_MARKER_TYPE_PREFIX = \"\" ; public static final String ERROR_ANNOTATION_TYPE = \"\" ; public static final String WARNING_ANNOTATION_TYPE = \"\" ; public static final String INFO_ANNOTATION_TYPE = \"\" ; public static final String TASK_ANNOTATION_TYPE = \"\" ; private IRubyAnnotation fOverlay ; public RubyMarkerAnnotation ( IMarker marker ) { super ( marker ) ; } public String [ ] getArguments ( ) { return null ; } public int getId ( ) { IMarker marker = getMarker ( ) ; if ( marker == null || ! marker . exists ( ) ) return - 1 ; if ( isProblem ( ) ) return marker . getAttribute ( IRubyModelMarker . ID , - 1 ) ; return - 1 ; } public boolean isProblem ( ) { String type = getType ( ) ; return WARNING_ANNOTATION_TYPE . equals ( type ) || ERROR_ANNOTATION_TYPE . equals"
}
```

#### python

An example of 'train' looks as follows.
```
{
    "gt": "", 
    "id": 0, 
    "input": "<s> from __future__ import absolute_import <EOL> import weakref <EOL> import operator <EOL> from . compat import threading , itertools_filterfalse <EOL> from . import py2k <EOL> import types <EOL> EMPTY_SET = frozenset ( ) <EOL> class KeyedTuple ( tuple ) : <EOL> def __new__ ( cls , vals , labels = None ) : <EOL> t = tuple . __new__ ( cls , vals ) <EOL> t . _labels = [ ] <EOL> if labels : <EOL> t . __dict__ . update ( zip ( labels , vals ) ) <EOL> t . _labels = labels <EOL> return t <EOL> def keys ( self ) : <EOL> return [ l for l in self . _labels if l is not None ] <EOL> @ property <EOL> def _fields ( self ) : <EOL> return tuple ( self . keys ( ) ) <EOL> def _asdict ( self ) : <EOL> return dict ( ( key , self . __dict__ [ key ] ) for key in self . keys ( ) ) <EOL> class ImmutableContainer ( object ) : <EOL> def _immutable ( self , * arg , ** kw ) : <EOL> raise TypeError ( \"\" % self . __class__ . __name__ ) <EOL> __delitem__ = __setitem__ = __setattr__ = _immutable <EOL> class immutabledict ( ImmutableContainer , dict ) : <EOL> clear = pop = popitem = setdefault = update = ImmutableContainer . _immutable <EOL> def __new__ ( cls , * args ) : <EOL> new = dict . __new__ ( cls ) <EOL> dict . __init__ ( new , * args ) <EOL> return new <EOL> def __init__ ( self , * args ) : <EOL> pass <EOL> def __reduce__ ( self ) : <EOL> return immutabledict , ( dict ( self ) , ) <EOL> def union ( self , d ) : <EOL> if not self : <EOL> return immutabledict ( d ) <EOL> else : <EOL> d2 = immutabledict ( self ) <EOL> dict . update ( d2 , d ) <EOL> return d2 <EOL> def __repr__ ( self ) : <EOL> return \"\" % dict . __repr__ ( self ) <EOL> class Properties ( object ) : <EOL> def __init__ ( self , data ) : <EOL> self . __dict__ [ '_data' ] = data <EOL> def __len__ ( self ) : <EOL> return len ( self . _data ) <EOL> def __iter__ ( self ) : <EOL> return iter ( list ( self . _data . values ( ) ) ) <EOL> def __add__ ( self , other ) : <EOL> return list ( self ) + list ( other ) <EOL> def __setitem__ ( self , key , object ) : <EOL> self . _data [ key ] = object <EOL> def __getitem__ ( self , key ) : <EOL> return self . _data [ key ] <EOL> def __delitem__ ( self , key ) : <EOL> del self . _data [ key ] <EOL> def __setattr__ ( self , key , object ) : <EOL> self . _data [ key ] = object <EOL> def __getstate__ ( self ) : <EOL> return { '_data' : self . __dict__ [ '_data' ] } <EOL> def __setstate__ ( self , state ) : <EOL> self . __dict__ [ '_data' ] = state [ '_data' ] <EOL> def __getattr__ ( self , key ) : <EOL> try : <EOL> return self . _data [ key ] <EOL> except KeyError : <EOL> raise AttributeError ( key ) <EOL> def __contains__ ( self , key ) : <EOL> return key in self . _data <EOL> def as_immutable ( self ) : <EOL> return ImmutableProperties ( self . _data ) <EOL> def update ( self , value ) : <EOL> self . _data . update ( value ) <EOL> def get ( self , key , default = None ) : <EOL> if key in self : <EOL> return self [ key ] <EOL> else : <EOL> return default <EOL> def keys ( self ) : <EOL> return list ( self . _data ) <EOL> def values ( self ) : <EOL> return list ( self . _data . values ( ) ) <EOL> def items ( self ) : <EOL> return list ( self . _data . items ( ) ) <EOL> def has_key ( self , key ) : <EOL> return key in self . _data <EOL> def clear ( self ) : <EOL> self . _data . clear ( ) <EOL> class OrderedProperties ( Properties ) : <EOL> def __init__ ( self ) : <EOL> Properties . __init__ ( self , OrderedDict ( ) ) <EOL> class ImmutableProperties ( ImmutableContainer , Properties ) : <EOL> class OrderedDict ( dict ) : <EOL> def __init__ ( self , ____sequence = None , ** kwargs ) : <EOL> self . _list = [ ] <EOL> if ____sequence is None : <EOL> if kwargs : <EOL> self . update ( ** kwargs ) <EOL> else : <EOL> self . update ( ____sequence , ** kwargs ) <EOL> def clear ( self ) : <EOL> self . _list = [ ] <EOL> dict . clear ( self ) <EOL> def copy ( self ) : <EOL> return self . __copy__ ( ) <EOL> def __copy__ ( self ) : <EOL> return OrderedDict ( self ) <EOL> def sort ( self , * arg , ** kw ) : <EOL> self . _list . sort ( * arg , ** kw ) <EOL> def update ( self , ____sequence = None , ** kwargs ) : <EOL> if ____sequence is not None : <EOL> if hasattr ( ____sequence , 'keys' ) : <EOL> for key in ____sequence . keys ( ) : <EOL> self . __setitem__ ( key , ____sequence [ key ] ) <EOL> else : <EOL> for key , value in ____sequence : <EOL> self [ key ] = value <EOL> if kwargs : <EOL> self . update ( kwargs ) <EOL> def setdefault ( self , key , value ) : <EOL> if key not in self : <EOL> self . __setitem__ ( key , value ) <EOL> return value <EOL> else : <EOL> return self . __getitem__ ( key ) <EOL> def __iter__ ( self ) : <EOL> return iter ( self . _list ) <EOL> def keys ( self ) : <EOL> return list ( self ) <EOL> def values ( self ) : <EOL> return [ self [ key ] for key in self . _list ] <EOL> def items ( self ) : <EOL> return [ ( key , self [ key ] ) for key in self . _list ] <EOL> if py2k : <EOL> def itervalues ( self ) : <EOL> return iter ( self . values ( ) ) <EOL> def iterkeys ( self ) : <EOL> return iter ( self ) <EOL> def iteritems ( self ) : <EOL> return iter ( self . items ( ) ) <EOL> def __setitem__ ( self , key , object ) : <EOL> if key not in self : <EOL> try : <EOL> self . _list . append ( key ) <EOL> except AttributeError : <EOL> self . _list = [ key ] <EOL> dict . __setitem__ ( self , key , object ) <EOL> def __delitem__ ( self , key ) : <EOL> dict . __delitem__ ( self , key ) <EOL> self . _list . remove ( key ) <EOL> def pop ( self , key , * default ) : <EOL> present = key in self <EOL> value = dict . pop ( self , key , * default ) <EOL> if present : <EOL> self . _list . remove ( key ) <EOL> return value <EOL> def popitem ( self ) : <EOL> item = dict . popitem ( self ) <EOL> self . _list . remove ( item [ 0 ] ) <EOL> return item <EOL> class OrderedSet ( set ) : <EOL> def __init__ ( self , d = None ) : <EOL> set . __init__ ( self ) <EOL> self . _list = [ ] <EOL> if d is not None : <EOL>"
}
```

### Data Fields

In the following each data field in go is explained for each config. The data fields are the same among all splits.

#### java, python

|field name| type |        description         |
|----------|------|----------------------------|
|id        |int32 | Index of the sample        |
|input     |string| Input code string          |
|gt        |string| Code string to be predicted|

### Data Splits

| name |train|
|------|----:|
|java  | 3000|
|python|10000|

## Dataset Creation

### Curation Rationale

[More Information Needed]

### Source Data

#### Initial Data Collection and Normalization

[More Information Needed]

#### Who are the source language producers?

[More Information Needed]

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
@article{raychev2016probabilistic,
  title={Probabilistic Model for Code with Decision Trees},
  author={Raychev, Veselin and Bielik, Pavol and Vechev, Martin},
  journal={ACM SIGPLAN Notices},
  pages={731--747},
  year={2016},
  publisher={ACM New York, NY, USA}
}
@inproceedings{allamanis2013mining,
  title={Mining Source Code Repositories at Massive Scale using Language Modeling},
  author={Allamanis, Miltiadis and Sutton, Charles},
  booktitle={2013 10th Working Conference on Mining Software Repositories (MSR)},
  pages={207--216},
  year={2013},
  organization={IEEE}
}
```

### Contributions

Thanks to @madlag (and partly also @ncoop57) for adding this dataset.
