# Create your views here.
from django.views import generic as views
from project.models import Place

import logging
log = logging.getLogger(__name__)


class BulkUploadFormAdminView (views.FormView):
    template_name = "bulkadmin/bulk_add_form.html"

    def form_valid(self, form):
        data = form.cleaned_data['data']
        Place.objects.bulk_create([Place(**d) for d in data])
        return super(BulkUploadFormAdminView, self).form_valid(form)

    def get_success_url(self):
        return '/admin/project/place/'
