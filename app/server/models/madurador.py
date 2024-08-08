from typing import Optional,List
from pydantic import BaseModel, Field

class SolicitudMaduradorSchema(BaseModel):
    device:str = Field(...)
    ultima: str = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"
    page: Optional[int] | None =1
    size: Optional[int] | None =50000
    empresa: Optional[int] | None =22
    utc: Optional[int] | None =300
    
    class Config:
        json_schema_extra = {
            "example": {
                "device": "ZGRU9015808",
                "ultima": "2024-05-18T10:11:04",
                "fechaI": "2024-04-18T11:11:04",
                "fechaF": "2024-04-18T13:11:04", 
                "page":1,
                "size":50000,
                "empresa":22,
                "utc":300

            }
        }


class TunelSchema(BaseModel):
    data:str = Field(...)
    status: Optional[int] | None =1
    class Config:
        json_schema_extra = {
            "example": {
                "data": "1TC2,Madurador,,0.10,...",   
                "status" :1
            }
        }

class WonderfulSchema(BaseModel):
    data:str = Field(...)
    status: Optional[int] | None =1
    class Config:
        json_schema_extra = {
            "example": {
                "data": "1CR2,Madurador,ZGRU4587968,0.10,...",   
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

class DatosMadurador(BaseModel):
    id:int = Field(...)
    return_air: float = Field(...)


#ProcesarWonderfulSchema

class ProcesarWonderfulSchema(BaseModel):
     #ZGRU2232647 -> 258
    id_g : int
    mes : str
    divece : str
    telemetria_id :int

    class Config:
        json_schema_extra = {
            "example": {
                "id_g" : 13000000000,
                "mes" : "7_2024",
                "divece" : "ZGRU2232647",
                "telemetria_id": 258
            }
        }
