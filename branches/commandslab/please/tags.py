#!/usr/bin/python3
import logging
from .package.package_config import PackageConfig
from .utils.writepackage import writepackage

def add_tags(tags):
    opened_config = PackageConfig.get_config()
    # TODO: check if opened_config is None
    
    if not "tags" in opened_config:
        opened_config["tags"] = ""

    current_tags = []
    if opened_config["tags"] != "":
        current_tags = opened_config["tags"].split("; ")
    for tag in tags:
        if tag not in current_tags:
            current_tags.append(tag)

    opened_config["tags"] = "; ".join(current_tags)
    opened_config.write()
    
def clear_tags():
    opened_config = PackageConfig.get_config()
    # TODO: check if opened_config is None
    if not "tags" in opened_config:
        pass
    opened_config["tags"] = " "
    opened_config.write()
    
def show_tags():
    _inst_logger= logging.getLogger ("please_logger.tags.show_tags")
    _inst_logger.debug("Output Tags")
    opened_config = PackageConfig.get_config()
    # TODO: check if opened_config is None
    if "tags" in opened_config:
        print(opened_config["tags"])
