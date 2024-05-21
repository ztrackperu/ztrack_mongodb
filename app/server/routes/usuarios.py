from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.usuarios import (
    retrieve_usuarios,
    retrieve_usuario,
    add_usuario,
    extraer_pass,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.usuarios import (
    ErrorResponseModel,
    ResponseModel,
    UsuariosSchema,
    UpdateUsuariosModel,

)
#aqui se definen las rutas de la API REST
router = APIRouter()


@router.get("/", response_description="usuarios recuperados")
async def get_usuarios():
    notificacions = await retrieve_usuarios()
    if notificacions:
        return ResponseModel(notificacions, "Datos de los usuarios recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/{user}", response_description="Datos del usuario recuperados")
async def get_usuario_data(user: str):
    notificacion = await retrieve_usuario(user)
    if notificacion:
        return ResponseModel(notificacion, "Datos del usuario recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "usuario doesn't exist.")

@router.post("/", response_description="Datos de los usuario agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data(notificacion: UsuariosSchema = Body(...)):
    new_notificacion = await add_usuario(notificacion)
    return ResponseModel(new_notificacion, "ok")

@router.get("/extraerPass/{user}", response_description="El conceptoOT maximo")
async def get_extraer_pass_data(user: str):
    notificacion = await extraer_pass(user)
    if notificacion:
        return ResponseModel(notificacion, "Datos del ConceptoOT maximo recuperado ")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

