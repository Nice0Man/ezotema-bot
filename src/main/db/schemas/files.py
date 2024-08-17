from pydantic import BaseModel, Field, ConfigDict


class FileBase(BaseModel):
    filename: str = Field(..., example="example.pdf")
    content_type: str = Field(..., example="application/pdf")

    model_config = ConfigDict(from_attributes=True)


class FileCreate(FileBase):
    content: bytes


class FileUpdate(BaseModel):
    filename: str | None = Field(None, example="example.pdf")
    content: bytes | None
    content_type: str | None = Field(None, example="application/pdf")


class CourseFileRead(FileBase):
    file_id: int
    course_id: int
