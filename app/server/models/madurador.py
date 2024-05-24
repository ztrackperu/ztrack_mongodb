from typing import Optional,List
from pydantic import BaseModel, Field

class SolicitudMaduradorSchema(BaseModel):
    device:str = Field(...)
    ultima: str = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"
    page: Optional[int] | None =1
    size: Optional[int] | None =3200
    empresa: Optional[int] | None =22
    class Config:
        json_schema_extra = {
            "example": {
                "device": "ZGRU9015808",
                "ultima": "2024-05-18T10:11:04",
                "fechaI": "2024-04-18T11:11:04",
                "fechaF": "2024-04-18T13:11:04", 
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

class DatosMadurador(BaseModel):
    id:int = Field(...)
    return_air: float = Field(...)
