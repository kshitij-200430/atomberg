# Battery Check Reminder Script

---

## How it works

1. Read all locks from DynamoDB.
2. Find the ones where the last battery check is older than 30 days.
3. Look up which user is connected to each lock in PostgreSQL.
4. Send an FCM notification to those users.

---

## Files in this project

- `script.py`  
  This is the main file. It does everything in one place.

---

## What you need before running

Create a `.env` file in the same folder:

AWS_REGION=ap-south-1
DYNAMO_TABLE=locks

PG_HOST=sample-rds-host.amazonaws.com
PG_PORT=5432
PG_USER=sample_user
PG_PASSWORD=sample_password
PG_DATABASE=sample_db

FCM_SERVICE_ACCOUNT_JSON=./serviceAccountKey.json


Download your Firebase service account JSON and save it as `serviceAccountKey.json`.

You also need:
pip install boto3 psycopg2-binary firebase-admin python-dotenv

---

## How to run

Run the script with:

python script.py

This script can also be set to run weekly using cron or any scheduler.

---

## Example table structure

**DynamoDB (locks):**
- lock_id  
- last_battery_check  

**PostgreSQL (lock_user_mapping):**
- lock_id  
- user_id  
- fcm_id  

---

