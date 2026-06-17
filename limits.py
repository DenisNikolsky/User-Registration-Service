from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    name: str
    age: int

class UserRegistration(BaseModel):
    name: str = Field(min_length=4, max_length=23)
    age: int = Field(ge=18, le=99)
    password: str = Field(min_length=6)