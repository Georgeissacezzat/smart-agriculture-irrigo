from pydantic import BaseModel
from typing import Optional


class SignUpUser (BaseModel):
    firstname : str
    lastname : str
    email : str
    password : str

class SignInUser (BaseModel):
    email : str
    password : str

class Updated_User(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None