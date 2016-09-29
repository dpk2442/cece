"""
.. module cece.util

Utilities for cece
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import yaml


def merge_nested_dicts(base, *dicts):
    """
        Merge multiple dictionaries together. The first dictionary is treated as
        the base dictionary, and is modified by overwriting properties with the
        values of the other dicts, in order. If a value within the dict is
        nested, the nested dictionaries are recursively merged.

        :param base: The base dictionary
        :param dicts: The list of dictionaries to extend the base with
        :returns: The base dictionary
    """

    if not isinstance(base, dict):
        raise TypeError("The supplied arguments must be dictionaries.")
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
    """
        Open and read a file, convert the contents to yaml, and close the file.

        :param path: Path to the yaml file
        :returns: The parsed yaml file contents
    """

    with open(path, "r") as f:
        return yaml.load(f.read())


def natural_sort(lst, key=lambda x: x):
    """
        Sort a list in a natural way.

        This works by splitting the key, which must be a string, into string and
        integer parts. The list of all of those parts is then used as a key for
        Python's built in sort function.

        :param lst: The list to sort
        :param key: The key function to use
    """

    def natural_key(obj):
        key_val = key(obj)
        return [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", key_val)]
    lst.sort(key=natural_key)


def makedirs(path):
    """
        Safely make a directory by ensuring every parent directory is created.

        :param path: The directory to create
    """

    if path and not os.path.isdir(path):
        os.makedirs(path)


def iterate_list_subsets(lst):
    """
        Iterate over the sublists of the given list. Each sublist starts at the
        beginning of the given list, and is one item longer than the previous
        one.

        For example, ``[1, 2, 3, 4, 5]`` would yield:

        * ``[1]``
        * ``[1, 2]``
        * ``[1, 2, 3]``
        * ``[1, 2, 3, 4]``
        * ``[1, 2, 3, 4, 5]``

        :param lst: The list to iterate
        :returns: An iterator over the sublists
    """

    for i in range(1, len(lst) + 1):
        yield lst[:i]
