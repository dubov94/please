from os import mkdir
from os.path import exists
import os.path
from ..log import logger
import shutil
from .. import globalconfig
from ..utils.exceptions import PleaseException
from .template_utils import get_template_full_path
from .statement_template_generator import generate_description, generate_analysis, generate_statement
from .source_code_file_generator import generate_checker, generate_solution, generate_validator
from ..package.config import ConfigFile
from . import info_generator

class ProblemExistsError(PleaseException):
    pass

def generate_package(name, replaces, shortname):
    ''' Generates {default}.package file '''
    # maybe we will have templates not only for default.package?
    default_package_path = get_template_full_path(name) or get_template_full_path(globalconfig.defaultpackage)

    new_path = os.path.join(shortname, name)
    if default_package_path:
        shutil.copy(default_package_path, new_path)
    else:
        with open(new_path, 'w') as empty:
            pass
    package = ConfigFile(new_path)
    for replace, data in replaces.items():
        package[replace] = data
    package.write()

def generate_problem_advanced(shortname, human_language, programming_language):
    ''' Generates file structure of problem (templates (checker, validator, etc) and default.package) '''
    if exists(shortname):
        raise PleaseException("%s already exists" % shortname)
    
    mkdir(shortname)

    statement_path = os.path.join(shortname, globalconfig.statements_dir)
    tests_path = os.path.join(shortname, globalconfig.tests_dir)
    solutions_path = os.path.join(shortname, globalconfig.solutions_dir)

    # make dirs
    mkdir(statement_path)
    mkdir(tests_path)
    mkdir(solutions_path)

    mainsol = globalconfig.solutions_dir + '/' + generate_solution(solutions_path, programming_language)
    replaces = {'please_version': str(globalconfig.please_version),
                'shortname': shortname,
                'description': globalconfig.statements_dir + '/' + generate_description(statement_path, human_language),
                'analysis': globalconfig.statements_dir + '/' + generate_analysis(statement_path, human_language),
                'statement': globalconfig.statements_dir + '/' + generate_statement(statement_path, human_language),
                'validator': generate_validator(shortname, programming_language),
                'checker': generate_checker(shortname, programming_language),
                'main_solution': mainsol,
                'solution': '{\n    source = ' + mainsol + '\n    expected = OK\n}',
                'well_done_test' : 'endswith_EOLN, no_symbols_less_32, no_left_right_space, no_double_space, no_top_bottom_emptyline, not_empty',
                'well_done_answer': 'endswith_EOLN, no_symbols_less_32, no_left_right_space, no_double_space, no_top_bottom_emptyline, not_empty'}

    generate_package(globalconfig.default_package, replaces, shortname)

    # generate empty tests.please
    with open(os.path.join(shortname, globalconfig.default_tests_config), 'w'):
        pass

    # copy testlib.h & testlib.pas
    testlib_h = get_template_full_path("testlib.h")
    testlib_pas = get_template_full_path("testlib.pas")
    if testlib_h is not None:
        shutil.copy(testlib_h, os.path.join(shortname, 'testlib.h'))
    if testlib_pas is not None:
        shutil.copy(testlib_pas, os.path.join(shortname, 'testlib.pas'))

def generate_problem(shortname, handle_exception=True):
        generate_problem_advanced(shortname,
                              globalconfig.default_human_language,
                              globalconfig.default_programming_language)
        info_generator.create_md5_file(shortname)
        logger.info("Problem %s has been created successfully", str(shortname))
