from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.nestle import (
    proceso_control_nestle,
    pedir_grafica,
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
    SolicitudDataNestleSchema,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/control_nestle", response_description="Datos de tunel se homologan con ztrack")
async def control_nestle_api():
    notificacions = await proceso_control_nestle()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")



@router.post("/grafica_nestle/", response_description="Datos del tunel agregados a la base de datos.")
async def add_tunel_data(notificacion: SolicitudDataNestleSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await pedir_grafica(notificacion)
    return ResponseModel(new_notificacion, "ok")