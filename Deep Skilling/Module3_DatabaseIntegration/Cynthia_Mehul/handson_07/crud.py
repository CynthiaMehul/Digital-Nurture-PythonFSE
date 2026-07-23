"""
Step 90 - Comparison

Before (Lazy Loading)
---------------------
Queries Executed : 5
Loading Strategy : Lazy Loading
Performance      : Multiple database round-trips

After (Eager Loading)
------------------
Queries Executed : 1
Loading Strategy : Eager Loading
Performance      : Single database round-trip

joinedload() eliminates the N+1 Query Problem by fetching all
related objects in one SQL query using JOINs.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from models import (
    Department,
    Student,
    Course,
    Enrollment,
)

engine = create_engine(
    "mysql+mysqlconnector://root:root@localhost/college_db_orm",
    echo=True
)

Session = sessionmaker(bind=engine)
session = Session()

dept1 = Department(
    dept_name="Computer Science"
)

dept2 = Department(
    dept_name="Artificial Intelligence"
)

dept3 = Department(
    dept_name="Electronics"
)

session.add_all([
    dept1,
    dept2,
    dept3
])

session.commit()


student1 = Student(
    first_name="Cynthia",
    last_name="J",
    email="cynthia@example.com",
    enrollment_year=2024,
    department=dept2
)

student2 = Student(
    first_name="Rahul",
    last_name="K",
    email="rahul@example.com",
    enrollment_year=2023,
    department=dept1
)

student3 = Student(
    first_name="Priya",
    last_name="S",
    email="priya@example.com",
    enrollment_year=2022,
    department=dept2
)

student4 = Student(
    first_name="Arun",
    last_name="M",
    email="arun@example.com",
    enrollment_year=2023,
    department=dept3
)

student5 = Student(
    first_name="Neha",
    last_name="P",
    email="neha@example.com",
    enrollment_year=2024,
    department=dept1
)

session.add_all([
    student1,
    student2,
    student3,
    student4,
    student5
])

session.commit()


from datetime import date

course1 = Course(
    course_code="CS101",
    course_name="Database Systems",
    credits=4
)

course2 = Course(
    course_code="CS102",
    course_name="Operating Systems",
    credits=3
)

course3 = Course(
    course_code="CS103",
    course_name="Computer Networks",
    credits=4
)

session.add_all([
    course1,
    course2,
    course3
])

session.commit()

enrollment1 = Enrollment(
    student=student1,
    course=course1,
    enrollment_date=date(2024, 7, 1),
    grade="A"
)

enrollment2 = Enrollment(
    student=student2,
    course=course2,
    enrollment_date=date(2024, 7, 2),
    grade="B"
)

enrollment3 = Enrollment(
    student=student3,
    course=course1,
    enrollment_date=date(2024, 7, 3),
    grade="A"
)

enrollment4 = Enrollment(
    student=student4,
    course=course3,
    enrollment_date=date(2024, 7, 4),
    grade="C"
)

session.add_all([
    enrollment1,
    enrollment2,
    enrollment3,
    enrollment4
])

session.commit()

# Step 83
students = session.query(Student).join(Department).filter(
    Department.dept_name == "Computer Science"
).all()

for student in students:
    print(
        student.first_name,
        student.last_name,
        student.department.dept_name
   )

# # Step 84

enrollments = session.query(Enrollment).all()

for enrollment in enrollments:
    print(
        enrollment.student.first_name,
        "-",
        enrollment.course.course_name
    )

"""
Observation

With echo=True, SQLAlchemy executed multiple SQL queries.

One query retrieved all enrollments.

Additional queries were executed to retrieve the related
Student and Course objects.

This is known as the N+1 Query Problem.
"""

# Step 85

student = session.query(Student).filter(
    Student.email == "cynthia@example.com"
).first()

student.enrollment_year = 2025

session.commit()

print(student.first_name, student.enrollment_year)

# Step 86

enrollment = session.query(Enrollment).first()
session.delete(enrollment)
session.commit()
print("Enrollment deleted successfully!")

print("\nRemaining Enrollments:")
remaining = session.query(Enrollment).all()
for e in remaining:
    print(
        e.enrollment_id,
        e.student.first_name,
        "-",
        e.course.course_name
    )


"""
Step 87 

Using lazy loading, SQLAlchemy executed multiple SQL queries.

Observed:
- 1 query to fetch enrollments
- Additional queries to fetch Student objects
- Additional queries to fetch Course objects

This behavior is known as the N+1 Query Problem.
"""

# Step 88

enrollments = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    ).all()
)

print("\nEnrollment Details:\n")

for enrollment in enrollments:
    print(
        enrollment.student.first_name,
        "-",
        enrollment.course.course_name
    )


"""
Step 89

When querying enrollments using:

    session.query(Enrollment).all()

SQLAlchemy first retrieves all Enrollment records.
When enrollment.student or enrollment.course is accessed,
SQLAlchemy issues additional SQL queries to fetch the related
Student and Course objects.

Observed SQL Queries:
- 1 query to fetch all enrollments
- 2 queries to fetch Student records
- 2 queries to fetch Course records

Total SQL Queries: 5

This behavior is called the N+1 Query Problem because one query
retrieves the parent objects and additional queries are executed
for each related object.

When querying enrollments using:

    session.query(Enrollment).options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    ).all()

SQLAlchemy generated a single SQL statement with LEFT OUTER JOINs
to retrieve Enrollment, Student and Course data together.

Observed SQL Queries:
- 1 JOIN query

Total SQL Queries: 1

No additional SQL statements were executed while accessing:

    enrollment.student.first_name
    enrollment.course.course_name

"""