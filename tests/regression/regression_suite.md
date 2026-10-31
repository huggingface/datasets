# `datasets` Regression Test Suite

**Target repository:** `huggingface/datasets`
**Author:** QA Engineering
**Date:** 2026-06-29
**Scope source:** `qa_brief.yaml`

---

## 1. Overview

This document defines a manual/semi-automated regression test suite for the Hugging Face
`datasets` library. It was built by:

1. **Mining historical issue data** (`github-bug-reports-and-issues.jsonl`) — a snapshot of
   **984 issues** (3019 records incl. 2035 PRs) for `huggingface/datasets`, spanning
   **2020-04 → 2021-09**, to find the bug categories that *keep repeating*.
2. **Cross-checking the live repository** via the GitHub Search API (June 2026) to confirm
   which of those categories are *still* generating open issues today (current issue numbers
   reach **#8269**), and to surface coverage gaps.
3. **Mapping the result onto the `qa_brief.yaml` focus areas** to produce a prioritized suite
   split into a **30-minute smoke pass** and a **180-minute full regression run** with a
   minimum of **120 test cases** (this suite contains **128**).

### 1.1 Budgets & constraints (from `qa_brief.yaml`)

| Constraint | Value |
|---|---|
| Smoke pass budget | 30 minutes |
| Full regression budget | 180 minutes |
| Minimum test cases | 120 (**this suite: 128**) |
| Priority labels | `bug`, `regression`, `streaming`, `cache`, `arrow`, `data-loading`, `critical`, `flaky` |

### 1.2 Focus areas (from `qa_brief.yaml`)

`data loading` · `streaming` · `caching` · `arrow serialization` ·
`dataset splits and slicing` · `map and filter transformations` ·
`multiprocessing and parallelism` · `trust_remote_code handling`

---

## 2. Data-driven category analysis

### 2.1 Historical bug volume by category (984 issues, 2020-04 → 2021-09)

Issues were classified by keyword/label matching against the focus areas. An issue may match
more than one category (e.g. a `num_proc` crash inside `.map()` counts under both
*map/filter* and *multiprocessing*), so column totals exceed 984.

| Rank | Category | Total issues | Open (snapshot) | Closed | % of issues |
|---|---|---:|---:|---:|---:|
| 1 | Data loading | 472 | 147 | 325 | 48% |
| 2 | Caching | 287 | 77 | 210 | 29% |
| 3 | Splits & slicing | 282 | 89 | 193 | 29% |
| 4 | Arrow serialization | 253 | 78 | 175 | 26% |
| 5 | Encoding/decoding (features) | 239 | 85 | 154 | 24% |
| 6 | Map & filter | 220 | 63 | 157 | 22% |
| 7 | Multiprocessing & parallelism | 153 | 46 | 107 | 16% |
| 8 | Memory / OOM | 49 | 20 | 29 | 5% |
| 9 | Streaming | 40 | 22 | 18 | 4% |

**Reading the table:** Historically, **data loading** is by far the single largest driver of
bugs (~half of all issues touch it), followed by a tight cluster of **caching, splits/slicing,
and arrow serialization**. Streaming had *low absolute volume* in 2020-21 — but note it was a
*new feature* then, which is the classic profile of a category that grows later (see §2.2).

### 2.2 Live cross-check — currently open issues (GitHub Search API, June 2026)

Queried directly against `repo:huggingface/datasets is:issue is:open`. Current data
(issue numbers up to #8269) confirms the historical categories are still active.

| Category (live query) | Open issues now | Representative current issue |
|---|---:|---|
| **All open issues** | **893** | — |
| **All open `label:bug`** | **97** | #7037 `Dataset.to_json()` bug; #6937 JSON loader coerces floats→ints |
| Splits & slicing | 332 | #8269 MetadataConfigs drops parquet shards; #4526 split cache reused across splits |
| Map & filter | 237 | #5870 `map` behaviour differs Dataset vs IterableDataset; #6787 `TimeoutError in map` |
| Multiprocessing | 127 | #6936 `save_to_disk()` freezes on s3 with multiprocessing; #6357 pass mp context |
| trust_remote_code | 36 | #7723 "Don't remove `trust_remote_code`!"; #7692 xopen invalid start byte w/ streaming + remote code |

> **Note on `data loading`, `caching`, `arrow`, `streaming` live counts:** the live search
> queries for these four returned successfully but their issue bodies contained control
> characters that broke strict JSON parsing during collection, so exact live counts are not
> quoted here. Given they are the top historical categories and the library's core surface,
> they are treated as **high priority** regardless. This is flagged as a known data-collection
> limitation, not an assumption that they are low-risk.

### 2.3 Key findings

1. **Data loading is the #1 historical bug driver (48% of issues)** and remains the core
   surface of the library — it gets the largest share of test cases.
2. **The 2020-21 patterns persist in 2026.** `num_proc` hangs/freezes (#6936), `map`
   semantics (#5870, #6787), splits/sharding (#8269, #4526), and serialization (#7037, #6937)
   are *still* open. The historical suite design is therefore still valid.
3. **`trust_remote_code` is a newer, contentious surface** (36 open, incl. #7723/#7692). It
   barely registered historically because the argument did not exist in 2020-21 — a clear
   **coverage gap** that this suite explicitly fills (see §3 TC-TRC-*).
4. **Streaming is under-represented historically but high-growth.** Low 2020-21 volume + an
   actively maturing feature ⇒ we deliberately *over-weight* streaming relative to its
   historical count to avoid a coverage gap.

### 2.4 Coverage-gap summary

| Gap | Evidence | Suite response |
|---|---|---|
| `trust_remote_code` security/behaviour | Did not exist in 2020-21 snapshot; 36 open today | New dedicated section TC-TRC-01..10 |
| Streaming maturity | Only 40 historical issues but feature still growing; #7692 ties streaming+remote code | Over-weighted: TC-STR-01..18 |
| Multiprocessing hangs/freezes | #6936 (s3 freeze), #6357 still open; classic flaky class | Dedicated flaky-tagged section TC-MP-01..14 |
| Cross-cutting "behaviour differs by mode" | #5870 (map differs Dataset vs Iterable), #2923/#2866 (errors differ streaming vs normal) | Parity test cases TC-XCUT-* |

---

## 3. Test suite structure & conventions

### 3.1 Test case ID scheme

`TC-<AREA>-<NN>` — area codes:

| Code | Area |
|---|---|
| `DL` | Data loading |
| `STR` | Streaming |
| `CACHE` | Caching |
| `ARROW` | Arrow serialization |
| `SPLIT` | Splits & slicing |
| `MAP` | Map & filter transformations |
| `MP` | Multiprocessing & parallelism |
| `TRC` | trust_remote_code handling |
| `XCUT` | Cross-cutting / parity |

### 3.2 Priority levels

- **P0 – Critical:** core paths; failure blocks release. All P0 cases are in the smoke pass.
- **P1 – High:** common real-world usage; in full regression, selected ones in smoke.
- **P2 – Medium:** edge cases / less-common configurations; full regression only.

### 3.3 Tag legend

Tags map to `qa_brief.yaml` `priority_labels`: `bug`, `regression`, `streaming`, `cache`,
`arrow`, `data-loading`, `critical`, `flaky`.

### 3.4 Standard preconditions (apply to all cases unless overridden)

- **ENV-1:** Clean Python venv with a single pinned `datasets` version under test, plus
  `pyarrow`, `pandas`, `numpy`.
- **ENV-2:** Cache dir reset before each case: `HF_DATASETS_CACHE` pointed at an empty temp
  directory (prevents stale-cache cross-talk; see TC-CACHE-*).
- **ENV-3:** Network available for hub-backed cases; offline cases set `HF_DATASETS_OFFLINE=1`.
- **ENV-4:** Fixtures (small local CSV/JSON/Parquet/text files and a tiny loading script)
  staged under `./fixtures/`.

### 3.5 Test-run profiles

| Profile | Budget | Cases | Selection rule |
|---|---|---|---|
| **Smoke** | 30 min | **24** P0 cases | One or two canary cases per focus area; happy paths + top regressions only |
| **Full regression** | 180 min | **128** (all) | Every case below |

---

## 4. Smoke pass (P0, ≤30 min, 24 cases)

Run in this order; abort the release pipeline on any failure.

| # | TC ID | Area | Title |
|---|---|---|---|
| 1 | TC-DL-01 | Data loading | Load a Hub dataset by name (happy path) |
| 2 | TC-DL-02 | Data loading | Load local CSV via `load_dataset("csv", ...)` |
| 3 | TC-DL-03 | Data loading | Load local JSON / JSONL |
| 4 | TC-DL-05 | Data loading | `load_dataset` with explicit `split=` |
| 5 | TC-DL-09 | Data loading | Checksum / split-size verification passes |
| 6 | TC-STR-01 | Streaming | `streaming=True` returns an `IterableDataset` and iterates |
| 7 | TC-STR-03 | Streaming | Streamed vs non-streamed first-row parity |
| 8 | TC-CACHE-01 | Caching | Second load reuses cache (no re-download) |
| 9 | TC-CACHE-04 | Caching | `download_mode="force_redownload"` bypasses cache |
| 10 | TC-ARROW-01 | Arrow | Round-trip `save_to_disk` / `load_from_disk` |
| 11 | TC-ARROW-03 | Arrow | Load Parquet file preserves schema |
| 12 | TC-SPLIT-01 | Splits | `train_test_split` produces non-empty splits |
| 13 | TC-SPLIT-04 | Splits | Percentage slicing `split="train[:10%]"` |
| 14 | TC-SPLIT-07 | Splits | `select()` returns rows and supports `.shape` |
| 15 | TC-MAP-01 | Map/filter | `map()` adds a column (single process) |
| 16 | TC-MAP-04 | Map/filter | `filter()` returns correct subset |
| 17 | TC-MAP-07 | Map/filter | `map(batched=True)` happy path |
| 18 | TC-MP-01 | Multiprocessing | `map(num_proc=4)` completes & matches single-proc |
| 19 | TC-MP-05 | Multiprocessing | `filter(num_proc>1)` completes without hang |
| 20 | TC-TRC-01 | trust_remote_code | Script dataset blocked without `trust_remote_code` |
| 21 | TC-TRC-02 | trust_remote_code | Script dataset loads with `trust_remote_code=True` |
| 22 | TC-XCUT-01 | Cross-cutting | Same dataset loads in normal AND streaming mode |
| 23 | TC-ARROW-06 | Arrow | `to_pandas()` / `to_dict()` round-trip values |
| 24 | TC-DL-12 | Data loading | Offline mode loads already-cached dataset |

---

## 5. Full regression test cases

> Format for each case: **Priority · Tags · Preconditions · Steps · Expected results.**
> `[SMOKE]` marks cases also in the 30-minute pass.

### 5.1 Data loading (TC-DL) — *largest category: 48% of historical bugs*

---

#### TC-DL-01 — Load a Hub dataset by name (happy path) `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading, critical
- **Preconditions:** ENV-1..4; network up; pick a small canonical dataset (e.g. `rotten_tomatoes`).
- **Steps:**
  1. Call `load_dataset("rotten_tomatoes")`.
  2. Inspect the returned object type and keys.
  3. Read `ds["train"][0]`.
- **Expected:** Returns a `DatasetDict` with `train`/`validation`/`test`; each is a `Dataset`;
  first row is a dict with the documented features; no exception.

#### TC-DL-02 — Load local CSV `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading
- **Preconditions:** `./fixtures/data.csv` with header + ≥3 rows.
- **Steps:**
  1. `load_dataset("csv", data_files="./fixtures/data.csv")`.
  2. Check `ds["train"].column_names` and row count.
- **Expected:** Columns match CSV header; row count equals data rows; dtypes inferred correctly.

#### TC-DL-03 — Load local JSON / JSONL `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading
- **Preconditions:** `./fixtures/data.jsonl` (one JSON object per line).
- **Steps:**
  1. `load_dataset("json", data_files="./fixtures/data.jsonl")`.
  2. Verify nested fields are preserved.
- **Expected:** Loads without `ArrowInvalid`; nested structures preserved; counts correct.

#### TC-DL-04 — JSON numeric type coercion (regression of #6937)
- **Priority:** P1 · **Tags:** data-loading, bug, regression
- **Preconditions:** JSONL where a field has mixed `1`, `2.5` values.
- **Steps:**
  1. Load with the JSON builder.
  2. Inspect the resolved feature dtype and the actual loaded values.
- **Expected:** Floats are NOT silently coerced to integers; the value `2.5` is preserved
  (guards regression #6937).

#### TC-DL-05 — `load_dataset` with explicit `split=` `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading
- **Preconditions:** ENV; dataset with multiple splits.
- **Steps:**
  1. `load_dataset(name, split="train")`.
  2. Confirm a single `Dataset` (not a `DatasetDict`) is returned.
- **Expected:** Returns `Dataset` object for the requested split only.

#### TC-DL-06 — Load multiple `data_files` mapped to splits
- **Priority:** P1 · **Tags:** data-loading
- **Preconditions:** `train.csv`, `test.csv` fixtures.
- **Steps:**
  1. `load_dataset("csv", data_files={"train":"train.csv","test":"test.csv"})`.
- **Expected:** `DatasetDict` with exactly `train` and `test`; correct per-split counts.

#### TC-DL-07 — Load with a named config / subset
- **Priority:** P1 · **Tags:** data-loading
- **Preconditions:** A dataset exposing multiple configs (e.g. `glue`, config `mrpc`).
- **Steps:**
  1. `load_dataset("glue", "mrpc")`.
- **Expected:** Correct config-specific features and splits load.

#### TC-DL-08 — Missing config raises actionable error
- **Priority:** P2 · **Tags:** data-loading
- **Preconditions:** Multi-config dataset.
- **Steps:**
  1. Call `load_dataset` with a non-existent config name.
- **Expected:** Raises `ValueError` listing available configs; message is human-readable.

#### TC-DL-09 — Checksum / split-size verification passes `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading, critical, regression
- **Preconditions:** A dataset with recorded `dataset_infos`/metadata.
- **Steps:**
  1. Load the dataset normally.
  2. Observe verification of number of examples and checksums.
- **Expected:** No `NonMatchingSplitsSizesError` / `NonMatchingChecksumError` on a healthy
  dataset (guards regression class #2941, #2882).

#### TC-DL-10 — `verification_mode="no_checks"` skips verification
- **Priority:** P2 · **Tags:** data-loading
- **Preconditions:** Dataset whose recorded sizes intentionally mismatch (fixture).
- **Steps:**
  1. Load with `verification_mode="no_checks"`.
- **Expected:** Load succeeds without raising; documents the escape hatch behaviour.

#### TC-DL-11 — Load Parquet directly
- **Priority:** P1 · **Tags:** data-loading, arrow
- **Preconditions:** `./fixtures/data.parquet`.
- **Steps:**
  1. `load_dataset("parquet", data_files="./fixtures/data.parquet")`.
- **Expected:** Schema and values preserved; no exception.

#### TC-DL-12 — Offline mode loads cached dataset `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading, cache
- **Preconditions:** Dataset previously loaded into cache; then set `HF_DATASETS_OFFLINE=1`.
- **Steps:**
  1. Re-run `load_dataset(name)` with offline flag set.
- **Expected:** Loads from cache with no network call; no hang/timeout.

#### TC-DL-13 — Offline mode without cache fails fast
- **Priority:** P2 · **Tags:** data-loading
- **Preconditions:** Empty cache; `HF_DATASETS_OFFLINE=1`.
- **Steps:**
  1. Attempt to load an uncached dataset.
- **Expected:** Raises a clear offline error promptly (no long network retry/hang).

#### TC-DL-14 — Load text file dataset
- **Priority:** P1 · **Tags:** data-loading
- **Preconditions:** `./fixtures/corpus.txt`.
- **Steps:**
  1. `load_dataset("text", data_files="./fixtures/corpus.txt")`.
- **Expected:** One row per line; `text` column present.

#### TC-DL-15 — Load from in-memory pandas / dict
- **Priority:** P1 · **Tags:** data-loading
- **Steps:**
  1. `Dataset.from_pandas(df)` and `Dataset.from_dict({...})`.
- **Expected:** Correct features inferred; counts match the source.

#### TC-DL-16 — `pathlib.Path` accepted for paths (regression of #6829)
- **Priority:** P1 · **Tags:** data-loading, bug, regression
- **Preconditions:** Fixture path as a `pathlib.Path`.
- **Steps:**
  1. Pass a `Path` object to `load_dataset(..., data_files=Path(...))` and to `save_to_disk`.
- **Expected:** `Path` objects accepted (guards regression #6829, where Path stopped working).

#### TC-DL-17 — gzip / compressed content decoding (regression of #2918)
- **Priority:** P2 · **Tags:** data-loading, bug
- **Preconditions:** gzip-compressed JSON/CSV fixture.
- **Steps:**
  1. Load the compressed file.
- **Expected:** Decompresses and loads correctly; no "Can not decode content-encoding: gzip".

#### TC-DL-18 — `data_dir` directory globbing
- **Priority:** P2 · **Tags:** data-loading
- **Preconditions:** Directory of multiple CSVs.
- **Steps:**
  1. `load_dataset("csv", data_dir="./fixtures/csvs/")`.
- **Expected:** All matching files concatenated into one dataset; total count correct.

### 5.2 Streaming (TC-STR) — *over-weighted: high-growth, gap-filled*

---

#### TC-STR-01 — `streaming=True` yields `IterableDataset` `[SMOKE]`
- **Priority:** P0 · **Tags:** streaming, critical
- **Steps:**
  1. `load_dataset(name, split="train", streaming=True)`.
  2. `next(iter(ds))`.
- **Expected:** Object is an `IterableDataset`; first element is a feature dict; no full download.

#### TC-STR-02 — Streaming local files
- **Priority:** P1 · **Tags:** streaming, data-loading
- **Steps:**
  1. Stream a local CSV/JSON fixture with `streaming=True`.
- **Expected:** Iterates rows lazily; values correct.

#### TC-STR-03 — Streamed vs non-streamed first-row parity `[SMOKE]`
- **Priority:** P0 · **Tags:** streaming, regression
- **Steps:**
  1. Load dataset normally and streaming.
  2. Compare first N rows.
- **Expected:** Identical content and feature schema between modes (guards #2923/#2866 class).

#### TC-STR-04 — `IterableDataset.map()` lazy transform
- **Priority:** P1 · **Tags:** streaming, map
- **Steps:**
  1. Apply `.map(fn)` to a streamed dataset; iterate.
- **Expected:** Transform applied lazily per element; result matches eager `.map`.

#### TC-STR-05 — `IterableDataset.filter()`
- **Priority:** P1 · **Tags:** streaming, map
- **Steps:**
  1. `.filter(pred)` on streamed dataset; iterate.
- **Expected:** Only matching rows yielded.

#### TC-STR-06 — `remove_columns` on `IterableDataset` (regression of #2944)
- **Priority:** P1 · **Tags:** streaming, regression
- **Steps:**
  1. `streamed.remove_columns([...])`; iterate.
- **Expected:** Listed columns absent from yielded rows (feature added in #2944).

#### TC-STR-07 — `take()` / `skip()` on streamed dataset
- **Priority:** P1 · **Tags:** streaming
- **Steps:**
  1. `ds.take(5)` and `ds.skip(5)`; iterate both.
- **Expected:** `take` yields first 5; `skip` yields from the 6th onward; no overlap.

#### TC-STR-08 — Streaming `shuffle(buffer_size=...)`
- **Priority:** P2 · **Tags:** streaming, flaky
- **Steps:**
  1. `ds.shuffle(seed=42, buffer_size=100)`; iterate.
- **Expected:** Order differs from unshuffled; with fixed seed the order is reproducible.

#### TC-STR-09 — Stream sharded dataset across files
- **Priority:** P2 · **Tags:** streaming
- **Steps:**
  1. Stream a multi-shard dataset.
- **Expected:** All shards traversed; total iterated count equals sum of shard counts.

#### TC-STR-10 — Convert streamed → `torch` iterable for DataLoader
- **Priority:** P2 · **Tags:** streaming
- **Steps:**
  1. `ds.with_format("torch")`; wrap in a `torch.utils.data.DataLoader`.
- **Expected:** Batches yield tensors; no crash.

#### TC-STR-11 — Streaming respects `features=` override
- **Priority:** P2 · **Tags:** streaming, arrow
- **Steps:**
  1. Stream with an explicit `Features` schema.
- **Expected:** Yielded rows cast to the declared schema.

#### TC-STR-12 — Streaming over gzip/remote compressed shards
- **Priority:** P2 · **Tags:** streaming, bug
- **Steps:**
  1. Stream a gzip-compressed remote/​local shard.
- **Expected:** Transparent decompression; rows correct (relates to #2918).

#### TC-STR-13 — Streamed `IterableDatasetDict` per-split access
- **Priority:** P2 · **Tags:** streaming
- **Steps:**
  1. `load_dataset(name, streaming=True)` (no split); access `["train"]`.
- **Expected:** Returns `IterableDatasetDict`; each split iterable independently.

#### TC-STR-14 — `rename_column` on streamed dataset
- **Priority:** P2 · **Tags:** streaming
- **Steps:**
  1. `streamed.rename_column("a","b")`; iterate.
- **Expected:** Column renamed in yielded rows.

#### TC-STR-15 — `cast_column` on streamed dataset
- **Priority:** P2 · **Tags:** streaming, arrow
- **Steps:**
  1. `streamed.cast_column("label", ClassLabel(...))`; iterate.
- **Expected:** Values cast lazily; no error.

#### TC-STR-16 — Interrupt/resume streaming iteration
- **Priority:** P2 · **Tags:** streaming, flaky
- **Steps:**
  1. Begin iterating, stop after K, create a fresh iterator.
- **Expected:** Fresh iterator restarts from the beginning deterministically.

#### TC-STR-17 — Streaming + `trust_remote_code` script dataset (regression of #7692)
- **Priority:** P1 · **Tags:** streaming, bug, regression
- **Preconditions:** A script-based dataset that supports streaming.
- **Steps:**
  1. `load_dataset(script, streaming=True, trust_remote_code=True)`; iterate.
- **Expected:** Streams without "invalid start byte"/decode error (guards #7692).

#### TC-STR-18 — Empty streamed dataset handled
- **Priority:** P2 · **Tags:** streaming
- **Steps:**
  1. Stream a dataset/filter that yields zero rows.
- **Expected:** Iterator simply ends; no exception.

### 5.3 Caching (TC-CACHE) — *2nd largest: 29% of historical bugs*

---

#### TC-CACHE-01 — Second load reuses cache `[SMOKE]`
- **Priority:** P0 · **Tags:** cache, critical
- **Steps:**
  1. Load dataset (cold). 2. Load again (warm), timing both.
- **Expected:** Second load reads from cache (no re-download); markedly faster.

#### TC-CACHE-02 — Cache survives across processes
- **Priority:** P1 · **Tags:** cache
- **Steps:**
  1. Load in process A; load again in a fresh process B (same `HF_DATASETS_CACHE`).
- **Expected:** Process B reuses the cache produced by A.

#### TC-CACHE-03 — Distinct `cache_dir` isolates caches
- **Priority:** P1 · **Tags:** cache
- **Steps:**
  1. Load with `cache_dir=A`, then `cache_dir=B`.
- **Expected:** Two independent cache trees; neither pollutes the other.

#### TC-CACHE-04 — `force_redownload` bypasses cache `[SMOKE]`
- **Priority:** P0 · **Tags:** cache, regression
- **Steps:**
  1. Load (cache populated). 2. Load with `download_mode="force_redownload"`.
- **Expected:** Data re-downloaded/re-prepared; works as documented (guards FORCE_REDOWNLOAD #2904).

#### TC-CACHE-05 — `reuse_dataset_if_exists` default
- **Priority:** P1 · **Tags:** cache
- **Steps:**
  1. Load twice with default download mode.
- **Expected:** Prepared dataset reused; no rebuild.

#### TC-CACHE-06 — Cache reused after moving cache directory (regression of #2496)
- **Priority:** P1 · **Tags:** cache, bug, regression
- **Steps:**
  1. Build cache in dir A. 2. Move dir A → dir B; point `HF_DATASETS_CACHE` to B. 3. Reload.
- **Expected:** Cache still valid (fingerprint not invalidated by path change) — guards #2496.

#### TC-CACHE-07 — `map` results cached and reused
- **Priority:** P1 · **Tags:** cache, map
- **Steps:**
  1. Run `.map(fn)`; re-run identical `.map(fn)`.
- **Expected:** Second run loads cached arrow file (fingerprint match); function not re-executed.

#### TC-CACHE-08 — Different `map` fn ⇒ new cache (fingerprint changes)
- **Priority:** P1 · **Tags:** cache, map
- **Steps:**
  1. `.map(fn1)` then `.map(fn2)` (different logic).
- **Expected:** Distinct fingerprints; fn2 actually executed (no stale reuse).

#### TC-CACHE-09 — `load_from_cache_file=False` forces recompute
- **Priority:** P2 · **Tags:** cache, map
- **Steps:**
  1. `.map(fn, load_from_cache_file=False)` twice.
- **Expected:** Function re-runs both times.

#### TC-CACHE-10 — Deterministic fingerprint across runs (regression of #2775)
- **Priority:** P2 · **Tags:** cache, flaky, regression
- **Steps:**
  1. In two fresh processes, build the same dataset+map; compare `_fingerprint`.
- **Expected:** Fingerprints identical & deterministic (guards #2775 non-deterministic fingerprint).

#### TC-CACHE-11 — `cleanup_cache_files()` removes stale files
- **Priority:** P2 · **Tags:** cache
- **Steps:**
  1. Generate several cached map files; call `ds.cleanup_cache_files()`.
- **Expected:** Returns count removed; stale files deleted; current dataset still usable.

#### TC-CACHE-12 — Windows-style path / permission handling (regression of #2937)
- **Priority:** P2 · **Tags:** cache, bug
- **Preconditions:** Run on Windows or simulate locked-file scenario.
- **Steps:**
  1. Load dataset to default cache; ensure temp files are released.
- **Expected:** No `PermissionError` on cache files (guards #2937, #2471).

#### TC-CACHE-13 — Per-split cache isolation (regression of #4526)
- **Priority:** P1 · **Tags:** cache, split, bug, regression
- **Steps:**
  1. Process `train` split with `.map`; then process `test` split with same fn.
- **Expected:** `test` is NOT served the `train` cache; outputs differ correctly (guards #4526).

#### TC-CACHE-14 — Disk-space / cache growth sanity (relates to #2591)
- **Priority:** P2 · **Tags:** cache, flaky
- **Steps:**
  1. Run repeated `.map` operations; monitor cache dir size.
- **Expected:** No unbounded growth from a single repeated identical op (cache reused, not duplicated).

### 5.4 Arrow serialization (TC-ARROW) — *26% of historical bugs*

---

#### TC-ARROW-01 — `save_to_disk` / `load_from_disk` round-trip `[SMOKE]`
- **Priority:** P0 · **Tags:** arrow, critical
- **Steps:**
  1. `ds.save_to_disk(path)`; 2. `load_from_disk(path)`; 3. compare.
- **Expected:** Loaded dataset equals original (schema, counts, values).

#### TC-ARROW-02 — Round-trip a `DatasetDict`
- **Priority:** P1 · **Tags:** arrow
- **Steps:**
  1. Save/load a multi-split `DatasetDict`.
- **Expected:** All splits restored identically.

#### TC-ARROW-03 — Parquet load preserves schema `[SMOKE]`
- **Priority:** P0 · **Tags:** arrow, data-loading
- **Steps:**
  1. Load a Parquet fixture with nested + nullable columns.
- **Expected:** Schema/types preserved; nulls intact.

#### TC-ARROW-04 — `cast_column` to `ClassLabel`
- **Priority:** P1 · **Tags:** arrow
- **Steps:**
  1. `ds.cast_column("label", ClassLabel(names=[...]))`.
- **Expected:** Integer-encoded labels; `.features` reflect `ClassLabel`.

#### TC-ARROW-05 — `cast` whole-dataset schema change
- **Priority:** P1 · **Tags:** arrow
- **Steps:**
  1. `ds.cast(Features({...}))` with a compatible new schema.
- **Expected:** Values cast correctly; incompatible casts raise a clear error.

#### TC-ARROW-06 — `to_pandas` / `to_dict` round-trip `[SMOKE]`
- **Priority:** P0 · **Tags:** arrow
- **Steps:**
  1. `df = ds.to_pandas()`, `d = ds.to_dict()`; rebuild via `from_pandas`/`from_dict`.
- **Expected:** Values preserved both directions.

#### TC-ARROW-07 — `map` with missing/None values (regression of #2831)
- **Priority:** P1 · **Tags:** arrow, map, bug, regression
- **Steps:**
  1. `.map` over a column containing `None`/missing values.
- **Expected:** No `ArrowInvalid`; nulls handled (guards #2831).

#### TC-ARROW-08 — Added column length must match (regression of #2768)
- **Priority:** P1 · **Tags:** arrow, map, bug, regression
- **Steps:**
  1. In `.map(batched=True)`, return a column whose length matches the batch.
- **Expected:** Succeeds; a deliberate length-mismatch raises the documented clear error
  (guards #2768 "Added column's length must match table's length").

#### TC-ARROW-09 — JSON → Arrow nested type (regression of #2799)
- **Priority:** P2 · **Tags:** arrow, data-loading, bug
- **Steps:**
  1. Load JSON containing deeply nested/heterogeneous structures.
- **Expected:** Loads without `ArrowNotImplementedError`, or fails with a clear, documented message (guards #2799).

#### TC-ARROW-10 — Int overflow / large values
- **Priority:** P2 · **Tags:** arrow
- **Steps:**
  1. Build a dataset with very large ints exceeding int32.
- **Expected:** Promoted to int64 / handled without silent corruption.

#### TC-ARROW-11 — `Sequence` feature with None entries (regression of #2892)
- **Priority:** P2 · **Tags:** arrow, bug
- **Steps:**
  1. Encode a `Sequence(...)` feature where some rows are `None`.
- **Expected:** Encodes without error (guards #2892).

#### TC-ARROW-12 — `to_json` export correctness (regression of #7037)
- **Priority:** P1 · **Tags:** arrow, bug, regression
- **Steps:**
  1. `ds.to_json(path)`; reload via JSON builder; compare.
- **Expected:** Export is valid and round-trips (guards #7037 `to_json` bug).

#### TC-ARROW-13 — `to_csv` / `to_parquet` exports
- **Priority:** P2 · **Tags:** arrow
- **Steps:**
  1. `ds.to_csv(...)` and `ds.to_parquet(...)`; reload.
- **Expected:** Round-trip values preserved (allowing for CSV stringification).

#### TC-ARROW-14 — Memory-mapped read of large arrow table
- **Priority:** P2 · **Tags:** arrow, flaky
- **Steps:**
  1. `load_from_disk` a large dataset; access random rows.
- **Expected:** Backed by memory-map; RAM stays bounded; random access works.

#### TC-ARROW-15 — `concatenate_datasets` schema compatibility
- **Priority:** P1 · **Tags:** arrow
- **Steps:**
  1. Concatenate two datasets with identical schemas; then with incompatible ones.
- **Expected:** Compatible concat works; incompatible raises a clear schema error.

#### TC-ARROW-16 — `interleave_datasets`
- **Priority:** P2 · **Tags:** arrow, streaming
- **Steps:**
  1. Interleave two datasets with given probabilities.
- **Expected:** Mixed output respects ratios; works for both eager and streaming.

### 5.5 Splits & slicing (TC-SPLIT) — *29% of historical bugs; 332 open today*

---

#### TC-SPLIT-01 — `train_test_split` non-empty `[SMOKE]`
- **Priority:** P0 · **Tags:** split, critical, regression
- **Steps:**
  1. `ds.train_test_split(test_size=0.2)`.
- **Expected:** Both splits non-empty; sizes ≈ ratio (guards #676 empty-split regression).

#### TC-SPLIT-02 — `train_test_split` reproducible with seed
- **Priority:** P1 · **Tags:** split, flaky
- **Steps:**
  1. Run twice with same `seed`; compare indices.
- **Expected:** Identical partition across runs.

#### TC-SPLIT-03 — `train_test_split` on a `Dataset` (not DatasetDict) (regression of #1600)
- **Priority:** P1 · **Tags:** split, bug, regression
- **Steps:**
  1. Call `train_test_split` on a single `Dataset`.
- **Expected:** Works (the method exists on `Dataset`); guards #1600 AttributeError class.

#### TC-SPLIT-04 — Percentage slicing `split="train[:10%]"` `[SMOKE]`
- **Priority:** P0 · **Tags:** split
- **Steps:**
  1. `load_dataset(name, split="train[:10%]")`.
- **Expected:** Returns ~10% of train rows.

#### TC-SPLIT-05 — Absolute index slicing `split="train[:100]"`
- **Priority:** P1 · **Tags:** split
- **Steps:**
  1. `load_dataset(name, split="train[:100]")`.
- **Expected:** Exactly 100 rows (or fewer if dataset smaller).

#### TC-SPLIT-06 — Combined / additive split expression
- **Priority:** P2 · **Tags:** split
- **Steps:**
  1. `split="train+test"` and `split="train[:50%]+test[50%:]"`.
- **Expected:** Concatenated per the expression; counts add up.

#### TC-SPLIT-07 — `select()` returns rows & supports `.shape` `[SMOKE]`
- **Priority:** P0 · **Tags:** split, regression
- **Steps:**
  1. `sub = ds.select(range(10))`; read `sub.shape`, `sub[0]`.
- **Expected:** 10 rows; `.shape` returns `(10, n_cols)` (guards #1622 select().shape).

#### TC-SPLIT-08 — `select()` with out-of-range index
- **Priority:** P2 · **Tags:** split
- **Steps:**
  1. `ds.select([0, len(ds)+5])`.
- **Expected:** Raises a clear `IndexError`-style error; no silent wrap.

#### TC-SPLIT-09 — `shard()` partitions correctly
- **Priority:** P1 · **Tags:** split
- **Steps:**
  1. `ds.shard(num_shards=4, index=i)` for i in 0..3; concatenate.
- **Expected:** Shards are disjoint and cover the full dataset exactly once.

#### TC-SPLIT-10 — Integer / slice / list indexing
- **Priority:** P1 · **Tags:** split
- **Steps:**
  1. `ds[0]`, `ds[:5]`, `ds[[1,3,5]]`.
- **Expected:** Row dict, column-wise dict-of-lists, and selected rows respectively.

#### TC-SPLIT-11 — Negative indexing
- **Priority:** P2 · **Tags:** split
- **Steps:**
  1. `ds[-1]`.
- **Expected:** Returns last row (or documented error if unsupported) — behaviour is consistent.

#### TC-SPLIT-12 — `sort()` then slice
- **Priority:** P2 · **Tags:** split
- **Steps:**
  1. `ds.sort("col")[:5]`.
- **Expected:** Rows sorted ascending; slice reflects new order.

#### TC-SPLIT-13 — `shuffle(seed)` reproducibility
- **Priority:** P1 · **Tags:** split, flaky
- **Steps:**
  1. `ds.shuffle(seed=42)` twice; compare order.
- **Expected:** Deterministic identical order across runs.

#### TC-SPLIT-14 — Named-split metadata preserved
- **Priority:** P2 · **Tags:** split
- **Steps:**
  1. After slicing, inspect `ds.split` attribute.
- **Expected:** Split name/metadata reflects the slice expression.

#### TC-SPLIT-15 — NonMatchingSplitsSizes surfaced on corrupt split (regression of #2941)
- **Priority:** P1 · **Tags:** split, data-loading, bug, regression
- **Preconditions:** Fixture with deliberately wrong recorded split size.
- **Steps:**
  1. Load with default verification.
- **Expected:** Raises `NonMatchingSplitsSizesError` (detection works; guards #2941).

#### TC-SPLIT-16 — Parquet shard export keeps all shards (regression of #8269)
- **Priority:** P1 · **Tags:** split, arrow, bug, regression
- **Steps:**
  1. Export a multi-shard config to parquet; reload.
- **Expected:** No shards dropped; full row count preserved (guards #8269).

### 5.6 Map & filter transformations (TC-MAP) — *237 open today*

---

#### TC-MAP-01 — `map()` adds a column (single proc) `[SMOKE]`
- **Priority:** P0 · **Tags:** map, critical
- **Steps:**
  1. `ds.map(lambda x: {"len": len(x["text"])})`.
- **Expected:** New `len` column present with correct values; original columns intact.

#### TC-MAP-02 — `map()` modifies existing column
- **Priority:** P1 · **Tags:** map
- **Steps:**
  1. `ds.map(lambda x: {"text": x["text"].lower()})`.
- **Expected:** Column updated in place; row count unchanged.

#### TC-MAP-03 — `map(remove_columns=...)`
- **Priority:** P1 · **Tags:** map
- **Steps:**
  1. `ds.map(fn, remove_columns=["text"])`.
- **Expected:** Listed columns removed; new columns retained.

#### TC-MAP-04 — `filter()` correct subset `[SMOKE]`
- **Priority:** P0 · **Tags:** map, critical
- **Steps:**
  1. `ds.filter(lambda x: x["label"] == 1)`.
- **Expected:** Only matching rows remain; count correct.

#### TC-MAP-05 — `filter(fn_kwargs=...)` (regression of #2927/#2950)
- **Priority:** P1 · **Tags:** map, bug, regression
- **Steps:**
  1. `ds.filter(pred, fn_kwargs={"threshold": 5})`.
- **Expected:** kwargs passed through correctly (guards #2927, fixed in PR #2950).

#### TC-MAP-06 — `map(fn_kwargs=...)`
- **Priority:** P1 · **Tags:** map
- **Steps:**
  1. `ds.map(fn, fn_kwargs={"suffix": "!"})`.
- **Expected:** Extra kwargs reach the function.

#### TC-MAP-07 — `map(batched=True)` `[SMOKE]`
- **Priority:** P0 · **Tags:** map, critical
- **Steps:**
  1. `ds.map(batch_fn, batched=True, batch_size=100)`.
- **Expected:** Batched processing; output equals non-batched equivalent.

#### TC-MAP-08 — `map(batched=True)` that changes row count
- **Priority:** P1 · **Tags:** map
- **Steps:**
  1. Batched fn that splits each row into multiple (data augmentation pattern).
- **Expected:** Output row count grows accordingly; no length-mismatch error.

#### TC-MAP-09 — `map(with_indices=True)`
- **Priority:** P1 · **Tags:** map
- **Steps:**
  1. `ds.map(lambda x, i: {"idx": i}, with_indices=True)`.
- **Expected:** Indices match position 0..n-1.

#### TC-MAP-10 — `map(with_rank=True)` under multiprocessing
- **Priority:** P2 · **Tags:** map, multiprocessing
- **Steps:**
  1. `ds.map(fn, with_rank=True, num_proc=2)`.
- **Expected:** Rank passed; covers full range of worker ranks.

#### TC-MAP-11 — `set_transform` / `with_transform` (on-the-fly)
- **Priority:** P1 · **Tags:** map
- **Steps:**
  1. `ds.with_transform(transform)`; read rows.
- **Expected:** Transform applied lazily at access; underlying arrow unchanged.

#### TC-MAP-12 — `map` keeps features when fn returns subset
- **Priority:** P2 · **Tags:** map, arrow
- **Steps:**
  1. fn returns only some output keys.
- **Expected:** Documented merge behaviour; no unexpected column loss.

#### TC-MAP-13 — `filter` empty result
- **Priority:** P2 · **Tags:** map
- **Steps:**
  1. Predicate matching nothing.
- **Expected:** Returns a valid 0-row dataset; no crash.

#### TC-MAP-14 — `map` error inside fn surfaces clearly
- **Priority:** P2 · **Tags:** map
- **Steps:**
  1. fn raises a Python exception on one row.
- **Expected:** Error propagates with a traceback identifying the failure (not swallowed).

#### TC-MAP-15 — Dataset vs IterableDataset `map` parity (regression of #5870)
- **Priority:** P1 · **Tags:** map, streaming, bug, regression
- **Steps:**
  1. Apply identical `.map` eagerly and on a streamed version; compare outputs.
- **Expected:** Same results & semantics across both (guards #5870 behaviour divergence).

#### TC-MAP-16 — `map` caching reuse correctness
- **Priority:** P1 · **Tags:** map, cache
- **Steps:**
  1. Run `.map(fn)` twice in the same session.
- **Expected:** Second run uses cache; output identical.

### 5.7 Multiprocessing & parallelism (TC-MP) — *flaky-prone; #6936/#6357 open*

---

#### TC-MP-01 — `map(num_proc=4)` completes & matches single-proc `[SMOKE]`
- **Priority:** P0 · **Tags:** multiprocessing, critical, flaky
- **Steps:**
  1. Run `.map(fn)` with `num_proc=1` and `num_proc=4`; compare outputs.
- **Expected:** Identical results; multi-proc run completes without hang.

#### TC-MP-02 — `num_proc` > dataset length (regression of #2470)
- **Priority:** P1 · **Tags:** multiprocessing, bug, regression
- **Steps:**
  1. `.map(fn, num_proc=16)` on a 4-row dataset.
- **Expected:** No crash; gracefully uses ≤ len workers (guards #2470).

#### TC-MP-03 — `num_proc` memory usage bounded (regression of #2256)
- **Priority:** P2 · **Tags:** multiprocessing, flaky, bug
- **Steps:**
  1. `.map(fn, num_proc=8)` on a moderately large dataset; monitor RSS.
- **Expected:** Memory stays within expected bounds; no per-worker full-copy blow-up (#2256).

#### TC-MP-04 — Multiprocessed `map` preserves order
- **Priority:** P1 · **Tags:** multiprocessing
- **Steps:**
  1. `.map` with indices via `num_proc>1`.
- **Expected:** Output row order matches input order after recombination.

#### TC-MP-05 — `filter(num_proc>1)` no hang `[SMOKE]`
- **Priority:** P0 · **Tags:** multiprocessing, critical, flaky
- **Steps:**
  1. `.filter(pred, num_proc=4)`.
- **Expected:** Completes within timeout; correct subset (guards #2600 filter mp crash).

#### TC-MP-06 — `map(num_proc>1)` with caching
- **Priority:** P1 · **Tags:** multiprocessing, cache
- **Steps:**
  1. Run multiproc `.map` twice.
- **Expected:** Per-shard cache files reused on the second run.

#### TC-MP-07 — Custom multiprocessing context (relates to #6357)
- **Priority:** P2 · **Tags:** multiprocessing
- **Steps:**
  1. If supported, pass a `multiprocessing` context (e.g. spawn) to `.map`.
- **Expected:** Honoured without deadlock (tracks feature request #6357).

#### TC-MP-08 — `save_to_disk(num_proc>1)` no freeze (regression of #6936)
- **Priority:** P1 · **Tags:** multiprocessing, arrow, bug, regression
- **Steps:**
  1. `ds.save_to_disk(path, num_proc=4)` to local disk.
- **Expected:** Completes without freezing (guards #6936 class; s3 variant noted as env-dependent).

#### TC-MP-09 — `num_proc=1` equals default behaviour
- **Priority:** P2 · **Tags:** multiprocessing
- **Steps:**
  1. Compare `num_proc=1` vs default (None).
- **Expected:** Identical results; no spurious process spawning.

#### TC-MP-10 — Exception in worker propagates (no silent hang)
- **Priority:** P1 · **Tags:** multiprocessing, flaky
- **Steps:**
  1. fn raises in one worker during `num_proc>1` map.
- **Expected:** Error surfaces to main process promptly; pool torn down; no hang.

#### TC-MP-11 — Keyboard-interrupt cleans up workers
- **Priority:** P2 · **Tags:** multiprocessing, flaky
- **Steps:**
  1. Start a long multiproc `.map`; send SIGINT.
- **Expected:** All child processes terminated; no orphan processes/locks left.

#### TC-MP-12 — Parallel `load_dataset` from multiple processes
- **Priority:** P2 · **Tags:** multiprocessing, cache, flaky
- **Steps:**
  1. Launch N processes loading the same uncached dataset simultaneously.
- **Expected:** Lock file coordinates them; exactly one prepares cache; no corruption.

#### TC-MP-13 — `map(num_proc>1)` with `with_rank`
- **Priority:** P2 · **Tags:** multiprocessing
- **Steps:**
  1. fn uses `rank` to write per-rank artefacts.
- **Expected:** Each rank gets a distinct, contiguous rank id.

#### TC-MP-14 — Deterministic output across `num_proc` values
- **Priority:** P1 · **Tags:** multiprocessing, flaky
- **Steps:**
  1. Run identical `.map` at num_proc 1, 2, 4, 8.
- **Expected:** Output dataset identical regardless of worker count.

### 5.8 trust_remote_code handling (TC-TRC) — *coverage gap; 36 open today*

---

#### TC-TRC-01 — Script dataset blocked without flag `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading, critical
- **Preconditions:** A dataset that requires a remote/local loading script.
- **Steps:**
  1. `load_dataset(script_dataset)` WITHOUT `trust_remote_code`.
- **Expected:** Raises/prompts requiring explicit `trust_remote_code=True`; arbitrary code is
  NOT executed by default (security-critical).

#### TC-TRC-02 — Script dataset loads with flag `[SMOKE]`
- **Priority:** P0 · **Tags:** data-loading, critical
- **Steps:**
  1. `load_dataset(script_dataset, trust_remote_code=True)`.
- **Expected:** Loads successfully; documented behaviour.

#### TC-TRC-03 — `trust_remote_code=False` explicit
- **Priority:** P1 · **Tags:** data-loading
- **Steps:**
  1. `load_dataset(script_dataset, trust_remote_code=False)`.
- **Expected:** Explicitly refuses to run the script; clear error.

#### TC-TRC-04 — Pure-data dataset ignores the flag
- **Priority:** P1 · **Tags:** data-loading
- **Steps:**
  1. Load a parquet/csv-only dataset with and without the flag.
- **Expected:** Identical results; no script => flag is a no-op (no spurious prompt).

#### TC-TRC-05 — Flag still accepted / not removed (regression of #7723)
- **Priority:** P1 · **Tags:** data-loading, regression
- **Steps:**
  1. Call `load_dataset(..., trust_remote_code=True)` on the version under test.
- **Expected:** Argument is accepted (not removed/deprecated-to-error) — guards #7723.

#### TC-TRC-06 — Streaming + trust_remote_code (regression of #7692)
- **Priority:** P1 · **Tags:** streaming, data-loading, regression
- **Steps:**
  1. `load_dataset(script, streaming=True, trust_remote_code=True)`; iterate.
- **Expected:** Streams correctly without decode error (guards #7692). (Dup of TC-STR-17 cross-ref.)

#### TC-TRC-07 — Loading-script dataset with config + remote code
- **Priority:** P2 · **Tags:** data-loading
- **Steps:**
  1. Load a script dataset specifying a config name with the flag set.
- **Expected:** Correct config loads; code executed only because flag was set.

#### TC-TRC-08 — Cached script dataset reuse honours flag
- **Priority:** P2 · **Tags:** data-loading, cache
- **Steps:**
  1. Load script dataset with flag (cache built); reload.
- **Expected:** Reuse from cache; no re-execution surprise; consistent results.

#### TC-TRC-09 — Clear, actionable error message text
- **Priority:** P2 · **Tags:** data-loading
- **Steps:**
  1. Trigger the block; read the error/prompt message.
- **Expected:** Message names the dataset and tells the user exactly how to opt in.

#### TC-TRC-10 — Env/global default behaviour
- **Priority:** P2 · **Tags:** data-loading
- **Steps:**
  1. Check whether any global setting can pre-authorize; verify documented default is "deny".
- **Expected:** Secure-by-default; any opt-in mechanism behaves as documented.

### 5.9 Cross-cutting / parity (TC-XCUT)

---

#### TC-XCUT-01 — Same dataset loads normal AND streaming `[SMOKE]`
- **Priority:** P0 · **Tags:** streaming, data-loading, critical
- **Steps:**
  1. Load a dataset both ways; compare schema + first rows.
- **Expected:** Both succeed; schemas match (guards #2923/#2866 "works in one mode only").

#### TC-XCUT-02 — Features schema identical eager vs streaming
- **Priority:** P1 · **Tags:** streaming, arrow
- **Steps:**
  1. Compare `.features` from eager and streamed loads.
- **Expected:** Equal feature definitions.

#### TC-XCUT-03 — `map` output parity eager vs streaming
- **Priority:** P1 · **Tags:** map, streaming, regression
- **Steps:**
  1. Same transform applied both ways; compare first N rows. (See TC-MAP-15.)
- **Expected:** Identical transformed rows.

#### TC-XCUT-04 — Error parity across modes
- **Priority:** P2 · **Tags:** streaming, data-loading
- **Steps:**
  1. Trigger the same fault (e.g. bad column) in eager and streaming.
- **Expected:** Comparable, clear errors in both modes (no "silent in streaming" divergence).

#### TC-XCUT-05 — Version round-trip compatibility
- **Priority:** P2 · **Tags:** arrow, cache, regression
- **Steps:**
  1. `save_to_disk` with the version under test; `load_from_disk` it back.
- **Expected:** Self-consistent round-trip; documented behaviour for older on-disk formats.

#### TC-XCUT-06 — `with_format` consistency (torch/numpy/pandas)
- **Priority:** P1 · **Tags:** arrow
- **Steps:**
  1. `ds.with_format("numpy"/"torch"/"pandas")`; read a row.
- **Expected:** Correct container types per format; values numerically equal across formats.

---

## 6. Traceability matrix (category → cases → evidence)

| Focus area | Test cases | Historical issues anchored | Live (2026) issues anchored |
|---|---|---|---|
| Data loading | TC-DL-01..18 (18) | #2882, #2937, #2941, #2918 | #6829, #6937 |
| Streaming | TC-STR-01..18 (18) | #2923, #2866, #2944, #2918 | #7692 |
| Caching | TC-CACHE-01..14 (14) | #2496, #2904, #2775, #2591, #2937, #2471 | #4526 |
| Arrow serialization | TC-ARROW-01..16 (16) | #2831, #2768, #2799, #2892, #2591 | #7037 |
| Splits & slicing | TC-SPLIT-01..16 (16) | #676, #1600, #1622, #2941 | #8269, #4526 |
| Map & filter | TC-MAP-01..16 (16) | #2927, #2950 | #5870, #6787, #6789 |
| Multiprocessing | TC-MP-01..14 (14) | #2470, #2256, #2600 | #6936, #6357 |
| trust_remote_code | TC-TRC-01..10 (10) | (n/a — feature post-dates snapshot) | #7723, #7692, #7531 |
| Cross-cutting | TC-XCUT-01..06 (6) | #2923, #2866 | #5870 |
| **Total** | **128 cases** | | |

---

## 7. Data sources & method notes

- **Historical analysis:** `github-bug-reports-and-issues.jsonl` — 984 issues (PRs excluded),
  `huggingface/datasets`, snapshot 2020-04 → 2021-09. Categorized by keyword/label matching
  against the `qa_brief.yaml` focus areas (issues may match multiple categories).
- **Live cross-check:** GitHub Search API, June 2026, `repo:huggingface/datasets is:issue
  is:open` queries per focus area. Current issue numbers reach #8269.
- **PR-structure context:** The supplied `open-source-pull-requests-with-documentation-changes.json`
  turned out to be a transformers *model-class → SHA* mapping, **not** PR templates. PR
  conventions were therefore derived from the 2035 real PRs inside the `.jsonl` snapshot
  (concise descriptive title + explanatory body + `Fix #NNNN` issue references).
- **Known limitation:** Live exact open-counts for `data loading`, `caching`, `arrow`, and
  `streaming` were not captured cleanly because some issue bodies contained control characters
  that broke strict JSON parsing during collection. These remain high-priority on volume +
  core-surface grounds; the gap is in the *count*, not the prioritization.
