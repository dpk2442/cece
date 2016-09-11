from __future__ import print_function
from __future__ import unicode_literals

import cece.util
import future.utils
import os
import shutil

class Compiler(object):

    def __init__(self, config, guides):
        self._config = config
        self._guides = guides

    def compile(self):
        if os.path.isdir("build"):
            shutil.rmtree("build")
        os.mkdir("build")

        cur_dir = os.getcwd()
        os.chdir("build")

        for path, value in future.utils.viewitems(self._guides):
            if value["type"] == "folder":
                self._compile_folder(path, value)
            elif value["type"] == "page":
                self._compile_page(path, value)

        os.chdir(cur_dir)

    def _compile_folder(self, path, folder):
        cece.util.makedirs(path)
        index_path = os.path.join(path, "index.html")
        source = str(folder)
        with open(index_path, "w") as f:
            f.write(source)

    def _compile_page(self, path, page):
        cece.util.makedirs(path)
        index_path = os.path.join(path, "index.html")
        source = str(page)
        with open(index_path, "w") as f:
            f.write(source)
