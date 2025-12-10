# Battery Check Reminder Script

---

## What it does


1. Scans DynamoDB table `locks` for `last_checked` older than 30 days.
2. Looks up users and their `fcm_id` from Postgres table `lock_user_mapping`.
3. Sends an FCM notification to each `fcm_id`.
4. Writes a CSV `sends_YYYYMMDD.csv` with results.


## Tracking clicks / measuring effectiveness


The notification includes a `click_url` in the message data that points to a tracking endpoint you must provide. When users click, that endpoint should record the click (campaign, user, lock). Weekly you can compare number of clicks vs number of notifications sent from the CSV to measure effectiveness.


## Requirements


- Python 3.9+
- boto3
- psycopg2-binary
- firebase-admin


## Setup


1. Put your Firebase service account JSON path in env var `FIREBASE_SERVICE_ACCOUNT` or name the file `serviceAccount.json`.
2. Set env vars:
- `AWS_REGION` (default `ap-south-1`)
- `DYNAMO_TABLE` (default `locks`)
- `PG_CONN` (e.g. `host=... dbname=... user=... password=...`)
3. Ensure DynamoDB `locks` items have `lock_id` and `last_checked` (ISO8601 or unix seconds).
4. Ensure Postgres table `lock_user_mapping(lock_id, user_id, fcm_id)` exists.


## Run
battery-script.py
