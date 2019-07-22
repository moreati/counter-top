# counter-top

These benchmaarks compare different methods for implementing a cuonter in Python.
Where possible, both the key-missing and key-present cases were measured.
The benchmarks were run using [pyperf](https://pypi.org/project/pyperf), on several CPython releases, and PyPy.

## Results

| Benchmark | py27 | py35 | py35 | py36 | py37 | py38 | pypy | pypy3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dict, try/except, missing | 771 ns | 458 ns | 458 ns | 360 ns | 423 ns | 362 ns | **35.1 ns** | 41.9 ns |
| dict, try/except, present | 98.4 ns | 149 ns | 149 ns | 125 ns | 124 ns | 123 ns | 20.8 ns | **20.5 ns** |
| dict, if/else, missing | 83.5 ns | 91.8 ns | 91.8 ns | 81.2 ns | 81.6 ns | 79.5 ns | 25.0 ns | **24.7 ns** |
| dict, if/else, present | 122 ns | 168 ns | 168 ns | 146 ns | 151 ns | 145 ns | 21.9 ns | **21.2 ns** |
| dict, get, absent | 175 ns | 229 ns | 229 ns | 186 ns | 164 ns | 185 ns | 26.8 ns | **26.3 ns** |
| dict, get, present | 177 ns | 255 ns | 255 ns | 204 ns | 177 ns | 205 ns | **21.0 ns** | 21.0 ns |
| dict, setdefault | 215 ns | 307 ns | 307 ns | 246 ns | 228 ns | 247 ns | **30.5 ns** | 31.0 ns |
| defaultdict | 85.8 ns | 134 ns | 134 ns | 115 ns | 113 ns | 114 ns | 21.6 ns | **20.5 ns** |
| Counter | 347 ns | 509 ns | 509 ns | 382 ns | 316 ns | 383 ns | 21.2 ns | **20.7 ns** |

## Recommendations

1. If you can, Use PyPy, with `collections.Counter()`
1. If you must use CPython, use it with `collections.defaultdict()` 
