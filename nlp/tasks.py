from nlp.models import record_aggregate
from django.db import connection


def generate_aggregate():
    cursor = connection.cursor()
    cursor.execute('''
        SELECT count(*) as 'count' ,api_name,
           date_format(created_at - interval 1 day, '%Y-%m-%d') AS `day_logged` 
           FROM textclassify.nlp_record group by `day_logged`,api_name
    ''')
    row = cursor.fetchone()
    rec_agg = record_aggregate(api_name=row['count'],api_name=row['count'],created_at=row)

