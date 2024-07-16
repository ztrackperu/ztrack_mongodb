from typing import Optional,List
from pydantic import BaseModel, Field


class TunelSchema(BaseModel):
    data:str = Field(...)
    status: Optional[int] | None =1
    class Config:
        json_schema_extra = {
            "example": {
                "data": "TUNEL,ECUADOR,HORTIFRUIT:1A,123321,...",   
                "status" :1
            }
        }

#respuesta cuando todo esta bien
def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

#respuesta cuando algo sale mal 
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

