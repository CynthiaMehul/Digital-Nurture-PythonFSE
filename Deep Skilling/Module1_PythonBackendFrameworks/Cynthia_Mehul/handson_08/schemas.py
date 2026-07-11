from pydantic import BaseModel, ConfigDict
from typing import Optional

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int

class CourseUpdate(BaseModel):
    name: Optional[str]=None
    code: Optional[str]=None
    credits: Optional[int]=None
    department_id: Optional[int]=None

class CourseResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    course_id: int
    name: str
    code: str
    credits: int
    department_id: int
