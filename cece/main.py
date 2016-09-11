from __future__ import print_function
from __future__ import unicode_literals

import cece.compiler
import cece.parser
import json


def main():
    # load config
    config = cece.util.load_yaml_file("config.yaml")

    # parse guides
    parser = cece.parser.Parser(config)
    guides = parser.parse()

    # compile guides
    compiler = cece.compiler.Compiler(config, guides)
    compiler.compile()
