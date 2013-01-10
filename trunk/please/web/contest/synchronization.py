import os

from please import globalconfig
from please.contest.contest import Contest as PleaseContest
#from please.package.config import ConfigFile
#from please.add_source.add_source import add_solution, del_solution
from please.utils.exceptions import PleaseException

from contest.models import Contest
from please.web.problem.models import Problem
from please.web.problem.views.file_utils import ChangeDir


def get_contest_by_path(path):
    try:
        model = Contest.objects.get(path=path)
    except Problem.DoesNotExist:
        if path[-1] == os.sep:
            path = path[:-1]
        else:
            path += os.sep
        model = Problem.objects.get_or_create(path=path)[0]
    return model


def import_to_database(model=None, path=None):
    assert ((model is None) != (path is None))
    if path is not None:
        model = get_contest_by_path(path)

    contest_path = path or str(model.path)

    if not os.path.exists(contest_path):
        model.delete()
        return None

    conf = PleaseContest(contest_path).config

    model.name = conf.get("name", "")
    method = conf.get("id_method", "")
    if method:
        for id in Contest.ID_METHODS:
            if id[1] == method:
                model.id_method = id[0]
                break
    model.statement_name = conf['statement'].get("name", "")
    model.statement_location = conf['statement'].get("location", "")
    model.statement_date = conf['statement'].get("date", "")
    model.statement_template = conf['statement'].get("template", "contest.tex")

    '''
    old_solutions = {i.path.replace(os.sep, '/') for i in model.solution_set.all()}
    for solution in conf.get("solution", []):
        path = solution['source'].replace(os.sep, '/')
        sol = Solution.objects.get_or_create(path=path, problem=model)[0]
        old_solutions.discard(path)
        sol.input = solution.get('input', '')
        sol.output = solution.get('output', '')
        sol.expected_verdicts.clear()
        sol.possible_verdicts.clear()
        for verdict in solution['expected']:
            sol.expected_verdicts.add(Verdict.objects.get_or_create(name=verdict)[0])
        for verdict in solution.get('possible'):
            sol.possible_verdicts.add(Verdict.objects.get_or_create(name=verdict)[0])
        if path == conf['main_solution'].replace(os.sep, '/'):
            model.main_solution = sol
        sol.save()
    
    for old in old_solutions:
        model.solution_set.get(path=old).delete()
    '''

    model.save()
    return model

def export_from_database(model=None, path=None):
    assert (model is None) != (path is None)
    if path is not None:
        model = get_contest_by_path(path)

    contest = PleaseContest(model.path, True)
    conf = contest.config
    conf['please_version'] = conf['please_version'] or str(globalconfig.please_version)
    conf['name'] = str(model.name)
    for id in Contest.ID_METHODS:
        if id[0] == model.id_method:
            conf['id_method'] = id[1]
    conf['statement']['name'] = str(model.statement_name)
    conf['statement']['location'] = str(model.statement_location)
    conf['statement']['date'] = str(model.statement_date)
    conf['statement']['template'] = str(model.statement_template)
    contest.save()

    '''
        for solution in model.solution_set.all():
            solution.path = solution.path.replace(os.sep, '/')
            sources.append(str(solution.path))
            if str(solution.path) in already_there:
                continue
            args = []
            if solution.input:
                args += ['input', str(solution.input)]
            if solution.output:
                args += ['output', str(solution.output)]
            if solution.possible_verdicts.count() != 0:
                args += (['possible'] +
                        list(map(str, solution.possible_verdicts.all())))
            if solution.expected_verdicts.count() != 0:
                args += (['expected'] +
                        list(map(str, solution.expected_verdicts.all())))
            try:
                add_solution(str(solution.path), args)
            except PleaseException:
                solution.delete()
        for sol in already_there:
            if (sol not in sources) and (sol != conf['main_solution'].replace(os.sep, '/')):
                del_solution(sol)
    '''

def import_tree(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.contest'):
                paths.append(os.path.join(root, file))
                contest = Contest(path=os.path.join(root, file))
                contest.save()
                import_to_database(contest)
    return paths
