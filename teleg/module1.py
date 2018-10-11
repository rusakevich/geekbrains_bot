from google.cloud import bigquery
import os
#from google.cloud.bigquery import Dataset
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/v_rusakevich/Documents/Виджеты power bi/Yolla-d505c9833f92.json'
client = bigquery.Client()
QUERY = (
'SELECT geo.country,count(distinct user_pseudo_id) as volume '
'FROM  `yolla-33cfc.analytics_152199848.events_201*` '
'WHERE event_name = "ecommerce_purchase" and event_date = @dates '
'group by geo.country ')

param = bigquery.ScalarQueryParameter('dates', 'STRING', '20180802')

job_config = bigquery.QueryJobConfig()
job_config.query_parameters = [param]

query_job = client.query(QUERY, job_config=job_config) 


rows = query_job.result()
for row in rows:
    print(row.country, row.volume)

