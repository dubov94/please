import os
import shutil
import sys
from ..package import config
import logging

log = logging.getLogger("please_logger.add_source")

def __readpackage():
    input_stream = open("default.package", "r", encoding = "utf-8")
    config_file = input_stream.read()
    input_stream.close()
    return config_file

def __writepackage(text):
    output_stream = open("default.package", "w", encoding = "utf-8")
    output_stream.write(text)
    output_stream.close()

def add_main_solution_with_config(package_config, path):
    temp = os.path.split(path)
    basename =  os.path.basename(path)
    path = os.path.join(*temp)
    basename = os.path.basename(path)
    if path.replace("\\","/") != "solutions/"+basename:
        shutil.copy(path, os.path.join("solutions", basename))
    package_config['main_solution'] = "solutions" + '/' + basename

def add_main_solution (path):
    package_config = config.Config(__readpackage())
    add_main_solution_with_config(package_config,path)
    package_text = package_config.get_text()
    __writepackage(package_text)   
    log.info("Main solution %s was added successfully", path)
def add_solution_with_config (package_config, path, expected_list = [], possible_list = []):
    temp = os.path.split(path)
    basename =  os.path.basename(path)
    path = os.path.join(*temp)
    if path.replace("\\","/") != "solutions/"+basename:
        shutil.copy(path, os.path.join("solutions", basename))
    config_file  = config.Config("")
    config_file ["source"] = "solutions" + '/' + basename
    config_file ["expected_verdicts"] = expected_list
    config_file ["possible_verdicts"] = possible_list
    package_config.set("solution", config_file, None, True)

def add_solution (path,expected_list = [], possible_list = []):
    package_config  = config.Config(__readpackage())
    add_solution_with_config(package_config,path,expected_list,possible_list)
    package_text = package_config.get_text()
    __writepackage(package_text)
    log.info("Solution %s was added successfully", path)
    log.debug("Solution %s with expected: %s and possible: %s was added", path, str(expected_list), str(possible_list))

def add_solution_with_expected(path, expected_list = []):
    add_solution(path, expected_list, ['OK'])

def add_checker_with_config (package_config,path):
    temp = os.path.split(path)
    basename =  os.path.basename(path)
    path = os.path.join(*temp)
    basename =  os.path.basename(path)
    if path.replace("\\","/") != basename:
        shutil.copy(path, os.path.join(basename))
    package_config["checker"] = basename

def add_checker (path):
    package_config = config.Config(__readpackage())
    add_checker_with_config(package_config,path)
    package_text = package_config.get_text()
    __writepackage(package_text)   
    log.info("Checker %s was added successfully", path)
def add_validator_with_config (package_config,path):
    basename =  os.path.basename(path)
    if path.replace("\\","/") != basename:
        shutil.copy(path, os.path.join(basename))
    package_config["validator"] = basename

def add_validator (path):
    package_config = config.Config(__readpackage())
    add_validator_with_config(package_config,path)
    package_text = package_config.get_text()
    __writepackage(package_text)  
    log.info("Validator %s was added successfully", path)