from fastapi import FastAPI, Depends, status, HTTPException, Response
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from typing import Optional
import models
import schemas
from database import sessionLocal, engine
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError


@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app=FastAPI(title="API", lifespan=lifespan)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    code = "ERROR"

    if exc.status_code == 404:
        code = "NOT_FOUND"
    elif exc.status_code == 400:
        code = "BAD_REQUEST"
    elif exc.status_code == 401:
        code = "UNAUTHORIZED"
    elif exc.status_code == 422:
        code = "UNPROCESSABLE_ENTITY"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": exc.detail,
                "field": None
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = exc.errors()[0]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "UNPROCESSABLE_ENTITY",
                "message": error["msg"],
                "field": error["loc"][-1]
            }
        }
    )

async def get_db():
    async with sessionLocal() as session:
        yield session


@app.get("/")
def root():
    return {"message":"API Running"}


# ---------------- API Versioning ----------------
# URL Versioning:
# Uses the API version in the URL (e.g. /api/v1/courses).
# It is simple, easy to understand, and convenient for testing.

# Header Versioning:
# Sends the API version in the request header
# (Accept: application/vnd.api+json;version=1).
# It keeps URLs clean but is harder to test and configure.
# -----------------------------------------------
@app.get("/api/v1/courses", status_code=status.HTTP_200_OK)
async def get_courses(db:AsyncSession=Depends(get_db), page: int=1, page_size: int=2, search: Optional[str]=None):
    offset=(page-1)*page_size
    query=select(models.Course)
    if search:
        query=query.where(
            or_(
                models.Course.name.ilike(f"%{search}%"),
                models.Course.code.ilike(f"%{search}%")
            )
        )
    count_query=select(func.count()).select_from(query.subquery())
    total=await db.scalar(count_query)
    query=query.offset(offset).limit(page_size)
    courses=await db.execute(query)
    courses=courses.scalars().all()

    if courses is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found")
    next_url=None
    prev_url=None

    if offset+page_size<total:
        next_url=f"/api/v1/courses?page={page+1}&page_size={page_size}"
    if page>1:
        prev_url=f"/api/v1/courses?page={page-1}&page_size={page_size}"
    return {
        "count": total,
        "next": next_url,
        "previous": prev_url,
        "results": courses
    }

@app.get("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, status_code=status.HTTP_200_OK)
async def get_course_by_id(course_id: int, db:AsyncSession=Depends(get_db)):
    course=await db.execute(select(models.Course).where(models.Course.course_id==course_id))
    course=course.scalar()
    
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found")
    
    return course

@app.post("/api/v1/courses", response_model=schemas.CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(req:schemas.CourseCreate, response: Response, db:AsyncSession=Depends(get_db)):
    if req.credits<0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credits cannot be negative")
    new_course=models.Course(name=req.name, code=req.code, 
            credits=req.credits, department_id=req.department_id)
    
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    response.headers["Location"]=f"/api/v1/courses/{new_course.course_id}"
    return new_course

@app.put("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, status_code=status.HTTP_200_OK)
async def complete_course_update(course_id: int, req:schemas.CourseCreate, db:AsyncSession=Depends(get_db)):
    course=await db.execute(select(models.Course).where(models.Course.course_id==course_id))
    course=course.scalar()

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found")
    
    course.name=req.name
    course.code=req.code
    course.credits=req.credits
    course.department_id=req.department_id

    await db.commit()
    await db.refresh(course)
    return course

@app.patch("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, status_code=status.HTTP_200_OK)
async def partial_course_update(course_id: int, req:schemas.CourseUpdate, db:AsyncSession=Depends(get_db)):
    course=await db.execute(select(models.Course).where(models.Course.course_id==course_id))
    course=course.scalar()

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found")
    if req.name is not None:
        course.name=req.name
    if req.code is not None:
        course.code=req.code
    if req.credits is not None:
        course.credits=req.credits
    if req.department_id is not None:
        course.department_id=req.department_id

    await db.commit()
    await db.refresh(course)
    return course

@app.delete("/api/v1/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id:int, db:AsyncSession=Depends(get_db)):
    course=await db.execute(select(models.Course).where(models.Course.course_id==course_id))
    course=course.scalar()

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found")
    
    await db.delete(course)
    await db.commit()







