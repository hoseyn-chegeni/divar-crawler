from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    description: str


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    jobs: list[Job] = []

    class Config:
        orm_mode = True
