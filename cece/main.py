"""
.. module cece.main

The main module for cece. This contains the entry point for the application.
"""

from __future__ import print_function
from __future__ import unicode_literals

import cece.compiler
import cece.parser
import future.utils
import json


def main():
    """
        The main entry point for cece.
    """

    # load config
    config = cece.util.load_yaml_file("config.yaml")
    config["variants"] = {}
    for variant_group_id, variant_group in future.utils.viewitems(config["variant_groups"]):
        for variant in variant_group["variants"]:
            config["variants"][variant["id"]] = variant

    # parse guides
    parser = cece.parser.Parser(config)
    guides = parser.parse()

    # compile guides
    compiler = cece.compiler.Compiler(config, guides)
    compiler.compile()
