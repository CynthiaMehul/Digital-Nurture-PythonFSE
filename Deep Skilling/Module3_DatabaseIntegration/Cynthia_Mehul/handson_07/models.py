from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    CHAR,
    Boolean
)
from sqlalchemy.orm import declarative_base, relationship

engine = create_engine(
    "mysql+mysqlconnector://root:root@localhost/college_db_orm",
    echo=True
)

Base = declarative_base()

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False)

    students = relationship("Student", back_populates="department")
    professors = relationship("Professor", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    enrollment_year = Column(Integer)
    is_active=Column(Boolean,default=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(20), unique=True)
    course_name = Column(String(100))
    credits = Column(Integer)

    enrollments = relationship("Enrollment", back_populates="course")
    schedules = relationship("CourseSchedule", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(
        Integer,
        ForeignKey("students.student_id")
    )
    course_id = Column(
        Integer,
        ForeignKey("courses.course_id")
    )
    enrollment_date = Column(Date)
    grade = Column(CHAR(2))

    student = relationship(
        "Student",
        back_populates="enrollments"
    )
    course = relationship(
        "Course",
        back_populates="enrollments"
    )


class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(
        Integer,
        ForeignKey("departments.department_id")
    )

    department = relationship(
        "Department",
        back_populates="professors"
    )

class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id=Column(Integer,primary_key=True,autoincrement=True)
    course_id=Column(Integer, ForeignKey("courses.course_id"))
    day_of_week=Column(String(20), nullable=False)
    start_time=Column(String(10), nullable=False)
    end_time=Column(String(10), nullable=False)

    course=relationship("Course", back_populates="schedules")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("All tables created successfully!")