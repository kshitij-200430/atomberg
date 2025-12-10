# battery-check

Simple weekly script to notify users whose locks haven't had a battery check in 30 days.
Minimal Python version. No Flask. Tracking server uses Python stdlib.

## Files
- send_weekly_notifications.py  -> scan DynamoDB, query Postgres, send FCM messages
- track_server_simple.py       -> tiny HTTP server that logs clicks into Postgres
- db_schema.sql                -> Postgres tables to create
- .env.example                 -> environment variables

## Setup
1. Create Postgres tables:
   psql -h <host> -U <user> -d <db> -f db_schema.sql

2. Create a Firebase service account JSON and put path in .env

3. Copy .env.example to .env and fill values.

4. Install deps:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

## Run for testing
1. Start tracking server (public domain recommended for real use):
   python track_server_simple.py

2. Run sender:
   python send_weekly_notifications.py

## Schedule
Use cron or EventBridge to run send_weekly_notifications.py weekly.

## Notes
- DynamoDB `locks` table must have `lock_id` (string) and `last_battery_check` (ISO string).
- Postgres `lock_user_mapping` must have `lock_id`, `user_id`, `fcm_id`.
- Tracking works by opening the URL in the notification; it inserts a row into `notification_clicks`.
