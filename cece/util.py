"""
.. module cece.util

Utilities for cece
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import sys
import yaml


def load_yaml_file(path):
    """
        Open and read a file, convert the contents to yaml, and close the file.

        :param path: Path to the yaml file
        :type path: string
        :returns: The parsed yaml file contents
    """

    try:
        with open(path, "r") as f:
            return yaml.load(f)
    except yaml.YAMLError as e:
        print("Error parsing \"{0}\":".format(path))
        print(e)
        sys.exit(1)


def natural_sort(lst, key=lambda x: x):
    """
        Sort a list in a natural way.

        This works by splitting the key, which must be a string, into string and
        integer parts. The list of all of those parts is then used as a key for
        Python's built in sort function.

        :param lst: The list to sort
        :type lst: list
        :param key: The key function to use
        :type key: function
    """

    def natural_key(obj):
        key_val = key(obj)
        return [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", key_val)]
    lst.sort(key=natural_key)


def makedirs(path):
    """
        Safely make a directory by ensuring every parent directory is created.

        :param path: The directory to create
        :type path: string
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
        :type lst: list
        :returns: An iterator over the sublists
    """

    for i in range(1, len(lst) + 1):
        yield lst[:i]
