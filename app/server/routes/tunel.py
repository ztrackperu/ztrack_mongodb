from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.tunel import (
    data_madurador,

    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.tunel import (
    ErrorResponseModel,
    ResponseModel,
    TunelSchema,


)
#aqui se definen las rutas de la API REST
router = APIRouter()