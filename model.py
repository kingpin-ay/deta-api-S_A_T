from pydantic import BaseModel


class Feedback(BaseModel):
    name : str = None
    email : str = None
    feedback : str = None