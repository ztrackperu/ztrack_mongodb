from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
#from fastapi_pagination import Page, add_pagination
from fastapi_pagination import Page, add_pagination, paginate
#from fastapi_pagination.ext.motor import paginate

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.madurador import (
    data_madurador,
    obtener_madurador,


)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
    SolicitudMaduradorSchema,
    DatosMadurador,

)
#aqui se definen las rutas de la API REST
router = APIRouter()


@router.post("/DatosGraficaTabla/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data(notificacion: SolicitudMaduradorSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await data_madurador(notificacion)
    return ResponseModel(new_notificacion, "ok")
   #return paginate(new_notificacion)


@router.get("/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def obtener_notificacion_data()->Page[DatosMadurador]:
    #convertir en json
    #print(notificacion)
    #enviar a la funcion añadir  
    #print ("desde r")
    new_notificacion = await obtener_madurador()
    return ResponseModel(new_notificacion, "ok")
    #return paginate(new_notificacion)