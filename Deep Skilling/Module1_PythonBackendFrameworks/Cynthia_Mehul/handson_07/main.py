from fastapi import FastAPI, Depends, status, HTTPException, BackgroundTasks
import models
import schemas
from database import sessionLocal, Base, engine
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Course Management API",
    description="API for managing courses, students and enrollments.",
    version="1.0.0",

    contact={
        "name": "Cynthia",
        "email": "cynthia@example.com"
    },
    lifespan=lifespan
)

async def get_db():
    async with sessionLocal() as session:
        yield session

def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")

@app.get('/')
def root():
    return {'message': 'API running'}

@app.post('/api/courses/', tags=["Courses"], 
          status_code=status.HTTP_201_CREATED, 
          response_model=schemas.CourseResponse,
          summary="Create a new course",
          response_description="The created course")
async def add_course(req: schemas.CourseCreate, db: AsyncSession=Depends(get_db)):
    new_course=models.Course(name=req.name, code=req.code, 
                             credits=req.credits, department_id=req.department_id)
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

@app.get('/api/courses/', tags=["Courses"], response_model=list[schemas.CourseResponse])
async def get_courses(db: AsyncSession=Depends(get_db)):
    courses = await db.execute(select(models.Course))
    courses = courses.scalars().all()
    return courses

@app.get("/api/courses/{id}", tags=["Courses"], response_model=schemas.CourseResponse)
async def get_course_by_id(id:int,db:AsyncSession=Depends(get_db)):
    course=await db.execute(select(models.Course).where(models.Course.course_id==id))
    course=course.scalar()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Course not found")
    return course

@app.put("/api/courses/{id}", tags=["Courses"], response_model=schemas.CourseResponse)
async def update_course(id:int, updated:schemas.CourseUpdate, db:AsyncSession=Depends(get_db)):
    course=await db.execute(select(models.Course).where(models.Course.course_id==id))
    course=course.scalar()

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Course not found")
    
    if updated.name is not None:
        course.name=updated.name
    if updated.code is not None:
        course.code=updated.code
    if updated.credits is not None:
        course.credits=updated.credits
    if updated.department_id is not None:
        course.department_id=updated.department_id

    await db.commit()
    await db.refresh(course)
    return course

@app.delete("/api/courses/{id}", tags=["Courses"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id:int, db:AsyncSession=Depends(get_db)):
    course=await db.execute(select(models.Course).where(models.Course.course_id==id))
    course=course.scalar()
    
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Course not found")
    
    await db.delete(course)
    await db.commit()

@app.get('/api/courses/{id}/students', tags=["Courses"], response_model=list[schemas.StudentResponse])
async def get_students_enrolled_in_course(id:int, db:AsyncSession=Depends(get_db)):
    students=await db.execute(select(models.Student).join(models.Enrollment).where(models.Enrollment.course_id==id))
    students=students.scalars().all()
    return students


@app.post("/api/students/",tags=["Students"], status_code=status.HTTP_201_CREATED,response_model=schemas.StudentResponse)
async def create_student(req: schemas.StudentCreate,db: AsyncSession = Depends(get_db)):
    student = models.Student(**req.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student

@app.get("/api/students/",tags=["Students"], response_model=list[schemas.StudentResponse])
async def get_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student))
    return result.scalars().all()

@app.get("/api/students/{id}",tags=["Students"], response_model=schemas.StudentResponse)
async def get_student(id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.student_id == id))
    student = result.scalar()

    if student is None:
        raise HTTPException(status_code=404,detail="Student not found")
    return student

@app.put("/api/students/{id}",tags=["Students"], response_model=schemas.StudentResponse)
async def update_student(id: int,updated: schemas.StudentUpdate,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.student_id == id))
    student = result.scalar()

    if student is None:
        raise HTTPException(status_code=404,detail="Student not found")

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(student, key, value)

    await db.commit()
    await db.refresh(student)
    return student

@app.delete("/api/students/{id}",tags=["Students"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.student_id == id))
    student = result.scalar()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    await db.delete(student)
    await db.commit()


@app.post("/api/enrollments/",tags=["Enrollments"], status_code=status.HTTP_201_CREATED,response_model=schemas.EnrollmentResponse)
async def create_enrollment(req: schemas.EnrollmentCreate,background_tasks: BackgroundTasks,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Student).where(models.Student.student_id == req.student_id))
    student = result.scalar()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    enrollment = models.Enrollment(**req.model_dump())

    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)

    background_tasks.add_task(
        send_confirmation_email,
        student.email
    )
    return enrollment

@app.get("/api/enrollments/",tags=["Enrollments"], response_model=list[schemas.EnrollmentResponse])
async def get_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment))
    return result.scalars().all()

@app.get("/api/enrollments/{id}",tags=["Enrollments"], response_model=schemas.EnrollmentResponse)
async def get_enrollment(id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).where(models.Enrollment.enrollment_id == id))
    enrollment = result.scalar()

    if enrollment is None:
        raise HTTPException(status_code=404,detail="Enrollment not found")

    return enrollment

@app.put("/api/enrollments/{id}",tags=["Enrollments"], response_model=schemas.EnrollmentResponse)
async def update_enrollment(id: int,updated: schemas.EnrollmentUpdate,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).where(models.Enrollment.enrollment_id == id))
    enrollment = result.scalar()

    if enrollment is None:
        raise HTTPException(
            status_code=404,
            detail="Enrollment not found"
        )

    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(enrollment, key, value)

    await db.commit()
    await db.refresh(enrollment)
    return enrollment

@app.delete("/api/enrollments/{id}",tags=["Enrollments"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(id: int,db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Enrollment).where(models.Enrollment.enrollment_id == id))
    enrollment = result.scalar()

    if enrollment is None:
        raise HTTPException(status_code=404,detail="Enrollment not found")

    await db.delete(enrollment)
    await db.commit()





