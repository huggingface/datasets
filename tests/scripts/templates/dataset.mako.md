<%!
"""Dataset catalog documentation template.

Displayed in https://www.tensorflow.org/datasets/catalog/.

"""

import collections
import tensorflow_datasets as tfds
from tensorflow_datasets.core.utils import py_utils

%>

<%def name="echo(obj)">\
${obj}
</%def>

## --------------------------- Builder sections ---------------------------

<%def name="display_description(builder)">\
*   **Description**:

${builder.info.description}

</%def>

<%def name="display_config_description(builder)">\
% if builder.builder_config:
*   **Config description**: ${builder.builder_config.description}
% endif
</%def>

<%def name="display_homepage(builder)">\
*   **Homepage**: [${builder.info.homepage}](${builder.info.homepage})
</%def>

<%def name="display_source(builder)">\
*   **Source code**:
    [`${py_utils.get_class_path(builder)}`](${py_utils.get_class_url(builder)})
</%def>

<%def name="display_versions(builder)">\
<%
def list_versions(builder):
  for v in builder.versions:  # List all available versions (in default order)
    if v == builder.version:  # Highlight the default version
      version_name = '**`{}`** (default)'.format(str(v))
    else:
      version_name = '`{}`'.format(str(v))
    yield '{}: {}'.format(version_name, v.description or 'No release notes.')
%>\
*   **Versions**:
% for version_str in list_versions(builder):
    * ${version_str}
% endfor
</%def>

<%def name="display_download_size(builder)">\
*   **Download size**: `${tfds.units.size_str(builder.info.download_size)}`
</%def>

<%def name="display_dataset_size(builder)">\
*   **Dataset size**: `${tfds.units.size_str(builder.info.dataset_size)}`
</%def>

<%
def build_autocached_info(builder):
  """Returns the auto-cache information string."""
  always_cached = set()
  never_cached = set()
  unshuffle_cached = set()
  for split_name in builder.info.splits.keys():
    split_name = str(split_name)
    cache_shuffled = builder._should_cache_ds(
        split_name, shuffle_files=True, read_config=tfds.ReadConfig())
    cache_unshuffled = builder._should_cache_ds(
        split_name, shuffle_files=False, read_config=tfds.ReadConfig())

    if cache_shuffled == cache_unshuffled == True:
      always_cached.add(split_name)
    elif cache_shuffled == cache_unshuffled == False:
      never_cached.add(split_name)
    else:  # Dataset is only cached when shuffled_files is False
      assert not cache_shuffled and cache_unshuffled
      unshuffle_cached.add(split_name)


  if not len(builder.info.splits):
    autocached_info = 'Unknown'
  elif len(always_cached) == len(builder.info.splits.keys()):
    autocached_info = 'Yes'  # All splits are auto-cached.
  elif len(never_cached) == len(builder.info.splits.keys()):
    autocached_info = 'No'  # Splits never auto-cached.
  else:  # Some splits cached, some not.
    autocached_info_parts = []
    if always_cached:
      split_names_str = ', '.join(always_cached)
      autocached_info_parts.append('Yes ({})'.format(split_names_str))
    if never_cached:
      split_names_str = ', '.join(never_cached)
      autocached_info_parts.append('No ({})'.format(split_names_str))
    if unshuffle_cached:
      split_names_str = ', '.join(unshuffle_cached)
      autocached_info_parts.append(
          'Only when `shuffle_files=False` ({})'.format(split_names_str))
    autocached_info = ', '.join(autocached_info_parts)
  return autocached_info

%>
<%def name="display_autocache(builder)">\
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    ${build_autocached_info(builder)}
</%def>

<%def name="display_manual(builder)">\
% if builder.MANUAL_DOWNLOAD_INSTRUCTIONS:
*   **Manual download instructions**: This dataset requires you to download the
    source data manually into `download_config.manual_dir`
    (defaults to `~/tensorflow_datasets/manual/${builder.info.name}/`):<br/>
    ${builder.MANUAL_DOWNLOAD_INSTRUCTIONS}
% endif
</%def>

<%def name="display_splits(builder)">\
*   **Splits**:
<%
def get_num_examples(split_info):
  if split_info.num_examples:
    return '{:,}'.format(split_info.num_examples)
  else:
    return 'Not computed'
%>\

Split  | Examples
:----- | -------:
%for split_name, split_info in sorted(builder.info.splits.items()):
'${split_name}' | ${get_num_examples(split_info)}
%endfor

</%def>

<%def name="display_features(builder)">\
*   **Features**:

```python
${builder.info.features}
```
</%def>

<%def name="display_supervised(builder)">\
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `${str(builder.info.supervised_keys)}`
</%def>

<%def name="display_citation(builder)">\
% if builder.info.citation:
*   **Citation**:

```
${builder.info.citation}
```
% endif
</%def>

<%

Section = collections.namedtuple('Section', 'get_signature, make')

# Getter function returns a hashable signature of the section value
# which allow to detect sections shared accross all builders.
def get_description(builder):
  return builder.info.description

def get_config_description(builder):
  return builder.builder_config.description

def get_homepage(builder):
  return builder.info.homepage

def get_source(builder):
  return True  # Always common to all configs

def get_versions(builder):
  return tuple((str(v), v.description) for v in builder.versions)

def get_download_size(builder):
  return builder.info.download_size

def get_dataset_size(builder):
  return builder.info.dataset_size

def get_manual(builder):
  return builder.MANUAL_DOWNLOAD_INSTRUCTIONS

def get_autocache(builder):
  return build_autocached_info(builder)

def get_splits(builder):
  return tuple(
      (str(s.name), int(s.num_examples)) for s in builder.info.splits.values()
  )

def get_features(builder):
  return repr(builder.info.features)

def get_supervised(builder):
  return builder.info.supervised_keys

def get_citation(builder):
  return builder.info.citation

all_sections = [
    Section(get_description, display_description),
    Section(get_config_description, display_config_description),
    Section(get_homepage, display_homepage),
    Section(get_source, display_source),
    Section(get_versions, display_versions),
    Section(get_download_size, display_download_size),
    Section(get_dataset_size, display_dataset_size),
    Section(get_manual, display_manual),
    Section(get_autocache, display_autocache),
    Section(get_splits, display_splits),
    Section(get_features, display_features),
    Section(get_supervised, display_supervised),
    Section(get_citation, display_citation),
]

%>

## --------------------------- Single builder ---------------------------

<%def name="display_builder(builder, sections)">\
% for section in sections:
${section.make(builder)}\
% endfor
</%def>

## --------------------------- Builder configs ---------------------------

<%def name="display_all_builders(builders)">\
<%

# For each fields, extract if the field is shared or unique accross builder.
common_sections = []
unique_sections = []
for section in all_sections:
  if len(set(section.get_signature(b) for b in builders)) == 1:
    common_sections.append(section)
  else:
    unique_sections.append(section)

%>

${display_builder(next(iter(builders)), common_sections)}

% for i, builder in enumerate(builders):
<%
header_suffix = '(default config)' if i == 0 else ''
%>\
${'##'} ${builder.name}/${builder.builder_config.name} ${header_suffix}

${display_builder(builder, unique_sections)}
% endfor
</%def>

## --------------------------- Main page ---------------------------

${'#'} `${builder.name}`

%if builder.MANUAL_DOWNLOAD_INSTRUCTIONS:
Warning: Manual download required. See instructions below.
%endif

<%doc>First case: Single builder.</%doc>\
% if not builder.builder_config:
${display_builder(builder, all_sections)}
<%doc>Second case: Builder configs.</%doc>\
% else:
${display_all_builders(config_builders)}
% endif
