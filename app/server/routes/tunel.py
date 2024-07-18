from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.tunel import (
    data_hortifruit,
    homologar_hortifruit_123321,

    
)
#Aqui importamos el modelo necesario para la clase 
from server.models.tunel import (
    ErrorResponseModel,
    ResponseModel,
    TunelSchema,


)


#aqui se definen las rutas de la API REST
router = APIRouter()


@router.post("/Hortifruit/", response_description="Datos del tunel agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_tunel_hortifruit_data(notificacion: TunelSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    new_notificacion = await data_hortifruit(notificacion)
    return ResponseModel(new_notificacion, "ok")

@router.get("/HortifruitA/123321", response_description="Datos de tunel se homologan con ztrack")
async def homologar_HortifruitA_123321():
    notificacions = await homologar_hortifruit_123321()
    if notificacions:
        return ResponseModel(notificacions, "Datos homologados 123321!")
    return ResponseModel(notificacions, "Lista vacía devuelta")