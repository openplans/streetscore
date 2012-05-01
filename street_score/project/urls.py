from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from . import resources, views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$',
        TemplateView.as_view(template_name='index.html'),
        name='home'),

    url(r'^ratings/$',
        resources.RatingListView.as_view(),
        name='rating_list'),

    url(r'^ratings/(?P<id>\d+)$',
        resources.RatingInstanceView.as_view(),
        name='rating_instance'),

    url(r'^survey_sessions/$',
        resources.SurveySessionListView.as_view(),
        name='survey_session_list'),

    url(r'^data/?$',
        views.csv_data,
        name='data_csv_list'),
)
