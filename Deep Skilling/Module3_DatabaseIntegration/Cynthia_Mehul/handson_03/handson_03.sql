use college_db;

-- 35)
SELECT e.student_id, s.first_name, s.last_name FROM enrollments e 
JOIN students s ON e.student_id=s.student_id 
GROUP BY student_id 
HAVING COUNT(*) > 
(SELECT AVG(count_of_enrollments) FROM 
(SELECT COUNT(*) as count_of_enrollments FROM enrollments e GROUP BY student_id) 
AS number_of_enrollments); 

-- 36) 
SELECT c.course_id FROM courses c 
WHERE NOT EXISTS 
(SELECT * FROM enrollments e 
WHERE e.course_id=c.course_id 
AND e.grade!='A');

-- 37)
SELECT p1.prof_name, p1.salary, d.dept_name
FROM professors p1
JOIN departments d
ON p1.department_id=d.department_id
WHERE p1.salary=(SELECT MAX(p2.salary) FROM professors p2 
WHERE p2.department_id = p1.department_id);

-- 38)
SELECT dept_name, avg_salary
FROM (SELECT d.dept_name, AVG(p.salary) AS avg_salary
FROM departments d
JOIN professors p
ON d.department_id = p.department_id
GROUP BY d.dept_name
) AS salary_table
WHERE avg_salary > 85000;

-- 39) 
CREATE VIEW vw_student_enrollment_summary AS
SELECT s.student_id, CONCAT(s.first_name,' ',s.last_name) AS student_name, d.dept_name,
COUNT(e.course_id) AS total_courses,
AVG(
	CASE
		WHEN e.grade='A' THEN 4
		WHEN e.grade='B' THEN 3
		WHEN e.grade='C' THEN 2
		WHEN e.grade='D' THEN 1
		WHEN e.grade='F' THEN 0
	END
) AS GPA
FROM students s
JOIN departments d
ON s.department_id=d.department_id
LEFT JOIN enrollments e
ON s.student_id=e.student_id
GROUP BY s.student_id,student_name,d.dept_name;

SELECT * from vw_student_enrollment_summary;

-- 40)
CREATE VIEW vw_course_stats AS
SELECT course_name, course_code, COUNT(e.student_id) as total_enrollments, 
AVG(
	CASE
		WHEN e.grade='A' THEN 4
		WHEN e.grade='B' THEN 3
		WHEN e.grade='C' THEN 2
		WHEN e.grade='D' THEN 1
		WHEN e.grade='F' THEN 0
	END
) AS avg_gpa
FROM courses c 
JOIN enrollments e 
ON c.course_id=e.course_id
GROUP BY c.course_id;

SELECT * from vw_course_stats;


-- 41)
CREATE VIEW vw_student_enrollment_summary_2 AS
SELECT s.student_id, CONCAT(s.first_name,' ',s.last_name) AS student_name, d.dept_name,
COUNT(e.course_id) AS total_courses,
AVG(
	CASE
		WHEN e.grade='A' THEN 4
		WHEN e.grade='B' THEN 3
		WHEN e.grade='C' THEN 2
		WHEN e.grade='D' THEN 1
		WHEN e.grade='F' THEN 0
	END
) AS GPA
FROM students s
JOIN departments d
ON s.department_id=d.department_id
LEFT JOIN enrollments e
ON s.student_id=e.student_id
GROUP BY s.student_id,student_name,d.dept_name
HAVING GPA>3.0;

SELECT * from vw_student_enrollment_summary_2;

-- 42)

UPDATE vw_student_enrollment_summary
SET grade = 'A'
WHERE student_id = 1;

-- Multi-table views are generally not updatable because
-- the data comes from more than one base table.
-- The DBMS cannot always determine which underlying table
-- should be modified when an UPDATE, INSERT, or DELETE is issued.

-- 43) 

DROP VIEW vw_student_enrollment_summary;
DROP VIEW vw_course_stats;

-- CREATE VIEW vw_student_enrollment_summary AS
-- SELECT
--     *
-- FROM students
-- WITH CHECK OPTION;

CREATE VIEW vw_student_enrollment_summary AS
SELECT *
FROM students
WHERE department_id = 1
WITH CHECK OPTION;

-- The update is rejected since view is created with CHECK OPTION
UPDATE vw_student_enrollment_summary SET department_id=2 WHERE student_id=1; 

-- 44)

DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_enrollment_date DATE
)
BEGIN
    DECLARE enrollment_count INT;

    SELECT COUNT(*)
    INTO enrollment_count
    FROM enrollments
    WHERE student_id = p_student_id
      AND course_id = p_course_id;

    IF enrollment_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student already enrolled.';
    ELSE
        INSERT INTO enrollments
        (student_id, course_id, enrollment_date)
        VALUES
        (p_student_id, p_course_id, p_enrollment_date);
    END IF;

END$$

DELIMITER ;

CALL sp_enroll_student(1,3,'2025-03-28');
select * from enrollments;

-- 45)

CREATE TABLE department_transfer_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_department INT,
    new_department INT,
    transfer_date DATE
);



DELIMITER $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id INT,
    IN p_new_department INT
)
BEGIN
    DECLARE old_dept INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		ROLLBACK;
	END;

    
    SELECT department_id INTO old_dept 
    FROM students WHERE student_id = p_student_id;

    START TRANSACTION;
		UPDATE students
		SET department_id = p_new_department
		WHERE student_id = p_student_id;

		INSERT INTO department_transfer_log
		(student_id, old_department, new_department, transfer_date)
		VALUES (p_student_id, old_dept, p_new_department, CURDATE());
    COMMIT;
END$$

DELIMITER ;

-- 46)
-- department_transfer_log table remains empty indicating the transaction is 
-- successfully rolled back since department_id 999 does not exist.
CALL sp_transfer_student(5,999);
select * from department_transfer_log;

-- 47)

DELIMITER $$
CREATE PROCEDURE savepoint_insert()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
		ROLLBACK TO SAVEPOINT first_insert;
	END;

    START TRANSACTION;
	INSERT INTO enrollments (student_id, course_id, enrollment_date)
	VALUES (3,2,'2026-07-21');
    
    SAVEPOINT first_insert;
    
    INSERT INTO enrollments (student_id, course_id, enrollment_date)
	VALUES (999,3,'2026-04-21');
COMMIT;
END$$
DELIMITER ;

CALL savepoint_insert();
-- The first enrollment is seen in the table but the second insert statement is rejected.
SELECT * from enrollments;
