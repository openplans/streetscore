import csv
import datetime
from django.db import connections
from django.http import HttpResponse

from .models import Rating

def csv_data(request):
    now = datetime.datetime.utcnow()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=beautifulst_data_%s.csv' % (now.strftime('%Y%m%d%H%M%S'), )

    # Get the data
    ratings = Rating.objects.all().select_related()

    # Init the csv writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['lat1','lon1','lat2','lon2','score'])

    # Write the contents
    for rating in ratings:
        writer.writerow([
            rating.place1.lat, rating.place1.lon,
            rating.place2.lat, rating.place2.lon,
            rating.score])

    return response
