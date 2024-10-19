from pydantic import BaseModel, Field, ConfigDict


# Base schema with common fields
class UserBase(BaseModel):
    username: str = Field(..., example="example_user")
    chat_id: int = Field(..., example=123456789)
    email: str | None = None

    model_config = ConfigDict(from_attributes=True)


# Schema for creating a new user
class UserCreate(UserBase):
    id: int = Field(..., example=1)


# Schema for reading user data
class UserRead(UserBase):
    id: int


# Schema for updating user data
class UserUpdate(BaseModel):
    email: str | None = Field(None, example="user@mail.com")
    username: str | None = Field(None, example="new_username")
    chat_id: int | None = Field(None, example=987654321)
