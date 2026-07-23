use college_db;

-- 48)
EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students sr
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year=2022;


/*
49)
EXPLAIN Analysis:

- The students table uses a Full Table Scan (type = ALL)
  because there is no index on enrollment_year.

- The enrollments table uses the student_id index
  (type = ref), making the join efficient.

- The courses table uses the PRIMARY KEY
  (type = eq_ref), which is the most efficient join type
  for primary key lookups.

50)
Estimated rows examined:
- students     : 8
- enrollments  : 1
- courses      : 1
*/

-- 51)
CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);
SHOW INDEX FROM students;

-- 52)
CREATE UNIQUE INDEX idx_enrollments_student_course ON enrollments(student_id, course_id);
SHOW INDEX FROM enrollments;

-- 53)
CREATE INDEX idx_course_code ON courses(course_code);
SHOW INDEX FROM courses;

-- 54)
EXPLAIN
SELECT
    s.first_name,
    s.last_name,
    c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year=2022;

/*
EXPLAIN Comparison

Before adding indexes:
- The students table performed a Full Table Scan (type = ALL).
- MySQL scanned all rows to find students with enrollment_year = 2022.

After adding indexes:
- MySQL uses the index on students.enrollment_year to filter matching rows.
- The query plan shows an Index Scan ref instead of a Full Table Scan.
- This reduces the number of rows examined and improves query performance.
- The indexes on enrollments(student_id, course_id) and courses(course_code)
  also help optimize joins and prevent duplicate enrollments.
*/


-- 55)
/*

MySQL does not support partial indexes with a WHERE clause.
Instead, a normal index was created on enrollments(student_id).

If using PostgreSQL, the equivalent partial index would be:

CREATE INDEX idx_enrollment_pending
ON enrollments(student_id)
WHERE grade IS NULL;
*/

