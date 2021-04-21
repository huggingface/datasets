---
name: Bug report
about: Create a report to help reproduce and fix the bug
title: ''
labels: bug
assignees: ''

---

## Describe the bug
A clear and concise description of what the bug is.

## Steps to reproduce the bug
```python
# Sample code to reproduce the bug
```

## Expected results
A clear and concise description of the expected results.

## Actual results
Specify the actual results or traceback.

## Versions
Paste the output of the following code:
```python
import datasets
import sys
import platform

print(f"""
- Datasets: {datasets.__version__}
- Python: {sys.version}
- Platform: {platform.platform()}
""")
```
