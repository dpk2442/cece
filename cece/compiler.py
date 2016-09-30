"""
.. module cece.compiler

The compiler takes a parsed set of guides and compiles and writes the output to
the file system.
"""

from __future__ import print_function
from __future__ import unicode_literals

import cece.util
import future.utils
import jinja2
import markdown
import os
import shutil


class Compiler(object):
    """
        The compiler object.

        :param config: The configuration
        :type config: dict
        :param guides: The parsed set of guides to output
        :type guides: dict
    """

    def __init__(self, config, guides):
        self._config = config
        self._guides = guides
        self._markdown = markdown.Markdown()
        self._template_env = jinja2.Environment(loader=jinja2.PackageLoader("cece", "templates"))
        self._template_env.globals["make_id_url"] = self._make_id_url

    def _make_id_url(self, id):
        """
            Make url from an id.

            :param id: The id to form into a url
            :type id: string
        """

        return "/{}/".format(id.replace("\\", "/"))

    def compile(self):
        """
            Compile the provided guides and write out the result to the file
            system.
        """

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
        """
            Compile a folder, which is a listing of links to other folders or
            pages.

            :param path: The path of the folder
            :type path: string
            :param folder: The data for the folder
            :type folder: dict
        """

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
        """
            Compile a page.

            :param path: The path of the page
            :type path: string
            :param page: The data for the page
            :type page: dict
        """

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
