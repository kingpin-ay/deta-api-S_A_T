from pydantic import BaseModel


class Feedback(BaseModel):
    email: str = None
    feedback: str = None
    name: str = None


class UserData(BaseModel):
    username: str = None
    password: str = None