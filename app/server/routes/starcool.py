from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.starcool import (
    homologar_starcool01,
    homologar_starcool_general,
    camposol_datos ,
    data_usda,
    data_usda_validar,
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
    SolicitudCamposolSchema,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/homologar_starcool01", response_description="Datos de tunel se homologan con ztrack")
async def homologar_starcool_ZGRU1092515():
    notificacions = await homologar_starcool01()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/starcool_general", response_description="Datos de tunel se homologan con ztrack")
async def homologar_starcool_ZGRU1092515():
    notificacions = await homologar_starcool_general()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/camposol", response_description="Datos de tunel se homologan con ztrack")
async def camposol():
    notificacions = await camposol_datos()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")


@router.post("/camposol_grafica/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data_t(notificacion: SolicitudCamposolSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await data_usda(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)


@router.post("/camposol_grafica_validar/", response_description="Datos de los notificacion agregados a la base de datos.")
async def add_notificacion_data_t(notificacion: SolicitudCamposolSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_usda_validar(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)