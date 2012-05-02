import csv

from django import forms


class BulkUploadForm(forms.Form):
    data = forms.FileField(help_text="""
        <p>Select the CSV file to upload.  The file should have a header for
           each column you want to populate.  When you have selected your
           file, click the 'Upload' button below.</p>
        """)

    def clean(self):
        cleaned_data = super(BulkUploadForm, self).clean()

        cleaned_data['data'] = BulkUploadForm.load_csv(cleaned_data['data'])
        return cleaned_data

    @staticmethod
    def load_csv(f):
        reader = csv.reader(f)
        data = []

        i = 0
        for row in reader:
            if i == 0:
                header = row
            else:
                data.append(dict(zip(header, row)))
            i += 1

        return data
