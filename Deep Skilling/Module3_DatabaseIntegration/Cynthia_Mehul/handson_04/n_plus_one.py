# Step 56

import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="college_db"
)

cursor = conn.cursor(dictionary=True)

query_count = 0
start = time.time()

cursor.execute("SELECT * FROM enrollments")
query_count += 1
enrollments = cursor.fetchall()

for enrollment in enrollments:
    cursor.execute(
    "SELECT first_name FROM students WHERE student_id=%s",
    (enrollment["student_id"],)
    )
    query_count += 1
    student = cursor.fetchone()
    print(student["first_name"])

end = time.time()

print(f"\nQueries executed: {query_count}")
print(f"Execution Time: {end-start:.6f} seconds")