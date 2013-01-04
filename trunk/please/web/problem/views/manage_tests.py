from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from problem.models import Problem
from problem.forms import ManageTestsForm
from problem.views.file_utils import *
from problem.views.upload_files import *
from please.command_line.generate_tests import generate_tests, generate_tests_with_tags
from please import globalconfig
import os.path


def manage_tests(request, problem):
    tp_path = os.path.join(problem.path, globalconfig.default_tests_config)
    if request.method == 'POST':
        form = ManageTestsForm(request.POST)
        if form.is_valid():
            file_write(form.cleaned_data["tests_please_content"], tp_path)

            if "generate_tests" in request.POST:
                stags = form.cleaned_data["tags_for_generate_tests"]
                with ChangeDir(problem.path):
                    if stags != "":
                        generate_tests_with_tags(stags.split(" "))
                    else:
                        generate_tests()
    else:
        form = ManageTestsForm(initial={"tests_please_content": file_read(tp_path)})

    answer = {'form': form, 'problem_id': problem.id}
    answer.update({'upload_files': upload_files(request, problem)})
    return answer