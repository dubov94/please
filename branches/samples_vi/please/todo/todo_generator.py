import os
import hashlib
from ..solution_tester import package_config
from ..todo import painter
from .. import globalconfig
from ..template import info_generator

#TODO: make it nonstatic class
class TodoGenerator:

    @staticmethod
    def __read_md5_values(root_path = '.'):
        md5path = os.path.join(root_path, '.please', 'md5.config')
        if not os.path.exists(md5path):
            info_generator.create_md5_file(root_path)
            
        md5values = {}
        with open(md5path) as md5file:
            for s in md5file:
                resource, md5 = s.strip().split(':')
                md5values[resource] = md5
        return md5values                    

    @staticmethod
    def is_item_modified(item, config):
        md5values = TodoGenerator.__read_md5_values()
        status = TodoGenerator.__get_item_status(config, md5values, item)
        return status == "ok"

    @staticmethod
    def get_todo(root_path = '.'):
        md5values = TodoGenerator.__read_md5_values()
        config = package_config.PackageConfig.get_config()
        items = ["statement", "checker", "description", "analysis", "validator", "main_solution"]
        for item in items:
            TodoGenerator.print_to_console(
                    TodoGenerator.__get_item_status(config, md5values, item), item)
        tests_description_path = globalconfig.default_tests_config
        TodoGenerator.print_to_console(
                TodoGenerator.__get_item_status(config, md5values,
                    "tests_description", tests_description_path), "tests description")
    
    @staticmethod   
    def print_to_console(status, text):
        """ prints message to please console. color depends on objective's status"""
        if (status == "ok"):
            print(painter.ok(text + " ok"))
        elif (status == "warning"):
            print(painter.warning(text + " is default"))
        else:
            print(painter.error(text + " does not exist"))
    
    @staticmethod
    def __get_item_status(config, md5values, item=None, path=None):
        """
        Description:
        this function returns one of three item statuses (types):
        1) error - the file does not exist, or it's path is not written in config
        2) warning - the file exists, it's path is written in config file, or it's path is default,
        but the file is default(it's content is same as in creation of problem)
        3) ok - the file exists, it's path is written in config file, or it's path is default,
        and this file is not default(it's content was modified after creation problem)
        """
        if (path != None):
            item_path = path
        else:
            if (item in config):
                item_path = config[item]
            else:
                return "error"
        if (os.path.exists(item_path)):
            hashobj = hashlib.md5()
            with open(item_path,"rb") as item_file:
                hashobj.update(item_file.read())
            if (hashobj.hexdigest() != md5values[item]):
                return "ok" 
            else:
                return "warning"
        else:
            return "error"

