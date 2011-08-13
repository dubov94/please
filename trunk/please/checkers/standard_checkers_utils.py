import os
from please import log
import logging
from ..command_line.matcher import Matcher
from ..command_line.template import Template
from ..template import problem_template_generator as problem_gen
from ..package import config
import codecs
import sys
from .. import globalconfig as global_config
from ..solution_tester import package_config

log = logging.getLogger("please_logger.checkers.standard_checker_utils")

class AddStandartCheckerError (Exception) :
    pass

def __writepackage(text):
    output_stream = open("default.package", "w", encoding = "utf-8")
    output_stream.write(text)
    output_stream.close()

def add_standard_checker_to_solution (checker):
    """
    Description : 
       If checker is found in global directory then this function
       will write the global path to the checker into config file.
    """
    opened_config = package_config.PackageConfig.get_config()
    checker_name = checker + ".cpp"
    checker_global_path = os.path.join(global_config.root, global_config.checkers_dir, checker_name)
    
    if not os.path.exists(checker_global_path) :
        raise Exception("Standart checker " + checker_name + " not found!")
    else:
        opened_config['checker'] = checker_name
        config_file = opened_config.get_text()
        __writepackage(config_file)
        log.info("Standard checker %s was added successfully", checker_name)