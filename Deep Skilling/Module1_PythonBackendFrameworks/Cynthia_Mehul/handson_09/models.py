from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base=declarative_base()

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    email=Column(String, unique=True)
    hashed_password=Column(String)
    is_active=Column(Boolean, default=True)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    credits = Column(Integer, nullable=False)