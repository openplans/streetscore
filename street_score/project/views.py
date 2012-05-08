import csv
import datetime
import logging
from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from django.db import connections
from django.http import HttpResponse
from django.views import generic as views

from .models import Criterion, Rating, UserInfo, SiteConfiguration

log = logging.getLogger(__name__)

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
    writer.writerow(['lat1','lon1','lat2','lon2','score','user_lat', 'user_lon'])

    # Write the contents
    for rating in ratings:
        writer.writerow([
            rating.place1.lat, rating.place1.lon,
            rating.place2.lat, rating.place2.lon,
            rating.score,
            rating.user_info.lat, rating.user_info.lon])

    return response


class MainUIView (views.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainUIView, self).get_context_data(**kwargs)

        session_key = self.request.session.session_key
        if not self.request.session.exists(session_key):
            self.request.session.create()
            session_key = self.request.session.session_key

        # Using the browser session, get the current user info (or create it if
        # none exists for the current session).
        session = Session.objects.get(session_key=session_key)
        user_info = UserInfo.objects.get_or_create(session=session)[0]
        criteria = Criterion.objects.all()
        site = Site.objects.get_current()

        try:
            site_config = SiteConfiguration.objects.get(site=site)
        except SiteConfiguration.DoesNotExist:
            site_config = None

        context.update({
            'user_info': user_info,
            'initial_vote_count': user_info.ratings.count(),
            'site': site,
            'site_config': site_config,
            'criteria': criteria
        })
        return context
