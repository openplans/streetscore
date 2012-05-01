import csv
import datetime
from django.contrib.gis.geos import GEOSGeometry
from django.db import connections
from django.http import HttpResponse



DATA_DUMP_QUERY = """
WITH
segment_meta_data AS (
  SELECT osm_id                        AS segment_id,
         ST_length(way)                AS segment_length,
         FLOOR(ST_length(way) / 200.0) AS num_blocks
  FROM philly_street_osm_line),

all_blocks AS
  (
    -- The scores for segments that appear on the left.  In this view, a score
    -- of 0 is losing, a score of 1 is winning.
    SELECT segment1_id as segment_id,
           block1_index as block_index
      FROM project_rating

    UNION

    -- The scores for segments that appear on the right.
    SELECT segment2_id as segment_id,
           block2_index as block_index
      FROM project_rating

    GROUP BY segment_id, block_index),

block_meta_data AS
  (SELECT smd.segment_id,
         block_index,
         segment_length,
         num_blocks,
         ((200 * block_index) / segment_length) AS block_start_percentage,
         ST_transform(ST_line_interpolate_point(way, (200 * block_index) / segment_length), 4326) AS point
  FROM segment_meta_data AS smd,
       all_blocks AS ab,
       philly_street_osm_line
  WHERE smd.segment_id = ab.segment_id
    AND smd.segment_id = osm_id)

SELECT meta1.point AS point1,
       meta2.point AS point2,
       rating.score AS score
  FROM block_meta_data AS meta1,
       block_meta_data AS meta2,
       project_rating as rating

  WHERE rating.segment1_id = meta1.segment_id
    AND rating.block1_index = meta1.block_index
    AND rating.segment2_id = meta2.segment_id
    AND rating.block2_index = meta2.block_index
"""

def csv_data(request):
    now = datetime.datetime.utcnow()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=beautifulst_data_%s.csv' % (now.strftime('%Y%m%d%H%M%S'), )

    # Get the data
    cursor = connections['default'].cursor()
    cursor.execute(DATA_DUMP_QUERY)

    data = cursor.fetchall()

    # Init the csv writer
    writer = csv.writer(response)

    # Write the header row
    keys = [col[0] for col in cursor.description]
    writer.writerow(['lat1','lon1','lat2','lon2','score'])

    # Write the contents
    for row in data:
        p1 = GEOSGeometry(row[0])
        p2 = GEOSGeometry(row[1])
        writer.writerow([p1.y, p1.x, p2.y, p2.x, row[2]])

    return response
