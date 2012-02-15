from django.test import TestCase
from nose.tools import *


class BaseSegmentsTest(TestCase):
    """Base for tests that use the Segment model"""

    def setUp(self):
        super(BaseSegmentsTest, self).setUp()

        # Create the segments table manually, since we're not managing it with
        # the ORM.  This SQL comes from running ``manage.py sqlall project`` at
        # the command line.
        segments_table_sql = """
            CREATE TABLE "philly_street_osm_line" (
                "osm_id" integer NOT NULL PRIMARY KEY
            )
            ;

            SELECT AddGeometryColumn('philly_street_osm_line', 'way', 900913, 'LINESTRING', 2);
            CREATE INDEX "philly_street_osm_line_way_id" ON "philly_street_osm_line" USING GIST ( "way" GIST_GEOMETRY_OPS );
            COMMIT;
        """
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(segments_table_sql)

        from project.models import Segment
        Segment.objects.all().delete()

    def tearDown(self):
        super(BaseSegmentsTest, self).tearDown()

        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            DROP TABLE philly_street_osm_line;
            COMMIT;
        """)
