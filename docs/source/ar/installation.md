## التثبيت

قبل البدء، ستحتاج إلى إعداد بيئة العمل الخاصة بك وتثبيت الحزم المناسبة. تم اختبار 🤗 Datasets على **Python 3.7+**.

<Tip>

إذا كنت تريد استخدام 🤗 Datasets مع TensorFlow أو PyTorch، ستحتاج إلى تثبيتهما بشكل منفصل. راجع صفحة تثبيت TensorFlow](https://www.tensorflow.org/install/pip#tensorflow-2-packages-are-available) أو صفحة تثبيت PyTorch](https://pytorch.org/get-started/locally/#start-locally) للاطلاع على أمر التثبيت المحدد لإطار العمل الخاص بك.

</Tip>

## البيئة الافتراضية

يجب تثبيت 🤗 Datasets في [بيئة افتراضية](https://docs.python.org/3/library/venv.html) للحفاظ على التنظيم وتجنب تعارضات الاعتمادات.

1. قم بإنشاء دليل المشروع الخاص بك والانتقال إليه:

```bash
mkdir ~/my-project
cd ~/my-project
```

2. ابدأ بيئة افتراضية داخل دليلك:

```bash
python -m venv .env
```

3. قم بتنشيط وتعطيل البيئة الافتراضية باستخدام الأوامر التالية:

```bash
# تنشيط البيئة الافتراضية
source .env/bin/activate

# إلغاء تنشيط البيئة الافتراضية
source .env/bin/deactivate
```

بمجرد إنشاء بيئتك الافتراضية، يمكنك تثبيت 🤗 Datasets فيها.

## pip

أسهل طريقة لتثبيت 🤗 Datasets هي باستخدام pip:

```bash
pip install datasets
```

قم بتشغيل الأمر التالي للتحقق مما إذا كان 🤗 Datasets قد تم تثبيته بشكل صحيح:

```bash
python -c "from datasets import load_dataset; print(load_dataset('squad', split='train')[0])"
```

يقوم هذا الأمر بتنزيل الإصدار 1 من [مجموعة بيانات Stanford Question Answering Dataset (SQuAD)](https://rajpurkar.github.io/SQuAD-explorer/)، وتحميل قسم التدريب، وطباعة أول مثال تدريبي. يجب أن ترى ما يلي:

```python
{'answers': {'answer_start': [515], 'text': ['Saint Bernadette Soubirous']}, 'context': 'Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend "Venite Ad Me Omnes". Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary.', 'id': '5733be284776f41900661182', 'question': 'To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?', 'title': 'University_of_Notre_Dame'}
```

## الصوت

للعمل مع مجموعات البيانات الصوتية، تحتاج إلى تثبيت ميزة [`Audio`] كاعتماد إضافي:

```bash
pip install datasets[audio]
```

<Tip warning={true}>

لفك تشفير ملفات mp3، تحتاج إلى وجود إصدار 1.1.0 على الأقل من مكتبة النظام `libsndfile`. عادة ما يتم تضمينه مع حزمة بايثون [`soundfile`](https://github.com/bastibe/python-soundfile)، والتي يتم تثبيتها كاعتماد صوتي إضافي لـ 🤗 Datasets.

بالنسبة لنظام Linux، يتم حزم الإصدار المطلوب من `libsndfile` مع `soundfile` بدءًا من الإصدار 0.12.0. يمكنك تشغيل الأمر التالي لتحديد إصدار `libsndfile` الذي يستخدمه `soundfile`:

```bash
python -c "import soundfile; print(soundfile.__libsndfile_version__)"
```

</Tip>

## الرؤية

للعمل مع مجموعات البيانات الصورية، تحتاج إلى تثبيت ميزة [`Image`] كاعتماد إضافي:

```bash
pip install datasets[vision]
```

## المصدر

يتيح بناء 🤗 Datasets من المصدر إجراء تغييرات على قاعدة التعليمات البرمجية. لتثبيته من المصدر، استنسخ المستودع وقم بالتثبيت باستخدام الأوامر التالية:

```bash
git clone https://github.com/huggingface/datasets.git
cd datasets
pip install -e .
```

مرة أخرى، يمكنك التحقق مما إذا كان 🤗 Datasets قد تم تثبيته بشكل صحيح باستخدام الأمر التالي:

```bash
python -c "from datasets import load_dataset; print(load_dataset('squad', split='train')[0])"
```

## كوندا

يمكن أيضًا تثبيت 🤗 Datasets من كوندا، وهو نظام إدارة الحزم:

```bash
conda install -c huggingface -c conda-forge datasets
```