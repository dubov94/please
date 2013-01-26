import os
from please import globalconfig

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse

from ..models import Contest, ContestProblem
from ..forms import AddContestProblemForm
from .contests import edit_or_create_contest_block
from please.contest.commands import command_generate_statement
from please.web.problem.views.file_utils import ChangeDir
from ..helpers import contest_sync

@contest_sync(read=True, write=True)
def index(request, id):
    contest = get_object_or_404(Contest, id=id)
    if request.method == 'POST' and 'save_and_generate' in request.POST:
        with ChangeDir(os.path.dirname(contest.path)):
            command_generate_statement(os.path.basename(contest.path[:-8]))
    return render_to_response('contest/index.html', {
        'contest': contest,
        'insert_problem': insert_problem(request, contest),
        'edit_contest': edit_or_create_contest_block(request, contest),
        'pdf_exists': os.path.isfile(os.path.abspath(os.path.join(
                os.path.dirname(contest.path), 
                os.path.splitext(os.path.basename(contest.path))[0] + '.pdf')))
    }, RequestContext(request))

def view_statement(request, id):
    contest = get_object_or_404(Contest.objects, id=id)
    pdf_path = os.path.abspath(
            os.path.join(
                os.path.dirname(contest.path),
                os.path.splitext(
                    os.path.basename(contest.path))[0] + '.pdf'))
    return HttpResponse(FileWrapper(open(pdf_path, 'rb')), content_type='application/pdf')
    
@contest_sync(read=False, write=True)
def delete_problem(request, id, problem_id):
    ContestProblem.objects.get(id=problem_id).delete()
    probs = ContestProblem.objects.filter(contest__id=id)
    for i in range(len(probs)):
        probs[i].order = i
        probs[i].save()
    return redirect('/contests/{}'.format(id))

def insert_problem(request, contest):
    if request.method == 'POST':
        form = AddContestProblemForm(request.POST)
        if form.is_valid():
            problem = form.cleaned_data['problem']
            id_in_contest = form.cleaned_data['id_in_contest']
            order = ContestProblem.objects.filter(contest=contest).count()
            ContestProblem(problem=problem, id_in_contest=id_in_contest, order=100, contest=contest).save()           
    else:
        form = AddContestProblemForm()
    return {
        'form': form,
    }

@contest_sync(read=True, write=True)
def problem_up(request, id, problem_id):
    prob2 = ContestProblem.objects.get(id=problem_id)
    prob1 = ContestProblem.objects.get(order=prob2.order - 1, contest__id=id)
    print(prob1.order, prob2.order)
    prob1.order, prob2.order = prob2.order, prob1.order
    print(prob1.order, prob2.order)
    prob1.save()
    prob2.save()
    return redirect('/contests/{}'.format(id))

@contest_sync(read=True, write=True)
def problem_down(request, id, problem_id):
    prob2 = ContestProblem.objects.get(id=problem_id)
    prob1 = ContestProblem.objects.get(order=prob2.order + 1, contest__id=id)
    prob1.order, prob2.order = prob2.order, prob1.order
    prob1.save()
    prob2.save()
    return redirect('/contests/{}'.format(id))
