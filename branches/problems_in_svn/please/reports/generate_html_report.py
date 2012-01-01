from ..solution_tester.check_solution import get_test_results_from_solution
from ..solution_tester.package_config import PackageConfig
from .html_report import HtmlReporter

import os.path

def generate_html_for_solution(config, solution, expected_verdicts = ["OK"], possible_verdicts = []):
    ''' Generates <div> block with tabled report for given solution  '''
    report = get_test_results_from_solution(solution, config)
    html_reporter = HtmlReporter()
    
    for test, checker_verdict in sorted(report[2].items(), key = lambda x: int(os.path.basename(x[0]))):
        html_reporter.add_test(solution, os.path.basename(test), checker_verdict[0])

    footer = ""
    if len(report[0]) > 0:
        footer += "unexpected but met: <b>%s</b><br />" % "</b>,<b> ".join(report[0].keys())
    if len(report[1]) > 0:
        footer += "expected but not met: <b>%s</b><br />" % "</b>,<b> ".join(report[1])

    return "<div style='display: inline; float: left; margin: 5px; font-family: monospace'>" + html_reporter.str() + footer + "</div>"

def generate_html_report():
    config = PackageConfig.get_config()
    solution = config["main_solution"]

    html = generate_html_for_solution(config, solution)
    generated = set()
    generated.add(solution)

    for solve in config["solution"]:
        if not solve["source"] in generated:
            html += generate_html_for_solution(config, solve["source"], solve["expected_verdicts"], solve["possible_verdicts"])
            generated.add(solve["source"])

    html = "<div style='width: 10000px'>" + html + "</div>"
    with open("report.html", "w", encoding = "utf-8") as output:
        output.write(html)