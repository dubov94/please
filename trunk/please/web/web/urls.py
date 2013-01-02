from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^problems/(?P<id>\d+)/todo/$', 'problem.views.todo.show'),
    url(r'^problems/(?P<id>\d+)/materials/edit/$', 'problem.views.materials.edit'),
    url(r'^problems/(?P<id>\d+)/files/upload/main$', 'problem.views.files.upload_main', name='file_upload'),
    url(r'^problems/(?P<id>\d+)/files/upload/additional$', 'problem.views.files.upload_additional'),
    url(r'^problems/(?P<id>\d+)/solutions/add/$', 'problem.views.solutions.add'),
    url(r'^problems/(?P<id>\d+)/tests/', 'problem.views.tests.show'),
    url(r'^problems/confirmation/$', TemplateView.as_view(template_name='problem_edit_success.html')),
    url(r'^problems/create/$', 'problem.views.problems.create'),
    url(r'^problems/$', 'problem.views.problems.search_by_tag'),
    url(r'^$', 'problem.views.problems.search_by_tag'),   
)
