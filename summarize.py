from __future__ import print_function

import pyperf


ENVIRONMENTS = [
    'py27',
    'py35',
    'py35',
    'py36',
    'py37',
    'py38',
    'pypy',
    'pypy3',
]

summary = {}

for environment in ENVIRONMENTS:
    results_path = f'results/{environment}.json'
    with open(results_path) as f:
        suite = pyperf.BenchmarkSuite.load(f)

    summary[environment] = list(suite.get_benchmarks())

benchmark_names = [bm.get_name() for bm in summary[ENVIRONMENTS[0]]]

print('| Benchmark |',  ' | '.join(f'{env}' for env in ENVIRONMENTS), '|')
print('| --- |',        ' | '.join('---' for env in ENVIRONMENTS), '|')
for i, bm_name in enumerate(benchmark_names):
    row = []
    min_index = 999
    min_value = 999.0
    for j, env in enumerate(ENVIRONMENTS):
        bm = summary[env][i]
        value = bm.mean()
        if value < min_value:
            min_value = value
            min_index = j
        row.append(bm.format_value(value))
    row[min_index] = f'**{row[min_index]}**'
    print(f'| {bm_name} |', ' | '.join(row), '|')
