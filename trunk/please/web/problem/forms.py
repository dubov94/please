from django import forms
from problem.models import *
import os.path


class AddProblemForm(forms.Form):
    path = forms.CharField(max_length=255, required=True)


class AddTestsForm(forms.Form):
    test = forms.FileField(label='Specify a test file (or a zip archive with test files)')


class ProblemEditForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('path', 'name', 'short_name', 'input', 'output', 'time_limit', 'memory_limit')


class ProblemSearch(forms.Form):
    tags = forms.CharField(required=False)


class ProblemEditMaterialsForm(forms.Form):
    statement = forms.CharField(widget=forms.Textarea, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    analysis = forms.CharField(widget=forms.Textarea, required=False)


class ProblemUploadFilesForm(forms.Form):
    checker = forms.FileField(required=False)
    validator = forms.FileField(required=False)


class SolutionAddForm(forms.Form):
    solution_file = forms.FileField(required=True)
    input_file_name = forms.CharField(required=False)
    output_file_name = forms.CharField(required=False)
    expected_verdicts = forms.MultipleChoiceField(
            choices=[(verdict, verdict.name) for verdict in Verdict.objects.all()],
            required=True,
            initial=["OK"])
    possible_verdicts = forms.MultipleChoiceField(
            choices=[(verdict, verdict.name) for verdict in Verdict.objects.all()],
            required=False)


class ManageTestsForm(forms.Form):
    tests_please_content = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    tags_for_generate_tests = forms.CharField(required = False)


class AdditonalUpload(forms.Form):
    uploaded = forms.FileField(required=True, label='Select file')


def upload_files_form(path_str):
    class UploadFiles(forms.Form):
        path = forms.FilePathField(
            path=path_str,
            allow_files=False, allow_folders=True,
            required=False, recursive=True
        )
        path.choices[0] = (path_str, os.path.sep)
        file = forms.FileField(required=False)
    return UploadFiles


class TagsEditForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('tags',)
