from __future__ import print_function

import collections
import textwrap

import pyperf


INNER_LOOPS = 1


SINGLE_INCREMENT_TEMPLATES = [
    {
        "name": "dict, try/except, missing",
        "setup": "counts = dict()",
        "stmt": """\
            try:
                counts[{key}] += 1
            except KeyError:
                counts[-1] = 1
        """,
    },
    {
        "name": "dict, try/except, present",
        "setup": "counts = {{key: 0 for key in range({inner_loops})}}",
        "stmt": """\
            try:
                counts[{key}] += 1
            except KeyError:
                raise
        """,
    },
    {
        "name": "dict, if/else, missing",
        "setup": "counts = dict()",
        "stmt": """\
            if {key} in counts:
                counts[{key}] += 1
            else:
                counts[-1] = 1
        """,
    },
    {
        "name": "dict, if/else, present",
        "setup": "counts = {{key: 0 for key in range({inner_loops})}}",
        "stmt": """\
            if {key} in counts:
                counts[{key}] += 1
            else:
                counts[{key}] = 1
        """,
    },
    {
        "name": "dict, get, absent",
        "setup": "counts = dict()",
        "stmt": """\
            counts[{key}] = counts.get(-1, 0) + 1
        """,
    },
    {
        "name": "dict, get, present",
        "setup": "counts = {{key: 0 for key in range({inner_loops})}}",
        "stmt": """\
            counts[{key}] = counts.get({key}, 0) + 1
        """,
    },
    {
        "name": "dict, setdefault",
        "setup": "counts = {{key: 0 for key in range({inner_loops})}}",
        "stmt": """\
            counts.setdefault({key}, 0)
            counts[{key}] += 1
        """,
    },
    {
        "name": "defaultdict",
        "setup": "counts = defaultdict(int)",
        "stmt": """\
            counts[{key}] += 1
        """,
    },
    {
        "name": "Counter",
        "setup": "counts = Counter()",
        "stmt": """\
            counts[{key}] += 1
        """,
    },
]


MULTIPLE_INCREMENT_TEMPLATES = [
    {
        "name": "dict, try/except",
        "setup": "counts = {}",
        "stmt": textwrap.dedent("""\
            for key in keys:
                try:
                    counts[key] += 1
                except KeyError:
                    counts[key] = 1
        """),
    },
    {
        "name": "dict, if/else",
        "setup": "counts = {}",
        "stmt": textwrap.dedent("""\
            for key in keys:
                if key in counts:
                    counts[key] += 1
                else:
                    counts[key] = 1
        """),
    },
    {
        "name": "dict, setdefault",
        "setup": "counts = {}",
        "stmt": textwrap.dedent("""\
            for key in keys:
                counts.setdefault(key, 0)
                counts[key] += 1
        """),
    },
    {
        "name": "dict, get",
        "setup": "counts = {}",
        "stmt": textwrap.dedent("""\
            for key in keys:
                counts[key] = counts.get(key, 0) + 1
        """),
    },
    {
        "name": "defaultdict",
        "setup": "counts = defaultdict(int)",
        "stmt": textwrap.dedent("""\
            for key in keys:
                counts[key] += 1
        """),
    },
    {
        "name": "Counter",
        "setup": "counts = collections.Counter()",
        "stmt": textwrap.dedent("""\
            counts.update(keys)
        """),
    },
]


runner = pyperf.Runner()

for template in SINGLE_INCREMENT_TEMPLATES:
    setup = template['setup'].format(inner_loops=INNER_LOOPS)
    stmt = ''.join(textwrap.dedent(template['stmt']).format(key=i)
                   for i in range(INNER_LOOPS))
    runner.timeit(
        name=template['name'].format(variant='absent'),
        setup=setup,
        stmt=stmt,
        inner_loops=INNER_LOOPS,
        globals={
            'Counter': collections.Counter,
            'defaultdict': collections.defaultdict,
        },
    )
