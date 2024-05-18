from typing import Optional,List
from pydantic import BaseModel, Field

class NotificacionSchema(BaseModel):
    numNotificacion:int = Field(...)
    asunto: str = Field(...)
    numSolicitud: Optional[int] | None =None
    numOT: Optional[int] | None =None
    fechaN: str = Field(...)
    trabajo: str = Field(...)
    perfil: int = Field(...)
    estadoN: Optional[int] | None =1
    class Config:
        json_schema_extra = {
            "example": {
                "numNotificacion": 1,
                "asunto": "ENTREGA",
                "numSolicitud": 1000001, 
                "numOT": 1001000004, 
                "fechaN": "2024-05-03 21:26:35", 
                "trabajo": "Instalacion de luminarias", 
                "perfil": 1, 
                "estadoN": 1, 
              
            }
        }

class UpdateNotificacionModel(BaseModel):
    numNotificacion: Optional[int] | None =None
    asunto: Optional[str] | None =None
    numSolicitud: Optional[int] | None =None
    numOT: Optional[int] | None =None
    fechaN: Optional[str] | None =None
    trabajo: Optional[str] | None =None
    perfil: Optional[int] | None =None
    estadoN: Optional[int] | None =None
    class Config:
        json_schema_extra = {
            "example": {
                "numNotificacion": 1,
                "asunto": "ENTREGA",
                "numSolicitud": 1000001, 
                "numOT": 1001000004, 
                "fechaN": "2024-05-03 21:26:35", 
                "trabajo": "Instalacion de luminarias", 
                "perfil": 1, 
                "estadoN": 1, 
              
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

