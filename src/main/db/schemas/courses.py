from src.main.db.schemas.files import CourseFileRead
from pydantic import Field, BaseModel, ConfigDict


class CourseBase(BaseModel):
    name: str = Field(..., example="Course Name")
    description: str = Field(..., example="Description of the course")
    level: int = Field(..., example=1)
    price: float = Field(..., example=19.99)

    model_config = ConfigDict(from_attributes=True)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: str | None = Field(None, example="Updated Course Name")
    description: str | None = Field(None, example="Updated description of the course")
    level: int | None = Field(None, example=2)
    price: float | None = Field(None, example=29.99)


class CourseRead(CourseBase):
    course_id: int
    files: list[CourseFileRead] = []
