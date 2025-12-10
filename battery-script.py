import os
import csv
from datetime import datetime, timedelta
import boto3
import psycopg2
from psycopg2.extras import execute_values
from firebase_admin import credentials, initialize_app, messaging


aws_region = 'ap-south-1'
dynamo_table = 'locks'
pg_conn = 'host=localhost dbname=testdb user=test password=test123'
service_file = 'keyfile.json'
campaign = datetime.utcnow().strftime('%Y%m%d')


dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table = dynamodb.Table(dynamo_table)
cred = credentials.Certificate(service_file)
initialize_app(cred)(cred)


cutoff = datetime.utcnow() - timedelta(days=30)
resp = table.scan()
items = resp.get('Items', [])
old_locks = []
for it in items:
ts = it.get('last_checked')
if not ts:
old_locks.append(it['lock_id'])
continue
try:
last = datetime.fromisoformat(ts)
except Exception:
try:
last = datetime.utcfromtimestamp(int(ts))
except Exception:
old_locks.append(it['lock_id'])
continue
if last < cutoff:
old_locks.append(it['lock_id'])


if not old_locks:
print('no stale locks')
raise SystemExit


conn = psycopg2.connect(PG_CONN_STR)
cur = conn.cursor()
query = "select lock_id, user_id, fcm_id from lock_user_mapping where lock_id = ANY(%s)"
cur.execute(query, (old_locks,))
rows = cur.fetchall()


sends = []
for lock_id, user_id, fcm_id in rows:
if not fcm_id:
continue
message = messaging.Message(
notification=messaging.Notification(title='Check your lock battery', body='Please check battery for lock {}'.format(lock_id)),
token=fcm_id,
data={'campaign_id': CAMPAIGN_ID, 'lock_id': str(lock_id), 'user_id': str(user_id), 'click_url': 'https://trackme.site/click?c=' + campaign + '&u=' + str(user_id) + '&l=' + str(lock_id)
)
try:
res = messaging.send(message)
sends.append((user_id, fcm_id, lock_id, res, datetime.utcnow().isoformat()))
except Exception as e:
sends.append((user_id, fcm_id, lock_id, 'ERROR:'+str(e), datetime.utcnow().isoformat()))


cur.close()
conn.close()


csvfile = f'sends_{CAMPAIGN_ID}.csv'
with open(csvfile, 'w', newline='') as f:
w = csv.writer(f)
w.writerow(['user_id','fcm_id','lock_id','message_id_or_error','sent_at'])
w.writerows(sends)


print('done. wrote', csvfile)
