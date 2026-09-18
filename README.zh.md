<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/datasets/huggingface/documentation-images/raw/main/datasets-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://huggingface.co/datasets/huggingface/documentation-images/raw/main/datasets-logo-light.svg">
    <img alt="Hugging Face Datasets 库" src="https://huggingface.co/datasets/huggingface/documentation-images/raw/main/datasets-logo-light.svg" width="352" height="59" style="max-width: 100%;">
  </picture>
  <br/>
  <br/>
</p>

<p align="center">
    <a href="README.md">English</a> · <b>简体中文</b>
</p>

<p align="center">
    <a href="https://github.com/huggingface/datasets/actions/workflows/ci.yml?query=branch%3Amain"><img alt="构建状态" src="https://github.com/huggingface/datasets/actions/workflows/ci.yml/badge.svg?branch=main"></a>
    <a href="https://github.com/huggingface/datasets/blob/main/LICENSE"><img alt="GitHub 许可证" src="https://img.shields.io/github/license/huggingface/datasets.svg?color=blue"></a>
    <a href="https://huggingface.co/docs/datasets/index.html"><img alt="官方文档" src="https://img.shields.io/website/http/huggingface.co/docs/datasets/index.html.svg?down_color=red&down_message=offline&up_message=online"></a>
    <a href="https://github.com/huggingface/datasets/releases"><img alt="GitHub 发布版本" src="https://img.shields.io/github/release/huggingface/datasets.svg"></a>
    <a href="https://huggingface.co/datasets/"><img alt="数据集数量" src="https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen"></a>
    <a href="CODE_OF_CONDUCT.md"><img alt="贡献者公约" src="https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg"></a>
    <a href="https://zenodo.org/badge/latestdoi/250213286"><img src="https://zenodo.org/badge/250213286.svg" alt="DOI 引用"></a>
</p>

🤗 Datasets 是一个轻量级库，提供**两大**核心特性：

- **海量公共数据集的一行代码加载器 (One-line Dataloaders)**：只需一行代码即可下载并预处理 [HuggingFace Datasets Hub](https://huggingface.co/datasets) 上提供的成千上万个主流公共数据集（涵盖图像数据集、音频数据集、支持 467 种语言与方言的文本数据集、3D 医学影像、视频数据集、AI Agent 轨迹等）。借助如 `squad_dataset = load_dataset("rajpurkar/squad")` 这样简洁的命令，即可快速将任何数据集准备就绪，直接接入多种机器学习模型框架（NumPy/Pandas/PyTorch/TensorFlow/JAX/Polars）进行训练与评估。
- **高效的数据预处理 (Efficient Data Pre-processing)**：为公共数据集以及本地存储的 CSV、JSON、JSONL、Parquet、HDF5、XML、纯文本、PNG、JPEG、WAV、MP3、PDF、NIfTI 等格式数据提供简洁、高效且可复现的预处理能力。借助如 `processed_dataset = dataset.map(process_example)` 的直观命令，高效准备好数据集以供检查分析、ML 模型评估和训练。

[🎓 **官方文档**](https://huggingface.co/docs/datasets/) [🔎 **在 Hub 中发现数据集**](https://huggingface.co/datasets) [🌟 **在 Hub 上分享数据集**](https://huggingface.co/docs/datasets/share)

<h3 align="center">
    <a href="https://hf.co/course"><img src="https://raw.githubusercontent.com/huggingface/datasets/main/docs/source/imgs/course_banner.png"></a>
</h3>

# 🚀 核心特性

🤗 Datasets 旨在让社区能够轻松添加并分享新数据集，同时为大规模数据清洗与特征工程提供强大的操作能力：

| 特性 | 说明 |
|---------|-------------|
| 📦 **一行代码加载数据集** | 借助 `load_dataset()` 从 [Hugging Face Hub](https://huggingface.co/datasets) 或本地文件快速加载即取即用的 AI 数据集 |
| 🔍 **多样化数据格式支持** | 原生支持 CSV、JSON、JSONL、Parquet、Arrow、XML、Text、WebDataset 等多种主流格式 |
| 🖼️ **多模态数据原生支持** | 开箱即用支持文本 (Text)、音频 (Audio)、图像 (Image)、视频 (Video)、PDF 文档以及 NIfTI (3D 医学影像) 数据 |
| 🚀 **流式加载模式 (Streaming)** | 无需完整下载即可流式加载海量数据集 —— 使用 `streaming=True` 实时迭代数据（借助 Xet 后端最高提速 **100倍**） |
| 💾 **HF 存储桶 (Storage Buckets)** | 直接读写 [Hugging Face Storage Buckets](https://huggingface.co/docs/hub/storage-buckets)，适用于可变、海量规模的原始数据存储 |
| 🧠 **AI Agent 轨迹数据** | 从 Hub 直接加载和处理 AI Agent 交互轨迹数据（Prompt、工具调用、响应回复等） |
| ⚡ **Apache Arrow 后端** | 零拷贝（Zero-copy）内存映射存储 —— 数据集处理天然摆脱物理内存 (RAM) 容量限制 |
| 🔄 **智能缓存机制** | 无需等待数据重复计算 —— 历史处理结果自动缓存并智能复用 |
| 📊 **多框架无缝互操作** | 原生支持与 NumPy、Pandas、Polars、Arrow、PyTorch、TensorFlow、JAX 和 Spark 互相转换 |
| 🏎️ **多进程并行加速** | 使用 `map(num_proc=N)` 开启高速多进程并行数据处理 |
| 🔎 **搜索与向量索引** | 内置集成 FAISS 与 Elasticsearch 索引，轻松实现密集向量相似度检索与全文搜索 |
| 📦 **灵活的 JSON 类型** | 通过 `Json()` 特征类型提供灵活的 JSON / 结构化复杂数据支持 |

# 安装

## 使用 pip

🤗 Datasets 可从 PyPI 安装，建议在虚拟环境中（如 venv 或 conda）进行安装：

```bash
pip install datasets
```

如需体验最新的开发版本：

```bash
pip install "datasets @ git+https://github.com/huggingface/datasets.git"
```

## 使用 conda

```bash
conda install -c huggingface -c conda-forge datasets
```

## 可选扩展依赖

🤗 Datasets 通过 extras 支持各类丰富可选功能：

```bash
# 音频处理支持 (torchcodec)
pip install datasets[audio]

# 图像/视频处理支持 (Pillow, torchcodec)
pip install datasets[vision]

# PDF 与 NIfTI 医疗影像支持 (pdfplumber, nibabel)
pip install datasets[pdfs,nibabel]

# PyTorch / TensorFlow / JAX 深度学习框架集成
pip install datasets[torch,tensorflow,jax]
```

更多安装细节请参阅[官方安装指南](https://huggingface.co/docs/datasets/installation)。

# 快速上手

🤗 Datasets 的使用极其简洁直观 —— 其核心 API 围绕单个函数 `datasets.load_dataset(dataset_name, **kwargs)` 展开，用于快速实例化数据集。

以下是一个快速入门示例：

```python
from datasets import load_dataset

# 加载数据集并打印训练集中的第一个样本
squad_dataset = load_dataset('rajpurkar/squad')
print(squad_dataset['train'][0])

# 处理数据集 —— 为每个样本添加 context 上下文文本的字符长度列
dataset_with_length = squad_dataset.map(lambda x: {"length": len(x["context"])})

# 对 context 文本进行分词 (使用 🤗 Transformers 库中的分词器)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

tokenized_dataset = squad_dataset.map(lambda x: tokenizer(x['context']), batched=True)

# 使用对话模板 (Chat Template) 对聊天会话进行分词 (适用于支持聊天模板的模型)
# 这在微调指令/对话模型时非常有用

# 加载热门的对话数据集 (ultrachat_200k 包含约 20 万条 AI 助手对话)
chat_dataset = load_dataset('HuggingFaceH4/ultrachat_200k', split='train_sft')

chat_tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-7B-Instruct')

def tokenize_chat(examples):
    # 一步应用对话模板并完成分词
    return chat_tokenizer.apply_chat_template(examples["messages"])

tokenized_chat_dataset = chat_dataset.map(tokenize_chat, batched=True)
```

## 流式加载模式 (Streaming)

如果数据集体积超过磁盘容量，或者你不想等待漫长的下载过程，可以使用流式模式：

```python
# 无需完整下载即可流式迭代数据集
image_dataset = load_dataset('timm/imagenet-1k-wds', streaming=True)
for example in image_dataset["train"]:
    print(example["image"])
    break
```

## 多模态数据支持

🤗 Datasets 开箱即用支持多种模态的数据类型：

```python
# 音频数据集
dataset = load_dataset("openslr/librispeech_asr", "clean")

# 图像数据集
dataset = load_dataset("ILSVRC/imagenet-1k")

# 视频数据集
dataset = load_dataset("Shofo/shofo-tiktok-general-small")

# PDF 文档数据集
dataset = load_dataset("pixparse/pdfa-eng-wds")

# NIfTI (3D 医学影像)
dataset = load_dataset("dartbrains/localizer", "betas")
```

## 从本地文件加载

```python
# 从本地 CSV 文件加载
dataset = load_dataset('csv', data_files='my_data.csv')

# 从本地 Parquet 文件加载
dataset = load_dataset('parquet', data_files='data/*.parquet')

# 从本地目录加载 (自动检测数据格式)
dataset = load_dataset('./path/to/data')
```

## 从 Python 对象构建

```python
from datasets import Dataset

# 从字典构建
dataset = Dataset.from_dict({"text": ["Hello world", "How are you?"]})

# 从列表构建
dataset = Dataset.from_list([{"text": "Hello world"}, {"text": "How are you?"}])

# 从 Pandas DataFrame 构建
import pandas as pd
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
dataset = Dataset.from_pandas(df)

# 从生成器 (Generator) 构建
def gen():
    for i in range(10):
        yield {"value": i}
dataset = Dataset.from_generator(gen)
```

有关库的更多使用细节，请参阅[快速入门指南](https://huggingface.co/docs/datasets/quickstart)以及以下专题文档：

- [加载数据集 (Loading a dataset)](https://huggingface.co/docs/datasets/loading)
- [数据集内部结构与访问 (What's in a Dataset)](https://huggingface.co/docs/datasets/access)
- [使用 🤗 Datasets 处理数据 (Processing data with 🤗 Datasets)](https://huggingface.co/docs/datasets/process)
  - [处理音频数据 (Processing audio data)](https://huggingface.co/docs/datasets/audio_process)
  - [处理图像数据 (Processing image data)](https://huggingface.co/docs/datasets/image_process)
  - [处理文本数据 (Processing text data)](https://huggingface.co/docs/datasets/nlp_process)
  - [处理 PDF 文档 (Processing PDF data)](https://huggingface.co/docs/datasets/pdf_process)
  - [处理视频数据 (Processing video data)](https://huggingface.co/docs/datasets/video_process)
- [流式加载数据集 (Streaming a dataset)](https://huggingface.co/docs/datasets/stream)

# 核心数据类 (Core Classes)

本库提供两个主要的数据集类：

| 类名 | 说明 |
|-------|-------------|
| `Dataset` | 基于 Apache Arrow 的内存/内存映射数据集。原生支持按索引切片、随机访问以及智能缓存。 |
| `IterableDataset` | 面向超大规模或核外（Out-of-core）处理的惰性流式数据集。支持流式传输与无限迭代。 |

两者均支持通过 `DatasetDict` / `IterableDatasetDict` 进行包装，用于管理包含多个切分划分（如 train/test/validation）的数据集。

# 向 Hub 添加新数据集

我们为向 [HuggingFace Datasets Hub](https://huggingface.co/datasets) 上贡献新数据集准备了详尽的步骤指南。

你可以了解：
- [如何通过网页浏览器或 Python 脚本上传数据集到 Hub](https://huggingface.co/docs/datasets/upload_dataset) 以及
- [如何使用 Git 上传数据集](https://huggingface.co/docs/datasets/share)。

# 免责声明与注意事项

你可以使用 🤗 Datasets 加载由数据集创作者维护的版本化 Git 仓库中的数据集。出于实验可复现性考虑，建议用户在生产与科研环境中明确锁定所使用仓库的 `revision` 版本。

如果你是数据集所有者，希望更新任何信息（描述、引用、许可证等），或者不希望你的数据集被包含在 Hugging Face Hub 中，请在数据集页面的 Community 选项卡中发起 Discussion 或 Pull Request 与我们取得联系。非常感谢你对开源机器学习社区的贡献！

# 参与贡献

我们非常欢迎来自社区的贡献！请阅读我们的[贡献指南 (Contributing Guide)](CONTRIBUTING.md) 了解详细规范：

- 如何提交 Issue 与 Pull Request
- 代码风格规范（使用 [Ruff](https://docs.astral.sh/ruff/)）
- 测试要求
- 文档标准

# BibTeX 引用

如果你希望在学术研究中引用 🤗 Datasets 库，可以使用我们的[论文](https://huggingface.co/papers/2109.02846)：

```bibtex
@inproceedings{lhoest-etal-2021-datasets,
    title = "Datasets: A Community Library for Natural Language Processing",
    author = "Lhoest, Quentin  and
      Villanova del Moral, Albert  and
      Jernite, Yacine  and
      Thakur, Abhishek  and
      von Platen, Patrick  and
      Patil, Suraj  and
      Chaumond, Julien  and
      Drame, Mariama  and
      Plu, Julien  and
      Tunstall, Lewis  and
      Davison, Joe  and
      {\v{S}}a{\v{s}}ko, Mario  and
      Chhablani, Gunjan  and
      Malik, Bhavitvya  and
      Brandeis, Simon  and
      Le Scao, Teven  and
      Sanh, Victor  and
      Xu, Canwen  and
      Patry, Nicolas  and
      McMillan-Major, Angelina  and
      Schmid, Philipp  and
      Gugger, Sylvain  and
      Delangue, Cl{\'e}ment  and
      Matussi{\`e}re, Th{\'e}o  and
      Debut, Lysandre  and
      Bekman, Stas  and
      Cistac, Pierric  and
      Goehringer, Thibault  and
      Mustar, Victor  and
      Lagunas, Fran{\c{c}}ois  and
      Rush, Alexander  and
      Wolf, Thomas",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-demo.21",
    pages = "175--184",
    abstract = "The scale, variety, and quantity of publicly-available NLP datasets has grown rapidly as researchers propose new tasks, larger models, and novel benchmarks. Datasets is a community library for contemporary NLP designed to support this ecosystem. Datasets aims to standardize end-user interfaces, versioning, and documentation, while providing a lightweight front-end that behaves similarly for small datasets as for internet-scale corpora. The design of the library incorporates a distributed, community-driven approach to adding datasets and documenting usage. After a year of development, the library now includes more than 650 unique datasets, has more than 250 contributors, and has helped support a variety of novel cross-dataset research projects and shared tasks. The library is available at https://github.com/huggingface/datasets.",
    eprint={2109.02846},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
}
```

如需针对特定发布版本进行学术复现引用，可从该 [Zenodo 列表](https://zenodo.org/search?q=conceptrecid:%224817768%22&sort=-version&all_versions=True) 中获取对应版本的 DOI。

---

> 💡 **文档维护说明**：本中文文档由社区志愿者（[@JasonYeYuhe](https://github.com/JasonYeYuhe)）翻译维护，最后同步更新于 2026年9月6日。如发现内容与官方英文原版存在差异或新特性滞后，欢迎提交 PR 共同完善！
