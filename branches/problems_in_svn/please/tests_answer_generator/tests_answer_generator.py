from ..test_config_parser import parser
import io
import os
from please import globalconfig
from ..tests_generator import tests_generator
from ..invoker.invoker import ExecutionLimits
from ..validator_runner import validator_runner
from ..answers_generator import answers_generator
from ..solution_tester import package_config
import logging
from ..utils import utests
from ..well_done import well_done
from please.log import logger

error_str = "Validator executions has had "


def get_file_name(testinfo):
    return testinfo

def get_return_code (validators_result):
    return validators_result[0].return_code

def get_verdict (validators_result):
    return validators_result[0].verdict

class TestsAndAnswersGenerator:
    """
    function generate_all() generates all the tests of file tests.please
    function generate(tags) generates tests with tags
    tags - list of tags
    Example:
     TestsAndAnswersGenerator().generate(["BIG_TESTS"])
    """
    def validate(self):
        config = package_config.PackageConfig.get_config()
        count_errors = 0
        result = []
        if 'validator' in config and config['validator'] not in ["", None]:
            for test_filename in utests.get_tests():
                logger.info("Start validator on test: " + test_filename)
                validator_result = validator_runner.validate(config["validator"], test_filename)
                if get_return_code(validator_result) != 0:
                    count_errors += 1
                verd = get_verdict(validator_result)
                if verd == "FNF":
                    return (1, [])
                result.append((test_filename, verd))
                if verd != "OK":
                    logger.error(error_str + verd)
                    logger.error("\nSTDERR:\n" + validator_result[2].decode())
        else:
            logger.warning("Validator is empty")
        return (count_errors, result)

    def well_done(self):
        config = package_config.PackageConfig.get_config()
        if 'well_done_test' in config and config['well_done_test'] not in ["", None]:
            for test_filename in utests.get_tests():
                well_done.well_done_check_test(test_filename, config["well_done_test"].split(', '))
        else:
            logger.warning("Well_done config for tests is empty")

        if 'well_done_answer' in config and config['well_done_answer'] not in ["", None]:
            for test_filename in utests.get_tests():
                well_done.well_done_check_test(test_filename + '.a', config["well_done_answer"].split(', '))
        else:
            logger.warning("Well_done config for answers is empty")

    def __get_admit (self, tags):
        def admit(attr):
            for tag in tags:
                if not tag in attr:
                    return False
            return True

        return admit

    def __generate_answers (self, tests):
        result = []
        count_errors = 0
        config = package_config.PackageConfig.get_config()
        if 'well_done_test' in config and config['well_done_test'] not in ["", None]:
            for test_filename in tests:
                well_done.well_done_check_test(test_filename, config["well_done_test"].split(', '))
        else:
            logger.warning("Well_done config for tests is empty")
        tests_names = []
        if 'validator' in config and config['validator'] not in ["", None]:
            for test in tests:
                logger.info("Start validator on test: " + test)
                validator_result = validator_runner.validate(config["validator"], test)
                if get_return_code (validator_result) != 0:
                    count_errors += 1
                verd = get_verdict(validator_result)
                if verd == "FNF":
                    return (1, [])
                result.append((test, verd))
                if verd == "OK":
                    tests_names.append(test)
                else:
                    logger.error(error_str + verd)
                    logger.error("\nSTDERR:\n" + validator_result[2].decode())
        else:
            logger.warning("Validator is empty")
        answers_gen = answers_generator.AnswersGenerator()
        answers_gen.generate (tests_names, config ["main_solution"], [], config)
        if 'well_done_answer' in config and config['well_done_answer'] not in ["", None]:
            for test_filename in tests_names:
                well_done.well_done_check_test(test_filename + '.a', config["well_done_answer"].split(', '))
        else:
            logger.warning("Well_done config for answers is empty")
        return (count_errors, result)

    def generate_all(self):
        tests = tests_generator.TestsGenerator(parser.parse_test_config()).generate_all()
        return self.__generate_answers(tests)

    def generate (self,tags):
        tests = tests_generator.TestsGenerator(parser.parse_test_config()).generate( self.__get_admit ( tags ) )
        return self.__generate_answers(tests)