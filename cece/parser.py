from __future__ import print_function
from __future__ import unicode_literals

import cece.util
import fnmatch
import os


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

        self._contents[path] = {
            "type": "folder",
            "links": child_links,
            "name": meta["name"],
            "description": meta["description"]
        }

    def _load_guide(self, meta, path):
        # add entry for main guide folder
        self._contents[path] = {
            "type": "folder",
            "links": [],
            "name": meta["name"],
            "description": meta["description"]
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
            parent = path
            for variant_tag in actual_tags:
                tag_id = os.path.join(parent, variant_tag)
                if not tag_id in self._contents:
                    # add tag to parent links
                    self._contents[parent]["links"].append(tag_id)
                    # add entry for self
                    self._contents[tag_id] = {
                        "type": "folder",
                        "links": [],
                        "name": meta["name"],
                        "description": meta["description"]
                    }
                parent = tag_id
            
            # create entry for variant
            variant_id = os.path.join(path, *actual_tags)
            self._contents[variant_id] = {
                "type": "page",
                "name": meta["name"],
                "description": meta["description"],
                "source_path": os.path.join(os.getcwd(), variant_full_path)
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
