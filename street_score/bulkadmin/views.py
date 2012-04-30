# Create your views here.
from django.views import generic as views

class BulkUploadFormAdminView (views.FormView):
    template_name = "bulkadmin/bulk_add_form.html"

    def get_success_url(self):
        return '/admin/project/place/'
