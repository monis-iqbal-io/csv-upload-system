import csv
import os
from datetime import datetime
import pytz
from utils.db import get_connection

# In-memory progress tracker
progress_store = {}


def process_csv(file_path, mapping):

    file_name = os.path.basename(file_path)

    conn = get_connection()
    cursor = conn.cursor()

    inserted_count = 0
    updated_count = 0

    try:
        #LOAD CSV
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            rows = list(csv.DictReader(csvfile))

        total_rows = len(rows)

        #INIT PROGRESS
        progress_store[file_name] = {
            "status": "processing",
            "progress": 0,
            "inserted": 0,
            "updated": 0,
            "total": total_rows
        }

        ist = pytz.timezone('Asia/Kolkata')

        #INSERT INTO HISTORY TABLE
        cursor.execute("""
            INSERT INTO upload_files
            (file_name, total_rows, inserted_rows, updated_rows, status, upload_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (file_name, total_rows, 0, 0, 'processing', datetime.now(ist)))

        upload_id = cursor.fetchone()[0]
        conn.commit()

        #PROCESS LOOP
        for i, row in enumerate(rows):

            processed_data = {}

            #APPLY MAPPING
            for csv_field, db_field in mapping.items():
                processed_data[db_field] = row.get(csv_field)

            mobile = processed_data.get('mobile')

            #SKIP INVALID
            if not mobile:
                continue

            mobile = str(mobile).strip()    

            #Mobile should be digits and at least 10 characters long
            if not mobile.isdigit() or len(mobile) < 10:
                continue

            #CHECK EXISTING
            cursor.execute("SELECT id FROM users WHERE mobile=%s", (mobile,))
            existing = cursor.fetchone()

            if existing:
                #UPDATE
                cursor.execute("""
                    UPDATE users
                    SET name=%s, email=%s, city=%s, date=%s, file_name=%s
                    WHERE mobile=%s
                """, (
                    processed_data.get('name'),
                    processed_data.get('email'),
                    processed_data.get('city'),
                    processed_data.get('date'),
                    file_name,
                    mobile
                ))
                updated_count += 1
            else:
                #INSERT
                cursor.execute("""
                    INSERT INTO users (name, mobile, email, city, date, file_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    processed_data.get('name'),
                    mobile,
                    processed_data.get('email'),
                    processed_data.get('city'),
                    processed_data.get('date'),
                    file_name
                ))
                inserted_count += 1

            #CALCULATE PROGRESS
            processed = inserted_count + updated_count
            progress = int((processed / total_rows) * 100)

            #UPDATE LIVE STORE
            progress_store[file_name] = {
                "status": "processing",
                "progress": progress,
                "inserted": inserted_count,
                "updated": updated_count,
                "total": total_rows
            }

            #COMMIT IN BATCHES
            if i % 50 == 0:
                conn.commit()

        #FINAL STATUS UPDATE
        progress_store[file_name]["status"] = "completed"
        progress_store[file_name]["progress"] = 100

        cursor.execute("""
            UPDATE upload_files
            SET inserted_rows=%s,
                updated_rows=%s,
                status=%s
            WHERE id=%s
        """, (inserted_count, updated_count, 'completed', upload_id))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("ERROR in process_csv:", e)

        progress_store[file_name] = {
            "status": "failed",
            "progress": 0,
            "inserted": 0,
            "updated": 0,
            "total": 0
        }

    finally:
        cursor.close()
        conn.close()