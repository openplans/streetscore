# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.admin.helpers import AdminForm
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.admin.util import get_deleted_objects, model_ngettext
from django.views import generic as views
from django.utils.encoding import force_unicode
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

    def get_context_data(self, *args, **kwargs):
        context = super(BulkUploadFormAdminView, self).get_context_data(*args, **kwargs)

        # We're constructing an AdminForm from the view's form so that we can
        # use the admin templates that are shipped with Django out of the box.
        # I used code from django.contrib.admin.options as an example for the
        # following lines.
        form = context['form']
        fields = form.base_fields.keys()
        fieldsets = [(None, {'fields': fields})]
        bulkadminform = AdminForm(form, fieldsets, {}, model_admin=self)

        opts = self.model_admin.model._meta
        context.update({
            'title': u"Add many {0} from a CSV file".format(force_unicode(opts.verbose_name_plural)),
            'adminform': bulkadminform,
        })
        return context

    def get_success_url(self):
        opts = self.model_admin.model._meta
        return reverse(admin_urlname(opts, 'changelist'))

    def dispatch(self, request, model_admin=None, *args, **kwargs):
        self.model_admin = model_admin
        return super(BulkUploadFormAdminView, self).dispatch(request, *args, **kwargs)
