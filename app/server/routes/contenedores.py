from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.contenedores import (
    retrieve_contenedores,
    lista_contenedores,
    lista_contenedores_empresa,
    lista_contenedores_data,
    validar_live,
)
#Aqui importamos el modelo necesario para la clase 
from server.models.contenedores import (
    ErrorResponseModel,
    ResponseModel,
    ValidarLive,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/", response_description="contenedores recuperados")
async def get_contenedores():
    notificacions = await retrieve_contenedores()
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/ListaContenedores/{id}", response_description="contenedores recuperados")
async def get_lista_contenedores(id: int):
    notificacions = await lista_contenedores(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/ListaDispositivoEmpresa/{id}", response_description="contenedores recuperados")
async def get_lista_contenedores_empresa(id: int):
    notificacions = await lista_contenedores_empresa(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/ExtraerDatos/{id}", response_description="data recuperados")
async def get_extraer_datos_empresa(id: int):
    notificacions = await lista_contenedores_data(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.post("/VerificarLive/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def validar_live_data(notificacion: ValidarLive = Body(...)):
    #convertir en json
    #notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    new_notificacion = await validar_live(notificacion)
    return ResponseModel(new_notificacion, "ok")