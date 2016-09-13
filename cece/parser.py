from __future__ import print_function
from __future__ import unicode_literals

import cece.util
import fnmatch
import os


def _get_breadcrumbs(path):
    path = os.path.dirname(path)
    breadcrumbs = []
    while path:
        breadcrumbs.insert(0, path)
        path = os.path.dirname(path)
    return breadcrumbs


class ParsingException(Exception):
    
    def __init__(self, path, message):
        super(ParsingException, self).__init__("{}: {}".format(path, message))


class Parser(object):

    def __init__(self, config):
        self._config = config
        self._contents = None

    def parse(self):
        if self._contents:
            return self._contents

        self._contents = {}

        cur_dir = os.getcwd()
        os.chdir("guides")

        self._contents[""] = {
            "type": "folder",
            "links": [],
            "name": self._config["site_title"],
            "short_name": self._config["site_title"],
            "breadcrumbs": []
        }
        for f in os.listdir("."):
            self._load_dirs(f)
        for folder in filter(lambda x: x["type"] == "folder", self._contents.values()):
            cece.util.natural_sort(folder["links"], key=lambda x: self._contents[x]["name"])

        os.chdir(cur_dir)

        return self._contents

    def _load_folder(self, meta, path):
        child_links = []
        for child_folder in os.listdir(path):
            child_folder_path = os.path.join(path, child_folder)
            if os.path.isdir(child_folder_path):
                if self._load_dirs(child_folder_path):
                    child_links.append(child_folder_path)

        # add link to folder to parent
        self._contents[os.path.dirname(path)]["links"].append(path)
        # add entry for folder
        self._contents[path] = {
            "type": "folder",
            "links": child_links,
            "name": meta["name"],
            "short_name": meta["name"],
            "description": meta["description"],
            "breadcrumbs": _get_breadcrumbs(path)
        }

    def _load_guide(self, meta, path):
        # add entry for main guide folder
        self._contents[path] = {
            "type": "folder",
            "links": [],
            "name": meta["name"],
            "short_name": meta["name"],
            "description": meta["description"],
            "breadcrumbs": _get_breadcrumbs(path)
        }

        for variant_src_path in fnmatch.filter(os.listdir(path), "*.md"):
            variant_full_path = os.path.join(path, variant_src_path)

            # verify variant tags
            variant_tags = os.path.splitext(variant_src_path)[0].split("-")
            actual_tags = []
            for expected_variant_group in meta["variant_groups"]:
                expected_variant_group = self._config["variant_groups"][expected_variant_group]
                found_one = False
                for variant in expected_variant_group["variants"]:
                    if variant["id"] in variant_tags:
                        if found_one:
                            raise ParsingException(variant_full_path,
                                "Cannot have multiple variants in the variant group \"{}\"."
                                .format(expected_variant_group["name"]))
                        actual_tags.append(variant["id"])
                        found_one = True
                if not found_one:
                    raise ParsingException(variant_full_path,
                        "No variants for variant group \"{}\" found"
                        .format(expected_variant_group["name"]))

            # create entries for variant tags if they don't exist
            for variant_tags in cece.util.iterate_list_subsets(actual_tags[:-1]):
                current_tag = variant_tags[-1]
                parent = os.path.join(path, *variant_tags[:-1])
                tag_id = os.path.join(path, *variant_tags)
                if not tag_id in self._contents:
                    # add tag to parent links
                    self._contents[parent]["links"].append(tag_id)
                    # add entry for self
                    self._contents[tag_id] = {
                        "type": "folder",
                        "links": [],
                        "name": "{} ({})".format(meta["name"], ", ".join(self._config["variants"][variant_tag]["name"] for variant_tag in variant_tags)),
                        "short_name": self._config["variants"][current_tag]["name"],
                        "description": meta["description"],
                        "breadcrumbs": _get_breadcrumbs(tag_id)
                    }
            
            # create entry for variant
            current_tag = actual_tags[-1]
            parent = os.path.join(path, *actual_tags[:-1])
            variant_id = os.path.join(path, *actual_tags)
            # add variant to parent links
            self._contents[parent]["links"].append(variant_id)
            self._contents[variant_id] = {
                "type": "page",
                "name": "{} ({})".format(meta["name"], ", ".join(self._config["variants"][actual_tag]["name"] for actual_tag in actual_tags)),
                "short_name": self._config["variants"][current_tag]["name"],
                "description": meta["description"],
                "source_path": os.path.join(os.getcwd(), variant_full_path),
                "breadcrumbs": _get_breadcrumbs(variant_id)
            }

    def _load_dirs(self, root_dir):
        folder_meta_path = os.path.join(root_dir, "folder_meta.yaml")
        guide_meta_path = os.path.join(root_dir, "guide_meta.yaml")

        if os.path.exists(folder_meta_path):
            meta = cece.util.load_yaml_file(folder_meta_path)
            self._load_folder(meta, root_dir)
        elif os.path.exists(guide_meta_path):
            meta = cece.util.load_yaml_file(guide_meta_path)
            self._load_guide(meta, root_dir)
        else:
            return False

        return True
