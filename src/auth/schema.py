from pydantic import BaseModel, EmailStr



class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserRegisterSchema(UserLoginSchema):
    username: str