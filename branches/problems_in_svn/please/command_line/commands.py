from ..executors import trash_remover
from .. import globalconfig

PLEASE_VERSION = "0.1"

global_commands = ["create problem PROBLEM_NAME", 
             "export to ejudge contest CONTEST_ID problem[s] PROBLEM_LIST",
             "generate statements PROBLEMS_LIST",
             "help",
             "[show] todo PATH_TO_PROBLEM",
             "import polygon package PATH_TO_POLYGON_PACKAGE",
             "import polygon problem PROBLEM_LETTER from contest CONTEST_ID",
	     "delete problem PROBLEM_NAME", 
             ]

problem_commands = ["generate statement",
             "generate tests [with tag[s] TAGS_LIST]",
             "generate answers",
             "build all",
             "[show] todo",
             "set standard checker [name]",
             "add tag[s] TAGS_LIST",
             "show tags",
             "clear tags",
             "add solution PATH_TO_SOLUTION expected: EXPECTED_VERDICTS_LIST possible: POSSIBLE_VERDICTS_LIST",
             "add solution PATH_TO_SOLUTION with EXPECTED_VERDICTS_LIST",
             "set main solution PATH_TO_MAIN_SOLUTION",
             "set checker PATH_TO_CHECKER",
             "set validator PATH_TO_VALIDATOR",
             "check solution PATH_TO_SOLUTION",
             "check solutions",
             "stress test SOLUTION [CORRECT_SOLUTION] GENERATOR",
             "compute TL",
             "compute integer TL",
             "generate html report",
             "set problem name NAME",
             "check main solution",
             "clean",
             "validate tests",
             "[svn] sync",
             ]

def print_lite_help(in_problem_folder):
    print("Usage: please [command]")
    print("Commands available (try 'please help' for more information):\n")
    print("Global commands:\n")
    print(*sorted(global_commands), sep = "\n")
    print("\nCommands inside problem folder:\n")
    print(*sorted(problem_commands), sep = "\n")
    trash_remover.remove_logs_in_depth(out=False)

def print_help():
    print("""
Please version: {0}
Usage: please [command]

Global commands available:

  {1}:
    Generates file structure of a problem
    (checker, validator, default.package)
    example: please generate problem primes
    
  {2}:
    Exports problem to ejudge
    example: please export to ejudge problem 345348 task primes

  {3}:
    Generates PDF for problems listed. All the tasks must
    be in the directory, where you launch this command
    example: please generate statements island agripina dominoes
    
  {4}:
    Shows this help
    
  {5}:
    Shows TODO for given problem
    
  {6}:
    Imports Polygon package (in .zip format) to please package
    example: import polygon package centroid.zip
  
  {7}:
    Imports given Polygon problem from given contest

  {8}:
    Deletes local copy of the problem and moves it to .deleted folder
    in svn repository, if globalconfig.svn['url'] != ''""".format(PLEASE_VERSION, *global_commands))
    print("""
Commands available when inside problem's folder:

  {0}:
    Generates pdf statement for current problem
    
  {1}:
    Generates tests for current problem
    example: generate tests
             generate tests with qsort arrays
              
  {2} : Generates answers for all tests in .tests dir
    example : generate answers
             
  {3}:
    Shows TODO and builds everything
    
  {4}:
    Shows TODO
    
  {5}:
    Sets standard checker with name
    Default standard checkers:  acmp.cpp, dcmp.cpp, fcmp.cpp, 
                                hcmp.cpp, icmp.cpp, lcmp.cpp,
                                ncmp.cpp, rcmp4.cpp, rcmp6.cpp,
                                rcmp9.cpp, rcmp.cpp, rncmp.cpp,
                                wcmp.cpp, yesno.cpp
    example: add standard checker acmp
  
  {6}:
    Adds tags to current problem
    example: add tags qsort arrays
    
  {7}:
    Prints all tags associated with current problem
    
  {8}:
    Removes all tags associated with current problem
    
  {9}:
    Adds solution with some expected and possible verdicts
    example: add solution ../../sources/solution_tl_ml.cpp expected: TL,ML possible: OK,RE
   
  {10}:
    Adds solution with some expected verdicts and OK possible verdict
    example: add solution ../sources/solution_wa.cpp with WA

  {11}: 
    Sets main solution (solution that should pass all tests). Copies specified file in /solutions and edits default.package
    example: add main solution ../../sources/solution_ok.cpp
   
  {12}: 
    Sets checker. Copies specified file to the problem directory and edits default.package
    example: add checker ../../sources/checker.dpr
    
  {13}: 
    Sets validator. Copies specified file to the problem directory and edits default.package
    example: add validator ../../sources/validator.cpp

  {14}:
    Checks solution specified
    example: check solution solutiontl.cpp
    
  {15}
    Checks all solutions available    

  {16}:
    Performs a stress test of current solution
    example: stress test solutions/wrong.cpp "tests/gen.cpp 10 5"
             stress test solutions/wrong.cpp solutions/aa.cpp tests/gen.cpp
             
  {17}
    Computes adequate TL of current problem as ceiled doubled maximum running time of main solution

  {18}
    Computes adequate integer TL of current problem as doubled maximum running time of main solution
  
  {19}
    Generates html file report.html. This file contains tables with results of working of all solutions.
  
  {20}
    Sets current problem name
  
  {21}:
    Checks main solution, specified in default.package
    
  {22}
    Cleans up current directory - removes generated binary files, temporary folders, logs

  {23}:
    Validates all generated tests
    
  {24}:
    Syncronize local copy of the problem with svn repository (svn up, then add and commit new content)

""".format(*problem_commands))
    trash_remover.remove_logs_in_depth(out=False)















