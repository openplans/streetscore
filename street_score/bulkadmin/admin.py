from django.conf.urls import patterns, url
from django.contrib import admin
from functools import update_wrapper, partial
from . import forms
from . import views

import logging
log = logging.getLogger(__name__)


class BulkUploadAdmin (admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(BulkUploadAdmin, self).__init__(*args, **kwargs)

    def get_urls(self):
        urlpatterns = super(BulkUploadAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^bulk_add/$',
                wrap(self.bulk_add_view),
                name='%s_%s_bulk_add' % info),
        ) + urlpatterns

        return urlpatterns

    def bulk_add_view(self, request, form_url='', extra_context=None):
        view = views.BulkUploadFormAdminView.as_view(form_class=forms.BulkUploadForm)
        return view(request)
