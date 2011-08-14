import sys

import distribute_setup
distribute_setup.use_setuptools(version="0.6.19")

from setuptools import setup, find_packages

#print(find_packages())
#sys.exit()

'''packages = [ \
    'add_source',
    'answers_generator',
    'auto_TL',
    'build_all',
    'checker_runner',
    'checkers',
    'cleaner',
    'command_line',
    'directory_diff',
    'executors',
    'export2ejudge',
    'import_from_polygon',
    'invoker',
    'language',
    'language_configurator',
    'latex',
    'package',
    'reports',
    'solution_runner',
    'solution_tester',
    'stress_tester',
    'template',
    'test_config_parser',
    'tests_answer_generator',
    'tests_generator',
    'todo',
    'utils',
    'validator_runner'
]'''

#packages = ['please'] + ['please/' + s for s in packages]    

modules = [ \
    'please',
    'please/tags',
    'please/globalconfig',
    'please/log'
]

package_data = {
    'please': ['templates/*.*', 'checkers/*.*']
}

entry_points = {
    'console_scripts' : ['please = please:main']
}

install_requires = [
    'lxml',
    'psutil',
    'colorama',
    'HTML.py'
]

setup_params = { \
    'name'             : 'Please', 
    'version'          : '0.1', 
    'description'      : '***', 
    'py_modules'       : modules, 
    'package_dir'      : {'please': 'please'}, 
    'packages'         : find_packages(),
    'package_data'     : package_data,
    'install_requires' : install_requires,
    'dependency_links' : ['http://please.googlecode.com/svn/third_party/windows/psutil-0.3.0-py3.2-win32.egg',
                          'http://please.googlecode.com/svn/third_party/windows/HTML.py-0.04-py3.2.egg'],
    'entry_points'     : entry_points
}

    

setup(**setup_params)
