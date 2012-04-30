import os.path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from nose.tools import *
from bulkadmin import forms


class BulkUploadTest(TestCase):
    def get_test_file_name(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, 'import_test.csv')

    @istest
    def load_data_from_csv(self):
        csvname = self.get_test_file_name()

        with open(csvname) as csvfile:
            data = forms.BulkUploadForm.load_csv(csvfile)

            assert isinstance(data, list)
            assert_equal(len(data), 25)
            assert all([('lat' in place and 'lon' in place) for place in data])

    @istest
    def use_form_to_load_csv_data(self):
        csvname = self.get_test_file_name()

        with open(csvname) as csvfile:
            form = forms.BulkUploadForm({},
                {'data': SimpleUploadedFile('test.csv', csvfile.read())})

            assert form.is_valid()
            assert isinstance(form.cleaned_data['data'], list)
            assert_equal(len(form.cleaned_data['data']), 25)
