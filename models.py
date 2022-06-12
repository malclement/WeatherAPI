from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    password: str = Field(...)
    email: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Clement Malige",
                "password": "weakpassword",
                "email": "clement.malige@ensea.fr"
            }
        }


class UserLoginSchema(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "clement.malige@ensea.fr",
                "password": "weakpassword"
            }
        }