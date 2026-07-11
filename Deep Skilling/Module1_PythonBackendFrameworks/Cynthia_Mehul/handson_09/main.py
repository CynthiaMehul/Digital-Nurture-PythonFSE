from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select   
from jose import jwt
from jose import JWTError
import models
import schemas
import security
from database import sessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_db():
    async with sessionLocal() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)
async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    email = payload.get("sub")
    result = await db.execute(select(models.User).where(models.User.email == email))
    user = result.scalar()

    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return user

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app=FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/v1/auth/register")
async def create_user(req:schemas.CreateUser,db:AsyncSession=Depends(get_db),response_model=schemas.UserResponse):
    user=await db.execute(select(models.User).where(models.User.email==req.email))
    user=user.scalar()

    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User exists with this email ID")
    
    new_user=models.User(email=req.email, hashed_password=security.get_password_hash(req.password), is_active=True)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/api/v1/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute(
        select(models.User).where(
            models.User.email == form_data.username
        )
    )
    user = user.scalar()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not security.verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = security.create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/api/v1/courses",response_model=schemas.CourseResponse,status_code=status.HTTP_201_CREATED)
async def create_course(req: schemas.CourseCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    course = models.Course(name=req.name,code=req.code,credits=req.credits)
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course

@app.get("/api/v1/courses",response_model=list[schemas.CourseResponse])
async def get_all_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Course))
    courses = result.scalars().all()
    return courses

@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} does not exist"
        )

    await db.delete(user)
    await db.commit()