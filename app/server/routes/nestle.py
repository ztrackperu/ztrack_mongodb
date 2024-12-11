from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.nestle import (
    proceso_control_nestle,
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/control_nestle", response_description="Datos de tunel se homologan con ztrack")
async def control_nestle_api():
    notificacions = await proceso_control_nestle()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")


