import os.path

from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from nose.tools import *
from bulkadmin import forms
from project.models import Place


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

    @istest
    def test_BulkUploadFormAdminView(self):
        username = 'test_admin'
        email = 'test_admin@openplans.org'
        password = 'pw'
        client = Client()
        csvname = self.get_test_file_name()

        Place.objects.all().delete()
        User.objects.all().delete()

        User.objects.create_superuser(username, email, password)
        loggedin = client.login(username=username, password=password)
        assert (loggedin)

        with open(csvname) as csvfile:
            bulk_add_url = reverse(admin_urlname(Place._meta, 'bulk_add'))
            res = client.post(
                bulk_add_url,
                {'data': csvfile},
                follow=True)

        assert_equal(Place.objects.count(), 25)

    @istest
    def test_BulkUploadFormAdminView_excluding_duplicates(self):
        username = 'test_admin'
        email = 'test_admin@openplans.org'
        password = 'pw'
        client = Client()
        csvname = self.get_test_file_name()

        Place.objects.all().delete()
        User.objects.all().delete()

        User.objects.create_superuser(username, email, password)
        loggedin = client.login(username=username, password=password)
        assert (loggedin)

        with open(csvname) as csvfile:
            bulk_add_url = reverse(admin_urlname(Place._meta, 'bulk_add'))
            res = client.post(
                bulk_add_url,
                {'data': csvfile,
                 'exclude_duplicates': 'checked'},
                follow=True)

        assert_equal(Place.objects.count(), 20)

    @istest
    def test_BulkUploadFormAdminView_excluding_duplicates_with_existing_data(self):
        username = 'test_admin'
        email = 'test_admin@openplans.org'
        password = 'pw'
        client = Client()
        csvname = self.get_test_file_name()

        Place.objects.all().delete()
        User.objects.all().delete()

        User.objects.create_superuser(username, email, password)
        loggedin = client.login(username=username, password=password)
        assert (loggedin)

        # First, insert some data, duplicates and all
        with open(csvname) as csvfile:
            bulk_add_url = reverse(admin_urlname(Place._meta, 'bulk_add'))
            res = client.post(
                bulk_add_url,
                {'data': csvfile},
                follow=True)

        # Then, try inserting data, excluding duplicates
        with open(csvname) as csvfile:
            bulk_add_url = reverse(admin_urlname(Place._meta, 'bulk_add'))
            res = client.post(
                bulk_add_url,
                {'data': csvfile,
                 'exclude_duplicates': 'checked'},
                follow=True)

        assert_equal(Place.objects.count(), 25)
