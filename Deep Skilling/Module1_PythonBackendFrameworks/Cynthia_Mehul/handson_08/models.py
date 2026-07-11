from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base=declarative_base()

class Course(Base):
    __tablename__="courses"
    course_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, unique=True)
    credits = Column(Integer)
    department_id = Column(Integer)

