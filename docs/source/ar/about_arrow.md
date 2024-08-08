# Datasets 🤝 Arrow

## ما هو Arrow؟

[Arrow](https://arrow.apache.org/) يتيح معالجة ونقل كميات كبيرة من البيانات بسرعة. إنه تنسيق بيانات محدد يخزن البيانات في تخطيط ذاكرة عمودي. يوفر هذا العديد من المزايا الهامة:

* التنسيق القياسي لـ Arrow يسمح [بالقراءة بدون نسخ](https://en.wikipedia.org/wiki/Zero-copy) والتي تزيل فعليًا جميع النفقات العامة للتسلسل.
* Arrow لا يعتمد على لغة برمجة معينة، لذلك فهو يدعم لغات برمجة مختلفة.
* Arrow موجه نحو الأعمدة، لذلك فهو أسرع في الاستعلام ومعالجة شرائح أو أعمدة من البيانات.
* يسمح Arrow بالتسليم بدون نسخ إلى أدوات التعلم الآلي القياسية مثل NumPy وPandas وPyTorch وTensorFlow.
* يدعم Arrow العديد من أنواع الأعمدة، والتي قد تكون متداخلة.

## الذاكرة الخرائطية

🤗 يستخدم Datasets Arrow لنظام التخزين المؤقت المحلي الخاص به. يسمح ذلك بدعم مجموعات البيانات بواسطة ذاكرة تخزين مؤقت على القرص، يتم تعيينها إلى الذاكرة للبحث السريع. تسمح هذه البنية باستخدام مجموعات بيانات كبيرة على أجهزة ذات ذاكرة جهاز صغيرة نسبيًا.

على سبيل المثال، لا يستغرق تحميل مجموعة بيانات Wikipedia الإنجليزية الكاملة سوى بضعة ميغابايت من ذاكرة الوصول العشوائي (RAM):

```python
>>> import os; import psutil; import timeit
>>> from datasets import load_dataset

# Process.memory_info is expressed in bytes, so convert to megabytes
>>> mem_before = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
>>> wiki = load_dataset("wikipedia", "20220301.en", split="train")
>>> mem_after = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

>>> print(f"RAM memory used: {(mem_after - mem_before)} MB")
RAM memory used: 50 MB
```

هذا ممكن لأن بيانات Arrow يتم تعيينها إلى الذاكرة فعليًا من القرص، وليس تحميلها في الذاكرة. تسمح الخرائط الذاكرية بالوصول إلى البيانات على القرص، وتستفيد من قدرات الذاكرة الظاهرية للبحث السريع.

## الأداء

إن التكرار فوق مجموعة بيانات ذات خريطة ذاكرة باستخدام Arrow سريع. إن التكرار فوق Wikipedia على جهاز كمبيوتر محمول يمنحك سرعات تتراوح بين 1-3 جيجابت/ثانية:

```python
>>> s = """batch_size = 1000
... for batch in wiki.iter(batch_size):
...     ...
... """

>>> elapsed_time = timeit.timeit(stmt=s, number=1, globals=globals())
>>> print(f"Time to iterate over the {wiki.dataset_size >> 30} GB dataset: {elapsed_time:.1f} sec, "
...       f"ie. {float(wiki.dataset_size >> 27)/elapsed_time:.1f} Gb/s")
Time to iterate over the 18 GB dataset: 31.8 sec, ie. 4.8 Gb/s
```