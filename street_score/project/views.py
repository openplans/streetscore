import csv
import datetime
from django.http import HttpResponse


def csv_data(request):
    now = datetime.datetime.utcnow()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=beautifulst_data_%s.csv' % (now.strftime('%Y%m%d%H%M%S'), )

    # Get the data
    data = [{'H1': 'A', 'H2': 'B', 'H3': 3}, {'H1': 'C', 'H2': 'D', 'H3': 6}]

    # Init the csv writer
    writer = csv.writer(response)

    # Write the header row
    keys = data[0].keys()
    writer.writerow(keys)

    # Write the contents
    for row in data:
        writer.writerow([row[key] for key in keys])

    return response
