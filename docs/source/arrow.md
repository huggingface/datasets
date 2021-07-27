# Datasets 🤝 Arrow

TO DO:

A brief introduction on why Datasets chose to use Arrow. For example, include some context and background like design decisions and constraints. The user should understand why we decided to use Arrow instead of something else.

## What is Arrow?

Arrow enables large amounts of data to be processed and moved quickly. It is a specific data format that stores data in a columnar memory layout. This provides several significant advantages:

* Arrow's standard format allows zero copy reads which removes virtually all serialization overhead.
* Arrow is language-agnostic so it supports different programming languages.
* Arrow is column-oriented so it is faster at querying and processing data.

### Performance

TO DO:

Discussion on Arrow's speed and performance, especially as it relates to Datasets. In particular, this [tweet] from Thom is worth explaining how Datasets can iterate over such a massive dataset so quickly.

### Memory

TO DO:

Discussion on memory-mapping and efficiency, which enables this:

```python
>>> from datasets import total_allocated_bytes
>>> print("The number of bytes allocated on the drive is", dataset.dataset_size)
The number of bytes allocated on the drive is 1492156
>>> print("For comparison, here is the number of bytes allocated in memory:", total_allocated_bytes())
For comparison, here is the number of bytes allocated in memory: 0
```

[tweet]: https://twitter.com/Thom_Wolf/status/1272512974935203841