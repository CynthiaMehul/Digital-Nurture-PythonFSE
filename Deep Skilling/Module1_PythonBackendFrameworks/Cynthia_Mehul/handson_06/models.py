from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(20))
    credits: Mapped[int]
    department_id: Mapped[int]