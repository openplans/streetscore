# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.admin.util import get_deleted_objects, model_ngettext
from django.views import generic as views
from django.utils.translation import ugettext_lazy, ugettext as _
from project.models import Place

import logging
log = logging.getLogger(__name__)


class BulkUploadFormAdminView (views.FormView):
    template_name = "bulkadmin/bulk_add_form.html"

    def form_valid(self, form):
        data = form.cleaned_data['data']
        Place.objects.bulk_create([Place(**d) for d in data])

        if self.model_admin:
            n = len(data)
            self.model_admin.message_user(
                self.request,
                _("Successfully inserted {count:d} {items}.").format(
                    count=n, items=model_ngettext(self.model_admin.opts, n))
            )

        return super(BulkUploadFormAdminView, self).form_valid(form)

    def get_success_url(self):
        return '/admin/project/place/'

    def dispatch(self, request, model_admin=None, *args, **kwargs):
        self.model_admin = model_admin
        return super(BulkUploadFormAdminView, self).dispatch(request, *args, **kwargs)
