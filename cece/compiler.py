from __future__ import print_function
from __future__ import unicode_literals

import cece.util
import future.utils
import jinja2
import markdown
import os
import shutil

class Compiler(object):

    def __init__(self, config, guides):
        self._config = config
        self._guides = guides
        self._markdown = markdown.Markdown()
        self._template_env = jinja2.Environment(loader=jinja2.PackageLoader("cece", "templates"))
        self._template_env.globals["make_id_url"] = self._make_id_url

    def _make_id_url(self, id):
        return "/{}/".format(id.replace("\\", "/"))

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
        # make directories
        cece.util.makedirs(path)

        # load and compile the template
        template = self._template_env.get_template("folder.html")
        source = template.render(
            site_title=self._config["site_title"], guides=self._guides, data=folder)

        # get the path to the html file and write it
        index_path = os.path.join(path, "index.html")
        with open(index_path, "w") as f:
            f.write(source)

    def _compile_page(self, path, page):
        # make directories
        cece.util.makedirs(path)

        # load and compile the markdown source
        with open(page["source_path"], "r") as f:
            md_content = f.read()
        content = self._markdown.reset().convert(md_content)

        # load and compile the template
        template = self._template_env.get_template("page.html")
        source = template.render(
            site_title=self._config["site_title"], guides=self._guides, content=content, data=page)

        # get the path to the html file and write it
        index_path = os.path.join(path, "index.html")
        with open(index_path, "w") as f:
            f.write(source)
