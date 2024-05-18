from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.notificaciones import (
    add_notificacion,
    delete_notificacion,
    retrieve_notificacion,
    retrieve_notificacions,
    update_notificacion,
    extraer_notificacion,
 
)
#Aqui importamos el modelo necesario para la clase 
from server.models.notificaciones import (
    ErrorResponseModel,
    ResponseModel,
    NotificacionSchema,
    UpdateNotificacionModel,

)
#aqui se definen las rutas de la API REST
router = APIRouter()


@router.post("/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def add_notificacion_data(notificacion: NotificacionSchema = Body(...)):
    #convertir en json
    notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    new_notificacion = await add_notificacion(notificacion)
    return ResponseModel(new_notificacion, "ok")

@router.get("/", response_description="notificacion recuperados")
async def get_notificacions():
    notificacions = await retrieve_notificacions()
    if notificacions:
        return ResponseModel(notificacions, "Datos de las notificaciones recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")


@router.get("/{id}", response_description="Datos de la notificacion recuperados")
async def get_notificacion_data(id: int):
    notificacion = await retrieve_notificacion(id)
    if notificacion:
        return ResponseModel(notificacion, "Datos de la notificacion recuperado exitosamente")
    return ErrorResponseModel("Ocurrió un error.", 404, "notificacion doesn't exist.")


@router.put("/{id}")
async def update_notificacion_data(id: int, req: UpdateNotificacionModel = Body(...)):
    #ANALIZADOR DE ESTRUCTURA req
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_notificacion = await update_notificacion(id, req)
    if updated_notificacion:
        return ResponseModel(
            #"ConceptoOT with ID: {} name update is successful".format(id),
            "ok",
            "notificacion  updated successfully",
        )
    return ErrorResponseModel("An error occurred",404,"There was an error updating the notificacion data.",)

@router.delete("/{id}", response_description="notificacion data deleted from the database")
async def delete_notificacion_data(id: int):
    deleted_notificacion = await delete_notificacion(id)
    if deleted_notificacion:
        return ResponseModel(
            "notificacion with ID: {} removed".format(id), "notificacion deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "notificacion with id {0} doesn't exist".format(id)
    )

@router.get("/maximo/", response_description="El conceptoOT maximo")
async def get_maximo_notificacion_data():
    notificacion = await extraer_notificacion()
    if notificacion:
        return ResponseModel(notificacion, "Datos del ConceptoOT maximo recuperado ")
    return ErrorResponseModel("Ocurrió un error.", 404, "ConceptoOT doesn't exist.")

