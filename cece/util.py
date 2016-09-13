from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import yaml


def merge_nested_dicts(*dicts):
    base = dicts[0]
    if not isinstance(base, dict):
        raise TypeError("The supplied arguments must be dictionaries.")
    dicts = dicts[1:]
    for d in dicts:
        if not isinstance(d, dict):
            raise TypeError("The supplied arguments must be dictionaries.")
        for key in d:
            if key in base and isinstance(base[key], dict) and isinstance(d[key], dict):
                base[key] = merge_nested_dicts(base[key], d[key])
            else:
                base[key] = d[key]
    return base


def load_yaml_file(path):
    with open(path, "r") as f:
        return yaml.load(f.read())


def natural_sort(lst, key=lambda x: x):
    def natural_key(obj):
        key_val = key(obj)
        return [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", key_val)]
    lst.sort(key=natural_key)


def makedirs(path):
    if path and not os.path.isdir(path):
        os.makedirs(path)


def iterate_list_subsets(lst):
    for i in range(1, len(lst) + 1):
        yield lst[:i]
