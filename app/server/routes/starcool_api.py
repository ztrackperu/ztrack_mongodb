from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.starcool_api import (
    homologar_api_starcool_general,
    procesar_starcool_optimizado,
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/homologar_api_starcool", response_description="Datos de tunel se homologan con ztrack")
async def homologar_starcool_ZGRU1092515():
    #notificacions = await homologar_api_starcool_general()
    notificacions = await procesar_starcool_optimizado()

    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")





