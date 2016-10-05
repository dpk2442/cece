"""
.. module cece.main

The main module for cece. This contains the entry point for the application.
"""

from __future__ import print_function
from __future__ import unicode_literals

import cece.compiler
import cece.parser
import future.utils


def main():
    """
        The main entry point for cece.
    """

    # load config
    config = cece.util.load_yaml_file("config.yaml")

    # convert nested variants in variant groups in config file into a flat
    # dictionary of all variants
    config["variants"] = {}
    for variant_group_id, variant_group in future.utils.viewitems(config["variant_groups"]):
        for variant in variant_group["variants"]:
            config["variants"][variant["id"]] = variant

    # parse guides
    parser = cece.parser.Parser(config)
    try:
        guides = parser.parse()
    except cece.parser.ParsingException as e:
        print("Error parsing directory:")
        print(e)

    # compile guides
    compiler = cece.compiler.Compiler(config, guides)
    compiler.compile()
