from typing import Optional,List
from pydantic import BaseModel, Field


class SolicitudDataNestleSchema(BaseModel):
    device:str = Field(...)
    telemetria_id: int = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"

    
    class Config:
        json_schema_extra = {
            "example": {
                "device": "ZGRU6740381",
                "telemetria_id": 389,
                "fechaI": "2024-12-10T11:11:04",
                "fechaF": "2024-12-11T13:11:04" 
            }
        }


class SolicitudMaduradorSchema(BaseModel):
    device:str = Field(...)
    ultima: str = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"
    page: Optional[int] | None =1
    size: Optional[int] | None =5000
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

class SolicitudMaduradorSchemaF(BaseModel):
    device:int = Field(...)
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


class ViticolaSchema(BaseModel):
    dispositivo:str = Field(...)
    data:str = Field(...)
    status: Optional[int] | None =1
    class Config:
        json_schema_extra = {
            "example": {
                "dispositivo" : "ZGRU7215000",
                "data": "1BA2,Madurador,ZGRU7215000,-6.00,-2.90,-3277.00,1.10,-9.30,57.70,91.50,-3277.00,36.80,0.50,0.30,0.50,0.00,76.00,32766.00,3276.60,3276.60,439.00,60.00,15.80,15.90,15.20,25.40,3276.60,60.00,100.00,7577.30,320.90,3276.60,3276.60,6550.70,1.10,0.18,0.00,9.74,4.07,1,99.00,1,1,0,254,0,32766.00,3276.60,3276.60,3276.60,18.00,6.00,0,0,255.00,255.00,255.00,255.00,0.00,0,0,0,0.00,0.00,THERMOKING,-14.9768,-74.8981,0,0,0",
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
    device : str
    telemetria_id :int

    class Config:
        json_schema_extra = {
            "example": {
                "id_g" : 13000000000,
                "mes" : "7_2024",
                "device" : "ZGRU2232647",
                "telemetria_id": 258
            }
        }


class SolicitudCamposolSchema(BaseModel):
    sensor: str = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"
    
    class Config:
        json_schema_extra = {
            "example": {
                "sensor": "U1",
                "fechaI": "2024-04-18T11:11:04",
                "fechaF": "2024-04-18T13:11:04"
            }
        }

class SolicitudIndustriaSchema(BaseModel):
    imei: str = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"  
    class Config:
        json_schema_extra = {
            "example": {
                "imei": "867869061617106",
                "fechaI": "2024-04-18T11:11:04",
                "fechaF": "2024-04-18T13:11:04"
            }
        }

class SolicitudZtrackSchema(BaseModel):
    imei: int = Field(...)
    fechaI: Optional[str] | None ="0"
    fechaF: Optional[str] | None ="0"  
    class Config:
        json_schema_extra = {
            "example": {
                "imei": 15184,
                "fechaI": "2024-04-18T11:11:04",
                "fechaF": "2024-04-18T13:11:04"
            }
        }
        
