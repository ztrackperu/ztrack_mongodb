from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.starcool import (
    homologar_starcool01,
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/homologar_starcool01", response_description="Datos de tunel se homologan con ztrack")
async def homologar_starcool_ZGRU1092515():
    notificacions = await homologar_starcool01()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")


