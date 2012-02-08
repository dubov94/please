from ..solution_runner.solution_runner import SolutionInfo, run_solution
from .. import globalconfig
import os
from ..utils.exceptions import PleaseException
from ..invoker.invoker import ExecutionLimits 
from ..solution_tester import package_config
from ..utils import utests
from ..utils.form_error_output import process_err_exit
import logging
    
logger = logging.getLogger("please_logger.answers_generator")

class AnswersGenerator :
    """
     Description : 
      This class runs the solution (source_path) on list of tests (tests).
    
       tests - list of names of the tests
       source_path - path to the running solution
       solution_config = {"input" : solution_input_file, 
                 "output" : solution_output_file}
                 solution_input_file - the input file which is used in running solution
                 solution_input_file - the output file which is used in running solution 
       There are 2 methods :
         
         generate(tests,source_path,args,execution_limits,solution_config)
    """
   
    @staticmethod
    def check_correct_finished(solution_result, solution_src):
        invoker_result = solution_result[0]
        if invoker_result.verdict != "OK":
            raise PleaseException(process_err_exit("Solution %s crashed with"
                    % (solution_src), invoker_result.verdict, invoker_result.return_code,
                    *solution_result[1:3]))
        
    @staticmethod
    def generate (tests=None, source_path=None, args=None, solution_config=None, execution_limits = globalconfig.default_limits) :
        config = package_config.PackageConfig.get_config()
        # TODO: check if config is None
        result = []
        if tests is None:
            tests = utests.get_tests()
        source_path = source_path or config['main_solution']
        args = args or (config['args'] if 'args' in config else [])
        solution_config = solution_config or {"input" : config['input'], "output" : config['output']}
        for num, test in enumerate(tests):
            logger.info('Generating answer for test #{0} by {1}'.format(str(num+1), str(source_path)))
            AnswersGenerator.check_correct_finished(
                run_solution ((SolutionInfo (source_path, args, execution_limits,
                                         solution_config, test, test + ".a"))), source_path)
            result.append(test + '.a')
        return result
    
