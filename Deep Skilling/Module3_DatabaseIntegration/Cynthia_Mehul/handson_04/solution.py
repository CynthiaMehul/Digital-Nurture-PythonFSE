# Step 57

import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="college_db"
)

cursor = conn.cursor(dictionary=True)

start = time.time()

cursor.execute("""
SELECT
e.enrollment_id,
s.first_name
FROM enrollments e
JOIN students s
ON s.student_id=e.student_id
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

end = time.time()

print("\nQueries Executed: 1")
print("Time Taken:", end-start)