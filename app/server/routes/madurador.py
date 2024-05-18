from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.madurador import (
    data_madurador,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.madurador import (
    ErrorResponseModel,
    ResponseModel,
    SolicitudMaduradorSchema,

)
#aqui se definen las rutas de la API REST
router = APIRouter()


@router.post("/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data(notificacion: SolicitudMaduradorSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    new_notificacion = await data_madurador(notificacion)
    return ResponseModel(new_notificacion, "ok")

