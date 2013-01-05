from ..checker_runner import checker_runner
from ..solution_runner.solution_runner import run_solution, SolutionInfo
from .. import globalconfig
from ..utils import utests
from ..utils.error_window import PreventErrorWindow
from ..utils import form_error_output
import os
import logging

logger = logging.getLogger("please_logger.solution_tester.tester")


class TestSolution:
    '''Tests given solution.
        Usage:
            config = {}
            config["checker"] = "checker.cpp"
            config["tests_dir"] = ".tests"
            config["expected"] = ["OK", "ML"]
            config["possible"] = ["TL"]
            config["execution_limits"] = ExecutionLimits()
            config["solution_config"] = ... (nobody knows now :-))
            config["solution_args"] = ["-p", "-f"]
            tester = TestSolution(config)
            result = tester.test_solution("solution.dpr")
         Returns:
            result is tuple of:
                a) dictionary of unexpected, but met verdicts and list of paths to
                tests, where it happened
                b) list of expected, but not met verdicts
                c) and dictionary of tests names and list of
                    1) checker verdict on them
                    2) and real time of solution running
            Sample:
                result = ( {"WA":[".tests/1", ".tests/2"], "PE":[".tests/17"]}, ["OK", "ML"],
                {".tests/1":[ResultInfo, stdout, stderr],
                ".tests/2":[ResultInfo, stdout, stderr], ... ,
                ".tests/17":[ResultInfo, stdout, stderr],
                ".tests/18":[ResultInfo, stdout, stderr]})
     '''
    def __init__(self, config):
        #all necessary parameters in config are below:
        self.checker = config["checker"]
        self.tests_dir = globalconfig.temp_tests_dir
        self.expected = config.get("expected") or globalconfig.default_expected
        self.possible = config.get("possible") or globalconfig.default_possible
        self.execution_limits = config.get("execution_limits") or globalconfig.default_limits
        self.solution_config = config.get("solution_config") or {
            'input': config.get('input'),
            'output': config.get('output')}
        self.solution_args = config.get("solution_args") or []

    def one_test(self, solution, test, answer, program_out):
        with PreventErrorWindow():
            solution_info = SolutionInfo(solution, self.solution_args, self.execution_limits, \
                                                             self.solution_config, test, program_out)
            solution_run_result = run_solution(solution_info)
            result = ""
            stdout = ""
            stderr = ""
            if solution_run_result[0].verdict != "OK":
                if solution_run_result[0].verdict == "RE":
                    logger.error(form_error_output.process_err_exit("Solution %s is failed" % solution,
                                solution_run_result[0].verdict, solution_run_result[0].return_code,
                                solution_run_result[1].decode(), solution_run_result[2].decode()))
                result = solution_run_result[0].verdict
            else:
                checker_info = checker_runner.CheckerInfo(self.checker, test, answer, program_out)
                check_result = checker_runner.run_checker(checker_info)
                #tuple: ResultInfo, stdout, stderr
                if check_result[0].return_code in globalconfig.checker_return_codes:
                    result = globalconfig.checker_return_codes[check_result[0].return_code]
                else:
                    result = "CF"
                stdout = check_result[1]
                stderr = check_result[2]

            #take = return code + realtime
            result_info = solution_run_result[0]
            result_info.verdict = result
        return [result_info, stdout, stderr]

    def test_solution(self, solution):
        met_not_expected = {}
        expected_not_met = []
        testing_result = {}
        verdicts = dict(zip(self.expected, [0] * len(self.expected)))
        #{"WA":0, "OK":0, "TL":0 ... }
        program_out = os.path.join(self.tests_dir, globalconfig.temp_solution_out_file)
        #.tests/out
        for num, test in enumerate(utests.get_tests(self.tests_dir)):
            #.tests/1, .tests/2 ...
            answer = test + ".a"
            #.tests/1.a, .tests/2.a ...
            logger.info('Testing {0} on test #{1}'.format(solution, str(num + 1)))
            result = self.one_test(solution, test, answer, program_out)
            verdict = result[0].verdict
            if verdict in verdicts:
                verdicts[verdict] += 1
            elif verdict not in self.possible:
                met_not_expected.setdefault(verdict, []).append(test)
                #{"PE":[".tests/1", ".tests/4"]}
            testing_result[test] = result
            #{".tests/1":[ResultInfo,stdout,stderr], ".tests/2":[ResultInfo,stdout,stderr]}
        for item, value in verdicts.items():
            if value == 0:  # if didn't meet
                expected_not_met.append(item)
        if os.path.exists(program_out):
            os.remove(program_out)
        return (met_not_expected, expected_not_met, testing_result)
