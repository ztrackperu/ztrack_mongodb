from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.industria import (
    data_industria_grafica,
    data_industria_tabla,
    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
    SolicitudIndustriaSchema,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/industria", response_description="Datos de tunel se homologan con ztrack")
async def camposol():
    notificacions = await data_industria_grafica()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados starcool!")
    return ResponseModel(notificacions, "Lista vacía devuelta")


@router.post("/industria_grafica/", response_description="Datos de los notificacion agregados a la base de datos.")
async def addndustria_grafica_search(notificacion: SolicitudIndustriaSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_industria_grafica(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)

@router.post("/industria_tabla/", response_description="Datos de los notificacion agregados a la base de datos.")
async def industria_tabla_search(notificacion: SolicitudIndustriaSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_industria_tabla(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)