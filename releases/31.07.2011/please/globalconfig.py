import os
from .invoker.invoker import ExecutionLimits
from logging import INFO,ERROR,CRITICAL,WARNING,DEBUG
please_version = 0.1
root = os.path.split(__file__)[0]

default_limits = ExecutionLimits(20, 3512)
# templates
default_template_dir = "templates"
default_template_contest = "contest.tex"
default_template_statement = "statement.tex"
user_template_dir = ""

default_programming_language = "cpp"
default_human_language = "ru"

# config for folders in problem
statements_dir = "statements"
solutions_dir = "solutions"

# temporary folders
temp_statements_dir = ".statements"

# logging conts
standart_logging_lvl = INFO
detailed_logging_lvl = DEBUG
console_logging_lvl = INFO

checkers_dir = "checkers"

# checker return codes -> verdicts
checker_return_codes = {0:"OK", 1:"WA", 2:"PE"}

#temporary solution output file
temp_solution_out_file = ".out"

#information about ejudge server (protocol pscp)
ejudge_host = "10.0.0.21"
ejudge_port = "22"
ejudge_login = "ejudge"
ejudge_password = "ejudge"
ejudge_contests_dir = "/var/lib/ejudge/"

#information about polygon
access = {'login': 'gurovic', "password" : "12345"}
polygon_url = "http://polygon.lksh.ru"
ejudge_contests_dir = "/var/lib/ejudge/"