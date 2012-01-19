from django.conf.urls import patterns, include, url
from django.views import generic as views
from . import resources

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^/$',
        views.TemplateView.as_view(template_name='bootstrap-fluid.html'),
        name='home'),

    url(r'^answer/$',
        resources.AnswerListView.as_view(),
        name='answer_instance'),
    url(r'^answer/(P<id>\d+)$',
        resources.AnswerListView.as_view(),
        name='answer_list'),
)
