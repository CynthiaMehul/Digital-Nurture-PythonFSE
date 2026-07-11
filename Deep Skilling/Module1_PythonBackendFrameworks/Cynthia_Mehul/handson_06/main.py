from fastapi import FastAPI
from schemas import CourseCreate, CourseUpdate
from typing import Optional
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import select, delete
from models import Course
from contextlib import asynccontextmanager
from database import engine, Base
import models


@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app=FastAPI(title="Course Management API", version="1.0", lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "API Running"}

'''    
@app.post("/api/courses")
async def create_course(course: CourseCreate):
    return course
'''

@app.post("/api/courses/")
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = Course(
        name=course.name,
        code=course.code,
        credits=course.credits,
        department_id=course.department_id
    )
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course
''''
@app.get("/api/courses/{course_id}")
async def get_course(course_id: int):
    return {"course_id":course_id}
'''
@app.get("/api/courses/{course_id}")
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar()
    if course is None:
        return {"message": "Course not found"}
    return course

'''
@app.get("/api/courses/")
async def get_courses(skip: int=0, limit: int=10, department_id: Optional[int]=None):
    return {
        "skip":skip,
        "limit":limit,
        "deparment_id":department_id
    }
'''

@app.get("/api/courses/")
async def get_courses(skip: int = 0, limit: int = 10, department_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    query = select(Course)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

'''
@app.get("/api/courses/")
async def get_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    courses = result.scalars().all()
    return courses
'''


@app.put("/api/courses/{course_id}")
async def update_course(
    course_id: int,
    updated: CourseUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar()

    if course is None:
        return {"message": "Course not found"}

    if updated.name is not None:
        course.name = updated.name

    if updated.code is not None:
        course.code = updated.code

    if updated.credits is not None:
        course.credits = updated.credits

    if updated.department_id is not None:
        course.department_id = updated.department_id

    await db.commit()
    await db.refresh(course)

    return course

@app.delete("/api/courses/{course_id}")
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar()

    if course is None:
        return {"message": "Course not found"}

    await db.delete(course)
    await db.commit()

    return {"message": "Course deleted"}